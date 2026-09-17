"""Validate the Smart Campus directory, relationship graph, and generated local views."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
ALLOWED_RELATIONSHIPS = {
    "requests_validation_from",
    "provides_data_to",
    "collaborates_with",
    "refers_to",
    "supports",
}
CANONICAL_AGENTS = {
    "schedule-deadline-agent",
    "gpa-academic-standing-agent",
    "academic-advisor-agent",
    "scholarship-matching-agent",
    "library-research-agent",
    "clubs-activities-agent",
    "administrative-procedure-agent",
    "regulation-qa-agent",
    "department-contact-agent",
    "teaching-material-assistant",
    "research-assistant-agent",
    "class-support-agent",
    "student-wellbeing-agent",
    "soft-skills-coach-agent",
    "campus-router-agent",
    "campus-aggregator-agent",
}
SPECIALISTS = CANONICAL_AGENTS - {"campus-router-agent", "campus-aggregator-agent"}


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle)
    except (OSError, yaml.YAMLError) as error:
        raise ValueError(f"Cannot parse {path}: {error}") from error
    if not isinstance(data, dict):
        raise ValueError(f"Expected a YAML mapping in {path}")
    return data


def has_duplicates(values: list[Any]) -> bool:
    return len(values) != len(set(values))


def validate_metadata(directory_path: Path, relationships_path: Path) -> tuple[list[str], int]:
    """Validate source metadata without requiring generated files."""
    errors: list[str] = []
    try:
        directory = load_yaml(directory_path)
        relationship_data = load_yaml(relationships_path)
    except ValueError as error:
        return [str(error)], 0

    agents = directory.get("agents")
    if not isinstance(agents, list):
        return ["agent-directory.yaml: 'agents' must be a list"], 0

    ids = [item.get("id") for item in agents if isinstance(item, dict)]
    if len(ids) != len(agents) or any(not isinstance(agent_id, str) for agent_id in ids):
        errors.append("agent-directory.yaml: every agent must have a string id")
    if has_duplicates(ids):
        errors.append("agent-directory.yaml: duplicate agent IDs found")
    id_set = set(ids)
    if len(ids) != 16:
        errors.append(f"agent-directory.yaml: expected exactly 16 agents, found {len(ids)}")
    if id_set != CANONICAL_AGENTS:
        missing = sorted(CANONICAL_AGENTS - id_set)
        unexpected = sorted(id_set - CANONICAL_AGENTS)
        if missing:
            errors.append(f"agent-directory.yaml: missing canonical agents: {', '.join(missing)}")
        if unexpected:
            errors.append(f"agent-directory.yaml: unexpected agents: {', '.join(unexpected)}")

    graph = relationship_data.get("relationships")
    if not isinstance(graph, dict):
        return errors + ["agent-relationships.yaml: 'relationships' must be a mapping"], 0
    declared_types = relationship_data.get("allowed_relationship_types", sorted(ALLOWED_RELATIONSHIPS))
    if not isinstance(declared_types, list) or set(declared_types) != ALLOWED_RELATIONSHIPS:
        errors.append("agent-relationships.yaml: allowed_relationship_types must list the supported relationship types exactly once")
    allowed_types = set(declared_types) if isinstance(declared_types, list) else ALLOWED_RELATIONSHIPS

    relationship_count = 0
    for source, edges in graph.items():
        if source not in id_set:
            errors.append(f"agent-relationships.yaml: unknown source: {source}")
        if not isinstance(edges, list):
            errors.append(f"agent-relationships.yaml: {source} must contain a list of relationships")
            continue
        for index, edge in enumerate(edges, start=1):
            relationship_count += 1
            label = f"{source} relationship #{index}"
            if not isinstance(edge, dict):
                errors.append(f"{label}: relationship must be a mapping")
                continue
            target = edge.get("target")
            if target not in id_set:
                errors.append(f"{label}: unknown target: {target}")
            if source == target:
                errors.append(f"{label}: self relationships are not allowed")
            relation_type = edge.get("relationship")
            if relation_type not in allowed_types:
                errors.append(f"{label}: invalid relationship type: {relation_type}")
            for field in ("triggers", "expected_output", "send", "do_not_send"):
                value = edge.get(field)
                if not isinstance(value, list):
                    errors.append(f"{label}: {field} must be a list")
                elif field in {"triggers", "expected_output"} and not value:
                    errors.append(f"{label}: {field} must not be empty")
                elif has_duplicates(value):
                    errors.append(f"{label}: {field} contains duplicate fields")
            send = edge.get("send", [])
            do_not_send = edge.get("do_not_send", [])
            if isinstance(send, list) and isinstance(do_not_send, list):
                overlap = sorted(set(send) & set(do_not_send))
                if overlap:
                    errors.append(f"{label}: fields appear in both send and do_not_send: {', '.join(overlap)}")

    router_targets = {
        edge.get("target")
        for edge in graph.get("campus-router-agent", [])
        if isinstance(edge, dict)
    }
    expected_router_targets = CANONICAL_AGENTS - {"campus-router-agent"}
    if router_targets != expected_router_targets:
        missing = sorted(expected_router_targets - router_targets)
        unexpected = sorted(router_targets - expected_router_targets)
        errors.append(
            "campus-router-agent must reference all 15 other agents"
            + (f"; missing: {', '.join(missing)}" if missing else "")
            + (f"; unexpected: {', '.join(unexpected)}" if unexpected else "")
        )

    aggregator_targets = {
        edge.get("target")
        for edge in graph.get("campus-aggregator-agent", [])
        if isinstance(edge, dict)
    }
    if not SPECIALISTS.issubset(aggregator_targets):
        missing = sorted(SPECIALISTS - aggregator_targets)
        errors.append(f"campus-aggregator-agent must represent every specialist output; missing: {', '.join(missing)}")
    if "campus-router-agent" not in aggregator_targets:
        errors.append("campus-aggregator-agent must represent the Router routing plan")
    return errors, relationship_count


def expected_local_payload(source: str, graph: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    return {
        "current_agent": source,
        "related_agents": [
            {
                "agent": edge["target"],
                "relationship": edge["relationship"],
                "reason": edge["reason"],
                "when_to_use": edge["triggers"],
                "send": edge["send"],
                "do_not_send": edge["do_not_send"],
                "expected_output": edge["expected_output"],
            }
            for edge in graph.get(source, [])
        ],
    }


def validate_generated_files(root: Path) -> list[str]:
    errors: list[str] = []
    try:
        directory = load_yaml(root / "shared" / "agent-directory.yaml")
        graph = load_yaml(root / "shared" / "agent-relationships.yaml").get("relationships", {})
    except ValueError as error:
        return [str(error)]
    if not isinstance(graph, dict):
        return ["agent-relationships.yaml: 'relationships' must be a mapping"]

    for agent in directory.get("agents", []):
        if not isinstance(agent, dict) or "id" not in agent or "subspace" not in agent:
            continue
        path = root / "subspaces" / agent["subspace"] / agent["id"] / "agent" / "related-agents.yaml"
        if not path.is_file():
            errors.append(f"missing generated file: {path.relative_to(root)}")
            continue
        try:
            actual = load_yaml(path)
        except ValueError as error:
            errors.append(str(error))
            continue
        expected = expected_local_payload(agent["id"], graph)
        if actual != expected:
            errors.append(f"generated file is out of sync: {path.relative_to(root)}")
    return errors


def validate_repository(root: Path = ROOT) -> tuple[list[str], int]:
    errors, relationship_count = validate_metadata(
        root / "shared" / "agent-directory.yaml",
        root / "shared" / "agent-relationships.yaml",
    )
    if not errors:
        errors.extend(validate_generated_files(root))
    return errors, relationship_count


def main() -> int:
    errors, relationship_count = validate_repository()
    if errors:
        for error in errors:
            print(f"[ERROR] {error}")
        return 1
    print("[OK] agent-directory.yaml: 16 agents")
    print(f"[OK] agent-relationships.yaml: {relationship_count} relationships")
    print("[OK] all relationship sources and targets exist")
    print("[OK] Router references all other agents; Aggregator represents all specialist outputs")
    print("[OK] generated related-agents files are synchronized")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
