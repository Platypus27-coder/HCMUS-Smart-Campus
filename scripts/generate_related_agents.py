"""Generate each agent's local relationship view from the master graph."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
DIRECTORY_PATH = ROOT / "shared" / "agent-directory.yaml"
RELATIONSHIPS_PATH = ROOT / "shared" / "agent-relationships.yaml"
HEADER = """# AUTO-GENERATED FILE
# Source: shared/agent-relationships.yaml
# Do not manually edit.
# Update the canonical relationship graph and regenerate instead.
"""


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"Expected a YAML mapping in {path.relative_to(ROOT)}")
    return data


def agent_folder(agent: dict[str, Any]) -> Path:
    """Return the repository folder for an agent from canonical directory metadata."""
    return ROOT / "subspaces" / agent["subspace"] / agent["id"]


def local_relationships(source: str, graph: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    """Convert source-of-truth edge fields to the local related-agent view."""
    result: list[dict[str, Any]] = []
    for edge in graph.get(source, []):
        result.append(
            {
                "agent": edge["target"],
                "relationship": edge["relationship"],
                "reason": edge["reason"],
                "when_to_use": edge["triggers"],
                "send": edge["send"],
                "do_not_send": edge["do_not_send"],
                "expected_output": edge["expected_output"],
            }
        )
    return result


def render_yaml(payload: dict[str, Any]) -> str:
    body = yaml.safe_dump(
        payload,
        allow_unicode=True,
        sort_keys=False,
        default_flow_style=False,
        width=1000,
    )
    return HEADER + body


def generate() -> list[tuple[str, Path, int]]:
    directory = load_yaml(DIRECTORY_PATH)
    relationship_data = load_yaml(RELATIONSHIPS_PATH)
    agents = directory.get("agents", [])
    graph = relationship_data.get("relationships", {})

    if not isinstance(agents, list) or not isinstance(graph, dict):
        raise ValueError("Agent directory or relationship graph has an invalid top-level structure")

    report: list[tuple[str, Path, int]] = []
    for agent in sorted(agents, key=lambda item: item["id"]):
        folder = agent_folder(agent)
        if not folder.is_dir():
            relative = folder.relative_to(ROOT)
            raise FileNotFoundError(f"Agent folder not found: {relative}")

        output_path = folder / "agent" / "related-agents.yaml"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        local_edges = local_relationships(agent["id"], graph)
        payload = {"current_agent": agent["id"], "related_agents": local_edges}
        output_path.write_text(render_yaml(payload), encoding="utf-8", newline="\n")
        report.append((agent["id"], output_path, len(local_edges)))
    return report


def main() -> int:
    try:
        report = generate()
    except (OSError, ValueError, yaml.YAMLError, KeyError) as error:
        print(f"[ERROR] generation failed: {error}")
        return 1

    print(f"[OK] generated {len(report)} related-agent files")
    for agent_id, output_path, edge_count in report:
        print(f"  {agent_id}: {edge_count} relationship(s) -> {output_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
