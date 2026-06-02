# SafeRx C# SDK

Official .NET SDK for the [SafeRx Drug Safety API](https://docs.saferx.online) — screen drugs across 7 safety domains covering 66,704 Egyptian pharmaceutical products.

## Installation

```bash
dotnet add package SafeRx
```

**Requirements:** .NET 8.0+, .NET Framework 4.6.2+, or .NET Standard 2.0+

## Quick Start

```csharp
using SaferxApi;

var client = new SaferxApiClient(
    apiKey: "sfx_free_your_key_here"
);

var response = await client.DrugSafety.CheckAsync(
    new DrugSafetyCheckRequest
    {
        Drugs = new List<string> { "Augmentin 1g", "Glucophage 500mg", "Marivan" },
        Lang = DrugSafetyCheckRequestLang.En,
    }
);

Console.WriteLine($"Status: {response.Status}");

foreach (var drug in response.Drugs)
{
    Console.WriteLine($"  {drug.BrandName} ({drug.ActiveIngredient}) - {drug.PriceEgp} EGP");
}

// Check alerts (highest priority safety issues)
foreach (var alert in response.Alerts)
{
    Console.WriteLine($"  [{alert.Severity}] {alert.Message}");
}
```

## Get an API Key

```bash
# Request verification code
curl -X POST https://saferx.online/api/developers/keys/free \
  -H "Content-Type: application/json" \
  -d '{"email":"you@example.com"}'

# Verify and receive key
curl -X POST https://saferx.online/api/developers/keys/free/verify \
  -H "Content-Type: application/json" \
  -d '{"email":"you@example.com","code":"123456"}'
```

Or register at the [Developer Portal](https://saferx.online/developer).

## Key Classes

| NuGet Package | `SafeRx` |
|---------------|----------|
| **Namespace** | `SaferxApi` |
| **Client class** | `SaferxApiClient` |
| **Import** | `using SaferxApi;` |

## Documentation

- [Full API docs](https://docs.saferx.online)
- [C# SDK guide](https://docs.saferx.online/sdks/c-sharp)
- [API Reference](https://docs.saferx.online/api-reference)
