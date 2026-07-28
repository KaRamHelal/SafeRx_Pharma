from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "sdks/python/src"))

from saferx_pharma.client import canonical_request, sign_request  # noqa: E402


EXPECTED_OPERATIONS = {
    "enterprise_capabilities",
    "enterprise_status",
    "enterprise_registry_autocomplete",
    "enterprise_registry_search",
    "enterprise_registry_resolve",
    "enterprise_registry_product_detail",
    "enterprise_registry_ingredients",
    "enterprise_safety_capabilities",
    "enterprise_safety_check",
    "enterprise_safety_check_read",
    "enterprise_safety_check_batch",
    "enterprise_erx_safety_check",
    "enterprise_allergy_resolve",
    "enterprise_allergy_families",
    "enterprise_allergy_substances",
    "enterprise_ocr_prescription_create",
    "enterprise_ocr_prescription_read",
    "enterprise_ocr_prescription_events",
    "enterprise_ocr_prescription_resolve",
    "enterprise_ocr_prescription_safety",
    "enterprise_ocr_prescription_review",
}


def test_public_projection_matches_current_enterprise_operation_set() -> None:
    spec = yaml.safe_load((ROOT / "openapi/enterprise-v1.yaml").read_text())
    operation_ids = {
        operation["operationId"]
        for item in spec["paths"].values()
        for method, operation in item.items()
        if method in {"get", "post"}
    }
    assert operation_ids == EXPECTED_OPERATIONS
    assert spec["servers"][0]["url"] == "https://saferx.online/api/enterprise/v1"


def test_public_response_schemas_are_closed() -> None:
    components = yaml.safe_load((ROOT / "openapi/components.yaml").read_text())
    serialized = (ROOT / "openapi/components.yaml").read_text()
    assert "additionalProperties: true" not in serialized
    assert components["components"]["securitySchemes"]["enterpriseApiKey"]["name"] == "X-SafeRx-API-Key"


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


def test_mcp_adapter_uses_only_signed_enterprise_operations() -> None:
    source = (ROOT / "mcp-server/src/index.ts").read_text()
    for header in (
        "X-SafeRx-API-Key",
        "X-SafeRx-Timestamp",
        "X-SafeRx-Nonce",
        "X-SafeRx-Signature",
    ):
        assert header in source
    assert "/api/enterprise/v1" in source
    assert "drug_safety" not in source
