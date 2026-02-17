#!/usr/bin/env node

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const API_KEY = process.env.SAFERX_API_KEY ?? "";
const BASE_URL = process.env.SAFERX_BASE_URL ?? "https://saferx.online";
const USER_AGENT = "SafeRx-MCP-Server/1.0";

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

// --- MCP Server ---

const server = new McpServer({
  name: "saferx",
  version: "1.0.0",
});

// Tool: check_drug_safety
server.tool(
  "check_drug_safety",
  "Screen drugs for safety issues across 6 domains: adverse effects (Black Box Warnings, monitoring), drug interactions, pregnancy/lactation risks, food interactions, clinical considerations, and dosing. Covers 28,000+ Egyptian pharmaceutical products with bilingual EN/AR support.",
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
              "diabetes",
              "hypertension",
              "epilepsy",
              "heart_failure",
              "asthma",
              "liver_disease",
              "kidney_disease",
              "thyroid",
              "depression",
              "blood_disorders",
              "ischemic_heart",
              "arrhythmia",
              "gout",
              "osteoporosis",
            ])
          )
          .optional()
          .describe("Patient comorbidities"),
      })
      .optional()
      .describe("Patient context for personalized safety screening"),
    include: z
      .array(z.enum(["ae", "ddi", "pllr", "food", "clinical", "dose"]))
      .optional()
      .describe(
        "Safety domains to check (ae=adverse effects, ddi=drug interactions, pllr=pregnancy/lactation, food=food interactions, clinical=population/condition safety, dose=max daily dose). Omit for all."
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
    if (args.include) body.include = args.include;
    if (args.lang) body.lang = args.lang;

    const resp = await fetch(`${BASE_URL}/api/drug_safety/check`, {
      method: "POST",
      headers: authHeaders(),
      body: JSON.stringify(body),
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
