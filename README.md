# SafeRx Enterprise API

[![API contract](https://img.shields.io/badge/contract-Enterprise%20v1-0f766e)](openapi/enterprise-v1.yaml)
[![Documentation](https://img.shields.io/badge/docs-docs.saferx.online-0f766e)](https://docs.saferx.online)
[![Fern mirror](https://img.shields.io/badge/Fern-saferx.docs.buildwithfern.com-0f766e)](https://saferx.docs.buildwithfern.com)

SafeRx is a regional medication-safety and prescription platform for pharmacies,
prescribers, and health systems. This repository is the public Enterprise API
surface: the OpenAPI contract, signed-request Python/TypeScript/C# SDKs, and the
source for the developer documentation at [docs.saferx.online](https://docs.saferx.online).

The Enterprise API is available to approved customers with an issued API key
and the entitlement for each route. This repository does not issue keys —
access is provisioned through SafeRx's Enterprise release process (see
[Developer access](https://docs.saferx.online/authentication/developer-portal)).

## Surface

All API calls use the Enterprise base URL:

`https://saferx.online/api/enterprise/v1`

The authenticated Enterprise contract includes:

- platform status and capabilities;
- bilingual registry autocomplete, search, resolution, product detail, and ingredient lookup;
- bounded medication safety checks, check retrieval, batch checks, and eRx safety;
- allergy reference resolution, family listing, and substance search;
- prescription OCR upload, status, events, medication resolution, safety, and review.

Route access is entitlement-bound: `registry_basic` covers registry lookup,
`erx` covers the eRx safety route, and `ocr_prescription` covers the OCR
workflow. MCP tools remain internal-only even though the Enterprise REST routes
they call are available to authenticated customers.

The contract is closed-schema. Responses do not permit undeclared top-level
fields, and the public projection does not contain storage, model, credential, or
person-specific fields.

## Authentication

Enterprise REST uses `saferx-hmac-sha256-v1`. Every request requires:

- `X-SafeRx-API-Key`
- `X-SafeRx-Timestamp`
- `X-SafeRx-Nonce`
- `X-SafeRx-Signature`

The signature binds the uppercase method, escaped path, RFC3986-sorted query,
lowercase SHA-256 body digest, timestamp, and nonce. The SDKs in `packages/`
implement this signing behavior. Do not copy the signing secret into source,
logs, or examples.

## Quick example

Use the generated Python client:

```python
from saferx_pharma import SafeRxClient

client = SafeRxClient(
    base_url="https://saferx.online/api/enterprise/v1",
    api_key="YOUR_ENTERPRISE_KEY",
)

result = client.enterprise_safety_check(
    body={
        "locale": "en",
        "medications": [{"input_text": "Augmentin 1g"}],
        "requested_domains": ["ddi", "food_interactions"],
    },
    idempotency_key="integration-check-001",
)
```

The operation method names are the OpenAPI operation IDs. See the contract for
request and response shapes.

## Repository layout

```
openapi/enterprise-v1.yaml       # public Enterprise API projection
openapi/components.yaml          # closed public schemas and signed headers
packages/python/                 # signing-aware Python client
packages/typescript/             # signing-aware TypeScript client
packages/csharp/                 # signing-aware C# client
packages/mcp-server/             # stdio MCP adapter (internal-only, being superseded)
fern/                            # Fern API reference and documentation source
postman/                         # signed-request examples
release/current.yaml             # current release manifest
scripts/release_preflight.py     # release and mirror validation
scripts/generate_enterprise_sdks.py  # SDK/client generation
CHANGELOG.md                     # release history
```

## Validation

```bash
python scripts/release_preflight.py
python scripts/generate_enterprise_sdks.py --check
cd packages/mcp-server && npm ci && npm run build
```

The current public release identity is recorded in `release/current.yaml`.

## Documentation

- [Enterprise API reference](https://docs.saferx.online)
- [Fern documentation mirror](https://saferx.docs.buildwithfern.com)
- [OpenAPI contract](openapi/enterprise-v1.yaml)
- [Postman collection](postman/SafeRx-Enterprise-API.postman_collection.json)
- [Release history](CHANGELOG.md)

## License

MIT
