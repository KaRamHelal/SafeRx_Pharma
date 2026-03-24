# Saferx Python Library

[![fern shield](https://img.shields.io/badge/%F0%9F%8C%BF-Built%20with%20Fern-brightgreen)](https://buildwithfern.com?utm_source=github&utm_medium=github&utm_campaign=readme&utm_source=https%3A%2F%2Fgithub.com%2FKaRamHelal%2FSafeRx_Pharma)
[![pypi](https://img.shields.io/pypi/v/saferx-pharma)](https://pypi.python.org/pypi/saferx-pharma)

The Saferx Python library provides convenient access to the Saferx APIs from Python.

## Table of Contents

- [What S Here](#what-s-here)
- [Quick Start](#quick-start)
- [Sd Ks](#sd-ks)
- [Mcp Server](#mcp-server)
- [Safety Domains](#safety-domains)
- [Api Tiers](#api-tiers)
- [Documentation](#documentation)
- [Links](#links)
- [License](#license)
- [Installation](#installation)
- [Reference](#reference)
- [Usage](#usage)
- [Async Client](#async-client)
- [Exception Handling](#exception-handling)
- [Advanced](#advanced)
  - [Access Raw Response Data](#access-raw-response-data)
  - [Retries](#retries)
  - [Timeouts](#timeouts)
  - [Custom Client](#custom-client)
- [Contributing](#contributing)

## What's Here

```
SafeRx_Pharma/
├── openapi/                  # OpenAPI 3.1.1 spec (source of truth)
│   └── drug-safety-v1.yaml   # ~2000 lines, fully typed
├── mcp-server/               # MCP server for AI assistants
│   └── src/index.ts           # Published: @saferx_pharma/mcp-server
├── fern/                     # Fern docs + SDK generation config
│   ├── docs.yml               # docs.saferx.online (26 pages)
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

Returns safety data across all 6 domains in ~40ms.

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
| Dosing | `dose` | 19K+ products, dual-source |

## API Tiers

| | Free | Pro | Enterprise |
|---|------|-----|------------|
| Requests/min | 20 | 60 | Custom |
| Requests/day | 60 | 500 | Custom |
| Max drugs/request | 20 | 20 | 50 |
| Auth | API Key | API Key | API Key |
| Database | Full (28,557 products) | Full | Full |
| Support | Email | Priority | Dedicated |

## Documentation

- [API Reference](https://saferx.docs.buildwithfern.com) — Interactive endpoint docs
- [Integration Guides](https://saferx.docs.buildwithfern.com/guides/integration-guides/pharmacy-dispensing) — Pharmacy, Hospital EHR, POS, Mobile, AI Agent
- [OpenAPI Spec](openapi/drug-safety-v1.yaml) — Machine-readable API definition
- [Postman Collection](postman/SafeRx-Drug-Safety-API.postman_collection.json) — Import and test in seconds

## Links

- **Website:** [saferx.online](https://saferx.online)
- **Developer Portal:** [saferx.online/developer.html](https://saferx.online/developer.html)
- **npm:** [@saferx_pharma/mcp-server](https://www.npmjs.com/package/@saferx_pharma/mcp-server)
- **Status:** [saferx.instatus.com](https://saferx.instatus.com)
- **Support:** support@saferx.online

## License

MIT

## Installation

```sh
pip install saferx-pharma
```

## Reference

A full reference for this library is available [here](https://github.com/KaRamHelal/SafeRx_Pharma/blob/HEAD/./reference.md).

## Usage

Instantiate and use the client with the following:

```python
from saferx import SafeRxClient

client = SafeRxClient(
    api_key="YOUR_API_KEY",
)
client.drug_safety.check(
    drugs=["Augmentin 1g", "Glucophage 500mg"],
    lang="ar",
)
```

## Async Client

The SDK also exports an `async` client so that you can make non-blocking calls to our API. Note that if you are constructing an Async httpx client class to pass into this client, use `httpx.AsyncClient()` instead of `httpx.Client()` (e.g. for the `httpx_client` parameter of this client).

```python
import asyncio

from saferx import AsyncSafeRxClient

client = AsyncSafeRxClient(
    api_key="YOUR_API_KEY",
)


async def main() -> None:
    await client.drug_safety.check(
        drugs=["Augmentin 1g", "Glucophage 500mg"],
        lang="ar",
    )


asyncio.run(main())
```

## Exception Handling

When the API returns a non-success status code (4xx or 5xx response), a subclass of the following error
will be thrown.

```python
from saferx.core.api_error import ApiError

try:
    client.drug_safety.check(...)
except ApiError as e:
    print(e.status_code)
    print(e.body)
```

## Advanced

### Access Raw Response Data

The SDK provides access to raw response data, including headers, through the `.with_raw_response` property.
The `.with_raw_response` property returns a "raw" client that can be used to access the `.headers` and `.data` attributes.

```python
from saferx import SafeRxClient

client = SafeRxClient(
    ...,
)
response = client.drug_safety.with_raw_response.check(...)
print(response.headers)  # access the response headers
print(response.status_code)  # access the response status code
print(response.data)  # access the underlying object
```

### Retries

The SDK is instrumented with automatic retries with exponential backoff. A request will be retried as long
as the request is deemed retryable and the number of retry attempts has not grown larger than the configured
retry limit (default: 2).

A request is deemed retryable when any of the following HTTP status codes is returned:

- [408](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/408) (Timeout)
- [429](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429) (Too Many Requests)
- [5XX](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/500) (Internal Server Errors)

Use the `max_retries` request option to configure this behavior.

```python
client.drug_safety.check(..., request_options={
    "max_retries": 1
})
```

### Timeouts

The SDK defaults to a 60 second timeout. You can configure this with a timeout option at the client or request level.

```python

from saferx import SafeRxClient

client = SafeRxClient(
    ...,
    timeout=20.0,
)


# Override timeout for a specific method
client.drug_safety.check(..., request_options={
    "timeout_in_seconds": 1
})
```

### Custom Client

You can override the `httpx` client to customize it for your use-case. Some common use-cases include support for proxies
and transports.

```python
import httpx
from saferx import SafeRxClient

client = SafeRxClient(
    ...,
    httpx_client=httpx.Client(
        proxy="http://my.test.proxy.example.com",
        transport=httpx.HTTPTransport(local_address="0.0.0.0"),
    ),
)
```

## Contributing

While we value open-source contributions to this SDK, this library is generated programmatically.
Additions made directly to this library would have to be moved over to our generation code,
otherwise they would be overwritten upon the next generated release. Feel free to open a PR as
a proof of concept, but know that we will not be able to merge it as-is. We suggest opening
an issue first to discuss with us!

On the other hand, contributions to the README are always very welcome!
