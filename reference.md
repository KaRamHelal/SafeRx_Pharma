# Reference
## Drug Safety
<details><summary><code>client.drugSafety.<a href="/src/api/resources/drugSafety/client/Client.ts">check</a>({ ...params }) -> SafeRx.DrugSafetyCheckResponse</code></summary>
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

```typescript
await client.drugSafety.check({
    drugs: ["Augmentin 1g", "Glucophage 500mg", "Marivan"],
    lang: "en"
});

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

**request:** `SafeRx.DrugSafetyCheckRequest` 
    
</dd>
</dl>

<dl>
<dd>

**requestOptions:** `DrugSafetyClient.RequestOptions` 
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.drugSafety.<a href="/src/api/resources/drugSafety/client/Client.ts">getMetadata</a>() -> SafeRx.MetadataResponse</code></summary>
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

```typescript
await client.drugSafety.getMetadata();

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

**requestOptions:** `DrugSafetyClient.RequestOptions` 
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.drugSafety.<a href="/src/api/resources/drugSafety/client/Client.ts">getDrugSafetyHealth</a>() -> SafeRx.GetDrugSafetyHealthResponse</code></summary>
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

```typescript
await client.drugSafety.getDrugSafetyHealth();

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

**requestOptions:** `DrugSafetyClient.RequestOptions` 
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Developers
<details><summary><code>client.developers.<a href="/src/api/resources/developers/client/Client.ts">createFreeKey</a>({ ...params }) -> SafeRx.CreateFreeKeyDevelopersResponse</code></summary>
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

```typescript
await client.developers.createFreeKey({
    email: "developer@example.com"
});

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

**request:** `SafeRx.CreateFreeKeyDevelopersRequest` 
    
</dd>
</dl>

<dl>
<dd>

**requestOptions:** `DevelopersClient.RequestOptions` 
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.developers.<a href="/src/api/resources/developers/client/Client.ts">verifyFreeKey</a>({ ...params }) -> SafeRx.VerifyFreeKeyDevelopersResponse</code></summary>
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

```typescript
await client.developers.verifyFreeKey({
    email: "developer@example.com",
    code: "123456"
});

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

**request:** `SafeRx.VerifyFreeKeyDevelopersRequest` 
    
</dd>
</dl>

<dl>
<dd>

**requestOptions:** `DevelopersClient.RequestOptions` 
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>
