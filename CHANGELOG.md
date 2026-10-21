# Changelog

All notable changes to the SafeRx Enterprise API, SDKs, and MCP adapter are
documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/);
releases are tagged `vX.Y.Z`.

Release history before this file existed (2026-08) predates consistent GitHub
Releases tracking. For the complete published version history, see
[PyPI (saferx-pharma)](https://pypi.org/project/saferx-pharma/#history),
[npm (saferx-pharma-sdk)](https://www.npmjs.com/package/saferx-pharma-sdk?activeTab=versions),
and [NuGet (SafeRx)](https://www.nuget.org/packages/SafeRx#versions-body-tab).
Entries below are not a backfilled reconstruction of that history.

## [2.0.5] - 2026-10-21

### Added
- `enterprise_erx_safety_check` has a working request contract. `erx_payload` is a structured
  prescription: `prescription_ref`, `lines[]` (1-50; `line_ref`, `input_text` and/or `sfrx_id`,
  `dose_text`/`route`/`dosage_form` to pick the product, `frequency_text`/`duration_text`
  echoed only), `current_medications[]` and `patient_context`. `requested_domains` is optional.
  The response is a `SafetyCheckResponse` with an `erx` echo of the prescription, line by line.
  Until this release no documented eRx body could succeed: the previous `erx_payload` was an
  empty closed object the backend refused.

### Fixed
- `SafetyCheckResponse` `signals[].risk_display.raw_source_label` is nullable; production
  returns `null` when the source carries no native label.
- The five deferred operations declare the `503 capability_unavailable` they return to an
  entitled caller, beside the `403 API_KEY_NOT_ENTITLED` every other caller receives.

## [2.0.4] - 2026-10-21

A support ticket could not run a DDI check at all: plain names returned
`422 target_resolution_required`, and `sfrx_id` values returned `503`. The
backend now resolves the way customers write medicines; this release carries
the contract and client side.

### Added
- **Medications may be given by `sfrx_id` alone.** `input_text` is optional
  when `sfrx_id` is present on `enterprise_safety_check` and
  `enterprise_registry_resolve` (and the hosted MCP tools). An explicit
  `sfrx_id` is authoritative and an unknown one is reported as
  `sfrx_id_unknown`, never replaced by a text match.
- **`dose_text`, `route` and `dosage_form` on safety-check medications.** They
  select the registry product (strength, route, form) and are not read by the
  safety evaluation. Inline qualifiers in `input_text` ("Warfarin 5 mg tablet",
  "Augmentin 1g", Arabic units) are parsed the same way.
- **A bare name runs the check.** "Warfarin" or "Aspirin" is evaluated as its
  default systemic variant with `review.required: true`,
  `default_variant_selected` (or `equivalent_product_selected`) in the reason
  codes, and a limitation naming the product and how to pin it.
- **`resolved_medications[]`** on `SafetyCheckResponse`: which registry product
  each request medication was evaluated as, with `resolution_status` and
  `review_reason_codes` (table in the Safety results concept page).

- **`enterprise_capabilities` and `enterprise_status` are available.** Both were
  published as deferred while production had been serving them to every entitled
  key; they are promoted with their real schemas (`EnterpriseCapabilities`,
  `EnterpriseStatus`), SDK methods and example fixtures, live-verified on
  2026-10-21. 16 operations are now available, 5 remain deferred.
- **Idempotent replay.** A retry with the same `Idempotency-Key` and body returns
  the original response with `X-SafeRx-Idempotent-Replay: true`; the same key with
  a different body is `409 quota.idempotency.conflict` (Rate limits page).
- **`SafetyCheckResponse` declares every field production returns**:
  `context_summary.context_sources` / `profile_context_version`,
  `display_obligations.approved_summary_template_id`, per-domain and per-signal
  `correction_anchors`, `SafetySignal.risk_display` / `title_origin` /
  `patient_context_attribution`, `LocalizedString.ar_normalized` / `eg_ar` /
  `source_locale`, and `SourceProvenance.model_release_id` / `resolver_version` /
  `search_artifact_id`. A strict client built to 2.0.3 rejected real responses.

### Fixed
- A retry with the same `Idempotency-Key` returned
  `503 trusted_accounting_finalization_unavailable` on every idempotency-governed
  operation (safety check, e-Rx check, OCR create), so the SDKs' retry loops never
  recovered from a transient failure. Server-side defect, fixed 2026-10-21.
- The hosted MCP tools `check_medication_safety` and `resolve_medications`
  answered every real call with `isError: "SafeRx rejected an invalid upstream
  response"`. Server-side defect in output validation, fixed 2026-10-21.
- Deferred operations denied inconsistently: four returned `503
  capability_unavailable` to callers without the bundle, one returned the
  documented `403 API_KEY_NOT_ENTITLED`. Every route now authenticates and checks
  entitlement first; `503 capability_unavailable` is reserved for an entitled
  caller of a disabled capability (Authentication overview, "Denial order").
- Internal per-domain adapter telemetry (`adapter_id`, `adapter_version`,
  `adapter_health_status`, `adapter_limitations`, `missing_context_reasons`,
  `schema_version`, `source_version`, `domain_release_id`) leaked on every
  `domain_coverage` item. Removed server-side; the published item schema was
  already right.
- `frequency_text` was advertised on safety-check medications but the backend
  refused it with `422`; it is removed from the contract and the MCP server
  schema. The backend now names the refused field in `request_invalid`.
- A one-character or over-long `input_text` next to other medications no longer
  fails the whole request (it was a `503 dependency_unavailable`); that entry is
  `unresolved` with `query_rejected` and the rest are evaluated.

## [2.0.3] - 2026-09-23

Outside-developer blackbox pass (published 2.0.2 packages, public repository
and docs.saferx.online only, real signed calls against production) found the
defects below. Backend corrections shipped in SafeRx production the same day;
this release carries the client and contract side.

### Fixed
- **Python and TypeScript clients reused the first attempt's nonce, timestamp,
  and signature on every retry.** The API rejects a reused nonce as a replay,
  so any transient `429`/`502`/`503`/`504` followed by the client's own retry
  ended in a hard denial instead of the retried result. Both clients now sign
  every attempt afresh (same `X-Request-ID` and `Idempotency-Key`, new nonce).
  The C# client already did this. Regression-tested behaviorally.
- **The Postman collection could never sign a request**: its pre-request
  script declared `query` twice (a syntax error, so it never ran) and signed
  an undefined `path`. It also targeted `/status` and `/capabilities`, two
  deferred operations no key can reach. Rewritten to a working
  `saferx-hmac-sha256-v1` implementation covering registry search,
  autocomplete, resolve, safety capabilities, and a safety check.
- `LocalizedString.en`/`.ar` no longer require a non-empty string: real
  registry records carry an empty string where no text exists in that
  language (for example `route.ar` on many products), so a strict validator
  rejected every live search, autocomplete, and product-detail response.
- `SourceProvenance` documents `arabic_content_snapshot_id`, present on every
  registry response. `model_release_id`, `resolver_version`, and
  `search_artifact_id` (pipeline identity the schema description already
  excluded) are now stripped server-side instead of leaking.
- `RegistryProductDetail`: documented `pharmacology.mechanism`,
  `pharmacology.summary`, `prose_details.directions_en`, and
  `warnings.warnings_en`, all returned live and previously undeclared; the
  internal `warnings.safety_check_actions` and the resolve echo's
  `query.source` are stripped server-side.
- `ProblemDetails.code` now documents the signed-request denial codes. Until
  this release every authentication or authorization failure was a single
  `403 API_KEY_DENIED`, so a wrong signature, a replayed nonce, and a missing
  entitlement were indistinguishable; the API now returns `401` with
  `API_KEY_INVALID` / `API_KEY_SIGNATURE_INVALID` / `API_KEY_TIMESTAMP_INVALID`
  / `API_KEY_NONCE_REJECTED`, and `403` with `API_KEY_NOT_ENTITLED` /
  `API_KEY_EXPIRED` / `API_KEY_DENIED`. The authentication guide carries the
  table.
- MCP guide: a key without `mcp_standard` is denied at the gateway for every
  JSON-RPC method (there is no filtered `tools/list`), and the hosted MCP
  endpoint no longer leaks `policy_id` in its denials.
- Developer access guide: links the actual self-service signup page and states
  that `enterprise_free` grants every documented surface (registry, safety,
  eRx, OCR, hosted MCP). Self-serve and admin-issued keys had been issued
  with registry-only route access because the plan catalog named entitlement
  bundles that did not exist; keys now derive their access from the
  organization's plan at validation time.
- Key rotation and revocation are described as handled by SafeRx on request;
  the Partner portal key console is not yet self-service, and the previous
  wording told developers to use it.
- `enterprise_capabilities`, `enterprise_status`, `enterprise_safety_check_read`,
  `enterprise_safety_check_batch`, `enterprise_allergy_resolve`,
  `enterprise_allergy_families`, and `enterprise_allergy_substances` were
  documented as returning `501` once reached. No backend implements them and
  no plan grants them, so every caller gets `403` (now `API_KEY_NOT_ENTITLED`).
  Corrected the documented response for all seven.
- Registry search/autocomplete/product-detail responses had carried
  `correction_anchors` and three internal Arabic-normalization keys on every
  `LocalizedString`; product detail also carried 14 undeclared fields. All
  stripped server-side (deployed 2026-09-14; confirmed absent in this pass).

### Added
- `RegistryProductSummaryList` and `RegistrySuggestionList` items document
  `manufacturer`, `product_tier`, `name_strength`, `match_reason`, `score`,
  and (for suggestions) `generic`/`strength`/`supplier`/`pharma_uses`/
  structured `match`.
- `MedicationResolution.candidates` rebuilt to the real shape
  (`candidate_id`, `confidence`, `display_name`, `normalized_name`,
  `dosage_form`, `route`, `manufacturer`, `strength`, `ingredient_names`,
  `match_reasons`, `equivalent_candidates`, `registry_concept_id`, `review`,
  `source_provenance`).

### Changed
- `scripts/release_preflight.py` fails if `release/current.yaml`'s
  `release_version` matches an already-tagged (`vX.Y.Z`) release whose
  `openapi/enterprise-v1.yaml`, `openapi/components.yaml`, or
  `release/current.yaml` content differs from what is checked in: a corrected
  contract always ships under a new version.

## [2.0.2] - 2026-08-15

### Fixed
- `ProblemDetails` was missing `operation_id` and `path`, both present on
  every real error response (confirmed against a live signed request to
  production); added both. `policy_id`, also present live, is deliberately
  not documented as public surface -- it is private policy-engine
  vocabulary that should be stripped at the gateway.
- `enterprise_registry_resolve`'s request schema required response-shaped
  fields no client could construct; corrected to the real
  locale + medications[] contract also used by the hosted MCP.
- `enterprise_erx_safety_check`'s request schema was an inline empty-object
  placeholder that rejected any real request; added the real
  `ErxSafetyCheckRequest` schema (`erx_payload` + `locale`).
- `SafetyCapabilities`'s response schema didn't match the real backend
  contract at all; rebuilt from the real shape (`domains`, `available`,
  `status`, snapshot IDs).
- `RegistryProductDetail`, `RegistryProductSummaryList`, and
  `RegistrySuggestionList` used invented field names (`display_name`,
  `generic_name`) instead of the real `tradename`/`generic` — affected
  three actively-available operations.
- `PrescriptionResult.candidate_medications`/`.transitions` and
  `SafetySignal.evidence_refs` were typed as always-empty objects that
  would reject any real populated response; given their real structure.
  `PrescriptionResult` was also missing the required `document_context`
  field.
- Removed private backend routing/accounting metadata (route class, response
  profile, quota metric) that every generated SDK client shipped as inert
  hardcoded fallback values.
- SDK clients now honor `Retry-After` and retry `429`, and support real
  `multipart/form-data` signing for `enterprise_ocr_prescription_create`
  (previously uncallable from any SDK — bodies were always JSON-encoded).

### Added
- `examples/` — synthetic request/response fixtures for every available
  operation, validated against the real bundled OpenAPI schemas in CI.
- Every operation now has a summary and description; every public schema
  property now has a description.
- Hosted MCP promoted from `internal_only` to `preview` — the three tools
  (`resolve_medications`, `check_medication_safety`,
  `get_safety_capabilities`) are documented at
  `/api/enterprise-mcp/v1/mcp`.
- New guides: Medication Identity, Patient Context, Safety Results,
  Registry Operations, eRx Safety Integration, OCR Prescription Lifecycle,
  Allergy Reference (documented as not yet available -- still 501 upstream).
- `.github/CODEOWNERS` for the public contract, SDK signing code, and
  release gates.
- The regression test suite now runs in CI on every PR and before every
  SDK publish (it previously only ran locally).

### Changed
- Repository reorganized: SDKs and the MCP adapter moved under `packages/`;
  the OpenAPI spec is now a single source of truth (`openapi/enterprise-v1.yaml`)
  mirrored into Fern via symlinks instead of hand-duplicated copies; release
  manifest renamed from a version-stamped filename to `release/current.yaml`.
- Public documentation pages corrected to reflect that the SDKs are actually
  published (they previously, incorrectly, described themselves as
  unpublished/internal-only).
- Quickstart, developer access, welcome, and terms pages corrected: the
  existing `enterprise_free` plan has real self-service signup (previous
  wording flatly claimed no self-service issuance existed at all).
- Security & Compliance pages expanded to cover credential storage,
  server-side-only SDK use, prohibited logging, synthetic-data testing,
  and incident reporting.
- Fixed a GitHub Actions script-injection risk in the SDK publish workflow
  (an untrusted `workflow_dispatch` input was interpolated directly into a
  shell script in a job holding registry publish secrets).
