# Reference
## Drug Safety
<details><summary><code>client.drug_safety.<a href="src/saferx/drug_safety/client.py">check</a>(...) -&gt; AsyncHttpResponse[DrugSafetyCheckResponse]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Screen one or more drugs across six safety domains in a single request.

The API resolves drug names via fuzzy matching, runs all requested safety
checks in parallel, and returns a unified response with alerts bubbled to
the top for easy triage.

**Typical response time:** ~40ms (warm cache, 3 drugs, all domains).
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from saferx import SafeRxClient

client = SafeRxClient(
    api_key="YOUR_API_KEY",
)
client.drug_safety.check(
    drugs=["Augmentin 1g", "Glucophage 500mg"],
    lang="ar",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**drugs:** `typing.Sequence[str]` 

Drug names to screen. Accepts trade names (e.g., "Augmentin 1g"),
generic names (e.g., "amoxicillin"), or partial matches.
Fuzzy matching resolves names to SafeRx product IDs.

- **Free/Pro tier:** max 20 drugs per request
- **Enterprise tier:** max 50 drugs per request
    
</dd>
</dl>

<dl>
<dd>

**patient_profile:** `typing.Optional[PatientProfile]` 
    
</dd>
</dl>

<dl>
<dd>

**include:** `typing.Optional[typing.Sequence[DomainCode]]` 

Safety domains to check. Omit to run all six domains.
Including fewer domains reduces response size and may improve latency.
    
</dd>
</dl>

<dl>
<dd>

**lang:** `typing.Optional[DrugSafetyCheckRequestLang]` 

Response language. Controls bilingual fields such as rationale text,
drug name translations, and clinical advice.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.drug_safety.<a href="src/saferx/drug_safety/client.py">get_metadata</a>() -&gt; AsyncHttpResponse[MetadataResponse]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns available populations, conditions, database versions, risk level
scales, and current tier limits.

Use this endpoint to:
- Populate dropdown menus with valid population and condition values
- Check database versions and coverage statistics
- Verify your tier and rate limits
- Cache metadata locally (changes infrequently — safe to cache for 24 hours)
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from saferx import SafeRxClient

client = SafeRxClient(
    api_key="YOUR_API_KEY",
)
client.drug_safety.get_metadata()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.drug_safety.<a href="src/saferx/drug_safety/client.py">get_drug_safety_health</a>() -&gt; AsyncHttpResponse[GetDrugSafetyHealthResponse]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns health status of the Drug Safety API subsystem including
overall system health and availability.

No authentication required. Designed for monitoring services.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from saferx import SafeRxClient

client = SafeRxClient(
    api_key="YOUR_API_KEY",
)
client.drug_safety.get_drug_safety_health()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Developers
<details><summary><code>client.developers.<a href="src/saferx/developers/client.py">create_free_key</a>(...) -&gt; AsyncHttpResponse[CreateFreeKeyDevelopersResponse]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Step 1 of 2: Request a verification code to get a free API key.

- Sends a 6-digit code to your email (expires in 30 minutes)
- Max 5 codes per email per hour (anti-spam)
- If email already has a verified key, returns it immediately
- Use POST /api/developers/keys/free/verify with the code to receive your key
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from saferx import SafeRxClient

client = SafeRxClient(
    api_key="YOUR_API_KEY",
)
client.developers.create_free_key(
    email="developer@example.com",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**email:** `str` — Your email address
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.developers.<a href="src/saferx/developers/client.py">verify_free_key</a>(...) -&gt; AsyncHttpResponse[VerifyFreeKeyDevelopersResponse]</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Step 2 of 2: Verify your email with the 6-digit code and receive your API key.

- Code expires after 30 minutes
- Max 5 wrong attempts per code (then must request new code)
- On success: issues sfx_free_ key (persistent, 1 per email)
- Free tier: 20 requests/minute, 60 requests/day
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from saferx import SafeRxClient

client = SafeRxClient(
    api_key="YOUR_API_KEY",
)
client.developers.verify_free_key(
    email="developer@example.com",
    code="123456",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**email:** `str` — The email you used in step 1
    
</dd>
</dl>

<dl>
<dd>

**code:** `str` — 6-digit verification code from email
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

