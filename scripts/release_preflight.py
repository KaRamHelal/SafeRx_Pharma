#!/usr/bin/env python3
"""Validate the SafeRx_Pharma public release inputs without publishing.

This gate is intentionally limited to the public repository. It proves that
the legacy public surface is still present, Fern points at the owned host, and
the checked-in mirrors are synchronized. Enterprise MIS artifacts are added
only through an explicit sanitized projection; this gate must not silently
copy internal OpenAPI components or OCR payload fields into the public repo.
"""

from __future__ import annotations

import hashlib
import os
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_SPEC = ROOT / "openapi/drug-safety-v1.yaml"
FERN_SPEC = ROOT / "fern/apis/drug-safety/openapi/drug-safety-v1.yaml"
FERN_API_SPEC = ROOT / "fern/apis/drug-safety/openapi/openapi.yaml"
DOCS_CONFIG = ROOT / "fern/docs.yml"
RELEASE_MANIFEST = ROOT / "release/2.0.1.yaml"
EXPECTED_RELEASE_VERSION = os.environ.get("SAFERX_RELEASE_VERSION", "2.0.1")

LEGACY_OPERATION_IDS = {
    "checkDrugSafety",
    "getDrugSafetyMetadata",
    "getDrugSafetyHealth",
    "createFreeApiKey",
    "verifyFreeApiKey",
}
FORBIDDEN_PUBLIC_PATTERNS = (
    r"(?i)openbao",
    r"(?i)clusterip",
    r"(?i)internal\.svc",
    r"(?i)(private[_-]?key|client[_-]?secret|password)",
)


def _load(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.relative_to(ROOT)} must contain a mapping")
    return value


def _operation_ids(spec: dict[str, Any]) -> set[str]:
    return {
        str(operation["operationId"])
        for path_item in spec.get("paths", {}).values()
        for method, operation in path_item.items()
        if method in {"get", "post", "put", "patch", "delete"}
        and isinstance(operation, dict)
        and "operationId" in operation
    }


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    errors: list[str] = []
    for path in (PUBLIC_SPEC, FERN_SPEC, FERN_API_SPEC, DOCS_CONFIG, RELEASE_MANIFEST):
        if not path.is_file():
            errors.append(f"required release input is missing: {path.relative_to(ROOT)}")

    if not errors:
        public = _load(PUBLIC_SPEC)
        fern = _load(FERN_SPEC)
        fern_api = _load(FERN_API_SPEC)
        docs = _load(DOCS_CONFIG)
        release = _load(RELEASE_MANIFEST)

        if public.get("openapi") != "3.1.1":
            errors.append("public OpenAPI must remain OpenAPI 3.1.1")
        if public.get("info", {}).get("version") != EXPECTED_RELEASE_VERSION:
            errors.append(f"public OpenAPI version must be {EXPECTED_RELEASE_VERSION}")
        if release.get("release_version") != EXPECTED_RELEASE_VERSION:
            errors.append(f"release manifest version must be {EXPECTED_RELEASE_VERSION}")
        if release.get("release_line") != "MIS":
            errors.append("release manifest must identify the MIS release line")
        if not LEGACY_OPERATION_IDS <= _operation_ids(public):
            errors.append("legacy public operation IDs are not all present")
        if _sha256(PUBLIC_SPEC) != _sha256(FERN_SPEC) or _sha256(PUBLIC_SPEC) != _sha256(FERN_API_SPEC):
            errors.append("public OpenAPI mirrors are not byte-identical")
        instances = docs.get("instances", [])
        if not any(instance.get("url") == "saferx.docs.buildwithfern.com" for instance in instances):
            errors.append("Fern docs config does not bind saferx.docs.buildwithfern.com")
        if not any(instance.get("custom-domain") == "docs.saferx.online" for instance in instances):
            errors.append("Fern docs config does not bind the owned docs.saferx.online host")

        for path in (PUBLIC_SPEC, FERN_SPEC, FERN_API_SPEC):
            text = path.read_text(encoding="utf-8")
            for pattern in FORBIDDEN_PUBLIC_PATTERNS:
                if re.search(pattern, text):
                    errors.append(f"forbidden public pattern in {path.relative_to(ROOT)}: {pattern}")

    if errors:
        print("public release preflight failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"public release preflight passed: MIS {EXPECTED_RELEASE_VERSION}, both docs hosts bound, public API mirrors synchronized")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
