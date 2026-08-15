import { createHash, createHmac, randomUUID } from "node:crypto";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const API_KEY = process.env.SAFERX_API_KEY ?? "";
const BASE_URL = (process.env.SAFERX_BASE_URL ?? "https://saferx.online/api/enterprise/v1").replace(/\/+$/, "");

if (!API_KEY) {
  console.error("SAFERX_API_KEY is required for the Enterprise MCP adapter.");
  process.exit(1);
}

type Operation = {
  method: "GET" | "POST";
  path: string;
  idempotencyRequired?: boolean;
};

const OPERATIONS: Record<string, Operation> = {
  enterprise_status: { method: "GET", path: "/status" },
  enterprise_capabilities: { method: "GET", path: "/capabilities" },
  enterprise_registry_search: { method: "GET", path: "/registry/search" },
  enterprise_safety_check: { method: "POST", path: "/safety/checks", idempotencyRequired: true },
};

function canonicalQuery(query: Record<string, string | number> = {}): string {
  return Object.entries(query)
    .sort(([left], [right]) => left.localeCompare(right))
    .map(([key, value]) => `${encodeURIComponent(key)}=${encodeURIComponent(String(value))}`)
    .join("&");
}

function signature(method: string, path: string, query: string, body: string, timestamp: string, nonce: string): string {
  const bodyHash = createHash("sha256").update(body).digest("hex");
  const canonical = [method.toUpperCase(), encodeURIComponent(path).replace(/%2F/g, "/"), query, bodyHash, timestamp, nonce].join("\n");
  return createHmac("sha256", API_KEY).update(canonical).digest("base64url");
}

async function call(operationId: string, input: { query?: Record<string, string | number>; body?: unknown; idempotencyKey?: string } = {}): Promise<unknown> {
  const operation = OPERATIONS[operationId];
  if (!operation) throw new Error(`Unknown Enterprise operation: ${operationId}`);
  if (operation.idempotencyRequired && !input.idempotencyKey) throw new Error(`${operationId} requires idempotencyKey`);

  const query = canonicalQuery(input.query);
  const body = input.body === undefined ? "" : JSON.stringify(input.body);
  const timestamp = new Date().toISOString();
  const nonce = randomUUID();
  const headers: Record<string, string> = {
    Accept: "application/json",
    "X-SafeRx-API-Key": API_KEY,
    "X-SafeRx-Timestamp": timestamp,
    "X-SafeRx-Nonce": nonce,
    "X-SafeRx-Signature": signature(operation.method, operation.path, query, body, timestamp, nonce),
    "X-Request-ID": randomUUID(),
    "X-SafeRx-Client-Kind": "mcp_stdio",
    "X-SafeRx-Client-Name": "saferx-enterprise-mcp",
    "X-SafeRx-Client-Version": "2.0.2-preview.1",
  };
  if (input.body !== undefined) headers["Content-Type"] = "application/json";
  if (input.idempotencyKey) headers["Idempotency-Key"] = input.idempotencyKey;

  const response = await fetch(`${BASE_URL}${operation.path}${query ? `?${query}` : ""}`, {
    method: operation.method,
    headers,
    body: input.body === undefined ? undefined : body,
  });
  const data = await response.json().catch(() => ({ status: response.status, title: "INVALID_RESPONSE" }));
  if (!response.ok) throw new Error(JSON.stringify(data));
  return data;
}

const server = new McpServer({ name: "saferx-enterprise-mcp", version: "2.0.2-preview.1" });

server.tool("enterprise_status", "Read the bounded Enterprise service status.", {}, async () => ({
  content: [{ type: "text", text: JSON.stringify(await call("enterprise_status"), null, 2) }],
}));

server.tool("enterprise_capabilities", "Read the bounded Enterprise capability metadata.", {}, async () => ({
  content: [{ type: "text", text: JSON.stringify(await call("enterprise_capabilities"), null, 2) }],
}));

server.tool(
  "enterprise_registry_search",
  "Search the bilingual SafeRx registry.",
  { q: z.string().min(1).max(120), locale: z.string().optional(), limit: z.number().int().min(1).max(100).optional() },
  async ({ q, locale, limit }) => ({
    content: [{ type: "text", text: JSON.stringify(await call("enterprise_registry_search", { query: { q, ...(locale ? { locale } : {}), ...(limit ? { limit } : {}) } }), null, 2) }],
  }),
);

server.tool(
  "enterprise_safety_check",
  "Run a bounded medication safety check and preserve review and limitation states.",
  {
    locale: z.enum(["ar-EG", "ar", "en", "mixed"]),
    medications: z.array(z.object({
      client_medication_id: z.string().nullable().optional(),
      input_text: z.string().min(1),
      sfrx_id: z.string().nullable().optional(),
      dose_text: z.string().nullable().optional(),
      route: z.string().nullable().optional(),
      frequency_text: z.string().nullable().optional(),
    })).min(1).max(50),
    requested_domains: z.array(z.enum(["pllr", "ddi", "clinical_dose", "food_interactions", "meal_timing", "allergy"])).min(1),
    idempotencyKey: z.string().min(8),
  },
  async ({ idempotencyKey, ...body }) => ({
    content: [{ type: "text", text: JSON.stringify(await call("enterprise_safety_check", { body, idempotencyKey }), null, 2) }],
  }),
);

await server.connect(new StdioServerTransport());
