# SafeRx Enterprise MCP integration (legacy)

> **Deprecated.** This stdio MCP adapter has been superseded by SafeRx's
> [hosted MCP server](https://docs.saferx.online/ai-integration/mcp-server), a
> Streamable HTTP endpoint at `/api/enterprise-mcp/v1/mcp` with the same three
> tools. Use the hosted endpoint for new integrations — it requires no local
> process and stays in sync with the Enterprise API automatically.

This package remains `internal_only` per
`contracts/public-availability-state-machine.yaml` in the SafeRx-MIS repository
— it is not part of the supported Enterprise API surface and is not a
substitute for the published authenticated Enterprise REST contract or the
hosted MCP endpoint. The source in `src/` is visible in this repository (it is
not secret), but it is not a supported public integration: no compatibility,
versioning, or support commitments apply to it.

## Build

```bash
npm ci
npm run build
```
