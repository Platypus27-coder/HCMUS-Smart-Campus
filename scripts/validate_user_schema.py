"""Lightweight validation for the user-context schema and demo profile."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SENSITIVE_FIELDS = {"student_id", "citizen_id", "financial_records", "health_records", "full_transcript"}


def load_json(path: Path) -> dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"Cannot parse {path.relative_to(ROOT)}: {error}") from error
    if not isinstance(data, dict):
        raise ValueError(f"Expected a JSON object in {path.relative_to(ROOT)}")
    return data


def required_fields(value: Any) -> set[str]:
    fields: set[str] = set()
    if isinstance(value, dict):
        required = value.get("required", [])
        if isinstance(required, list):
            fields.update(item for item in required if isinstance(item, str))
        for child in value.values():
            fields.update(required_fields(child))
    elif isinstance(value, list):
        for child in value:
            fields.update(required_fields(child))
    return fields


def validate() -> list[str]:
    errors: list[str] = []
    try:
        schema = load_json(ROOT / "shared" / "user-profile.schema.json")
        sample = load_json(ROOT / "examples" / "runtime" / "profile-summary.example.json")
    except ValueError as error:
        return [str(error)]

    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        errors.append("user-profile.schema.json: expected Draft 2020-12 $schema")
    if not isinstance(schema.get("properties"), dict):
        errors.append("user-profile.schema.json: top-level properties must be a mapping")
    if SENSITIVE_FIELDS & required_fields(schema):
        errors.append("user-profile.schema.json: sensitive identity or record fields must not be required")

    academic = sample.get("profile", {}).get("academic", {}) if isinstance(sample.get("profile"), dict) else {}
    metadata = sample.get("metadata", {})
    if academic.get("training_score", "missing") is not None:
        errors.append("demo profile: training_score must demonstrate null as unknown")
    if not isinstance(sample.get("demo_notice"), str) or "DEMO DATA" not in sample["demo_notice"]:
        errors.append("demo profile: explicit DEMO DATA notice is required")
    if sample.get("user_id") != "example-user":
        errors.append("demo profile: user_id must remain the non-real example-user identifier")
    if not isinstance(metadata, dict) or metadata.get("consent_to_store") is not False:
        errors.append("demo profile: consent_to_store must be false")

    schema_academic = schema.get("properties", {}).get("profile", {}).get("properties", {}).get("academic", {})
    training_definition = schema_academic.get("properties", {}).get("training_score", {}) if isinstance(schema_academic, dict) else {}
    if "null" not in training_definition.get("type", []):
        errors.append("user-profile.schema.json: training_score must permit null")
    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(f"[ERROR] {error}")
        return 1
    print("[OK] user-profile.schema.json parses as Draft 2020-12 metadata")
    print("[OK] demo profile is explicitly non-real and uses null for unknown training_score")
    print("[OK] sensitive identity and record fields are not required")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
