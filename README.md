# Saferx TypeScript Library

[![fern shield](https://img.shields.io/badge/%F0%9F%8C%BF-Built%20with%20Fern-brightgreen)](https://buildwithfern.com?utm_source=github&utm_medium=github&utm_campaign=readme&utm_source=https%3A%2F%2Fgithub.com%2FKaRamHelal%2FSafeRx_Pharma)
[![npm shield](https://img.shields.io/npm/v/saferx-pharma-sdk)](https://www.npmjs.com/package/saferx-pharma-sdk)

The Saferx TypeScript library provides convenient access to the Saferx APIs from TypeScript.

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
- [Request and Response Types](#request-and-response-types)
- [Exception Handling](#exception-handling)
- [Advanced](#advanced)
  - [Additional Headers](#additional-headers)
  - [Additional Query String Parameters](#additional-query-string-parameters)
  - [Retries](#retries)
  - [Timeouts](#timeouts)
  - [Aborting Requests](#aborting-requests)
  - [Access Raw Response Data](#access-raw-response-data)
  - [Logging](#logging)
  - [Runtime Compatibility](#runtime-compatibility)
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
npm i -s saferx-pharma-sdk
```

## Reference

A full reference for this library is available [here](https://github.com/KaRamHelal/SafeRx_Pharma/blob/HEAD/./reference.md).

## Usage

Instantiate and use the client with the following:

```typescript
import { SafeRxClient } from "saferx-pharma-sdk";

const client = new SafeRxClient({ apiKey: "YOUR_API_KEY" });
await client.drugSafety.check({
    drugs: ["Augmentin 1g", "Glucophage 500mg"],
    lang: "ar"
});
```

## Request and Response Types

The SDK exports all request and response types as TypeScript interfaces. Simply import them with the
following namespace:

```typescript
import { SafeRx } from "saferx-pharma-sdk";

const request: SafeRx.DrugSafetyCheckRequest = {
    ...
};
```

## Exception Handling

When the API returns a non-success status code (4xx or 5xx response), a subclass of the following error
will be thrown.

```typescript
import { SafeRxError } from "saferx-pharma-sdk";

try {
    await client.drugSafety.check(...);
} catch (err) {
    if (err instanceof SafeRxError) {
        console.log(err.statusCode);
        console.log(err.message);
        console.log(err.body);
        console.log(err.rawResponse);
    }
}
```

## Advanced

### Additional Headers

If you would like to send additional headers as part of the request, use the `headers` request option.

```typescript
import { SafeRxClient } from "saferx-pharma-sdk";

const client = new SafeRxClient({
    ...
    headers: {
        'X-Custom-Header': 'custom value'
    }
});

const response = await client.drugSafety.check(..., {
    headers: {
        'X-Custom-Header': 'custom value'
    }
});
```

### Additional Query String Parameters

If you would like to send additional query string parameters as part of the request, use the `queryParams` request option.

```typescript
const response = await client.drugSafety.check(..., {
    queryParams: {
        'customQueryParamKey': 'custom query param value'
    }
});
```

### Retries

The SDK is instrumented with automatic retries with exponential backoff. A request will be retried as long
as the request is deemed retryable and the number of retry attempts has not grown larger than the configured
retry limit (default: 2).

A request is deemed retryable when any of the following HTTP status codes is returned:

- [408](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/408) (Timeout)
- [429](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429) (Too Many Requests)
- [5XX](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/500) (Internal Server Errors)

Use the `maxRetries` request option to configure this behavior.

```typescript
const response = await client.drugSafety.check(..., {
    maxRetries: 0 // override maxRetries at the request level
});
```

### Timeouts

The SDK defaults to a 60 second timeout. Use the `timeoutInSeconds` option to configure this behavior.

```typescript
const response = await client.drugSafety.check(..., {
    timeoutInSeconds: 30 // override timeout to 30s
});
```

### Aborting Requests

The SDK allows users to abort requests at any point by passing in an abort signal.

```typescript
const controller = new AbortController();
const response = await client.drugSafety.check(..., {
    abortSignal: controller.signal
});
controller.abort(); // aborts the request
```

### Access Raw Response Data

The SDK provides access to raw response data, including headers, through the `.withRawResponse()` method.
The `.withRawResponse()` method returns a promise that results to an object with a `data` and a `rawResponse` property.

```typescript
const { data, rawResponse } = await client.drugSafety.check(...).withRawResponse();

console.log(data);
console.log(rawResponse.headers['X-My-Header']);
```

### Logging

The SDK supports logging. You can configure the logger by passing in a `logging` object to the client options.

```typescript
import { SafeRxClient, logging } from "saferx-pharma-sdk";

const client = new SafeRxClient({
    ...
    logging: {
        level: logging.LogLevel.Debug, // defaults to logging.LogLevel.Info
        logger: new logging.ConsoleLogger(), // defaults to ConsoleLogger
        silent: false, // defaults to true, set to false to enable logging
    }
});
```
The `logging` object can have the following properties:
- `level`: The log level to use. Defaults to `logging.LogLevel.Info`.
- `logger`: The logger to use. Defaults to a `logging.ConsoleLogger`.
- `silent`: Whether to silence the logger. Defaults to `true`.

The `level` property can be one of the following values:
- `logging.LogLevel.Debug`
- `logging.LogLevel.Info`
- `logging.LogLevel.Warn`
- `logging.LogLevel.Error`

To provide a custom logger, you can pass in an object that implements the `logging.ILogger` interface.

<details>
<summary>Custom logger examples</summary>

Here's an example using the popular `winston` logging library.
```ts
import winston from 'winston';

const winstonLogger = winston.createLogger({...});

const logger: logging.ILogger = {
    debug: (msg, ...args) => winstonLogger.debug(msg, ...args),
    info: (msg, ...args) => winstonLogger.info(msg, ...args),
    warn: (msg, ...args) => winstonLogger.warn(msg, ...args),
    error: (msg, ...args) => winstonLogger.error(msg, ...args),
};
```

Here's an example using the popular `pino` logging library.

```ts
import pino from 'pino';

const pinoLogger = pino({...});

const logger: logging.ILogger = {
  debug: (msg, ...args) => pinoLogger.debug(args, msg),
  info: (msg, ...args) => pinoLogger.info(args, msg),
  warn: (msg, ...args) => pinoLogger.warn(args, msg),
  error: (msg, ...args) => pinoLogger.error(args, msg),
};
```
</details>


### Runtime Compatibility


The SDK works in the following runtimes:



- Node.js 18+
- Vercel
- Cloudflare Workers
- Deno v1.25+
- Bun 1.0+
- React Native

### Customizing Fetch Client

The SDK provides a way for you to customize the underlying HTTP client / Fetch function. If you're running in an
unsupported environment, this provides a way for you to break glass and ensure the SDK works.

```typescript
import { SafeRxClient } from "saferx-pharma-sdk";

const client = new SafeRxClient({
    ...
    fetcher: // provide your implementation here
});
```

## Contributing

While we value open-source contributions to this SDK, this library is generated programmatically.
Additions made directly to this library would have to be moved over to our generation code,
otherwise they would be overwritten upon the next generated release. Feel free to open a PR as
a proof of concept, but know that we will not be able to merge it as-is. We suggest opening
an issue first to discuss with us!

On the other hand, contributions to the README are always very welcome!