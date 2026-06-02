# SafeRx Pharma

[![Latest Release](https://img.shields.io/github/v/release/KaRamHelal/SafeRx_Pharma?label=latest%20release&logo=github)](https://github.com/KaRamHelal/SafeRx_Pharma/releases/latest)

Drug safety intelligence for Egyptian pharmaceutical products. One API call, seven safety domains, 66,704 products.

## What's Here

```
SafeRx_Pharma/
├── openapi/                  # OpenAPI 3.1.1 spec (source of truth)
│   └── drug-safety-v1.yaml   # ~2000 lines, fully typed
├── mcp-server/               # MCP server for AI assistants
│   └── src/index.ts           # Published: @saferx_pharma/mcp-server
├── fern/                     # Fern docs + SDK generation config
│   ├── docs.yml               # docs.saferx.online (29 pages)
│   ├── docs/                  # Documentation content (MDX)
│   ├── generators.yml         # SDK generators (Python, TS, C#, Java, Go, Swift)
│   └── apis/                  # API definitions per SDK
├── postman/                  # Postman collection (8 requests)
└── LICENSE                   # MIT
```

## Quick Start

### Get a Free API Key

```bash
# Step 1: Request verification code
curl -X POST https://saferx.online/api/developers/keys/free \
  -H "Content-Type: application/json" \
  -d '{"email": "you@example.com"}'

# Step 2: Verify with the 6-digit code from your email
curl -X POST https://saferx.online/api/developers/keys/free/verify \
  -H "Content-Type: application/json" \
  -d '{"email": "you@example.com", "code": "123456"}'
```

### Check Drug Safety

```bash
curl -X POST https://saferx.online/api/drug_safety/check \
  -H "X-SafeRx-API-Key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: MyApp/1.0" \
  -d '{"drugs": ["Augmentin 1g", "Marivan", "Glucophage 500"]}'
```

Returns safety data across all 7 domains in ~40ms.

## SDKs

| Language | Package | Install |
|----------|---------|---------|
| Python | [`saferx-pharma`](https://pypi.org/project/saferx-pharma/) | `pip install saferx-pharma` |
| TypeScript | [`saferx-pharma-sdk`](https://www.npmjs.com/package/saferx-pharma-sdk) | `npm install saferx-pharma-sdk` |
| C# | [`SafeRx`](https://www.nuget.org/packages/SafeRx) | `dotnet add package SafeRx` |

```python
from saferx import SafeRxClient

client = SafeRxClient(api_key="sfx_free_...")
result = client.drug_safety.check(drugs=["Augmentin 1g", "Marivan"])
```

```typescript
import { SafeRxClient } from "saferx-pharma-sdk";

const client = new SafeRxClient({ apiKey: "sfx_free_..." });
const result = await client.drugSafety.check({ drugs: ["Augmentin 1g", "Marivan"] });
```

## MCP Server

For AI assistants (Claude Desktop, Claude Code, Cursor):

```bash
npx @saferx_pharma/mcp-server
```

Requires `SAFERX_API_KEY` environment variable. See [`mcp-server/README.md`](mcp-server/README.md) for configuration details.

## Safety Domains

| Domain | Code | Coverage |
|--------|------|----------|
| Adverse Effects | `ae` | 920K+ effects, Black Box Warnings |
| Drug Interactions | `ddi` | 337K+ interaction pairs |
| Pregnancy & Lactation | `pllr` | 24K+ products, 0-7 risk scale |
| Food Interactions | `food` | 38K+ interactions |
| Clinical Considerations | `clinical` | 5 populations, 14 conditions |
| Dosing | `dose` | Dose limits and calculation caveats |
| Allergy | `allergy` | Patient allergy matching and cross-reactivity |

## API Tiers

| | Free | Pro | Enterprise |
|---|------|-----|------------|
| Monthly quota | 100 checks | 15,000+ checks | Custom |
| Requests/min | 20 anti-abuse | 60 anti-abuse | Custom |
| Requests/day | 60 safety cap | 500 safety cap | Custom |
| Max drugs/request | 20 | 20 | 50 |
| Auth | API Key | API Key | API Key |
| Database | Full (66,704 products) | Full | Full |
| Support | Email | Priority | Dedicated |

## Documentation

- [API Reference](https://docs.saferx.online) — Interactive endpoint docs
- [Integration Guides](https://docs.saferx.online/guides/integration-guides/pharmacy-dispensing) — Pharmacy, Hospital EHR, POS, Mobile, AI Agent
- [OpenAPI Spec](openapi/drug-safety-v1.yaml) — Machine-readable API definition
- [Postman Collection](postman/SafeRx-Drug-Safety-API.postman_collection.json) — Import and test in seconds

## Links

- **Website:** [saferx.online](https://saferx.online)
- **Developer Portal:** [saferx.online/developer.html](https://saferx.online/developer.html)
- **Releases:** [github.com/KaRamHelal/SafeRx_Pharma/releases/latest](https://github.com/KaRamHelal/SafeRx_Pharma/releases/latest)
- **npm:** [@saferx_pharma/mcp-server](https://www.npmjs.com/package/@saferx_pharma/mcp-server)
- **Status:** [saferx.instatus.com](https://saferx.instatus.com)
- **Support:** support@saferx.online

## License

MIT
