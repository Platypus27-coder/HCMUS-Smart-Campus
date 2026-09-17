"""Validate the canonical routing rules and baseline scoring configuration."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle)
    except (OSError, yaml.YAMLError) as error:
        raise ValueError(f"Cannot parse {path.relative_to(ROOT)}: {error}") from error
    if not isinstance(data, dict):
        raise ValueError(f"Expected a YAML mapping in {path.relative_to(ROOT)}")
    return data


def duplicate_values(values: Any) -> bool:
    return not isinstance(values, list) or len(values) != len(set(values))


def validate() -> list[str]:
    errors: list[str] = []
    try:
        directory = load_yaml(ROOT / "shared" / "agent-directory.yaml")
        rules_data = load_yaml(ROOT / "shared" / "routing-rules.yaml")
        criteria = load_yaml(ROOT / "shared" / "routing-score-criteria.yaml")
    except ValueError as error:
        return [str(error)]

    agents = {agent.get("id"): agent for agent in directory.get("agents", []) if isinstance(agent, dict)}
    capabilities = {agent_id: set(agent.get("capabilities", [])) for agent_id, agent in agents.items()}
    hard_rules = rules_data.get("hard_rules", [])
    soft_rules = rules_data.get("soft_rules", [])
    for label, rules in (("hard_rules", hard_rules), ("soft_rules", soft_rules)):
        if not isinstance(rules, list):
            errors.append(f"routing-rules.yaml: {label} must be a list")
            continue
        ids = [rule.get("id") for rule in rules if isinstance(rule, dict)]
        if len(ids) != len(rules) or any(not isinstance(rule_id, str) or not rule_id for rule_id in ids):
            errors.append(f"routing-rules.yaml: every {label} entry needs a non-empty id")
        if len(ids) != len(set(ids)):
            errors.append(f"routing-rules.yaml: duplicate {label} IDs")

    for rule in soft_rules if isinstance(soft_rules, list) else []:
        if not isinstance(rule, dict):
            continue
        rule_id = rule.get("id", "<unknown>")
        for key in ("positive_intents", "positive_signals", "required_capabilities", "preferred_agents"):
            values = rule.get(key)
            if duplicate_values(values):
                errors.append(f"{rule_id}: {key} must be a duplicate-free list")
        for agent_id in rule.get("preferred_agents", []):
            if agent_id not in agents:
                errors.append(f"{rule_id}: unknown preferred agent: {agent_id}")
        for capability in rule.get("required_capabilities", []):
            for agent_id in rule.get("preferred_agents", []):
                if capability not in capabilities.get(agent_id, set()):
                    errors.append(f"{rule_id}: {agent_id} lacks required capability: {capability}")
        related = rule.get("related_intents", {})
        if related is not None and not isinstance(related, dict):
            errors.append(f"{rule_id}: related_intents must be a mapping")
        elif isinstance(related, dict):
            for intent, definition in related.items():
                supporting = definition.get("supporting_agents", []) if isinstance(definition, dict) else []
                if duplicate_values(supporting):
                    errors.append(f"{rule_id}: supporting agents for {intent} must be a duplicate-free list")
                for agent_id in supporting:
                    if agent_id not in agents:
                        errors.append(f"{rule_id}: unknown supporting agent: {agent_id}")

    weights = criteria.get("weights", {})
    if not isinstance(weights, dict):
        errors.append("routing-score-criteria.yaml: weights must be a mapping")
    else:
        values = list(weights.values())
        if not all(isinstance(value, (int, float)) and not isinstance(value, bool) for value in values):
            errors.append("routing-score-criteria.yaml: weights must be numeric")
        elif any(value < 0 for value in values):
            errors.append("routing-score-criteria.yaml: weights must be non-negative")
        elif abs(sum(values) - 1.0) > 1e-9:
            errors.append(f"routing-score-criteria.yaml: positive weights must sum to 1.0, found {sum(values):.6f}")

    penalties = criteria.get("penalties", {})
    if not isinstance(penalties, dict):
        errors.append("routing-score-criteria.yaml: penalties must be a mapping")
    else:
        for penalty_id, definition in penalties.items():
            value = definition.get("value") if isinstance(definition, dict) else None
            if not isinstance(value, (int, float)) or isinstance(value, bool) or value < 0:
                errors.append(f"routing-score-criteria.yaml: penalty {penalty_id} must be non-negative")

    thresholds = criteria.get("thresholds", {})
    threshold_values: dict[str, float] = {}
    for threshold_id in ("primary_agent", "supporting_agent", "ambiguous", "reject_below"):
        definition = thresholds.get(threshold_id, {}) if isinstance(thresholds, dict) else {}
        value = definition.get("min_score") if isinstance(definition, dict) else definition
        if not isinstance(value, (int, float)) or isinstance(value, bool) or not 0 <= value <= 1:
            errors.append(f"routing-score-criteria.yaml: threshold {threshold_id} must be between 0 and 1")
        else:
            threshold_values[threshold_id] = float(value)
    if len(threshold_values) == 4 and not (
        threshold_values["primary_agent"] >= threshold_values["supporting_agent"] >= threshold_values["ambiguous"] >= threshold_values["reject_below"]
    ):
        errors.append("routing-score-criteria.yaml: threshold ordering must be primary >= supporting >= ambiguous >= reject")
    margin = criteria.get("ambiguity", {}).get("minimum_primary_margin") if isinstance(criteria.get("ambiguity"), dict) else None
    if not isinstance(margin, (int, float)) or isinstance(margin, bool) or not 0 <= margin <= 1:
        errors.append("routing-score-criteria.yaml: minimum_primary_margin must be between 0 and 1")
    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(f"[ERROR] {error}")
        return 1
    print("[OK] routing rules reference known agents and capabilities")
    print("[OK] routing score weights sum to 1.0")
    print("[OK] routing penalties, thresholds, and ambiguity margin are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
