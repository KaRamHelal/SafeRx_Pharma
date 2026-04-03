# SafeRx Drug Safety API - C# SDK

This directory contains the Fern configuration for generating the C# SDK.

## Generating the SDK

```bash
cd fern/apis/drug-safety-csharp
fern generate --group csharp-sdk
```

## ⚠️ Known Issues

### StringContent Disposal Bug (Fern v2.20.5)

The generated SDK has a bug in retry logic that causes `ObjectDisposedException` when sandbox mode is disabled.

**Symptom:**
```
System.ObjectDisposedException: Cannot access a disposed object.
Object name: 'System.Net.Http.StringContent'.
```

**Root Cause:**
The `CloneRequestAsync()` method in `RawClient.cs` reuses the `StringContent` reference instead of creating a new instance. When the retry logic disposes the cloned request, it also disposes the shared content, causing subsequent operations to fail.

**Workaround:**

After regenerating the SDK, run the auto-fix script:

```bash
fern generate --group csharp-sdk
python scripts/fix_csharp_sdk_bug.py
```

To verify if the fix is applied:

```bash
python scripts/fix_csharp_sdk_bug.py --check
```

**Testing:**

```bash
cd testing/csharp_erp_simulation
dotnet build
dotnet run
```

All 3 test scenarios should pass without `ObjectDisposedException`.

**Tracking:**

This issue is tracked internally. The fix will be removed once Fern releases a version with the bug fixed.

## Publishing

After applying the fix:

```bash
cd generated/csharp-sdk

# Bump version in .version file
# Update CHANGELOG.md

# Build and publish
dotnet pack -c Release
dotnet nuget push bin/Release/SaferxApi.X.Y.Z.nupkg \
  --api-key [FROM E:\Secure\fern_sdk_publishing.txt] \
  --source https://api.nuget.org/v3/index.json
```

## Files

- `generators.yml` - Fern generator configuration (currently using v2.20.5)
- `openapi/openapi.yaml` - OpenAPI 3.0.3 spec (converted from 3.1.1 for C# compatibility)
- Output: `../../generated/csharp-sdk/`

## SDK Differences from Python/TypeScript

1. **OpenAPI Version**: Uses 3.0.3 (not 3.1.1) due to C# generator requirements
2. **Nullable Handling**: `nullable: true` instead of `oneOf` with null type
3. **Field Naming**: PascalCase properties with snake_case JSON serialization
4. **Manual Fix**: Requires StringContent cloning fix after generation

## Version History

- **0.0.5** (2026-02-17): Fixed ObjectDisposedException bug
- **0.0.4** (2026-02-17): Initial release with auth param fix
- **0.0.3** (2026-02-16): Namespace updates
- **0.0.1-0.0.2** (2026-02-15): Initial development
