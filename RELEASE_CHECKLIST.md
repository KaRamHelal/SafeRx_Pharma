# Release Checklist (SafeRx_Pharma)

## Before publishing
- Run `python scripts/release_preflight.py`.
- Run `fern check --local --api drug-safety --strict-broken-links`.
- Sync the checked-in public OpenAPI and Fern mirrors from the approved public
  projection. Do not copy internal MIS components or OCR payload fields.
- For an MIS release, set the coordinated version in:
  - `release/<version>.yaml`
  - `mcp-server/package.json`
  - `mcp-server/src/index.ts` (`version` and `USER_AGENT` string)

## Required repo secrets
- `FERN_TOKEN`
- `PYPI_TOKEN`
- `NPM_TOKEN`
- `NUGET_API_KEY`

## Workflow behavior (`Publish SDKs`)
- Publication runs only from an explicit `v*` tag or manual dispatch; ordinary
  `main` pushes run preflight only.
- Always publishes Python + TypeScript + C# SDKs and docs.
- Publishes the MCP server on every coordinated MIS release.
- The workflow refuses a release unless all artifact versions match the tag.
- The workflow refuses a release if any target registry already contains the
  immutable version.
- Concurrency is enabled: newer runs auto-cancel older in-progress runs.

## Common failure fix
### `npm ci` lockfile error in MCP step
- Pipeline now uses `npm install` in MCP step.
- If this reappears, verify workflow file wasn't reverted.

### Docs step hangs
- Docs step is non-interactive (`--force --no-prompt`) and has a timeout.

## Verification
- Verify every published package from a clean temporary environment before
  declaring the release complete.
- Actions run succeeds end-to-end.
- npm package version updates:
  - `npm view @saferx_pharma/mcp-server version`
- Docs live:
  - `https://docs.saferx.online`
