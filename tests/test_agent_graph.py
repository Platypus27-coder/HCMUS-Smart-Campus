"""Lightweight regression tests for coordination metadata."""

from __future__ import annotations

import copy
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import validate_agent_graph  # noqa: E402
import validate_routing_rules  # noqa: E402
import validate_user_schema  # noqa: E402
import simulate_routing  # noqa: E402


class AgentGraphTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = yaml.safe_load((ROOT / "shared" / "agent-directory.yaml").read_text(encoding="utf-8"))
        self.relationships = yaml.safe_load((ROOT / "shared" / "agent-relationships.yaml").read_text(encoding="utf-8"))

    def validate_modified(self, directory: dict, relationships: dict) -> list[str]:
        with tempfile.TemporaryDirectory() as temporary:
            temporary_root = Path(temporary)
            directory_path = temporary_root / "directory.yaml"
            relationships_path = temporary_root / "relationships.yaml"
            directory_path.write_text(yaml.safe_dump(directory, allow_unicode=True, sort_keys=False), encoding="utf-8")
            relationships_path.write_text(yaml.safe_dump(relationships, allow_unicode=True, sort_keys=False), encoding="utf-8")
            errors, _ = validate_agent_graph.validate_metadata(directory_path, relationships_path)
            return errors

    def test_repository_graph_and_generated_files_are_valid(self) -> None:
        result = subprocess.run(
            [sys.executable, "scripts/validate_agent_graph.py"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_generation_is_deterministic(self) -> None:
        command = [sys.executable, "scripts/generate_related_agents.py"]
        first = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
        target = ROOT / "subspaces" / "02-student-services" / "scholarship-matching-agent" / "agent" / "related-agents.yaml"
        first_content = target.read_text(encoding="utf-8")
        second = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
        self.assertEqual(second.returncode, 0, second.stdout + second.stderr)
        self.assertEqual(first_content, target.read_text(encoding="utf-8"))

    def test_unknown_target_is_rejected(self) -> None:
        relationships = copy.deepcopy(self.relationships)
        relationships["relationships"]["scholarship-matching-agent"][0]["target"] = "unknown-agent"
        errors = self.validate_modified(self.directory, relationships)
        self.assertTrue(any("unknown target" in error for error in errors), errors)

    def test_duplicate_agent_is_rejected(self) -> None:
        directory = copy.deepcopy(self.directory)
        directory["agents"].append(copy.deepcopy(directory["agents"][0]))
        errors = self.validate_modified(directory, self.relationships)
        self.assertTrue(any("duplicate agent IDs" in error for error in errors), errors)

    def test_send_do_not_send_overlap_is_rejected(self) -> None:
        relationships = copy.deepcopy(self.relationships)
        relationships["relationships"]["scholarship-matching-agent"][0]["do_not_send"].append("current_gpa")
        errors = self.validate_modified(self.directory, relationships)
        self.assertTrue(any("both send and do_not_send" in error for error in errors), errors)

    def test_routing_validator_accepts_repository_rules(self) -> None:
        self.assertEqual(validate_routing_rules.validate(), [])

    def test_routing_validator_rejects_bad_weight_sum(self) -> None:
        self.assert_routing_error(
            lambda criteria: criteria["weights"].update({"intent_match": 0.36}),
            "weights must sum",
        )

    def test_routing_validator_rejects_unknown_agent(self) -> None:
        def change(_: dict, rules: dict) -> None:
            rules["soft_rules"][0]["preferred_agents"] = ["unknown-router-target"]

        self.assert_routing_error(change, "unknown preferred agent")

    def test_routing_validator_rejects_invalid_threshold(self) -> None:
        self.assert_routing_error(
            lambda criteria: criteria["thresholds"]["primary_agent"].update({"min_score": 1.1}),
            "threshold primary_agent must be between 0 and 1",
        )

    def assert_routing_error(self, change, expected: str) -> None:
        directory = copy.deepcopy(self.directory)
        rules = yaml.safe_load((ROOT / "shared" / "routing-rules.yaml").read_text(encoding="utf-8"))
        criteria = yaml.safe_load((ROOT / "shared" / "routing-score-criteria.yaml").read_text(encoding="utf-8"))
        try:
            change(criteria)
        except TypeError:
            change(directory, rules)
        with tempfile.TemporaryDirectory() as temporary:
            temporary_root = Path(temporary)
            shared = temporary_root / "shared"
            shared.mkdir()
            (shared / "agent-directory.yaml").write_text(yaml.safe_dump(directory, allow_unicode=True), encoding="utf-8")
            (shared / "routing-rules.yaml").write_text(yaml.safe_dump(rules, allow_unicode=True), encoding="utf-8")
            (shared / "routing-score-criteria.yaml").write_text(yaml.safe_dump(criteria, allow_unicode=True), encoding="utf-8")
            with patch.object(validate_routing_rules, "ROOT", temporary_root):
                errors = validate_routing_rules.validate()
        self.assertTrue(any(expected in error for error in errors), errors)

    def test_user_schema_and_demo_profile_are_valid(self) -> None:
        self.assertEqual(validate_user_schema.validate(), [])

    def test_routing_examples(self) -> None:
        def run_example(name: str) -> dict:
            return simulate_routing.simulate(
                simulate_routing.load_input(ROOT / "examples" / "routing" / name)
            )

        single = run_example("single-intent.example.json")
        self.assertEqual([agent["id"] for agent in single["primary_agents"]], ["gpa-academic-standing-agent"])

        multi = run_example("multi-intent.example.json")
        self.assertEqual(
            {agent["id"] for agent in multi["primary_agents"]},
            {"scholarship-matching-agent", "gpa-academic-standing-agent", "academic-advisor-agent"},
        )

        ambiguous = run_example("ambiguous.example.json")
        self.assertTrue(ambiguous["needs_clarification"])
        self.assertEqual(ambiguous["primary_agents"], [])


if __name__ == "__main__":
    unittest.main()
