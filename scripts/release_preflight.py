#!/usr/bin/env python3
"""Validate the public Enterprise projection and its mirrors stay inside the
public/private boundary: only operations with a complete success contract may
ship as available, and no private release identity may leak into this repo."""

from __future__ import annotations

import hashlib
import re
import subprocess
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
# These operations exist in the maintained backend OpenAPI with no non-403 success
# response yet (live-confirmed 2026-08-15: no backend implements them and no key on
# any plan is entitled to call them). They stay present in the public spec (so the
# API surface and its migration state are honestly documented) but must never carry
# an invented 200/202 and must never appear as available in the release manifest,
# SDKs, or docs.
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
    # Browser-only saved-profile session controls: Enterprise is request-scoped
    # patient_context only and must never accept or echo these, at any nesting
    # depth or in any schema this repo ships (see plan v2 section 3.4).
    r"(?i)profile_context_mode",
    r"(?i)include_saved_current_medications",
    r"(?i)saved_profile_applied",
    r"(?i)resolver[_-]?candidate",
    r"(?i)(storage|model|resolver)[_-]?id\b",
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
    r"(?i)profile_context_mode",
    r"(?i)include_saved_current_medications",
    r"(?i)saved_profile_applied",
    # a lowercase letter AND a digit rules out documentation placeholders like
    # "YOUR_ENTERPRISE_KEY" / "<API_KEY>" while still catching real secret-shaped values
    r"(?i)(api[_-]?key|client[_-]?secret|password)\s*[:=]\s*['\"](?=[^'\"]*[a-z])(?=[^'\"]*[0-9])[A-Za-z0-9_\-]{12,}['\"]",
)
# Pre-2.0 candidate versions are forbidden in anything shipped to a public registry:
# see RELEASE_CHECKLIST.md ("all releases from now on are v2.0.0+").
LEGACY_VERSION_PATTERN = re.compile(r'"version"\s*:\s*"0\.|version\s*=\s*"0\.|<Version>0\.')

# This entire repository is public on GitHub, not just the narrower set of files that
# get packaged into a registry artifact or docs page (PUBLIC_SHIPPED_ROOTS above).
# README.md previously shipped a real private release identifier
# (mis-enterprise-2026.07.28-authenticated.1) and several source comments named the
# private backend repository and its internal file/service layout -- none of that was
# ever scanned because it wasn't inside PUBLIC_SHIPPED_ROOTS. This checks every
# git-tracked file in the repository (i.e. everything actually visible on GitHub) for
# the small set of internal-identifier patterns that must never appear anywhere here,
# regardless of whether the file is "shipped" in the packaging sense.
REPO_WIDE_FORBIDDEN_PATTERNS = (
    re.compile(r"SafeRx-MIS", re.IGNORECASE),
    re.compile(r"\bMIS\b"),
    re.compile(r"apps/gateway/cmd"),
    re.compile(r"apps/browser/src"),
    re.compile(r"services/[a-z][a-z-]*-service/src"),
)
REPO_WIDE_EXCLUDE_EXTENSIONS = {
    ".ico", ".svg", ".png", ".jpg", ".jpeg", ".gif", ".lock",
}
REPO_WIDE_EXCLUDE_FILES = {"package-lock.json"}


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


def _iter_tracked_files() -> list[Path]:
    output = subprocess.run(
        ["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout
    files = []
    for line in output.splitlines():
        if not line:
            continue
        path = ROOT / line
        if path.suffix in REPO_WIDE_EXCLUDE_EXTENSIONS or path.name in REPO_WIDE_EXCLUDE_FILES:
            continue
        if path.is_file():
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


# Files whose content defines "what release_version actually means" -- if any of these
# differ from what a version's git tag recorded, that version has already been published
# with different content and must not be reused.
_RELEASE_DEFINING_FILES = (PUBLIC_SPEC, PUBLIC_COMPONENTS, RELEASE_MANIFEST)


def _content_hash(read: Any) -> str:
    """read(path) -> bytes for each release-defining file; combine into one hash."""
    parts = sorted(hashlib.sha256(read(path)).hexdigest() for path in _RELEASE_DEFINING_FILES)
    return hashlib.sha256("".join(parts).encode()).hexdigest()


def _published_content_hash(version: str) -> str | None:
    """Content hash of the release-defining files as recorded by git tag v{version}, or
    None if that version has never been tagged (i.e. never actually published)."""
    tag = f"v{version}"
    check = subprocess.run(
        ["git", "rev-parse", "--verify", "--quiet", f"refs/tags/{tag}"],
        cwd=ROOT, capture_output=True, text=True,
    )
    if check.returncode != 0:
        return None

    def _read_at_tag(path: Path) -> bytes:
        rel = path.relative_to(ROOT).as_posix()
        result = subprocess.run(
            ["git", "show", f"{tag}:{rel}"], cwd=ROOT, capture_output=True,
        )
        if result.returncode != 0:
            return b""
        return result.stdout

    return _content_hash(_read_at_tag)


def _check_release_version_is_immutable(release: dict[str, Any]) -> list[str]:
    version = release.get("release_version")
    if not version:
        return ["release manifest is missing release_version"]
    published_hash = _published_content_hash(str(version))
    if published_hash is None:
        return []  # this version has never been tagged/published -- nothing to compare
    current_hash = _content_hash(lambda path: path.read_bytes())
    if published_hash != current_hash:
        return [
            f"release_version {version!r} was already published (git tag v{version} exists) "
            "with different contract content (openapi/enterprise-v1.yaml, "
            "openapi/components.yaml, or release/current.yaml changed since that tag). "
            "Overwriting a published version's content is prohibited -- bump release_version "
            "in release/current.yaml (and the matching CHANGELOG.md entry) before publishing again."
        ]
    return []


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
        errors.extend(_check_release_version_is_immutable(release))

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

        for path in _iter_tracked_files():
            if path == Path(__file__).resolve():
                continue  # this file's own pattern definitions, not a leak
            try:
                text = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            for pattern in REPO_WIDE_FORBIDDEN_PATTERNS:
                if pattern.search(text):
                    errors.append(f"forbidden internal reference in {path.relative_to(ROOT)}: {pattern.pattern}")

    if errors:
        print("Enterprise public preflight failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Enterprise public preflight passed: public contract, mirrors, and release manifest agree on the available operation set")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
