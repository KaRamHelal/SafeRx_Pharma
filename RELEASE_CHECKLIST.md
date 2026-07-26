# Release Checklist (SafeRx_Pharma)

## Before pushing
- Sync `fern/` + `openapi/` from `SafeRx_OCR`.
- If `mcp-server/**` changed, bump MCP version in:
  - `mcp-server/package.json`
  - `mcp-server/src/index.ts` (`version` and `USER_AGENT` string)

## Required repo secrets
- `FERN_TOKEN`
- `PYPI_TOKEN`
- `NPM_TOKEN`
- `NUGET_API_KEY`

## Workflow behavior (`Publish SDKs`)
- Always publishes Python + TypeScript + C# SDKs and docs.
- Publishes MCP **only when** `mcp-server/**` changed.
- MCP publish fails if version is not bumped.
- Concurrency is enabled: newer runs auto-cancel older in-progress runs.

## Common failure fix
### `npm ci` lockfile error in MCP step
- Pipeline now uses `npm install` in MCP step.
- If this reappears, verify workflow file wasn't reverted.

### Docs step hangs
- Docs step is non-interactive (`--force --no-prompt`) and has a timeout.

## Verification
- Actions run succeeds end-to-end.
- npm package version updates:
  - `npm view @saferx_pharma/mcp-server version`
- Docs live:
  - `https://docs.saferx.online`
