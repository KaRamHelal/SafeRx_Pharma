# saferx-pharma-sdk

Signed TypeScript client for the [SafeRx Enterprise API](https://docs.saferx.online).

**Server-side use only.** This client signs every request with your API key
as the HMAC secret -- never import or bundle it into browser or
client-controlled code.

```bash
npm install saferx-pharma-sdk
```

```typescript
import { SafeRxClient } from "saferx-pharma-sdk";

const client = new SafeRxClient(
  "https://saferx.online/api/enterprise/v1",
  process.env.SAFERX_API_KEY!,
);

const result = await client.request("enterprise_safety_check", {
  body: {
    locale: "en",
    medications: [{ input_text: "Augmentin 1g" }],
    requested_domains: ["ddi"],
  },
  idempotencyKey: "safety-check-001",
});
```

Full docs: https://docs.saferx.online
