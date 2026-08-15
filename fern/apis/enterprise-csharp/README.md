# SafeRx Enterprise C# SDK

Fern uses `openapi/enterprise-v1.yaml` as the API reference input. The published `SafeRx` NuGet
package is generated from this spec — see `packages/csharp` in the repository root for the
checked-in client used for integration validation.

```bash
cd fern/apis/enterprise-csharp
fern generate --group csharp-sdk
```

Do not run this against a spec other than the current `openapi/enterprise-v1.yaml` (or its
in-sync mirror here) — a stale spec produces client code for routes that no longer exist.
