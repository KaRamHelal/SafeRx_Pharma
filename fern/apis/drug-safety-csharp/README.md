# SafeRx Drug Safety API - C# SDK

This directory contains the Fern configuration for generating the C# SDK.

## Generating the SDK

```bash
cd fern/apis/drug-safety-csharp
fern generate --group csharp-sdk
```

## Known Issues

### StringContent Disposal Bug (Fern v2.20.5)

The generated SDK has a bug in retry logic that causes `ObjectDisposedException`.

**Symptom:**
```
System.ObjectDisposedException: Cannot access a disposed object.
Object name: 'System.Net.Http.StringContent'.
```

**Root Cause:**
The `CloneRequestAsync()` method in the generated `RawClient.cs` reuses the `StringContent` reference instead of creating a new instance. When retry disposes the cloned request, it also disposes the shared content.

**Workaround:**
After regenerating, manually patch `RawClient.cs` to clone `StringContent` instances in the retry path. This will be unnecessary once Fern fixes the upstream bug.

## Publishing

```bash
cd generated/csharp-sdk
dotnet pack -c Release
dotnet nuget push bin/Release/SaferxApi.X.Y.Z.nupkg \
  --api-key YOUR_NUGET_KEY \
  --source https://api.nuget.org/v3/index.json
```

## Files

- `generators.yml` - Fern generator configuration (currently using v2.20.5)
- `openapi/openapi.yaml` - OpenAPI 3.0.3 spec (converted from 3.1.1 for C# compatibility)

## SDK Differences from Python/TypeScript

1. **OpenAPI Version**: Uses 3.0.3 (not 3.1.1) due to C# generator requirements
2. **Nullable Handling**: `nullable: true` instead of `oneOf` with null type
3. **Field Naming**: PascalCase properties with snake_case JSON serialization

## Version History

- **0.0.5** (2026-02-17): Fixed ObjectDisposedException bug
- **0.0.4** (2026-02-17): Initial release with auth param fix
- **0.0.3** (2026-02-16): Namespace updates
- **0.0.1-0.0.2** (2026-02-15): Initial development
