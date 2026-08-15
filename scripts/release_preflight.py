#!/usr/bin/env python3
"""Validate the public Enterprise projection and its mirrors stay inside the
public/private boundary: only operations with a complete success contract may
ship as available, and no private release identity may leak into this repo."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_SPEC = ROOT / "openapi/enterprise-v1.yaml"
PUBLIC_COMPONENTS = ROOT / "openapi/components.yaml"
# fern/openapi, fern/apis/enterprise/openapi, and fern/apis/enterprise-csharp/openapi
# are symlinks to the two files above (single source of truth) -- these hash checks
# are defense-in-depth against a symlink ever being replaced by a real, driftable copy.
FERN_SPEC = ROOT / "fern/apis/enterprise/openapi/enterprise-v1.yaml"
FERN_COMPONENTS = ROOT / "fern/apis/enterprise/openapi/components.yaml"
FERN_CSHARP_SPEC = ROOT / "fern/apis/enterprise-csharp/openapi/enterprise-v1.yaml"
FERN_CSHARP_COMPONENTS = ROOT / "fern/apis/enterprise-csharp/openapi/components.yaml"
RELEASE_MANIFEST = ROOT / "release/current.yaml"
EXPECTED_AVAILABLE_OPERATION_IDS = {
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
# These operations exist in the maintained MIS OpenAPI with no non-501 success
# response yet. They stay present in the public spec (so the API surface and its
# migration state are honestly documented) but must never carry an invented 200/202
# and must never appear as available in the release manifest, SDKs, or docs.
EXPECTED_DEFERRED_OPERATION_IDS = {
    "enterprise_capabilities",
    "enterprise_status",
    "enterprise_safety_check_read",
    "enterprise_safety_check_batch",
    "enterprise_allergy_resolve",
    "enterprise_allergy_families",
    "enterprise_allergy_substances",
}
EXPECTED_OPERATION_IDS = EXPECTED_AVAILABLE_OPERATION_IDS | EXPECTED_DEFERRED_OPERATION_IDS
FORBIDDEN_PUBLIC_PATTERNS = (
    r"(?i)openbao",
    r"(?i)clusterip",
    r"(?i)internal\.svc",
    r"(?i)(private[_-]?key|client[_-]?secret|password|credential)",
    r"(?i)(person[_-]?specific|raw[_-]?pipeline|model[_-]?private)",
    r"(?i)(enterprise_mcp|admin_console)",
    r"(?i)drug_safety",
    r"(?i)mis-enterprise",
    r"(?i)authenticated_enterprise_customers",
    r"(?i)route_entitlements",
)

# Everything else in this repo that actually ships to a public registry or docs host
# (npm/PyPI/NuGet packages, docs.saferx.online pages) but historically was never scanned
# for internal leakage the way openapi/fern are above. This closes that gap: the
# mcp-server npm package was published to the public registry from this directory
# tree for over a year (see public-package-catalog.yaml / public-availability-state-
# machine.yaml, mcp-stdio is internal_only) without ever being checked against
# FORBIDDEN_PUBLIC_PATTERNS.
PUBLIC_SHIPPED_ROOTS = (
    ROOT / "packages/mcp-server/src",
    ROOT / "packages/mcp-server/README.md",
    ROOT / "packages/mcp-server/package.json",
    ROOT / "packages/python/src",
    ROOT / "packages/python/pyproject.toml",
    ROOT / "packages/typescript/src",
    ROOT / "packages/typescript/package.json",
    ROOT / "packages/csharp",
    ROOT / "packages/release-manifest.json",
    ROOT / "fern/docs/pages",
    ROOT / "release/current.yaml",
)
PUBLIC_SHIPPED_EXCLUDE_DIRS = {"node_modules", "dist", "obj", "bin", "__pycache__"}
PUBLIC_SHIPPED_EXTENSIONS = {".py", ".ts", ".tsx", ".cs", ".json", ".toml", ".csproj", ".mdx", ".md"}
# Deliberately narrower than FORBIDDEN_PUBLIC_PATTERNS: shipped code and prose docs
# legitimately use words like "credential" or "API key" when explaining auth to
# developers, so a bare word-ban produces wall-to-wall false positives there. This set
# targets real infra/internal identifiers and secret-shaped values instead of vocabulary.
FORBIDDEN_SHIPPED_PATTERNS = (
    r"(?i)openbao",
    r"(?i)clusterip",
    r"(?i)internal\.svc",
    r"(?i)drug_safety",
    r"(?i)(enterprise_mcp|admin_console)",
    r"(?i)mis-enterprise",
    r"(?i)authenticated_enterprise_customers",
    r"(?i)route_entitlements",
    # a lowercase letter AND a digit rules out documentation placeholders like
    # "YOUR_ENTERPRISE_KEY" / "<API_KEY>" while still catching real secret-shaped values
    r"(?i)(api[_-]?key|client[_-]?secret|password)\s*[:=]\s*['\"](?=[^'\"]*[a-z])(?=[^'\"]*[0-9])[A-Za-z0-9_\-]{12,}['\"]",
)
# Pre-2.0 candidate versions are forbidden in anything shipped to a public registry:
# see RELEASE_CHECKLIST.md ("all releases from now on are v2.0.0+, separate from the
# pre-MIS era") and contracts/public-package-catalog.yaml (initial_version '2.0.1').
LEGACY_VERSION_PATTERN = re.compile(r'"version"\s*:\s*"0\.|version\s*=\s*"0\.|<Version>0\.')


def _iter_public_shipped_files() -> list[Path]:
    files: list[Path] = []
    for root in PUBLIC_SHIPPED_ROOTS:
        if root.is_file():
            files.append(root)
            continue
        if not root.is_dir():
            continue
        for path in root.rglob("*"):
            if not path.is_file() or path.suffix not in PUBLIC_SHIPPED_EXTENSIONS:
                continue
            if PUBLIC_SHIPPED_EXCLUDE_DIRS & set(path.relative_to(ROOT).parts):
                continue
            files.append(path)
    return files


def _load(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.relative_to(ROOT)} must contain a mapping")
    return value


def _operations(spec: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        operation
        for item in spec.get("paths", {}).values()
        for method, operation in item.items()
        if method in {"get", "post", "put", "patch", "delete"}
        and isinstance(operation, dict)
        and "operationId" in operation
    ]


def _operation_ids(spec: dict[str, Any]) -> set[str]:
    return {str(operation["operationId"]) for operation in _operations(spec)}


def _available_operation_ids(spec: dict[str, Any]) -> set[str]:
    return {
        str(operation["operationId"])
        for operation in _operations(spec)
        if operation.get("x-status", "available") == "available"
    }


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    errors: list[str] = []
    required = (
        PUBLIC_SPEC, PUBLIC_COMPONENTS, FERN_SPEC, FERN_COMPONENTS,
        FERN_CSHARP_SPEC, FERN_CSHARP_COMPONENTS, RELEASE_MANIFEST,
    )
    for path in required:
        if not path.is_file():
            errors.append(f"required release input is missing: {path.relative_to(ROOT)}")

    if not errors:
        public = _load(PUBLIC_SPEC)
        components = _load(PUBLIC_COMPONENTS)
        fern = _load(FERN_SPEC)
        fern_csharp = _load(FERN_CSHARP_SPEC)
        release = _load(RELEASE_MANIFEST)
        if public.get("openapi") != "3.1.1":
            errors.append("Enterprise public OpenAPI must remain OpenAPI 3.1.1")
        if _operation_ids(public) != EXPECTED_OPERATION_IDS:
            errors.append("Enterprise operation IDs do not match the approved public projection")
        if _available_operation_ids(public) != EXPECTED_AVAILABLE_OPERATION_IDS:
            errors.append(
                "operations marked available in the public OpenAPI do not match the "
                "set with a complete, live-verified success contract"
            )
        for operation in _operations(public):
            operation_id = str(operation.get("operationId"))
            if operation_id in EXPECTED_DEFERRED_OPERATION_IDS:
                success_codes = {code for code in operation.get("responses", {}) if str(code)[0] in "23"}
                if success_codes:
                    errors.append(
                        f"deferred operation {operation_id} must not carry an invented "
                        f"success response: {sorted(success_codes)}"
                    )
        if public.get("servers", [{}])[0].get("url") != "https://saferx.online/api/enterprise/v1":
            errors.append("Enterprise server URL is not the current base URL")
        if components.get("components", {}).get("securitySchemes", {}).get("enterpriseApiKey", {}).get("name") != "X-SafeRx-API-Key":
            errors.append("signed Enterprise API-key header is missing")
        if _sha256(PUBLIC_SPEC) != _sha256(FERN_SPEC) or _sha256(PUBLIC_SPEC) != _sha256(FERN_CSHARP_SPEC):
            errors.append("Fern OpenAPI mirrors are not byte-identical")
        if _sha256(PUBLIC_COMPONENTS) != _sha256(FERN_COMPONENTS) or _sha256(PUBLIC_COMPONENTS) != _sha256(FERN_CSHARP_COMPONENTS):
            errors.append("Fern component mirrors are not byte-identical")
        if release.get("api_contract", {}).get("operation_count") != len(EXPECTED_AVAILABLE_OPERATION_IDS):
            errors.append("release manifest operation_count does not match the available public operation set")
        if release.get("status") not in {"preview", "available"}:
            errors.append("release manifest must carry a real public availability state (preview or available)")
        if "audience" in release.get("availability", {}) or "route_entitlements" in release.get("availability", {}):
            errors.append("release manifest availability block must not carry private audience/entitlement identifiers")

        for path in (PUBLIC_SPEC, PUBLIC_COMPONENTS, FERN_SPEC, FERN_COMPONENTS, FERN_CSHARP_SPEC, FERN_CSHARP_COMPONENTS):
            text = path.read_text(encoding="utf-8")
            if "additionalProperties: true" in text:
                errors.append(f"permissive response schema in {path.relative_to(ROOT)}")
            for pattern in FORBIDDEN_PUBLIC_PATTERNS:
                if re.search(pattern, text):
                    errors.append(f"forbidden public pattern in {path.relative_to(ROOT)}: {pattern}")

        for path in _iter_public_shipped_files():
            text = path.read_text(encoding="utf-8")
            for pattern in FORBIDDEN_SHIPPED_PATTERNS:
                if re.search(pattern, text):
                    errors.append(f"forbidden internal pattern in {path.relative_to(ROOT)}: {pattern}")
            if LEGACY_VERSION_PATTERN.search(text):
                errors.append(f"pre-2.0 candidate version string in publicly-shipped file {path.relative_to(ROOT)}")

    if errors:
        print("Enterprise public preflight failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Enterprise public preflight passed: public contract, mirrors, and release manifest agree on the available operation set")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
