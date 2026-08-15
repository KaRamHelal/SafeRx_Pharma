# SafeRx

Signed .NET client for the [SafeRx Enterprise API](https://docs.saferx.online).

```xml
<PackageReference Include="SafeRx" Version="2.0.2-preview.1" />
```

```csharp
using SafeRx;

using var http = new HttpClient();
var client = new SafeRxClient(
    http,
    new Uri("https://saferx.online/api/enterprise/v1"),
    Environment.GetEnvironmentVariable("SAFERX_API_KEY")!
);

var result = await client.RequestAsync(
    "enterprise_safety_check",
    new {
        locale = "en",
        medications = new[] { new { input_text = "Augmentin 1g" } },
        requested_domains = new[] { "ddi" }
    },
    idempotencyKey: "safety-check-001"
);
```

Full docs: https://docs.saferx.online
