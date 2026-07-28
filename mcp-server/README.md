# SafeRx Enterprise MCP adapter

This stdio adapter exposes signed SafeRx Enterprise operations to MCP hosts.
MCP is an internal-only surface; it is separate from authenticated Enterprise
REST availability.

## Run

```bash
SAFERX_API_KEY=YOUR_ENTERPRISE_KEY npx @saferx_pharma/mcp-server
```

The optional `SAFERX_BASE_URL` defaults to:

```text
https://saferx.online/api/enterprise/v1
```

The key is read only from the process environment. Do not commit it to an MCP
configuration file.

## Tools

| Tool | Operation |
|---|---|
| `enterprise_status` | `GET /status` |
| `enterprise_capabilities` | `GET /capabilities` |
| `enterprise_registry_search` | `GET /registry/search` |
| `enterprise_safety_check` | `POST /safety/checks` |

Every request uses the Enterprise HMAC signing headers. The package is not a
public package-availability claim and is released only through the MIS internal
artifact process.

## Build

```bash
npm ci
npm run build
```
