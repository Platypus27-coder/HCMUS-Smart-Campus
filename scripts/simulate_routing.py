"""Run deterministic routing-metadata simulations; this is not a production semantic router."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"Expected a YAML mapping in {path.relative_to(ROOT)}")
    return data


def load_input(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("Simulation input must be a JSON object")
    for field in ("detected_intents", "signals", "available_context"):
        if not isinstance(data.get(field, []), list):
            raise ValueError(f"Simulation input field '{field}' must be a list")
    return data


def ratio(available: set[str], requested: list[str]) -> float:
    if not requested:
        return 1.0
    return sum(value in available for value in requested) / len(requested)


def normalize(values: list[Any]) -> set[str]:
    return {str(value).casefold() for value in values}


def hard_rule_results(hard_rules: list[dict[str, Any]], requested_capabilities: set[str]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for rule in hard_rules:
        unavailable = set(rule.get("condition", {}).get("unavailable_capabilities", []))
        prohibited = sorted(requested_capabilities & unavailable)
        results.append(
            {
                "id": rule["id"],
                "action": rule["action"],
                "status": "blocked" if prohibited else "passed",
                "blocked_capabilities": prohibited,
            }
        )
    return results


def simulate(payload: dict[str, Any]) -> dict[str, Any]:
    directory = load_yaml(ROOT / "shared" / "agent-directory.yaml")
    rules_data = load_yaml(ROOT / "shared" / "routing-rules.yaml")
    criteria = load_yaml(ROOT / "shared" / "routing-score-criteria.yaml")
    agents = {agent["id"]: agent for agent in directory["agents"]}
    intents = set(payload.get("detected_intents", []))
    signals = normalize(payload.get("signals", []))
    context = set(payload.get("available_context", []))
    requested_capabilities = set(payload.get("requested_capabilities", []))
    hard_results = hard_rule_results(rules_data["hard_rules"], requested_capabilities)
    blocked = any(result["status"] == "blocked" for result in hard_results)

    weights = criteria["weights"]
    score_min = float(criteria["score_range"]["min"])
    score_max = float(criteria["score_range"]["max"])
    candidates: list[dict[str, Any]] = []
    for rule in rules_data["soft_rules"]:
        matching_intents = sorted(intents & set(rule["positive_intents"]))
        if not matching_intents:
            continue
        rule_signal_set = normalize(rule["positive_signals"])
        signal_match = 1.0 if signals & rule_signal_set else 0.0
        context_match = ratio(context, rule.get("context_fields", []))
        for agent_id in rule["preferred_agents"]:
            agent = agents[agent_id]
            capability_match = 1.0 if set(rule["required_capabilities"]).issubset(set(agent["capabilities"])) else 0.0
            components = {
                "intent_match": 1.0,
                "capability_match": capability_match,
                "semantic_signal_match": signal_match,
                "context_match": context_match,
                "relationship_relevance": 1.0,
                "input_availability": context_match,
            }
            penalties: dict[str, float] = {}
            if capability_match == 0:
                penalties["missing_required_capability"] = float(criteria["penalties"]["missing_required_capability"]["value"])
            weighted = sum(weights[name] * value for name, value in components.items())
            final_score = max(score_min, min(score_max, weighted - sum(penalties.values())))
            candidates.append(
                {
                    "id": agent_id,
                    "rule": rule["id"],
                    "matched_intents": matching_intents,
                    "components": components,
                    "weighted_score": round(weighted, 3),
                    "penalties": penalties,
                    "final_score": round(final_score, 3),
                }
            )

    candidates.sort(key=lambda item: (-item["final_score"], item["id"]))
    thresholds = criteria["thresholds"]
    primary_cutoff = float(thresholds["primary_agent"]["min_score"])
    supporting_cutoff = float(thresholds["supporting_agent"]["min_score"])
    ambiguous_cutoff = float(thresholds["ambiguous"]["min_score"])
    primary = [candidate for candidate in candidates if candidate["final_score"] >= primary_cutoff]
    supporting = [candidate for candidate in candidates if supporting_cutoff <= candidate["final_score"] < primary_cutoff]
    weak = [candidate for candidate in candidates if ambiguous_cutoff <= candidate["final_score"] < supporting_cutoff]
    discarded = [candidate for candidate in candidates if candidate["final_score"] < ambiguous_cutoff]

    clarification_reason: str | None = None
    if blocked:
        clarification_reason = "A hard rule prohibited one or more requested unavailable capabilities."
    elif len(primary) >= 2:
        margin = primary[0]["final_score"] - primary[1]["final_score"]
        true_multi_intent = len(intents) >= 2 and bool(criteria["multi_intent"].get("enabled"))
        if margin < float(criteria["ambiguity"]["minimum_primary_margin"]) and not true_multi_intent:
            clarification_reason = "Top routing candidates are too close for a single detected intent."
            weak = primary + weak
            primary = []

    return {
        "routing_version": "1.0",
        "simulation_notice": "Deterministic metadata test only; not a production semantic router.",
        "detected_intents": sorted(intents),
        "hard_rule_results": hard_results,
        "primary_agents": [
            {"id": item["id"], "score": item["final_score"], "reason": f"Matched {item['rule']}"}
            for item in primary
        ],
        "supporting_agents": [
            {"id": item["id"], "score": item["final_score"], "reason": f"Matched {item['rule']}"}
            for item in supporting
        ],
        "ambiguous_candidates": [{"id": item["id"], "score": item["final_score"]} for item in weak],
        "discarded_agents": [{"id": item["id"], "score": item["final_score"]} for item in discarded],
        "needs_clarification": clarification_reason is not None,
        "clarification_reason": clarification_reason,
        "candidate_scores": candidates,
    }


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python scripts/simulate_routing.py <example-input.json>")
        return 2
    try:
        result = simulate(load_input(Path(sys.argv[1])))
    except (OSError, ValueError, KeyError, json.JSONDecodeError, yaml.YAMLError) as error:
        print(f"[ERROR] simulation failed: {error}")
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
