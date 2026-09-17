# HCMUS Smart Campus Repository Instructions

## Project Overview

HCMUS Smart Campus – AI University Life Hub is a multi-agent university-life support prototype. The repository stores agent packages, verified knowledge resources, and coordination metadata for 6 subspaces and 16 canonical product agents.

## Current Project Status

Metadata and documentation do not prove a runtime feature exists. Do not claim that the repository has a production multi-agent runtime, agent-to-agent API calls, SIS access, private HCMUS data access, persistent memory, database, production RAG, Wesome AI runtime integration, automatic GPA service, scholarship matching engine, semantic router, or message broker unless implementation code proves it.

## Canonical Architecture

The six subspaces are Academic & Training, Student Services, Administration & One-stop Services, Teaching & Research, Student Life & Development, and Central Orchestration. The authoritative list of the 16 agents is `shared/agent-directory.yaml`; use `soft-skills-coach-agent`, never `soft-skill-agent`.

## Sources of Truth

| File | Purpose |
|---|---|
| `shared/agent-directory.yaml` | Canonical product-agent registry. |
| `shared/agent-relationships.yaml` | Canonical static inter-agent relationship graph. |
| `shared/routing-rules.yaml` | Canonical hard/soft routing conditions. |
| `shared/routing-score-criteria.yaml` | Baseline deterministic routing heuristic. |
| `shared/handoff-protocol.md` | Handoff and response contract. |
| `shared/user-profile.schema.json` | Runtime user-context schema. |
| `shared/user-memory-policy.md` | User-context and memory policy. |

`<agent>/agent/related-agents.yaml` is generated from the relationship graph. Never treat it as an independent source of truth.

## Repository Editing Rules

- Inspect relevant existing files before editing and preserve naming conventions and Vietnamese text.
- Avoid duplicate metadata and never use absolute filesystem paths in committed content.
- Use UTF-8 and deterministic serialization.
- After changing relationships, run `python scripts/generate_related_agents.py`.
- After changing metadata, run all relevant validators and available tests.
- Do not delete or rename user content unless explicitly requested and verified safe.

## Institutional Data Guardrails

Never fabricate scholarships, conditions, deadlines, academic regulations, training-score rules, tuition, contacts, phone numbers, opening hours, prerequisite rules, course schedules, or private HCMUS APIs. Use verified sources or explicit placeholders such as `source_url: null`.

## Runtime and User Data Guardrails

Never claim access to SIS, the student/grade portal, private student records, or internal HCMUS databases. Never commit real user profiles. Transfer only task-relevant context, preserve unknown values as unknown, and respect `do_not_send` fields in the relationship graph.

## Definition of Done

A coordination change is complete only when canonical files are internally consistent, generated relationship files are synchronized, validators and relevant tests pass, and no fabricated institutional facts or false runtime claims were introduced.
