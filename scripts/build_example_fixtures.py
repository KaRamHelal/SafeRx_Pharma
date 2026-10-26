#!/usr/bin/env python3
"""Build synthetic request/response example fixtures for every available
Enterprise operation, from shared building blocks so the envelope fields
(educational_context, source_provenance, display_obligations) stay
consistent across examples. Run with --check to verify fixtures are current.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "examples/enterprise"

EDUCATIONAL_CONTEXT: dict[str, Any] = {
    "classification": "pharmaceutical_education",
    "not_medical_advice": True,
    "not_dispensing_authorization": True,
    "professional_review_required": False,
    "basis": "curated_pharmaceutical_reference_data",
    "source_snapshot_id": "edu-snapshot-2026-08-01",
    "generated_at": "2026-08-15T12:00:00+00:00",
    "policy_version": "2026.08.01",
    "claim_catalog_version": "2026.08.01",
    "locale": "en",
    "supported_locales": ["ar-EG", "ar", "en"],
}

SOURCE_PROVENANCE: dict[str, Any] = {
    "registry_snapshot_id": "registry-2026-08-01",
    "safety_snapshot_id": "safety-2026-08-01",
    "policy_version": "2026.08.01",
    "claim_catalog_version": "2026.08.01",
}

DISPLAY_OBLIGATIONS: dict[str, Any] = {
    "must_show_educational_boundary": True,
    "must_show_professional_review_language": False,
    "must_show_source_snapshot": True,
    "must_preserve_arabic_text": True,
    "must_preserve_rtl_layout": True,
    "may_not_describe_as_medical_advice": True,
}

NOT_REQUIRED_REVIEW: dict[str, Any] = {
    "required": False,
    "status": "not_required",
    "reason_codes": [],
    "minimum_reviewer_role": "none",
    "review_deadline_policy": "not_applicable",
    "review_outcome": None,
    "reviewed_at": None,
}

LOCALIZED_AMOXICILLIN = {"en": "Amoxicillin 500mg Capsule", "ar": "أموكسيسيلين 500 مجم كبسولة"}
LOCALIZED_ORAL = {"en": "Oral", "ar": "فموي"}
LOCALIZED_CAPSULE = {"en": "Capsule", "ar": "كبسولة"}


CAPABILITIES_RESPONSE: dict[str, Any] = {
    "auth_scheme": "api_key",
    "available_operation_ids": [
        "enterprise_capabilities",
        "enterprise_status",
        "enterprise_registry_autocomplete",
        "enterprise_registry_search",
        "enterprise_registry_resolve",
        "enterprise_registry_product_detail",
        "enterprise_registry_ingredients",
        "enterprise_safety_check",
        "enterprise_safety_check_read",
        "enterprise_safety_check_batch",
        "enterprise_safety_capabilities",
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
        "mcp_hosted_streamable_http"
    ],
    "capability_refs": [
        {
            "capability_ref": "enterprise_metadata",
            "operation_ids": [
                "enterprise_capabilities",
                "enterprise_status"
            ],
            "quota_metrics": [
                "metadata_read"
            ],
            "response_profile_ids": [
                "rp_enterprise_metadata"
            ],
            "status": "implemented"
        },
        {
            "capability_ref": "registry",
            "operation_ids": [
                "enterprise_registry_autocomplete",
                "enterprise_registry_search",
                "enterprise_registry_resolve",
                "enterprise_registry_product_detail",
                "enterprise_registry_ingredients"
            ],
            "quota_metrics": [
                "ingredient_search_enterprise",
                "registry_product_detail_enterprise",
                "registry_resolve_enterprise",
                "registry_search_enterprise",
                "registry_suggest_enterprise"
            ],
            "response_profile_ids": [
                "rp_enterprise_registry_product",
                "rp_enterprise_registry_search",
                "rp_enterprise_registry_suggestion",
                "rp_enterprise_resolution"
            ],
            "status": "implemented"
        },
        {
            "capability_ref": "safety",
            "operation_ids": [
                "enterprise_safety_check",
                "enterprise_safety_check_read",
                "enterprise_safety_check_batch",
                "enterprise_safety_capabilities",
                "enterprise_erx_safety_check"
            ],
            "quota_metrics": [
                "erx_safety_check",
                "metadata_read",
                "safety_check_batch_enterprise",
                "safety_check_enterprise",
                "safety_check_read_enterprise"
            ],
            "response_profile_ids": [
                "rp_enterprise_batch",
                "rp_enterprise_erx",
                "rp_enterprise_metadata",
                "rp_enterprise_safety_standard"
            ],
            "status": "implemented"
        },
        {
            "capability_ref": "allergy",
            "operation_ids": [
                "enterprise_allergy_resolve",
                "enterprise_allergy_families",
                "enterprise_allergy_substances"
            ],
            "quota_metrics": [
                "allergy_resolve_enterprise",
                "allergy_substance_search",
                "metadata_read"
            ],
            "response_profile_ids": [
                "rp_enterprise_allergy"
            ],
            "status": "implemented"
        },
        {
            "capability_ref": "ocr",
            "operation_ids": [
                "enterprise_ocr_prescription_create",
                "enterprise_ocr_prescription_read",
                "enterprise_ocr_prescription_events",
                "enterprise_ocr_prescription_resolve",
                "enterprise_ocr_prescription_safety",
                "enterprise_ocr_prescription_review"
            ],
            "quota_metrics": [
                "ocr_prescription_enterprise",
                "ocr_prescription_events_enterprise",
                "ocr_prescription_read_enterprise",
                "ocr_prescription_resolve_enterprise",
                "ocr_prescription_review_enterprise",
                "ocr_prescription_safety_enterprise"
            ],
            "response_profile_ids": [
                "rp_enterprise_ocr"
            ],
            "status": "implemented"
        },
        {
            "capability_ref": "mcp",
            "operation_ids": [
                "mcp_hosted_streamable_http"
            ],
            "quota_metrics": [
                "mcp_metadata_read"
            ],
            "response_profile_ids": [
                "rp_mcp_capabilities"
            ],
            "status": "implemented"
        }
    ],
    "clinical_intelligence_source": "owner_services_only",
    "degraded": False,
    "dependency_status": [
        {
            "capability_ref": "enterprise_metadata",
            "reason_code": None,
            "safe_to_retry": False,
            "status": "implemented"
        },
        {
            "capability_ref": "registry",
            "reason_code": None,
            "safe_to_retry": False,
            "status": "implemented"
        },
        {
            "capability_ref": "safety",
            "reason_code": None,
            "safe_to_retry": False,
            "status": "implemented"
        },
        {
            "capability_ref": "allergy",
            "reason_code": None,
            "safe_to_retry": False,
            "status": "implemented"
        },
        {
            "capability_ref": "ocr",
            "reason_code": None,
            "safe_to_retry": False,
            "status": "implemented"
        },
        {
            "capability_ref": "mcp",
            "reason_code": None,
            "safe_to_retry": False,
            "status": "implemented"
        }
    ],
    "generated_at_utc": "2026-10-21T01:20:22.048885+00:00",
    "metadata_kind": "capabilities",
    "operations": [
        {
            "auth_policy": "api_key",
            "capability_ref": "enterprise_metadata",
            "dependency_status": "implemented",
            "display_obligations": {
                "bilingual_required": False,
                "educational_context_required": False,
                "review_state_required": False,
                "source_provenance_required": False
            },
            "idempotency_required": False,
            "method": "GET",
            "operation_id": "enterprise_capabilities",
            "path": "/api/enterprise/v1/capabilities",
            "quota_metric": "metadata_read",
            "response_profile_id": "rp_enterprise_metadata",
            "route_class": "enterprise_metadata"
        },
        {
            "auth_policy": "api_key",
            "capability_ref": "enterprise_metadata",
            "dependency_status": "implemented",
            "display_obligations": {
                "bilingual_required": False,
                "educational_context_required": False,
                "review_state_required": False,
                "source_provenance_required": False
            },
            "idempotency_required": False,
            "method": "GET",
            "operation_id": "enterprise_status",
            "path": "/api/enterprise/v1/status",
            "quota_metric": "metadata_read",
            "response_profile_id": "rp_enterprise_metadata",
            "route_class": "enterprise_metadata"
        },
        {
            "auth_policy": "api_key_plus_catalog_policy",
            "capability_ref": "registry",
            "dependency_status": "implemented",
            "display_obligations": {
                "bilingual_required": True,
                "educational_context_required": True,
                "review_state_required": False,
                "source_provenance_required": True
            },
            "idempotency_required": False,
            "method": "GET",
            "operation_id": "enterprise_registry_autocomplete",
            "path": "/api/enterprise/v1/registry/suggest",
            "quota_metric": "registry_suggest_enterprise",
            "response_profile_id": "rp_enterprise_registry_suggestion",
            "route_class": "enterprise_registry_read"
        },
        {
            "auth_policy": "api_key_plus_catalog_policy",
            "capability_ref": "registry",
            "dependency_status": "implemented",
            "display_obligations": {
                "bilingual_required": True,
                "educational_context_required": True,
                "review_state_required": False,
                "source_provenance_required": True
            },
            "idempotency_required": False,
            "method": "GET",
            "operation_id": "enterprise_registry_search",
            "path": "/api/enterprise/v1/registry/search",
            "quota_metric": "registry_search_enterprise",
            "response_profile_id": "rp_enterprise_registry_search",
            "route_class": "enterprise_registry_read"
        },
        {
            "auth_policy": "api_key_plus_catalog_policy",
            "capability_ref": "registry",
            "dependency_status": "implemented",
            "display_obligations": {
                "bilingual_required": True,
                "educational_context_required": True,
                "review_state_required": True,
                "source_provenance_required": True
            },
            "idempotency_required": False,
            "method": "POST",
            "operation_id": "enterprise_registry_resolve",
            "path": "/api/enterprise/v1/registry/resolve",
            "quota_metric": "registry_resolve_enterprise",
            "response_profile_id": "rp_enterprise_resolution",
            "route_class": "enterprise_registry_resolve"
        },
        {
            "auth_policy": "api_key_plus_catalog_policy",
            "capability_ref": "registry",
            "dependency_status": "implemented",
            "display_obligations": {
                "bilingual_required": True,
                "educational_context_required": True,
                "review_state_required": False,
                "source_provenance_required": True
            },
            "idempotency_required": False,
            "method": "GET",
            "operation_id": "enterprise_registry_product_detail",
            "path": "/api/enterprise/v1/registry/products/{sfrx_id}",
            "quota_metric": "registry_product_detail_enterprise",
            "response_profile_id": "rp_enterprise_registry_product",
            "route_class": "enterprise_registry_read"
        },
        {
            "auth_policy": "api_key_plus_catalog_policy",
            "capability_ref": "registry",
            "dependency_status": "implemented",
            "display_obligations": {
                "bilingual_required": True,
                "educational_context_required": True,
                "review_state_required": False,
                "source_provenance_required": True
            },
            "idempotency_required": False,
            "method": "GET",
            "operation_id": "enterprise_registry_ingredients",
            "path": "/api/enterprise/v1/registry/ingredients",
            "quota_metric": "ingredient_search_enterprise",
            "response_profile_id": "rp_enterprise_registry_search",
            "route_class": "enterprise_registry_read"
        },
        {
            "auth_policy": "api_key_plus_entitlement_policy",
            "capability_ref": "safety",
            "dependency_status": "implemented",
            "display_obligations": {
                "bilingual_required": True,
                "educational_context_required": True,
                "review_state_required": True,
                "source_provenance_required": True
            },
            "idempotency_required": True,
            "method": "POST",
            "operation_id": "enterprise_safety_check",
            "path": "/api/enterprise/v1/safety/checks",
            "quota_metric": "safety_check_enterprise",
            "response_profile_id": "rp_enterprise_safety_standard",
            "route_class": "enterprise_safety"
        },
        {
            "auth_policy": "api_key_plus_entitlement_policy",
            "capability_ref": "safety",
            "dependency_status": "implemented",
            "display_obligations": {
                "bilingual_required": True,
                "educational_context_required": True,
                "review_state_required": True,
                "source_provenance_required": True
            },
            "idempotency_required": False,
            "method": "GET",
            "operation_id": "enterprise_safety_check_read",
            "path": "/api/enterprise/v1/safety/checks/{check_id}",
            "quota_metric": "safety_check_read_enterprise",
            "response_profile_id": "rp_enterprise_safety_standard",
            "route_class": "enterprise_safety"
        },
        {
            "auth_policy": "api_key_plus_batch_entitlement_policy",
            "capability_ref": "safety",
            "dependency_status": "implemented",
            "display_obligations": {
                "bilingual_required": True,
                "educational_context_required": True,
                "review_state_required": True,
                "source_provenance_required": True
            },
            "idempotency_required": True,
            "method": "POST",
            "operation_id": "enterprise_safety_check_batch",
            "path": "/api/enterprise/v1/safety/check-batches",
            "quota_metric": "safety_check_batch_enterprise",
            "response_profile_id": "rp_enterprise_batch",
            "route_class": "enterprise_safety"
        },
        {
            "auth_policy": "api_key",
            "capability_ref": "safety",
            "dependency_status": "implemented",
            "display_obligations": {
                "bilingual_required": True,
                "educational_context_required": True,
                "review_state_required": True,
                "source_provenance_required": True
            },
            "idempotency_required": False,
            "method": "GET",
            "operation_id": "enterprise_safety_capabilities",
            "path": "/api/enterprise/v1/safety/capabilities",
            "quota_metric": "metadata_read",
            "response_profile_id": "rp_enterprise_metadata",
            "route_class": "enterprise_metadata"
        },
        {
            "auth_policy": "api_key_plus_erx_entitlement_policy",
            "capability_ref": "safety",
            "dependency_status": "implemented",
            "display_obligations": {
                "bilingual_required": True,
                "educational_context_required": True,
                "review_state_required": True,
                "source_provenance_required": True
            },
            "idempotency_required": True,
            "method": "POST",
            "operation_id": "enterprise_erx_safety_check",
            "path": "/api/enterprise/v1/erx/safety-checks",
            "quota_metric": "erx_safety_check",
            "response_profile_id": "rp_enterprise_erx",
            "route_class": "enterprise_safety"
        },
        {
            "auth_policy": "api_key_plus_entitlement_policy",
            "capability_ref": "allergy",
            "dependency_status": "implemented",
            "display_obligations": {
                "bilingual_required": True,
                "educational_context_required": True,
                "review_state_required": True,
                "source_provenance_required": True
            },
            "idempotency_required": False,
            "method": "POST",
            "operation_id": "enterprise_allergy_resolve",
            "path": "/api/enterprise/v1/allergies/resolve",
            "quota_metric": "allergy_resolve_enterprise",
            "response_profile_id": "rp_enterprise_allergy",
            "route_class": "enterprise_allergy_reference"
        },
        {
            "auth_policy": "api_key_plus_entitlement_policy",
            "capability_ref": "allergy",
            "dependency_status": "implemented",
            "display_obligations": {
                "bilingual_required": True,
                "educational_context_required": True,
                "review_state_required": True,
                "source_provenance_required": True
            },
            "idempotency_required": False,
            "method": "GET",
            "operation_id": "enterprise_allergy_families",
            "path": "/api/enterprise/v1/allergies/families",
            "quota_metric": "metadata_read",
            "response_profile_id": "rp_enterprise_allergy",
            "route_class": "enterprise_allergy_reference"
        },
        {
            "auth_policy": "api_key_plus_entitlement_policy",
            "capability_ref": "allergy",
            "dependency_status": "implemented",
            "display_obligations": {
                "bilingual_required": True,
                "educational_context_required": True,
                "review_state_required": True,
                "source_provenance_required": True
            },
            "idempotency_required": False,
            "method": "GET",
            "operation_id": "enterprise_allergy_substances",
            "path": "/api/enterprise/v1/allergies/substances",
            "quota_metric": "allergy_substance_search",
            "response_profile_id": "rp_enterprise_allergy",
            "route_class": "enterprise_allergy_reference"
        },
        {
            "auth_policy": "api_key_plus_ocr_entitlement_policy",
            "capability_ref": "ocr",
            "dependency_status": "implemented",
            "display_obligations": {
                "bilingual_required": True,
                "educational_context_required": True,
                "review_state_required": True,
                "source_provenance_required": True
            },
            "idempotency_required": True,
            "method": "POST",
            "operation_id": "enterprise_ocr_prescription_create",
            "path": "/api/enterprise/v1/ocr/prescriptions",
            "quota_metric": "ocr_prescription_enterprise",
            "response_profile_id": "rp_enterprise_ocr",
            "route_class": "enterprise_ocr"
        },
        {
            "auth_policy": "api_key_plus_ocr_entitlement_policy",
            "capability_ref": "ocr",
            "dependency_status": "implemented",
            "display_obligations": {
                "bilingual_required": True,
                "educational_context_required": True,
                "review_state_required": True,
                "source_provenance_required": True
            },
            "idempotency_required": False,
            "method": "GET",
            "operation_id": "enterprise_ocr_prescription_read",
            "path": "/api/enterprise/v1/ocr/prescriptions/{prescription_id}",
            "quota_metric": "ocr_prescription_read_enterprise",
            "response_profile_id": "rp_enterprise_ocr",
            "route_class": "enterprise_ocr"
        },
        {
            "auth_policy": "api_key_plus_ocr_entitlement_policy",
            "capability_ref": "ocr",
            "dependency_status": "implemented",
            "display_obligations": {
                "bilingual_required": True,
                "educational_context_required": True,
                "review_state_required": True,
                "source_provenance_required": True
            },
            "idempotency_required": False,
            "method": "GET",
            "operation_id": "enterprise_ocr_prescription_events",
            "path": "/api/enterprise/v1/ocr/prescriptions/{prescription_id}/events",
            "quota_metric": "ocr_prescription_events_enterprise",
            "response_profile_id": "rp_enterprise_ocr",
            "route_class": "enterprise_ocr"
        },
        {
            "auth_policy": "api_key_plus_ocr_entitlement_policy",
            "capability_ref": "ocr",
            "dependency_status": "implemented",
            "display_obligations": {
                "bilingual_required": True,
                "educational_context_required": True,
                "review_state_required": True,
                "source_provenance_required": True
            },
            "idempotency_required": False,
            "method": "POST",
            "operation_id": "enterprise_ocr_prescription_resolve",
            "path": "/api/enterprise/v1/ocr/prescriptions/{prescription_id}/medications/resolve",
            "quota_metric": "ocr_prescription_resolve_enterprise",
            "response_profile_id": "rp_enterprise_ocr",
            "route_class": "enterprise_ocr"
        },
        {
            "auth_policy": "api_key_plus_ocr_entitlement_policy",
            "capability_ref": "ocr",
            "dependency_status": "implemented",
            "display_obligations": {
                "bilingual_required": True,
                "educational_context_required": True,
                "review_state_required": True,
                "source_provenance_required": True
            },
            "idempotency_required": False,
            "method": "POST",
            "operation_id": "enterprise_ocr_prescription_safety",
            "path": "/api/enterprise/v1/ocr/prescriptions/{prescription_id}/safety-checks",
            "quota_metric": "ocr_prescription_safety_enterprise",
            "response_profile_id": "rp_enterprise_ocr",
            "route_class": "enterprise_ocr"
        },
        {
            "auth_policy": "api_key_plus_ocr_entitlement_policy",
            "capability_ref": "ocr",
            "dependency_status": "implemented",
            "display_obligations": {
                "bilingual_required": True,
                "educational_context_required": True,
                "review_state_required": True,
                "source_provenance_required": True
            },
            "idempotency_required": False,
            "method": "POST",
            "operation_id": "enterprise_ocr_prescription_review",
            "path": "/api/enterprise/v1/ocr/prescriptions/{prescription_id}/review",
            "quota_metric": "ocr_prescription_review_enterprise",
            "response_profile_id": "rp_enterprise_ocr",
            "route_class": "enterprise_ocr"
        },
        {
            "auth_policy": "api_key_plus_entitlement_policy",
            "capability_ref": "mcp",
            "dependency_status": "implemented",
            "display_obligations": {
                "bilingual_required": False,
                "educational_context_required": False,
                "review_state_required": False,
                "source_provenance_required": False
            },
            "idempotency_required": False,
            "method": "POST",
            "operation_id": "mcp_hosted_streamable_http",
            "path": "/api/enterprise-mcp/v1/mcp",
            "quota_metric": "mcp_metadata_read",
            "response_profile_id": "rp_mcp_capabilities",
            "route_class": "mcp_hosted_streamable_http"
        }
    ],
    "policy_version": "pol_2026_06_21_p4r_preflight",
    "quota_classes": [
        "allergy_resolve_enterprise",
        "allergy_substance_search",
        "erx_safety_check",
        "ingredient_search_enterprise",
        "mcp_metadata_read",
        "metadata_read",
        "ocr_prescription_enterprise",
        "ocr_prescription_events_enterprise",
        "ocr_prescription_read_enterprise",
        "ocr_prescription_resolve_enterprise",
        "ocr_prescription_review_enterprise",
        "ocr_prescription_safety_enterprise",
        "registry_product_detail_enterprise",
        "registry_resolve_enterprise",
        "registry_search_enterprise",
        "registry_suggest_enterprise",
        "safety_check_batch_enterprise",
        "safety_check_enterprise",
        "safety_check_read_enterprise"
    ],
    "quota_metric": "metadata_read",
    "request_id": "req_example_0001",
    "response_profile_id": "rp_enterprise_metadata",
    "response_profile_ids": [
        "rp_enterprise_allergy",
        "rp_enterprise_batch",
        "rp_enterprise_erx",
        "rp_enterprise_metadata",
        "rp_enterprise_ocr",
        "rp_enterprise_registry_product",
        "rp_enterprise_registry_search",
        "rp_enterprise_registry_suggestion",
        "rp_enterprise_resolution",
        "rp_enterprise_safety_standard",
        "rp_mcp_capabilities"
    ],
    "route_class": "enterprise_metadata",
    "source_provenance": {
        "activation_contract": "contracts/enterprise-trusted-outcome-activation.yaml",
        "quota_metrics_contract": "contracts/quota-metrics.yaml",
        "response_profiles_contract": "contracts/response-profiles.yaml",
        "route_policy_contract": "contracts/route-policy-map.yaml"
    },
    "stores_workflow_state": False,
    "trace_id": "trc_example_0001"
}

STATUS_RESPONSE: dict[str, Any] = {
    "auth_scheme": "api_key",
    "available_operation_ids": [
        "enterprise_capabilities",
        "enterprise_status",
        "enterprise_registry_autocomplete",
        "enterprise_registry_search",
        "enterprise_registry_resolve",
        "enterprise_registry_product_detail",
        "enterprise_registry_ingredients",
        "enterprise_safety_check",
        "enterprise_safety_check_read",
        "enterprise_safety_check_batch",
        "enterprise_safety_capabilities",
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
        "mcp_hosted_streamable_http"
    ],
    "capability_refs": [
        {
            "capability_ref": "enterprise_metadata",
            "operation_ids": [
                "enterprise_capabilities",
                "enterprise_status"
            ],
            "quota_metrics": [
                "metadata_read"
            ],
            "response_profile_ids": [
                "rp_enterprise_metadata"
            ],
            "status": "implemented"
        },
        {
            "capability_ref": "registry",
            "operation_ids": [
                "enterprise_registry_autocomplete",
                "enterprise_registry_search",
                "enterprise_registry_resolve",
                "enterprise_registry_product_detail",
                "enterprise_registry_ingredients"
            ],
            "quota_metrics": [
                "ingredient_search_enterprise",
                "registry_product_detail_enterprise",
                "registry_resolve_enterprise",
                "registry_search_enterprise",
                "registry_suggest_enterprise"
            ],
            "response_profile_ids": [
                "rp_enterprise_registry_product",
                "rp_enterprise_registry_search",
                "rp_enterprise_registry_suggestion",
                "rp_enterprise_resolution"
            ],
            "status": "implemented"
        },
        {
            "capability_ref": "safety",
            "operation_ids": [
                "enterprise_safety_check",
                "enterprise_safety_check_read",
                "enterprise_safety_check_batch",
                "enterprise_safety_capabilities",
                "enterprise_erx_safety_check"
            ],
            "quota_metrics": [
                "erx_safety_check",
                "metadata_read",
                "safety_check_batch_enterprise",
                "safety_check_enterprise",
                "safety_check_read_enterprise"
            ],
            "response_profile_ids": [
                "rp_enterprise_batch",
                "rp_enterprise_erx",
                "rp_enterprise_metadata",
                "rp_enterprise_safety_standard"
            ],
            "status": "implemented"
        },
        {
            "capability_ref": "allergy",
            "operation_ids": [
                "enterprise_allergy_resolve",
                "enterprise_allergy_families",
                "enterprise_allergy_substances"
            ],
            "quota_metrics": [
                "allergy_resolve_enterprise",
                "allergy_substance_search",
                "metadata_read"
            ],
            "response_profile_ids": [
                "rp_enterprise_allergy"
            ],
            "status": "implemented"
        },
        {
            "capability_ref": "ocr",
            "operation_ids": [
                "enterprise_ocr_prescription_create",
                "enterprise_ocr_prescription_read",
                "enterprise_ocr_prescription_events",
                "enterprise_ocr_prescription_resolve",
                "enterprise_ocr_prescription_safety",
                "enterprise_ocr_prescription_review"
            ],
            "quota_metrics": [
                "ocr_prescription_enterprise",
                "ocr_prescription_events_enterprise",
                "ocr_prescription_read_enterprise",
                "ocr_prescription_resolve_enterprise",
                "ocr_prescription_review_enterprise",
                "ocr_prescription_safety_enterprise"
            ],
            "response_profile_ids": [
                "rp_enterprise_ocr"
            ],
            "status": "implemented"
        },
        {
            "capability_ref": "mcp",
            "operation_ids": [
                "mcp_hosted_streamable_http"
            ],
            "quota_metrics": [
                "mcp_metadata_read"
            ],
            "response_profile_ids": [
                "rp_mcp_capabilities"
            ],
            "status": "implemented"
        }
    ],
    "clinical_intelligence_source": "owner_services_only",
    "degraded": False,
    "dependency_status": [
        {
            "capability_ref": "enterprise_metadata",
            "reason_code": None,
            "safe_to_retry": False,
            "status": "implemented"
        },
        {
            "capability_ref": "registry",
            "reason_code": None,
            "safe_to_retry": False,
            "status": "implemented"
        },
        {
            "capability_ref": "safety",
            "reason_code": None,
            "safe_to_retry": False,
            "status": "implemented"
        },
        {
            "capability_ref": "allergy",
            "reason_code": None,
            "safe_to_retry": False,
            "status": "implemented"
        },
        {
            "capability_ref": "ocr",
            "reason_code": None,
            "safe_to_retry": False,
            "status": "implemented"
        },
        {
            "capability_ref": "mcp",
            "reason_code": None,
            "safe_to_retry": False,
            "status": "implemented"
        }
    ],
    "generated_at_utc": "2026-10-21T01:20:52.059142+00:00",
    "metadata_kind": "status",
    "operations": [
        {
            "auth_policy": "api_key",
            "capability_ref": "enterprise_metadata",
            "dependency_status": "implemented",
            "display_obligations": {
                "bilingual_required": False,
                "educational_context_required": False,
                "review_state_required": False,
                "source_provenance_required": False
            },
            "idempotency_required": False,
            "method": "GET",
            "operation_id": "enterprise_capabilities",
            "path": "/api/enterprise/v1/capabilities",
            "quota_metric": "metadata_read",
            "response_profile_id": "rp_enterprise_metadata",
            "route_class": "enterprise_metadata"
        },
        {
            "auth_policy": "api_key",
            "capability_ref": "enterprise_metadata",
            "dependency_status": "implemented",
            "display_obligations": {
                "bilingual_required": False,
                "educational_context_required": False,
                "review_state_required": False,
                "source_provenance_required": False
            },
            "idempotency_required": False,
            "method": "GET",
            "operation_id": "enterprise_status",
            "path": "/api/enterprise/v1/status",
            "quota_metric": "metadata_read",
            "response_profile_id": "rp_enterprise_metadata",
            "route_class": "enterprise_metadata"
        },
        {
            "auth_policy": "api_key_plus_catalog_policy",
            "capability_ref": "registry",
            "dependency_status": "implemented",
            "display_obligations": {
                "bilingual_required": True,
                "educational_context_required": True,
                "review_state_required": False,
                "source_provenance_required": True
            },
            "idempotency_required": False,
            "method": "GET",
            "operation_id": "enterprise_registry_autocomplete",
            "path": "/api/enterprise/v1/registry/suggest",
            "quota_metric": "registry_suggest_enterprise",
            "response_profile_id": "rp_enterprise_registry_suggestion",
            "route_class": "enterprise_registry_read"
        },
        {
            "auth_policy": "api_key_plus_catalog_policy",
            "capability_ref": "registry",
            "dependency_status": "implemented",
            "display_obligations": {
                "bilingual_required": True,
                "educational_context_required": True,
                "review_state_required": False,
                "source_provenance_required": True
            },
            "idempotency_required": False,
            "method": "GET",
            "operation_id": "enterprise_registry_search",
            "path": "/api/enterprise/v1/registry/search",
            "quota_metric": "registry_search_enterprise",
            "response_profile_id": "rp_enterprise_registry_search",
            "route_class": "enterprise_registry_read"
        },
        {
            "auth_policy": "api_key_plus_catalog_policy",
            "capability_ref": "registry",
            "dependency_status": "implemented",
            "display_obligations": {
                "bilingual_required": True,
                "educational_context_required": True,
                "review_state_required": True,
                "source_provenance_required": True
            },
            "idempotency_required": False,
            "method": "POST",
            "operation_id": "enterprise_registry_resolve",
            "path": "/api/enterprise/v1/registry/resolve",
            "quota_metric": "registry_resolve_enterprise",
            "response_profile_id": "rp_enterprise_resolution",
            "route_class": "enterprise_registry_resolve"
        },
        {
            "auth_policy": "api_key_plus_catalog_policy",
            "capability_ref": "registry",
            "dependency_status": "implemented",
            "display_obligations": {
                "bilingual_required": True,
                "educational_context_required": True,
                "review_state_required": False,
                "source_provenance_required": True
            },
            "idempotency_required": False,
            "method": "GET",
            "operation_id": "enterprise_registry_product_detail",
            "path": "/api/enterprise/v1/registry/products/{sfrx_id}",
            "quota_metric": "registry_product_detail_enterprise",
            "response_profile_id": "rp_enterprise_registry_product",
            "route_class": "enterprise_registry_read"
        },
        {
            "auth_policy": "api_key_plus_catalog_policy",
            "capability_ref": "registry",
            "dependency_status": "implemented",
            "display_obligations": {
                "bilingual_required": True,
                "educational_context_required": True,
                "review_state_required": False,
                "source_provenance_required": True
            },
            "idempotency_required": False,
            "method": "GET",
            "operation_id": "enterprise_registry_ingredients",
            "path": "/api/enterprise/v1/registry/ingredients",
            "quota_metric": "ingredient_search_enterprise",
            "response_profile_id": "rp_enterprise_registry_search",
            "route_class": "enterprise_registry_read"
        },
        {
            "auth_policy": "api_key_plus_entitlement_policy",
            "capability_ref": "safety",
            "dependency_status": "implemented",
            "display_obligations": {
                "bilingual_required": True,
                "educational_context_required": True,
                "review_state_required": True,
                "source_provenance_required": True
            },
            "idempotency_required": True,
            "method": "POST",
            "operation_id": "enterprise_safety_check",
            "path": "/api/enterprise/v1/safety/checks",
            "quota_metric": "safety_check_enterprise",
            "response_profile_id": "rp_enterprise_safety_standard",
            "route_class": "enterprise_safety"
        },
        {
            "auth_policy": "api_key_plus_entitlement_policy",
            "capability_ref": "safety",
            "dependency_status": "implemented",
            "display_obligations": {
                "bilingual_required": True,
                "educational_context_required": True,
                "review_state_required": True,
                "source_provenance_required": True
            },
            "idempotency_required": False,
            "method": "GET",
            "operation_id": "enterprise_safety_check_read",
            "path": "/api/enterprise/v1/safety/checks/{check_id}",
            "quota_metric": "safety_check_read_enterprise",
            "response_profile_id": "rp_enterprise_safety_standard",
            "route_class": "enterprise_safety"
        },
        {
            "auth_policy": "api_key_plus_batch_entitlement_policy",
            "capability_ref": "safety",
            "dependency_status": "implemented",
            "display_obligations": {
                "bilingual_required": True,
                "educational_context_required": True,
                "review_state_required": True,
                "source_provenance_required": True
            },
            "idempotency_required": True,
            "method": "POST",
            "operation_id": "enterprise_safety_check_batch",
            "path": "/api/enterprise/v1/safety/check-batches",
            "quota_metric": "safety_check_batch_enterprise",
            "response_profile_id": "rp_enterprise_batch",
            "route_class": "enterprise_safety"
        },
        {
            "auth_policy": "api_key",
            "capability_ref": "safety",
            "dependency_status": "implemented",
            "display_obligations": {
                "bilingual_required": True,
                "educational_context_required": True,
                "review_state_required": True,
                "source_provenance_required": True
            },
            "idempotency_required": False,
            "method": "GET",
            "operation_id": "enterprise_safety_capabilities",
            "path": "/api/enterprise/v1/safety/capabilities",
            "quota_metric": "metadata_read",
            "response_profile_id": "rp_enterprise_metadata",
            "route_class": "enterprise_metadata"
        },
        {
            "auth_policy": "api_key_plus_erx_entitlement_policy",
            "capability_ref": "safety",
            "dependency_status": "implemented",
            "display_obligations": {
                "bilingual_required": True,
                "educational_context_required": True,
                "review_state_required": True,
                "source_provenance_required": True
            },
            "idempotency_required": True,
            "method": "POST",
            "operation_id": "enterprise_erx_safety_check",
            "path": "/api/enterprise/v1/erx/safety-checks",
            "quota_metric": "erx_safety_check",
            "response_profile_id": "rp_enterprise_erx",
            "route_class": "enterprise_safety"
        },
        {
            "auth_policy": "api_key_plus_entitlement_policy",
            "capability_ref": "allergy",
            "dependency_status": "implemented",
            "display_obligations": {
                "bilingual_required": True,
                "educational_context_required": True,
                "review_state_required": True,
                "source_provenance_required": True
            },
            "idempotency_required": False,
            "method": "POST",
            "operation_id": "enterprise_allergy_resolve",
            "path": "/api/enterprise/v1/allergies/resolve",
            "quota_metric": "allergy_resolve_enterprise",
            "response_profile_id": "rp_enterprise_allergy",
            "route_class": "enterprise_allergy_reference"
        },
        {
            "auth_policy": "api_key_plus_entitlement_policy",
            "capability_ref": "allergy",
            "dependency_status": "implemented",
            "display_obligations": {
                "bilingual_required": True,
                "educational_context_required": True,
                "review_state_required": True,
                "source_provenance_required": True
            },
            "idempotency_required": False,
            "method": "GET",
            "operation_id": "enterprise_allergy_families",
            "path": "/api/enterprise/v1/allergies/families",
            "quota_metric": "metadata_read",
            "response_profile_id": "rp_enterprise_allergy",
            "route_class": "enterprise_allergy_reference"
        },
        {
            "auth_policy": "api_key_plus_entitlement_policy",
            "capability_ref": "allergy",
            "dependency_status": "implemented",
            "display_obligations": {
                "bilingual_required": True,
                "educational_context_required": True,
                "review_state_required": True,
                "source_provenance_required": True
            },
            "idempotency_required": False,
            "method": "GET",
            "operation_id": "enterprise_allergy_substances",
            "path": "/api/enterprise/v1/allergies/substances",
            "quota_metric": "allergy_substance_search",
            "response_profile_id": "rp_enterprise_allergy",
            "route_class": "enterprise_allergy_reference"
        },
        {
            "auth_policy": "api_key_plus_ocr_entitlement_policy",
            "capability_ref": "ocr",
            "dependency_status": "implemented",
            "display_obligations": {
                "bilingual_required": True,
                "educational_context_required": True,
                "review_state_required": True,
                "source_provenance_required": True
            },
            "idempotency_required": True,
            "method": "POST",
            "operation_id": "enterprise_ocr_prescription_create",
            "path": "/api/enterprise/v1/ocr/prescriptions",
            "quota_metric": "ocr_prescription_enterprise",
            "response_profile_id": "rp_enterprise_ocr",
            "route_class": "enterprise_ocr"
        },
        {
            "auth_policy": "api_key_plus_ocr_entitlement_policy",
            "capability_ref": "ocr",
            "dependency_status": "implemented",
            "display_obligations": {
                "bilingual_required": True,
                "educational_context_required": True,
                "review_state_required": True,
                "source_provenance_required": True
            },
            "idempotency_required": False,
            "method": "GET",
            "operation_id": "enterprise_ocr_prescription_read",
            "path": "/api/enterprise/v1/ocr/prescriptions/{prescription_id}",
            "quota_metric": "ocr_prescription_read_enterprise",
            "response_profile_id": "rp_enterprise_ocr",
            "route_class": "enterprise_ocr"
        },
        {
            "auth_policy": "api_key_plus_ocr_entitlement_policy",
            "capability_ref": "ocr",
            "dependency_status": "implemented",
            "display_obligations": {
                "bilingual_required": True,
                "educational_context_required": True,
                "review_state_required": True,
                "source_provenance_required": True
            },
            "idempotency_required": False,
            "method": "GET",
            "operation_id": "enterprise_ocr_prescription_events",
            "path": "/api/enterprise/v1/ocr/prescriptions/{prescription_id}/events",
            "quota_metric": "ocr_prescription_events_enterprise",
            "response_profile_id": "rp_enterprise_ocr",
            "route_class": "enterprise_ocr"
        },
        {
            "auth_policy": "api_key_plus_ocr_entitlement_policy",
            "capability_ref": "ocr",
            "dependency_status": "implemented",
            "display_obligations": {
                "bilingual_required": True,
                "educational_context_required": True,
                "review_state_required": True,
                "source_provenance_required": True
            },
            "idempotency_required": False,
            "method": "POST",
            "operation_id": "enterprise_ocr_prescription_resolve",
            "path": "/api/enterprise/v1/ocr/prescriptions/{prescription_id}/medications/resolve",
            "quota_metric": "ocr_prescription_resolve_enterprise",
            "response_profile_id": "rp_enterprise_ocr",
            "route_class": "enterprise_ocr"
        },
        {
            "auth_policy": "api_key_plus_ocr_entitlement_policy",
            "capability_ref": "ocr",
            "dependency_status": "implemented",
            "display_obligations": {
                "bilingual_required": True,
                "educational_context_required": True,
                "review_state_required": True,
                "source_provenance_required": True
            },
            "idempotency_required": False,
            "method": "POST",
            "operation_id": "enterprise_ocr_prescription_safety",
            "path": "/api/enterprise/v1/ocr/prescriptions/{prescription_id}/safety-checks",
            "quota_metric": "ocr_prescription_safety_enterprise",
            "response_profile_id": "rp_enterprise_ocr",
            "route_class": "enterprise_ocr"
        },
        {
            "auth_policy": "api_key_plus_ocr_entitlement_policy",
            "capability_ref": "ocr",
            "dependency_status": "implemented",
            "display_obligations": {
                "bilingual_required": True,
                "educational_context_required": True,
                "review_state_required": True,
                "source_provenance_required": True
            },
            "idempotency_required": False,
            "method": "POST",
            "operation_id": "enterprise_ocr_prescription_review",
            "path": "/api/enterprise/v1/ocr/prescriptions/{prescription_id}/review",
            "quota_metric": "ocr_prescription_review_enterprise",
            "response_profile_id": "rp_enterprise_ocr",
            "route_class": "enterprise_ocr"
        },
        {
            "auth_policy": "api_key_plus_entitlement_policy",
            "capability_ref": "mcp",
            "dependency_status": "implemented",
            "display_obligations": {
                "bilingual_required": False,
                "educational_context_required": False,
                "review_state_required": False,
                "source_provenance_required": False
            },
            "idempotency_required": False,
            "method": "POST",
            "operation_id": "mcp_hosted_streamable_http",
            "path": "/api/enterprise-mcp/v1/mcp",
            "quota_metric": "mcp_metadata_read",
            "response_profile_id": "rp_mcp_capabilities",
            "route_class": "mcp_hosted_streamable_http"
        }
    ],
    "policy_version": "pol_2026_06_21_p4r_preflight",
    "quota_classes": [
        "allergy_resolve_enterprise",
        "allergy_substance_search",
        "erx_safety_check",
        "ingredient_search_enterprise",
        "mcp_metadata_read",
        "metadata_read",
        "ocr_prescription_enterprise",
        "ocr_prescription_events_enterprise",
        "ocr_prescription_read_enterprise",
        "ocr_prescription_resolve_enterprise",
        "ocr_prescription_review_enterprise",
        "ocr_prescription_safety_enterprise",
        "registry_product_detail_enterprise",
        "registry_resolve_enterprise",
        "registry_search_enterprise",
        "registry_suggest_enterprise",
        "safety_check_batch_enterprise",
        "safety_check_enterprise",
        "safety_check_read_enterprise"
    ],
    "quota_metric": "metadata_read",
    "request_id": "req_example_0001",
    "response_profile_id": "rp_enterprise_metadata",
    "response_profile_ids": [
        "rp_enterprise_allergy",
        "rp_enterprise_batch",
        "rp_enterprise_erx",
        "rp_enterprise_metadata",
        "rp_enterprise_ocr",
        "rp_enterprise_registry_product",
        "rp_enterprise_registry_search",
        "rp_enterprise_registry_suggestion",
        "rp_enterprise_resolution",
        "rp_enterprise_safety_standard",
        "rp_mcp_capabilities"
    ],
    "route_class": "enterprise_metadata",
    "source_provenance": {
        "activation_contract": "contracts/enterprise-trusted-outcome-activation.yaml",
        "quota_metrics_contract": "contracts/quota-metrics.yaml",
        "response_profiles_contract": "contracts/response-profiles.yaml",
        "route_policy_contract": "contracts/route-policy-map.yaml"
    },
    "stores_workflow_state": False,
    "trace_id": "trc_example_0001"
}


def envelope(**overrides: Any) -> dict[str, Any]:
    base = {
        "request_id": "req_example_0001",
        "schema_version": "1.0.0",
        "locale": "en",
        "educational_context": EDUCATIONAL_CONTEXT,
        "source_provenance": SOURCE_PROVENANCE,
    }
    base.update(overrides)
    return base


def build() -> dict[str, dict[str, Any]]:
    examples: dict[str, dict[str, Any]] = {}

    examples["enterprise_registry_resolve"] = {
        "request": {
            "body": {
                "locale": "en",
                "medications": [{"input_text": "amoxicillin 500mg"}],
            },
        },
        "response": {
            **envelope(),
            "display_obligations": DISPLAY_OBLIGATIONS,
            "items": [
                {
                    "request_id": "req_example_0001",
                    "result_id": "res_example_0001",
                    "schema_version": "1.0.0",
                    "surface": "enterprise_api",
                    "locale": "en",
                    "educational_context": EDUCATIONAL_CONTEXT,
                    "source_provenance": SOURCE_PROVENANCE,
                    "query": {"raw_text": "amoxicillin 500mg", "locale_hint": None},
                    "candidates": [
                        {
                            "candidate_id": "cand_example_0001",
                            "sfrx_id": "SRX-101-000042",
                            "registry_concept_id": None,
                            "confidence": 0.97,
                            "display_name": LOCALIZED_AMOXICILLIN,
                            "normalized_name": {"en": "amoxicillin 500 capsule", "ar": "اموكسيسيلين 500 كبسولة"},
                            "strength": "500mg",
                            "dosage_form": LOCALIZED_CAPSULE,
                            "route": LOCALIZED_ORAL,
                            "manufacturer": {"en": "Egyptian Pharma Co.", "ar": "شركة الأدوية المصرية"},
                            "ingredient_names": [{"en": "Amoxicillin", "ar": "أموكسيسيلين"}],
                            "match_reasons": [
                                {"en": "Generic name matched", "ar": "تطابق الاسم العلمي"},
                                {"en": "Strength matched", "ar": "تطابق التركيز"},
                            ],
                            "equivalent_candidates": [],
                            "review": NOT_REQUIRED_REVIEW,
                            "source_provenance": SOURCE_PROVENANCE,
                        },
                    ],
                    "selected_candidate_id": "SRX-101-000042",
                    "review": NOT_REQUIRED_REVIEW,
                    "limitations": [],
                    "display_obligations": DISPLAY_OBLIGATIONS,
                }
            ],
        },
    }

    examples["enterprise_registry_search"] = {
        "request": {"query_params": {"q": "amoxicillin", "locale": "en", "limit": 10}},
        "response": {
            **envelope(),
            "items": [
                {
                    "sfrx_id": "SRX-101-000042",
                    "tradename": LOCALIZED_AMOXICILLIN,
                    "generic": {"en": "Amoxicillin", "ar": "أموكسيسيلين"},
                    "manufacturer": {"en": "Egyptian Pharma Co.", "ar": "شركة الأدوية المصرية"},
                    "match_reason": {"en": "Prefix match", "ar": "تطابق بداية الاسم"},
                    "name_strength": {"en": "Amoxicillin 500", "ar": "أموكسيسيلين 500"},
                    "product_tier": "pharma",
                    "strength": "500mg",
                    "route": LOCALIZED_ORAL,
                    "dosage_form": LOCALIZED_CAPSULE,
                    "score": 102,
                }
            ],
            "pagination": {"limit": 10, "cursor": None, "next_cursor": None, "has_more": False},
            "display_obligations": DISPLAY_OBLIGATIONS,
        },
    }

    examples["enterprise_registry_autocomplete"] = {
        "request": {"query_params": {"q": "amox", "locale": "en", "limit": 5}},
        "response": {
            **envelope(),
            "items": [
                {
                    "sfrx_id": "SRX-101-000042",
                    "tradename": LOCALIZED_AMOXICILLIN,
                    "dosage_form": LOCALIZED_CAPSULE,
                    "route": LOCALIZED_ORAL,
                    "product_tier": "pharma",
                    "name_strength": {"en": "Amoxicillin 500", "ar": "أموكسيسيلين 500"},
                    "match_reason": {"en": "Trade name prefix match", "ar": "تطابق بداية الاسم التجاري"},
                    "match": {"score": 102, "type": "prefix"},
                    "score": 102,
                }
            ],
            "display_obligations": DISPLAY_OBLIGATIONS,
        },
    }

    examples["enterprise_registry_product_detail"] = {
        "request": {"path_params": {"sfrx_id": "SRX-101-000042"}},
        "response": {
            **envelope(),
            "display_obligations": DISPLAY_OBLIGATIONS,
            "sfrx_id": "SRX-101-000042",
            "parent_sfrx_id": None,
            "product_tier": "pharma",
            "tradename": LOCALIZED_AMOXICILLIN,
            "primary_name": None,
            "generic": {"en": "Amoxicillin", "ar": "أموكسيسيلين"},
            "strength": "500mg",
            "dosage_form": LOCALIZED_CAPSULE,
            "route": LOCALIZED_ORAL,
            "manufacturer": None,
            "supplier": None,
            "package": {"en": "Box of 21 capsules", "ar": "علبة 21 كبسولة"},
            "barcode": None,
            "category_trail": [
                {"level": "class", "label": {"en": "Antibiotics", "ar": "المضادات الحيوية"}},
            ],
            "clinical_uses": {"en": "Bacterial infections", "ar": "الالتهابات البكتيرية"},
            "pharmacology": {"details": None},
            "prose_details": {"description": None, "ingredients": None, "dosing": None},
            "warnings": {"requires_professional_review": False},
            "domain_availability": {
                "ddi": "available", "pllr": "available", "food_interactions": "available",
                "meal_timing": "available", "allergy": "available", "clinical_dose": "available",
            },
            "correction_anchors": [],
        },
    }

    examples["enterprise_registry_ingredients"] = {
        "request": {"query_params": {"q": "amoxicillin", "locale": "en"}},
        "response": {
            **envelope(),
            "display_obligations": DISPLAY_OBLIGATIONS,
            "items": [
                {
                    "ingredient_id": "ING-000123",
                    "ingredient_type": "active",
                    "display_name": {"en": "Amoxicillin", "ar": "أموكسيسيلين"},
                    "linked_product_count": 5,
                    "linked_sfrx_ids": ["SRX-101-000042"],
                    "correction_anchors": [],
                }
            ],
            "pagination": {"limit": 10, "cursor": None, "next_cursor": None, "has_more": False},
        },
    }

    examples["enterprise_safety_capabilities"] = {
        "request": {},
        "response": {
            "request_id": "req_example_0001",
            "schema_version": "1.0.0",
            "domains": {
                "ddi": {"available": True, "status": "active"},
                "pllr": {"available": True, "status": "active"},
                "food_interactions": {"available": True, "status": "active"},
                "meal_timing": {"available": True, "status": "active"},
                "allergy": {"available": True, "status": "active"},
                "clinical_dose": {"available": True, "status": "active"},
            },
            "available": True,
            "status": "ready",
            "safety_snapshot_id": "safety-2026-08-01",
            "registry_snapshot_id": "registry-2026-08-01",
        },
    }

    # Captured from production 2026-10-21 (identifiers replaced); these two operations were
    # promoted from deferred in 2.0.4 after live verification against this exact shape.
    examples["enterprise_capabilities"] = {"request": {}, "response": CAPABILITIES_RESPONSE}
    examples["enterprise_status"] = {"request": {}, "response": STATUS_RESPONSE}

    # 3.0.0 (2026-10-26): the v2 result (schema_version 2), shaped on a real backend capture,
    # ids replaced. Warfarin + aspirin is MAJOR in DDI V8.3.24.
    def v2_result(check_id: str, medications: list[dict[str, Any]]) -> dict[str, Any]:
        return {
            "schema_version": 2,
            "check_id": check_id,
            "request_id": "req_example_0002",
            "created_at": "2026-10-26T12:00:00+00:00",
            "outcome": {"highest_severity": "high", "action": "urgent_review", "finding_count": 1,
                        "alert_count": 1, "blocked": False},
            "release": {"safety_snapshot_id": "safety-2026-10-26", "registry_snapshot_id": "registry-2026-10-26"},
            "medications": medications,
            "domains": [{
                "domain": "ddi", "name": {"en": "Drug interactions", "ar": "التداخلات الدوائية"},
                "status": "evaluated", "finding_count": 1, "reason": None, "missing_context": [],
                "release_id": "ddi_V8.3.24",
            }],
            "findings": [{
                "finding_id": "ddi_SRX-101-000043_SRX-101-000042",
                "domain": "ddi",
                "kind": "alert",
                "severity": "high",
                "action": "urgent_review",
                "title": {"en": "Acetylsalicylic acid may increase the anticoagulant activities of Warfarin.",
                          "ar": "قد يزيد حمض أسيتيل الساليسيليك من التأثيرات المضادة للتخثر للوارفارين."},
                "explanation": None,
                "recommendation": {"en": "Monitor INR/PT. Watch for signs of bleeding (bruising, blood in urine/stool).",
                                   "ar": "راقب معدل INR. انتبه لعلامات النزيف (كدمات، دم في البول/البراز)."},
                "medication_refs": [medications[0]["ref"], medications[1]["ref"]],
                "subjects": [],
                "evidence": {
                    "grade": "curated_reference",
                    "source": {"en": "DDI release", "ar": "إصدار تداخلات الأدوية"},
                    "source_rating": {"value": 3, "label": {"en": "Major", "ar": "كبير"}},
                },
                "confidence": 0.8,
                "based_on_context": [],
                "review_required": True,
            }],
            "review": {
                "required": True,
                "reasons": [{"code": "severe_or_uncertain_signal", "message": {
                    "en": "A finding of moderate or higher severity, or with uncertain evidence, needs professional review.",
                    "ar": "نتيجة بشدة متوسطة أو أعلى، أو بدليل غير مؤكد، تحتاج مراجعة مهنية."}}],
                "minimum_reviewer_role": "qualified_professional",
            },
            "patient_context": {"status": "none", "applied_fields": []},
            "disclaimer": {
                "en": "Educational pharmaceutical information for qualified professionals. It is not medical advice or a dispensing authorization; review before relying on it.",
                "ar": "معلومات دوائية تعليمية للمختصين المؤهلين. ليست نصيحة طبية ولا تفويضًا بصرف الدواء؛ راجعها قبل الاعتماد عليها.",
            },
        }

    # As production returns them (live 2026-10-26): the generic is bilingual.
    V2_GENERICS = {
        "WARFARIN": {"en": "WARFARIN", "ar": "وارفارين"},
        "ACETYLSALICYLIC ACID": {"en": "ACETYLSALICYLIC ACID", "ar": "حمض أسيتيل الساليسيليك"},
    }

    def v2_medication(ref: str, role: str, given: str, sfrx_id: str, name_en: str, name_ar: str,
                      generic: str, strength: str, selection: str) -> dict[str, Any]:
        return {
            "ref": ref, "role": role, "input": given, "status": "resolved", "selection": selection,
            "product": {"sfrx_id": sfrx_id, "name": {"en": name_en, "ar": name_ar}, "generic": V2_GENERICS[generic],
                        "strength": strength, "form": {"en": "Oral Tablet", "ar": "أقراص"}},
        }

    examples["enterprise_safety_check"] = {
        "request": {
            "body": {
                "locale": "en",
                "medications": [
                    {"client_medication_id": "rx-line-1", "input_text": "Warfarin 5 mg tablet", "role": "target_medication"},
                    {"client_medication_id": "current-1", "sfrx_id": "SRX-101-000042", "role": "current_medication"},
                ],
                "requested_domains": ["ddi"],
                "idempotency_key": "example-safety-check-0001",
            },
            "headers": {"Idempotency-Key": "example-safety-check-0001"},
        },
        "response": v2_result("chk_0f1e2d3c4b5a69788796a5b4c3d2e1f0", [
            v2_medication("rx-line-1", "new", "Warfarin 5 mg tablet", "SRX-101-000043", "MAREVAN 5 MG 102 TABS.",
                          "ماريفان 5 مجم 102 قرص", "WARFARIN", "5 MG", "exact"),
            v2_medication("current-1", "current", "SRX-101-000042", "SRX-101-000042", "ASPIRIN PROTECT 100 MG 30 TABS.",
                          "أسبيرين بروتكت 100 مجم 30 قرص", "ACETYLSALICYLIC ACID", "100 MG", "by_id"),
        ]),
    }

    # eRx (2.0.5; v2 result in 3.0.0): lines plus current medications mapped onto the safety
    # check; each medication is named by the caller's line_ref / medication_ref, plus the echo.
    erx_response = v2_result("chk_a1b2c3d4e5f60718293a4b5c6d7e8f90", [
        v2_medication("1", "new", "Warfarin", "SRX-101-000043", "MAREVAN 5 MG 102 TABS.", "ماريفان 5 مجم 102 قرص",
                      "WARFARIN", "5 MG", "exact"),
        v2_medication("home-1", "current", "Aspirin", "SRX-101-000042", "ASPIRIN PROTECT 100 MG 30 TABS.",
                      "أسبيرين بروتكت 100 مجم 30 قرص", "ACETYLSALICYLIC ACID", "100 MG", "default_variant"),
    ])
    erx_response["review"]["reasons"].append({"code": "default_variant_selected", "message": {
        "en": "A medicine named in several variants was evaluated as its default product; confirm the product.",
        "ar": "تم تقييم دواء له عدة أشكال على أنه المنتج الافتراضي؛ تأكد من المنتج."}})
    erx_response["erx"] = {
        "prescription_ref": "RX-7781",
        "lines": [{"line_ref": "1", "medication_ref": "1", "sfrx_id": "SRX-101-000043", "status": "resolved",
                   "frequency_text": "once daily", "duration_text": "30 days"}],
    }
    examples["enterprise_erx_safety_check"] = {
        "request": {
            "body": {
                "locale": "en",
                "requested_domains": ["ddi"],
                "idempotency_key": "RX-7781-v1",
                "erx_payload": {
                    "prescription_ref": "RX-7781",
                    "lines": [
                        {
                            "line_ref": "1",
                            "input_text": "Warfarin",
                            "dose_text": "5 mg",
                            "route": "oral",
                            "dosage_form": "tablet",
                            "frequency_text": "once daily",
                            "duration_text": "30 days",
                        }
                    ],
                    "current_medications": [{"medication_ref": "home-1", "input_text": "Aspirin"}],
                },
            },
            "headers": {"Idempotency-Key": "RX-7781-v1"},
        },
        "response": erx_response,
    }

    examples["enterprise_ocr_prescription_create"] = {
        "request": {
            "multipart_fields": {
                "file": {"filename": "prescription.jpg", "content_type": "image/jpeg", "note": "binary image bytes"},
                "pipeline_profile": "auto",
                "include_ddi": True,
                "include_allergy": True,
            },
            "headers": {"Idempotency-Key": "example-ocr-create-0001"},
        },
        "response": {
            "request_id": "req_example_0001",
            "prescription_id": "rx_example_0001",
            "status": "accepted",
            "educational_context": EDUCATIONAL_CONTEXT,
            "source_provenance": SOURCE_PROVENANCE,
            "review": NOT_REQUIRED_REVIEW,
        },
    }

    prescription_result = {
        "request_id": "req_example_0001",
        "prescription_id": "rx_example_0001",
        "workflow_id": "wf_example_0001",
        "status": "processing",
        "pipeline_profile": "auto",
        "reason_code": None,
        "created_at": "2026-08-15T12:00:00+00:00",
        "updated_at": "2026-08-15T12:00:05+00:00",
        "transitions": [
            {
                "event_type": "ocr_completed",
                "from_state": "accepted",
                "to_state": "processing",
                "reason_code": None,
                "payload": {},
                "occurred_at": "2026-08-15T12:00:05+00:00",
            }
        ],
        "locale": "en",
        "educational_context": EDUCATIONAL_CONTEXT,
        "source_provenance": SOURCE_PROVENANCE,
        "review": NOT_REQUIRED_REVIEW,
        "document_context": {
            "document_type": "prescription",
            "is_prescription": True,
            "medications_present": True,
            "medication_section": "body",
        },
        "candidate_medications": [
            {
                "line_id": "line_0001",
                "position": 0,
                "raw_span": "Amoxicillin 500mg cap",
                "winner": None,
                "ocr_candidates": [
                    {"rank": 1, "recognized_text": "Amoxicillin 500mg cap", "locale": "en", "confidence": 0.95}
                ],
                "alternatives": [],
                "review_required": False,
                "review_state": "not_required",
                "correction_anchor_id": None,
            }
        ],
        "display_obligations": DISPLAY_OBLIGATIONS,
    }

    examples["enterprise_ocr_prescription_read"] = {
        "request": {"path_params": {"prescription_id": "rx_example_0001"}},
        "response": prescription_result,
    }

    resolved_result = json.loads(json.dumps(prescription_result))
    resolved_result["status"] = "resolved"
    resolved_result["candidate_medications"][0]["winner"] = {
        "sfrx_id": "SRX-101-000042",
        "display_name": LOCALIZED_AMOXICILLIN,
        "generic": {"en": "Amoxicillin", "ar": "أموكسيسيلين"},
        "final_score": 0.97,
        "confidence": 0.95,
        "review_state": "not_required",
    }

    examples["enterprise_ocr_prescription_resolve"] = {
        "request": {"path_params": {"prescription_id": "rx_example_0001"}, "body": {}},
        "response": resolved_result,
    }

    safety_checked_result = json.loads(json.dumps(resolved_result))
    safety_checked_result["status"] = "safety_checked"

    examples["enterprise_ocr_prescription_safety"] = {
        "request": {"path_params": {"prescription_id": "rx_example_0001"}, "body": {}},
        "response": safety_checked_result,
    }

    reviewed_result = json.loads(json.dumps(safety_checked_result))
    reviewed_result["status"] = "reviewed"
    reviewed_result["review"] = {
        "required": True,
        "status": "reviewed_acknowledged",
        "reason_codes": ["ocr_review_policy"],
        "minimum_reviewer_role": "qualified_professional",
        "review_deadline_policy": "before_relying_on_output",
        "review_outcome": "acknowledged_for_professional_review",
        "reviewed_at": "2026-08-15T12:05:00+00:00",
    }

    examples["enterprise_ocr_prescription_review"] = {
        "request": {
            "path_params": {"prescription_id": "rx_example_0001"},
            # This operation's request body is not yet declared in the maintained
            # OpenAPI (upstream also has no requestBody for this route) -- empty
            # body reflects the current real contract, not a simplification.
            "body": {},
        },
        "response": reviewed_result,
    }

    # ── 2.1.0 (2026-10-25): allergy reference, stored checks, async batches ────────────
    # Every check is stored and returns its check_id (read it back for 90 days).
    allergy_envelope = {
        **envelope(),
        "display_obligations": DISPLAY_OBLIGATIONS,
        "review": {**NOT_REQUIRED_REVIEW},
        "evidence_refs": [
            {
                "evidence_id": "allergy_release_allergy_V1.2.27",
                "domain": "allergy",
                "source_snapshot_id": "safety-2026-08-01",
                "evidence_grade": "primary_label",
                "citation_label": {"en": "Allergy release", "ar": "إصدار الحساسية"},
                "reason": {"en": "Allergy families, ingredients and products from the active allergy release.",
                           "ar": "عائلات الحساسية والمواد الفعالة والمنتجات من إصدار الحساسية النشط."},
                "justification": {"en": "Allergy families, ingredients and products from the active allergy release.",
                                  "ar": "عائلات الحساسية والمواد الفعالة والمنتجات من إصدار الحساسية النشط."},
            }
        ],
        "allergy_release_id": "allergy_V1.2.27",
    }
    for key in ("review_outcome", "reviewed_at"):
        allergy_envelope["review"].pop(key, None)
    penicillins = {"family_id": "BETA_LACTAM_PENICILLIN", "name": {"en": "Penicillins (Beta-Lactam)", "ar": "البنسلينات (بيتا لاكتام)"}}
    side_chain = {"family_id": "BETA_LACTAM_AMINOBENZYL_SIDECHAIN",
                  "name": {"en": "Beta-Lactams (Aminobenzyl Side Chain)", "ar": "بيتا لاكتام (سلسلة أمينوبنزيل الجانبية)"}}
    cephalosporin_cross = {
        "family_id": "BETA_LACTAM_CEPHALOSPORIN_1G",
        "name": {"en": "Cephalosporins (1st Generation)", "ar": "السيفالوسبورينات (الجيل الأول)"},
        "pair_id": "PEN_CEPH1G", "severity": 4, "severity_label": {"en": "Severe", "ar": "شديدة"},
        "bidirectional": True,
        "mechanism": {"en": "Shared beta-lactam ring and similar side chains.", "ar": "حلقة بيتا لاكتام مشتركة وسلاسل جانبية متشابهة."},
        "clinical_note": None,
    }

    examples["enterprise_allergy_families"] = {
        "request": {"query_params": {"locale": "en"}},
        "response": {
            **allergy_envelope,
            "items": [
                {
                    **penicillins,
                    "description": {"en": "Natural and semi-synthetic penicillins.", "ar": "البنسلينات الطبيعية وشبه الصناعية."},
                    "clinical_significance": "high",
                    "clinical_note": None,
                    "aliases": {"en": ["penicillin", "penicillins", "penicillin antibiotics"], "ar": ["بنسلين"]},
                    "member_ingredient_count": 18,
                    "cross_reactive_families": [cephalosporin_cross],
                    "patient_context_entry": {"input_text": "Penicillins (Beta-Lactam)", "resolved_family_id": "BETA_LACTAM_PENICILLIN"},
                }
            ],
            "pagination": {"limit": 82, "cursor": None, "next_cursor": None, "has_more": False},
        },
    }

    examples["enterprise_allergy_substances"] = {
        "request": {"query_params": {"q": "amox", "kind": "ingredient,product", "limit": 2}},
        "response": {
            **allergy_envelope,
            "query": "amox",
            "items": [
                {
                    "substance_id": "ingredient:3f9c2b1a7d4e6f80",
                    "kind": "ingredient",
                    "name": {"en": "AMOXICILLIN", "ar": "أموكسيسيللين"},
                    "families": [side_chain, penicillins],
                    "sfrx_id": None,
                    "generic_name": None,
                    "dosage_form": None,
                    "patient_context_entry": {"input_text": "AMOXICILLIN"},
                },
                {
                    "substance_id": "product:SRX-101-000042",
                    "kind": "product",
                    "name": LOCALIZED_AMOXICILLIN,
                    "families": [side_chain, penicillins],
                    "sfrx_id": "SRX-101-000042",
                    "generic_name": {"en": "AMOXICILLIN", "ar": "أموكسيسيللين"},
                    "dosage_form": LOCALIZED_CAPSULE,
                    "patient_context_entry": {"input_text": "Amoxicillin 500mg Capsule", "resolved_sfrx_id": "SRX-101-000042"},
                },
            ],
            "pagination": {"limit": 2, "cursor": None, "next_cursor": "2", "has_more": True},
        },
    }

    unresolved_review = {
        "required": True, "status": "pending", "reason_codes": ["allergy_unresolved"],
        "minimum_reviewer_role": "qualified_professional", "review_deadline_policy": "before_relying_on_output",
    }
    examples["enterprise_allergy_resolve"] = {
        "request": {"body": {"locale": "en", "items": [
            {"client_allergy_id": "a1", "input_text": "penicillin"},
            {"client_allergy_id": "a2", "input_text": "amoxicillin"},
            {"client_allergy_id": "a3", "input_text": "latex gloves"},
        ]}},
        "response": {
            **allergy_envelope,
            "review": unresolved_review,
            "items": [
                {"client_allergy_id": "a1", "input_text": "penicillin", "status": "normalized", "match_kind": "family",
                 "families": [penicillins], "resolved_family_id": "BETA_LACTAM_PENICILLIN", "resolved_sfrx_id": None,
                 "resolved_substance_id": None, "matched_name": "Penicillins (Beta-Lactam)", "candidate_count": 1,
                 "cross_reactive_families": [cephalosporin_cross],
                 "patient_context_entry": {"input_text": "penicillin", "resolved_family_id": "BETA_LACTAM_PENICILLIN"}},
                {"client_allergy_id": "a2", "input_text": "amoxicillin", "status": "normalized", "match_kind": "ingredient",
                 "families": [side_chain, penicillins], "resolved_family_id": None, "resolved_sfrx_id": None,
                 "resolved_substance_id": "ingredient:3f9c2b1a7d4e6f80", "matched_name": "amoxicillin", "candidate_count": 1,
                 "cross_reactive_families": [cephalosporin_cross], "patient_context_entry": {"input_text": "amoxicillin"}},
                {"client_allergy_id": "a3", "input_text": "latex gloves", "status": "unresolved", "match_kind": None,
                 "families": [], "resolved_family_id": None, "resolved_sfrx_id": None, "resolved_substance_id": None,
                 "matched_name": None, "candidate_count": 0, "cross_reactive_families": [], "patient_context_entry": None},
            ],
            "limitations": [{"en": "Resolution matches the active allergy release vocabulary exactly. Use the substances search for partial names, then pass the returned identifier.",
                             "ar": "تتم المطابقة حرفيًا مع مفردات إصدار الحساسية النشط. استخدم بحث المواد للأسماء الجزئية ثم مرّر المعرّف المُعاد."}],
        },
    }

    stored_result = json.loads(json.dumps(examples["enterprise_safety_check"]["response"]))
    stored_result["check_id"] = "chk_0f1e2d3c4b5a69788796a5b4c3d2e1f0"
    examples["enterprise_safety_check_read"] = {
        "request": {"path_params": {"check_id": "chk_0f1e2d3c4b5a69788796a5b4c3d2e1f0"}},
        "response": {
            "request_id": "req_example_0002",
            "check_id": "chk_0f1e2d3c4b5a69788796a5b4c3d2e1f0",
            "kind": "safety_check",
            "status": "completed",
            "created_at": "2026-10-25T12:00:00+00:00",
            "completed_at": "2026-10-25T12:00:00+00:00",
            "expires_at": "2027-01-23T12:00:00+00:00",
            "inputs": examples["enterprise_safety_check"]["request"]["body"],
            "result": stored_result,
        },
    }

    examples["enterprise_safety_check_batch"] = {
        "request": {"body": {"requested_domains": ["ddi"], "items": [
            {"client_item_id": "rx-1", "medications": [{"input_text": "Warfarin"}, {"input_text": "Aspirin"}]},
            {"client_item_id": "rx-2", "medications": [{"input_text": "Ibuprofen"}, {"input_text": "Warfarin"}]},
        ]}, "headers": {"Idempotency-Key": "batch-2026-10-25-001"}},
        "response": {
            "request_id": "req_example_0003",
            "batch_id": "bat_8a7b6c5d4e3f20112233445566778899",
            "status": "accepted",
            "item_count": 2,
            "items": [
                {"client_item_id": "rx-1", "check_id": "chk_11111111111111111111111111111111"},
                {"client_item_id": "rx-2", "check_id": "chk_22222222222222222222222222222222"},
            ],
            "result_retrieval": "GET /api/enterprise/v1/safety/checks/{check_id}",
        },
    }

    return examples


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def generate(verify: bool = False) -> int:
    examples = build()
    files = {
        OUT / f"{operation_id}.json": json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
        for operation_id, payload in examples.items()
    }
    if verify:
        for path, content in files.items():
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                print(f"stale example fixture: {path.relative_to(ROOT)}")
                return 1
        return 0
    for path, content in files.items():
        write(path, content)
    return 0


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    return generate(verify=args.check)


if __name__ == "__main__":
    raise SystemExit(main())
