from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "packages/python/src"))

from saferx_pharma.client import canonical_request, sign_request  # noqa: E402


EXPECTED_OPERATIONS = {
    "enterprise_registry_autocomplete",
    "enterprise_registry_search",
    "enterprise_registry_resolve",
    "enterprise_registry_product_detail",
    "enterprise_registry_ingredients",
    "enterprise_safety_capabilities",
    "enterprise_safety_check",
    "enterprise_erx_safety_check",
    "enterprise_ocr_prescription_create",
    "enterprise_ocr_prescription_read",
    "enterprise_ocr_prescription_events",
    "enterprise_ocr_prescription_resolve",
    "enterprise_ocr_prescription_safety",
    "enterprise_ocr_prescription_review",
}

# Present in the OpenAPI (documented, honestly marked x-status: deferred) but must
# never carry a success response or ship in a generated SDK client -- the maintained
# MIS OpenAPI only defines 501 for these operations today.
DEFERRED_OPERATIONS = {
    "enterprise_capabilities",
    "enterprise_status",
    "enterprise_safety_check_read",
    "enterprise_safety_check_batch",
    "enterprise_allergy_resolve",
    "enterprise_allergy_families",
    "enterprise_allergy_substances",
}


def test_public_projection_matches_current_enterprise_operation_set() -> None:
    spec = yaml.safe_load((ROOT / "openapi/enterprise-v1.yaml").read_text())
    operations = {
        operation["operationId"]: operation
        for item in spec["paths"].values()
        for method, operation in item.items()
        if method in {"get", "post"}
    }
    assert set(operations) == EXPECTED_OPERATIONS | DEFERRED_OPERATIONS
    available = {
        operation_id
        for operation_id, operation in operations.items()
        if operation.get("x-status", "available") == "available"
    }
    assert available == EXPECTED_OPERATIONS
    for operation_id in DEFERRED_OPERATIONS:
        success_codes = {code for code in operations[operation_id]["responses"] if str(code)[0] in "23"}
        assert not success_codes, f"{operation_id} must not carry an invented success response"
    assert spec["servers"][0]["url"] == "https://saferx.online/api/enterprise/v1"


def test_deferred_operations_are_excluded_from_generated_sdk_clients() -> None:
    ts_client = (ROOT / "packages/typescript/src/client.ts").read_text()
    cs_client = (ROOT / "packages/csharp/SafeRxClient.cs").read_text()
    py_client = (ROOT / "packages/python/src/saferx_pharma/client.py").read_text()
    for operation_id in DEFERRED_OPERATIONS:
        assert f'"{operation_id}"' not in ts_client
        assert f'"{operation_id}"' not in cs_client
        assert f"{operation_id!r}" not in py_client


def test_public_response_schemas_are_closed() -> None:
    components = yaml.safe_load((ROOT / "openapi/components.yaml").read_text())
    serialized = (ROOT / "openapi/components.yaml").read_text()
    assert "additionalProperties: true" not in serialized
    assert components["components"]["securitySchemes"]["enterpriseApiKey"]["name"] == "X-SafeRx-API-Key"
    public_surface_values = components["components"]["schemas"]["SafetyCheckResponse"]["properties"]["surface"]["enum"]
    assert set(public_surface_values) == {"browser", "enterprise_api", "partner_api"}
    assert "enterprise_mcp" not in serialized
    assert "admin_console" not in serialized
    assert "private" not in public_surface_values


def test_signature_binds_the_full_enterprise_path() -> None:
    body = b'{"locale":"en"}'
    timestamp = "2026-07-26T12:00:00+00:00"
    nonce = "nonce-1"
    canonical = canonical_request(
        "POST",
        "/api/enterprise/v1/safety/checks",
        "",
        hashlib.sha256(body).hexdigest(),
        timestamp,
        nonce,
    )
    assert canonical.splitlines()[1] == "/api/enterprise/v1/safety/checks"
    assert sign_request("test-key", "POST", "/api/enterprise/v1/safety/checks", "", body, timestamp, nonce)


def test_safety_check_request_is_request_scoped_patient_context() -> None:
    components = yaml.safe_load((ROOT / "openapi/components.yaml").read_text())
    schemas = components["components"]["schemas"]
    request = schemas["ClientSafetyCheckRequest"]
    # Enterprise has no saved profile: these are Browser-only session controls and
    # must never be accepted on the Enterprise request.
    assert "profile_context_mode" not in request["properties"]
    assert "include_saved_current_medications" not in request["properties"]
    assert request["additionalProperties"] is False
    assert "patient_context" in request["properties"]
    assert request["properties"]["patient_context"]["$ref"] == "#/components/schemas/PatientSafetyContext"
    medication_item = request["properties"]["medications"]["items"]
    assert set(medication_item["properties"]["role"]["enum"]) == {"target_medication", "current_medication"}
    patient_context = schemas["PatientSafetyContext"]
    assert patient_context["additionalProperties"] is False
    response = schemas["SafetyCheckResponse"]["properties"]["context_summary"]
    assert set(response["properties"]["status"]["enum"]) == {"request_context_applied", "baseline_only"}
    # A saved-profile-sourced state would only be reachable if Enterprise merged a
    # saved profile, which it never does.
    assert "saved_profile_applied" not in response["properties"]["status"]["enum"]


def test_sdk_clients_carry_no_private_route_metadata() -> None:
    # route_class/response_profile/quota_metric are internal MIS routing/accounting
    # vocabulary and were always emitted as a hardcoded fallback (no OpenAPI
    # x-route-class/x-response-profile/x-quota-metric extension ever set them) --
    # pure private-naming leakage into every consumer's dependency tree.
    forbidden = ("route_class", "response_profile", "quota_metric", "rp_enterprise_default", "enterprise_unknown")
    py_source = (ROOT / "packages/python/src/saferx_pharma/client.py").read_text()
    ts_source = (ROOT / "packages/typescript/src/client.ts").read_text()
    cs_source = (ROOT / "packages/csharp/SafeRxClient.cs").read_text()
    for term in forbidden:
        assert term not in py_source
        assert term not in ts_source
        assert term not in cs_source
    for term in ("routeClass", "responseProfile", "quotaMetric"):
        assert term not in ts_source
    for term in ("RouteClass", "ResponseProfile", "QuotaMetric"):
        assert term not in cs_source


def test_sdk_clients_honor_retry_after_on_429() -> None:
    py_source = (ROOT / "packages/python/src/saferx_pharma/client.py").read_text()
    ts_source = (ROOT / "packages/typescript/src/client.ts").read_text()
    cs_source = (ROOT / "packages/csharp/SafeRxClient.cs").read_text()
    assert "429" in py_source and "Retry-After" in py_source
    assert "429" in ts_source and "Retry-After" in ts_source
    assert "429" in cs_source and "RetryAfter" in cs_source


def test_sdk_clients_support_multipart_upload_signing() -> None:
    # enterprise_ocr_prescription_create is multipart/form-data-only per
    # PrescriptionUploadRequest; the gateway signs over the exact raw request bytes
    # regardless of content type (apps/gateway/cmd/gateway/identity_mode.go:
    # bodyHash := sha256.Sum256(bodyBytes)), so a JSON-only client can never call
    # this operation correctly. All three SDK clients must build a real multipart
    # body and sign over those exact bytes.
    from saferx_pharma import MultipartFile, encode_multipart, sign_request

    body, content_type = encode_multipart(
        {"pipeline_profile": "auto", "file": MultipartFile("rx.jpg", b"fake-bytes", "image/jpeg")}
    )
    assert content_type.startswith("multipart/form-data; boundary=")
    assert b'name="pipeline_profile"' in body
    assert b'name="file"; filename="rx.jpg"' in body
    assert b"Content-Type: image/jpeg" in body
    assert b"fake-bytes" in body
    assert sign_request("test-key", "POST", "/api/enterprise/v1/ocr/prescriptions", "", body, "2026-08-15T00:00:00+00:00", "nonce-1")

    ts_source = (ROOT / "packages/typescript/src/client.ts").read_text()
    cs_source = (ROOT / "packages/csharp/SafeRxClient.cs").read_text()
    assert "encodeMultipart" in ts_source and "multipart/form-data" in ts_source
    assert "MultipartEncoder" in cs_source and "multipart/form-data" in cs_source


def test_sdk_doc_examples_only_call_available_operations() -> None:
    # A doc example calling a deferred operation (e.g. client.enterprise_status())
    # would raise immediately, since deferred operations are excluded from
    # OPERATIONS and get no generated method -- exactly the class of bug a
    # blackbox read-the-docs-and-try-it pass is meant to catch (see plan section
    # 12). Every deferred operation id appearing as `client.<id>(` or
    # `client.request("<id>"` in any SDK doc page is that bug.
    import re

    deferred = DEFERRED_OPERATIONS
    docs_dir = ROOT / "fern/docs/pages/sdks"
    for path in docs_dir.glob("*.mdx"):
        text = path.read_text()
        for operation_id in deferred:
            assert not re.search(rf"client\.{operation_id}\s*\(", text), f"{path.name} calls deferred operation {operation_id}"
            assert f'"{operation_id}"' not in text and f"'{operation_id}'" not in text, f"{path.name} references deferred operation {operation_id}"


def test_every_operation_has_a_summary_and_description() -> None:
    spec = yaml.safe_load((ROOT / "openapi/enterprise-v1.yaml").read_text())
    for item in spec["paths"].values():
        for method, operation in item.items():
            if method not in {"get", "post"}:
                continue
            operation_id = operation["operationId"]
            assert operation.get("summary"), f"{operation_id} is missing a summary"
            assert operation.get("description"), f"{operation_id} is missing a description"


def test_medication_resolution_request_is_actually_constructible_by_a_client() -> None:
    # Previously required educational_context/source_provenance/review/summary --
    # response-shaped fields no client could construct, matching neither
    # resolver-service's real request contract (services/resolver-service/src/
    # saferx_resolver/schemas/resolution.py::MedicationResolutionRequest,
    # request_parser.py) nor the hosted MCP's resolve_medications tool schema,
    # which the same backend validates against.
    components = yaml.safe_load((ROOT / "openapi/components.yaml").read_text())
    schema = components["components"]["schemas"]["MedicationResolutionRequest"]
    for private_field in ("educational_context", "source_provenance", "review", "summary", "display_obligations"):
        assert private_field not in schema["properties"]
    assert set(schema["required"]) == {"locale", "medications"}
    medication_item = schema["properties"]["medications"]["items"]
    assert medication_item["required"] == ["input_text"]


def test_mcp_adapter_uses_only_signed_enterprise_operations() -> None:
    source = (ROOT / "packages/mcp-server/src/index.ts").read_text()
    for header in (
        "X-SafeRx-API-Key",
        "X-SafeRx-Timestamp",
        "X-SafeRx-Nonce",
        "X-SafeRx-Signature",
    ):
        assert header in source
    assert "/api/enterprise/v1" in source
    assert "drug_safety" not in source


def test_hosted_mcp_release_manifest_matches_the_three_promoted_tools() -> None:
    release = yaml.safe_load((ROOT / "release/current.yaml").read_text())
    hosted_mcp = release["hosted_mcp"]
    assert hosted_mcp["status"] == "preview"
    assert hosted_mcp["endpoint"] == "https://saferx.online/api/enterprise-mcp/v1/mcp"
    assert set(hosted_mcp["tools"]) == {
        "resolve_medications",
        "check_medication_safety",
        "get_safety_capabilities",
    }
    assert hosted_mcp["resources"] == []
    assert hosted_mcp["prompts"] == []
    doc = (ROOT / "fern/docs/pages/ai-integration/mcp-server.mdx").read_text()
    for forbidden in (
        "X-SafeRx-Actor-Class",
        "X-SafeRx-Partner-ID",
        "X-SafeRx-Organization-ID",
        "X-SafeRx-Quota-Reservation-ID",
    ):
        assert forbidden not in doc
