# SafeRx Enterprise MCP integration

> **Being superseded.** This stdio MCP adapter is scheduled to be replaced by
> SafeRx's hosted MCP surface. It is not the intended long-term MCP
> integration path — treat it as a legacy stopgap, not a stable target to
> build against.

This directory is `internal_only` per `contracts/public-availability-state-machine.yaml`
in the SafeRx-MIS repository — it is not part of the supported Enterprise API
surface and is not a substitute for the published authenticated Enterprise
REST contract. The source in `src/` is visible in this repository (it is not
secret), but it is not a supported public integration: no compatibility,
versioning, or support commitments apply to it.

## Build

```bash
npm ci
npm run build
```
