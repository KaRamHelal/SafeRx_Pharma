# SafeRx C# SDK

Screen drugs for adverse effects, interactions, pregnancy/lactation risks, food interactions, and dosing across 66,000+ Egyptian pharmaceuticals.

## Installation

```bash
dotnet add package SafeRx
```

## Quick Start

```csharp
using SaferxApi;

var client = new SaferxApiClient("sfx_free_YOUR_KEY_HERE");

var response = await client.DrugSafety.CheckAsync(new DrugSafetyCheckRequest
{
    Drugs = new[] { "Augmentin 1g", "Glucophage 500mg", "Marivan" },
    Include = new[] { "ae", "ddi", "pllr", "food", "clinical", "dose" },
    Lang = "en"
});

// High-severity alerts bubbled to top
foreach (var alert in response.Alerts)
{
    Console.WriteLine($"[{alert.Severity}] {alert.Message}");
}
```

## Documentation

- **API Docs:** https://docs.saferx.online
- **GitHub:** https://github.com/KaRamHelal/SafeRx_Pharma
- **Get a free API key:** `POST https://saferx.online/api/developers/keys/free`

## Safety Domains

| Domain | Description |
|--------|-------------|
| `ae` | Adverse effects, Black Box Warnings, monitoring |
| `ddi` | Drug-drug interactions (requires 2+ drugs) |
| `pllr` | Pregnancy & lactation risk ratings |
| `food` | Meal timing & food-drug conflicts |
| `clinical` | Population & condition safety alerts |
| `dose` | Maximum daily dose (dual-source: WHO DDD + OpenFDA MDD) |

## License

MIT
