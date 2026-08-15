# SafeRx Enterprise C# SDK

The SafeRx Enterprise client targets .NET 8 and uses the signed Enterprise request contract.

```csharp
using SafeRx;

var client = new SafeRxClient(
    http,
    new Uri("https://saferx.online/api/enterprise/v1"),
    Environment.GetEnvironmentVariable("SAFERX_API_KEY")!
);

var result = await client.RequestAsync(
    "enterprise_safety_check",
    body: request,
    idempotencyKey: "safety-check-001"
);
```

Enterprise API access requires an issued API key; this package alone does not grant access.
