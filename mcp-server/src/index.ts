#!/usr/bin/env node

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const API_KEY = process.env.SAFERX_API_KEY ?? "";
const BASE_URL = process.env.SAFERX_BASE_URL ?? "https://saferx.online";
const USER_AGENT = "SafeRx-MCP-Server/1.5.0";

if (!API_KEY) {
  console.error(
    "SAFERX_API_KEY is required. Get a free key: POST https://saferx.online/api/developers/keys/free"
  );
  process.exit(1);
}

function authHeaders(): Record<string, string> {
  return {
    "Content-Type": "application/json",
    "User-Agent": USER_AGENT,
    "X-SafeRx-API-Key": API_KEY,
  };
}

function asRecord(value: unknown): Record<string, unknown> {
  return value && typeof value === "object" && !Array.isArray(value)
    ? (value as Record<string, unknown>)
    : {};
}

function asArray(value: unknown): unknown[] {
  return Array.isArray(value) ? value : [];
}

function formatCount(label: string, value: unknown): string {
  return `- ${label}: ${asArray(value).length}`;
}

function formatIntelligenceBlock(data: Record<string, unknown>): string {
  const intelligence = asRecord(data.intelligence);
  if (Object.keys(intelligence).length === 0) {
    return "";
  }

  const synthesis = asRecord(intelligence.synthesis);
  const saferAlternatives = asRecord(intelligence.safer_alternatives);
  const alternativeSourceIds = Object.keys(saferAlternatives).filter(
    (key) => !key.startsWith("_")
  );
  const status = String(intelligence.status ?? "available");

  const lines = [
    "## Medication Intelligence",
    "",
    `- Status: ${status}`,
    formatCount("Cumulative dose warnings", intelligence.cumulative_warnings),
    formatCount("Cross-domain findings", synthesis.cross_domain_findings),
    formatCount("Predictive adverse effects", synthesis.predictive_ae),
    `- Safer alternative source drugs: ${alternativeSourceIds.length}`,
  ];

  const summary = synthesis.summary;
  if (typeof summary === "string" && summary.trim()) {
    lines.push(`- Summary: ${summary.trim()}`);
  }

  const processorErrors = asArray(intelligence.processor_errors);
  if (processorErrors.length > 0) {
    lines.push(`- Processor errors: ${processorErrors.length}`);
  }

  lines.push("", "```json", JSON.stringify(intelligence, null, 2), "```", "");
  return lines.join("\n");
}

// --- MCP Server ---

const server = new McpServer({
  name: "saferx",
  version: "1.5.0",
});

// Tool: check_drug_safety
server.tool(
  "check_drug_safety",
  "Screen drugs for safety issues across 7 domains: adverse effects (Black Box Warnings, monitoring), drug interactions, pregnancy/lactation risks, food interactions, clinical considerations, dosing, and patient allergy matching. Covers 66,000+ Egyptian pharmaceutical products with bilingual EN/AR support.",
  {
    drugs: z
      .array(z.string())
      .min(1)
      .max(20)
      .describe("Drug names to screen (trade or generic, e.g. 'Augmentin 1g')"),
    patient_profile: z
      .object({
        populations: z
          .array(
            z.enum(["pediatric", "geriatric", "cardiac", "hepatic", "renal"])
          )
          .optional()
          .describe("Patient populations for personalized alerts"),
        conditions: z
          .array(
            z.enum([
              "arrhythmia",
              "asthma",
              "bph",
              "coronary",
              "depression",
              "diabetes",
              "epilepsy",
              "gi_bleeding",
              "glaucoma",
              "heart_failure",
              "hypertension",
              "hyperthyroidism",
              "hypothyroidism",
              "parkinsons",
            ])
          )
          .optional()
          .describe("Patient comorbidities"),
        allergies: z
          .array(z.string())
          .optional()
          .describe("Known patient allergies for allergy-domain screening"),
        age: z
          .number()
          .int()
          .min(0)
          .max(150)
          .optional()
          .describe("Patient age in years; infers pediatric/geriatric context"),
        weight_kg: z
          .number()
          .min(0)
          .optional()
          .describe("Patient weight in kilograms for weight-based dose context"),
        crcl: z
          .number()
          .min(0)
          .optional()
          .describe("Creatinine clearance in mL/min; infers renal dose context"),
        egfr: z
          .number()
          .min(0)
          .optional()
          .describe("eGFR fallback renal-function input when crcl is unavailable"),
        child_pugh: z
          .enum(["A", "B", "C"])
          .optional()
          .describe("Child-Pugh class; infers hepatic dose context"),
        hepatic_status: z
          .enum(["normal", "mild", "moderate", "severe"])
          .optional()
          .describe("Hepatic impairment severity; used when child_pugh is unavailable"),
      })
      .optional()
      .describe("Patient context for personalized safety screening"),
    intelligence_context: z
      .object({
        user_id: z.string().optional().describe("Optional caller-side patient/profile identifier"),
        clinical_profile: z
          .object({
            age: z.number().int().min(0).max(150).optional(),
            crcl: z.number().min(0).optional().describe("Creatinine clearance in mL/min"),
            hepatic_status: z.enum(["normal", "mild", "moderate", "severe"]).optional(),
            pregnancy: z.boolean().optional(),
            lactation: z.boolean().optional(),
            conditions: z.array(z.string()).optional(),
            populations: z.array(z.string()).optional(),
            allergies: z.array(z.string()).optional(),
            diet_habits: z.array(z.string()).optional(),
          })
          .optional()
          .describe("Clinical profile used by Medication Intelligence processors"),
        medication_history: z
          .array(
            z.object({
              sfrx_id: z.string().describe("SafeRx product identifier"),
              start_date: z.string().optional().describe("Medication start date, preferably ISO 8601"),
              status: z
                .enum(["active", "historical"])
                .optional()
                .describe("Only active medications participate in cumulative dose aggregation"),
            })
          )
          .optional()
          .describe("Longitudinal medication history; use status=active or status=historical"),
      })
      .optional()
      .describe("Optional Medication Intelligence Platform context"),
    include: z
      .array(z.enum(["ae", "ddi", "pllr", "food", "clinical", "dose", "allergy"]))
      .min(1)
      .optional()
      .describe(
        "Safety domains to check (ae=adverse effects, ddi=drug interactions, pllr=pregnancy/lactation, food=food interactions, clinical=population/condition safety, dose=max daily dose, allergy=patient allergy matching). Omit for all."
      ),
    lang: z
      .enum(["en", "ar"])
      .optional()
      .default("en")
      .describe("Response language"),
  },
  async (args) => {
    const body: Record<string, unknown> = { drugs: args.drugs };
    if (args.patient_profile) body.patient_profile = args.patient_profile;
    if (args.intelligence_context) body.intelligence_context = args.intelligence_context;
    if (args.include) body.include = args.include;
    if (args.lang) body.lang = args.lang;

    const resp = await fetch(`${BASE_URL}/api/drug_safety/check`, {
      method: "POST",
      headers: authHeaders(),
      body: JSON.stringify(body),
    });

    const data = (await resp.json()) as Record<string, unknown>;

    if (!resp.ok) {
      return {
        content: [
          {
            type: "text" as const,
            text: `Error ${resp.status}: ${JSON.stringify(data)}`,
          },
        ],
        isError: true,
      };
    }

    // Format alerts prominently
    const alerts = (data.alerts ?? []) as Array<{
      severity: string;
      type: string;
      message: string;
    }>;
    let alertText = "";
    if (alerts.length > 0) {
      alertText =
        "## Safety Alerts\n\n" +
        alerts
          .map(
            (a) =>
              `- **${a.severity}** [${a.type}]: ${a.message}`
          )
          .join("\n") +
        "\n\n";
    }

    return {
      content: [
        {
          type: "text" as const,
          text:
            alertText +
            formatIntelligenceBlock(data) +
            "## Full Safety Data\n\n```json\n" +
            JSON.stringify(data, null, 2) +
            "\n```",
        },
      ],
    };
  }
);

// Tool: get_drug_metadata
server.tool(
  "get_drug_metadata",
  "Get SafeRx Drug Safety API metadata: available populations, conditions, database versions, risk scales, and current tier limits. Useful for discovering valid parameter values.",
  {},
  async () => {
    const resp = await fetch(`${BASE_URL}/api/drug_safety/metadata`, {
      headers: authHeaders(),
    });

    const data = await resp.json();

    if (!resp.ok) {
      return {
        content: [
          {
            type: "text" as const,
            text: `Error ${resp.status}: ${JSON.stringify(data)}`,
          },
        ],
        isError: true,
      };
    }

    return {
      content: [
        {
          type: "text" as const,
          text:
            "## SafeRx API Metadata\n\n```json\n" +
            JSON.stringify(data, null, 2) +
            "\n```",
        },
      ],
    };
  }
);

// Start server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch((err) => {
  console.error("Fatal:", err);
  process.exit(1);
});
