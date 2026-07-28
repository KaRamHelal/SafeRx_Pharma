#!/usr/bin/env python3
"""Validate the authenticated MIS Enterprise projection and its mirrors."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_SPEC = ROOT / "openapi/enterprise-v1.yaml"
PUBLIC_COMPONENTS = ROOT / "openapi/components.yaml"
FERN_SPEC = ROOT / "fern/apis/enterprise/openapi/enterprise-v1.yaml"
FERN_API_SPEC = ROOT / "fern/apis/enterprise/openapi/enterprise-api.yaml"
FERN_COMPONENTS = ROOT / "fern/apis/enterprise/openapi/components.yaml"
RELEASE_MANIFEST = ROOT / "release/2.0.2-preview.1.yaml"
EXPECTED_OPERATION_IDS = {
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
FORBIDDEN_PUBLIC_PATTERNS = (
    r"(?i)openbao",
    r"(?i)clusterip",
    r"(?i)internal\.svc",
    r"(?i)(private[_-]?key|client[_-]?secret|password|credential)",
    r"(?i)(person[_-]?specific|raw[_-]?pipeline|model[_-]?private)",
    r"(?i)(enterprise_mcp|admin_console)",
)


def _load(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.relative_to(ROOT)} must contain a mapping")
    return value


def _operation_ids(spec: dict[str, Any]) -> set[str]:
    return {
        str(operation["operationId"])
        for item in spec.get("paths", {}).values()
        for method, operation in item.items()
        if method in {"get", "post", "put", "patch", "delete"}
        and isinstance(operation, dict)
        and "operationId" in operation
    }


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    errors: list[str] = []
    required = (PUBLIC_SPEC, PUBLIC_COMPONENTS, FERN_SPEC, FERN_API_SPEC, FERN_COMPONENTS, RELEASE_MANIFEST)
    for path in required:
        if not path.is_file():
            errors.append(f"required release input is missing: {path.relative_to(ROOT)}")

    if not errors:
        public = _load(PUBLIC_SPEC)
        components = _load(PUBLIC_COMPONENTS)
        fern = _load(FERN_SPEC)
        fern_api = _load(FERN_API_SPEC)
        release = _load(RELEASE_MANIFEST)
        if public.get("openapi") != "3.1.1":
            errors.append("Enterprise public OpenAPI must remain OpenAPI 3.1.1")
        if public.get("info", {}).get("version") != "2026.07.28":
            errors.append("Enterprise public OpenAPI must match the authenticated MIS release")
        if _operation_ids(public) != EXPECTED_OPERATION_IDS:
            errors.append("Enterprise operation IDs do not match the approved public projection")
        if public.get("servers", [{}])[0].get("url") != "https://saferx.online/api/enterprise/v1":
            errors.append("Enterprise server URL is not the current base URL")
        if components.get("components", {}).get("securitySchemes", {}).get("enterpriseApiKey", {}).get("name") != "X-SafeRx-API-Key":
            errors.append("signed Enterprise API-key header is missing")
        if _sha256(PUBLIC_SPEC) != _sha256(FERN_SPEC) or _sha256(PUBLIC_SPEC) != _sha256(FERN_API_SPEC):
            errors.append("Fern OpenAPI mirrors are not byte-identical")
        if _sha256(PUBLIC_COMPONENTS) != _sha256(FERN_COMPONENTS):
            errors.append("Fern component mirrors are not byte-identical")
        if release.get("release_version") != "2026.07.28" or release.get("status") != "available":
            errors.append("release manifest must identify authenticated Enterprise availability")

        for path in (PUBLIC_SPEC, PUBLIC_COMPONENTS, FERN_SPEC, FERN_API_SPEC, FERN_COMPONENTS):
            text = path.read_text(encoding="utf-8")
            if "additionalProperties: true" in text:
                errors.append(f"permissive response schema in {path.relative_to(ROOT)}")
            for pattern in FORBIDDEN_PUBLIC_PATTERNS:
                if re.search(pattern, text):
                    errors.append(f"forbidden public pattern in {path.relative_to(ROOT)}: {pattern}")

    if errors:
        print("Enterprise public preflight failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Enterprise public preflight passed: authenticated signed contract and mirrors are synchronized")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
