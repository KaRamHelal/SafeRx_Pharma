# SafeRx MCP Server

Model Context Protocol server for the [SafeRx Drug Safety API](https://saferx.online). Enables AI assistants (Claude Desktop, Claude Code, Cursor) to check drug safety across 28,000+ Egyptian pharmaceutical products.

## Tools

| Tool | Description |
|------|-------------|
| `check_drug_safety` | Screen 1-20 drugs across 6 safety domains |
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
| Clinical | `clinical` | 5 populations, 14 conditions |
| Dosing | `dose` | Max daily dose (WHO DDD) |

## License

MIT
