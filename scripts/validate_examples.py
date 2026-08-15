#!/usr/bin/env python3
"""Validate every example fixture in examples/enterprise/ against the actual
request/response schemas in the bundled public OpenAPI. This is the check
that proves an example isn't just plausible-looking JSON -- it must satisfy
the same schema a real client response would be validated against.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
OPENAPI = ROOT / "openapi/enterprise-v1.yaml"
COMPONENTS = ROOT / "openapi/components.yaml"
EXAMPLES_DIR = ROOT / "examples/enterprise"

# enterprise_ocr_prescription_events is Server-Sent Events (text/event-stream),
# not a JSON body -- it has no request/response example fixture by design.
NO_FIXTURE_OPERATIONS = {"enterprise_ocr_prescription_events"}


def load(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def deref(node: Any, components: dict[str, Any], seen: frozenset[str] = frozenset()) -> Any:
    """Resolve every $ref (local '#/components/...' or cross-file
    './components.yaml#/components/...') against the components document,
    recursively, with cycle protection."""
    if isinstance(node, dict):
        if "$ref" in node:
            ref = node["$ref"]
            pointer = ref.split("#/", 1)[1] if "#/" in ref else ref
            if pointer in seen:
                return {}
            target: Any = components
            for part in pointer.split("/"):
                target = target[part]
            return deref(target, components, seen | {pointer})
        return {key: deref(value, components, seen) for key, value in node.items()}
    if isinstance(node, list):
        return [deref(item, components, seen) for item in node]
    return node


def operation_schemas() -> dict[str, dict[str, Any]]:
    spec = load(OPENAPI)
    components = load(COMPONENTS)
    result: dict[str, dict[str, Any]] = {}
    for item in spec["paths"].values():
        for method, operation in item.items():
            if method not in {"get", "post"} or not isinstance(operation, dict):
                continue
            operation_id = operation.get("operationId")
            if not operation_id or operation.get("x-status") == "deferred":
                continue
            request_schema = None
            request_body = operation.get("requestBody")
            if request_body:
                content = request_body.get("content", {})
                json_schema = content.get("application/json", {}).get("schema")
                if json_schema:
                    request_schema = deref(json_schema, components)
            response_schema = None
            success = operation.get("responses", {}).get("200") or operation.get("responses", {}).get("202")
            if success:
                json_schema = success.get("content", {}).get("application/json", {}).get("schema")
                if json_schema:
                    response_schema = deref(json_schema, components)
            result[operation_id] = {"request": request_schema, "response": response_schema}
    return result


def check() -> list[str]:
    errors: list[str] = []
    schemas = operation_schemas()
    covered = {path.stem for path in EXAMPLES_DIR.glob("*.json")}
    expected = set(schemas) - NO_FIXTURE_OPERATIONS
    if covered != expected:
        errors.append(f"example coverage mismatch: missing={sorted(expected - covered)} extra={sorted(covered - expected)}")

    for path in sorted(EXAMPLES_DIR.glob("*.json")):
        operation_id = path.stem
        if operation_id not in schemas:
            errors.append(f"{path.name}: no such operation {operation_id}")
            continue
        example = json.loads(path.read_text(encoding="utf-8"))
        response_schema = schemas[operation_id]["response"]
        if response_schema is not None:
            response_value = example.get("response")
            if response_value is None:
                errors.append(f"{path.name}: missing 'response' key")
            else:
                validator = Draft202012Validator(response_schema)
                for validation_error in sorted(validator.iter_errors(response_value), key=lambda e: list(e.path)):
                    errors.append(f"{path.name} response: {'/'.join(str(p) for p in validation_error.path) or '<root>'}: {validation_error.message}")

        request_schema = schemas[operation_id]["request"]
        if request_schema is not None:
            request_body = example.get("request", {}).get("body")
            if request_body is None:
                errors.append(f"{path.name}: operation has a JSON request body but example has no request.body")
            else:
                validator = Draft202012Validator(request_schema)
                for validation_error in sorted(validator.iter_errors(request_body), key=lambda e: list(e.path)):
                    errors.append(f"{path.name} request: {'/'.join(str(p) for p in validation_error.path) or '<root>'}: {validation_error.message}")
    return errors


def main() -> int:
    errors = check()
    if errors:
        print("Example fixture validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Example fixture validation passed: all fixtures validate against their real response schemas")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
