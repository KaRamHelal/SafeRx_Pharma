# SafeRx MCP Server

Model Context Protocol server for the [SafeRx Drug Safety API](https://saferx.online). Enables AI assistants (Claude Desktop, Claude Code, Cursor) to check drug safety across 66,000+ Egyptian pharmaceutical products.

## Tools

| Tool | Description |
|------|-------------|
| `check_drug_safety` | Screen 1-20 drugs across 7 safety domains and return full JSON safety data |
| `get_drug_metadata` | Get available populations, conditions, and database versions |

## Quick Start

```bash
SAFERX_API_KEY=sfx_free_... npx @saferx_pharma/mcp-server
```

Get a free API key at [docs.saferx.online](https://docs.saferx.online/api-reference/authentication/api-keys).

## Configuration

### Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "saferx": {
      "command": "npx",
      "args": ["-y", "@saferx_pharma/mcp-server"],
      "env": {
        "SAFERX_API_KEY": "sfx_free_..."
      }
    }
  }
}
```

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SAFERX_API_KEY` | **Yes** | — | API key (free/pro/enterprise). Get one at [docs.saferx.online](https://docs.saferx.online/api-reference/authentication/api-keys). |
| `SAFERX_BASE_URL` | No | `https://saferx.online` | API base URL |

## Build from Source

```bash
git clone https://github.com/KaRamHelal/SafeRx_Pharma.git
cd SafeRx_Pharma/mcp-server
npm install
npm run build
npm start
```

## Safety Domains

| Domain | Code | Description |
|--------|------|-------------|
| Adverse Effects | `ae` | Black Box Warnings, side effects, monitoring |
| Drug Interactions | `ddi` | 337K+ interaction pairs with severity |
| Pregnancy & Lactation | `pllr` | 0-7 risk scale, 24K+ products |
| Food Interactions | `food` | Meal timing, food-drug conflicts |
| Clinical | `clinical` | 5 populations, 14 conditions, matched renal/hepatic/pediatric context from patient values |
| Dosing | `dose` | Standard-dose summaries, dose limits, monitoring display, and daily-dose references |
| Allergy | `allergy` | Patient allergy matching, allergy families, and cross-reactivity warnings |

## Patient Context

`check_drug_safety` accepts optional `patient_profile` fields:

```json
{
  "age": 72,
  "weight_kg": 70,
  "crcl": 25,
  "child_pugh": "B",
  "conditions": ["diabetes"],
  "allergies": ["penicillin"]
}
```

Use these fields when asking an AI assistant to assess renal/hepatic dose adjustment, monitoring instructions, allergy warnings, or cross-reactivity. The tool returns the full API response under `Full Safety Data`, including `drugs[]`, `safety.clinical`, `safety.dosing`, and `safety.allergy.product_families`.

## License

MIT
