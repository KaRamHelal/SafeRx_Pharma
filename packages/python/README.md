# saferx-pharma

Signed Python client for the [SafeRx Enterprise API](https://docs.saferx.online).

```bash
pip install saferx-pharma
```

```python
from saferx_pharma import SafeRxClient

client = SafeRxClient(
    base_url="https://saferx.online/api/enterprise/v1",
    api_key="YOUR_ENTERPRISE_KEY",
)

result = client.enterprise_safety_check(
    body={
        "locale": "en",
        "medications": [{"input_text": "Augmentin 1g"}],
        "requested_domains": ["ddi"],
    },
    idempotency_key="safety-check-001",
)
```

Server-side use only -- this client signs requests with your API key as the
HMAC secret. Never embed it in browser or client-controlled code.

Full docs: https://docs.saferx.online
