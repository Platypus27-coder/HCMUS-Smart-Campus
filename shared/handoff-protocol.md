# HCMUS Smart Campus Handoff Protocol

**Version:** 1.0  
**Scope:** coordination metadata only. This protocol does not create a working Router, inter-agent API, persistent memory, RAG pipeline, or Wesome AI integration.

## Purpose

This protocol lets a future orchestration runtime exchange structured work between agents without giving every specialist global knowledge of the 17-agent system (15 specialists, Router, and Aggregator). The authoritative relationship graph is [`agent-relationships.yaml`](agent-relationships.yaml). A specialist consults only its generated `agent/related-agents.yaml`; the Router and Aggregator may consult the global directory and graph.

Routing is a separate concern: `routing-rules.yaml` generates candidates, `routing-score-criteria.yaml` evaluates the baseline deterministic heuristic, and hard rules always run before scoring. A score never overrides a safety or architecture rule.

## Routing result contract

Before preparing handoffs, a future Router should produce an internal result in this shape. `primary_agents` is an array because a genuine multi-intent request can have more than one primary domain.

```json
{
  "routing_version": "1.0",
  "detected_intents": ["scholarship_eligibility", "gpa_evaluation"],
  "primary_agents": [
    {"id": "scholarship-matching-agent", "score": 0.94, "reason": "Primary scholarship intent"}
  ],
  "supporting_agents": [
    {"id": "gpa-academic-standing-agent", "score": 0.81, "reason": "GPA validation required"}
  ],
  "discarded_agents": [],
  "needs_clarification": false,
  "clarification_reason": null
}
```

The conceptual decision order is: hard-rule evaluation → candidate generation → soft-rule matching → scoring → threshold evaluation → ambiguity evaluation → single/multi-agent decision → context filtering → handoff. If the best two single-intent candidates are closer than the configured ambiguity margin, request clarification unless separate intents clearly justify multi-agent routing.

## When to hand off

A handoff is appropriate when one of these conditions is true:

- The request includes an intent outside the current agent's declared capabilities.
- A related agent must calculate, verify, or provide a distinct specialist output.
- The current agent has a relationship-map trigger that matches the request.
- The user explicitly asks for a next step owned by another agent.

A handoff is unnecessary when the current agent can answer fully from its verified knowledge and user-provided context. Do not hand off merely to repeat an answer, obtain a generic opinion, or expose the whole user profile.

## Choosing the target

1. Identify the current agent's matching relationship trigger.
2. Select only the target listed in that relationship.
3. If no local relationship fits, return `unsupported` or ask the Router to determine the target; do not guess an agent name.
4. For a multi-intent request, the Router can create separate handoffs and later provide their responses to the Aggregator.

## Minimum-context and sensitive-data rules

- Include only fields in the relationship's `send` list that are known and necessary for the target task.
- Do not replace missing values with zero, defaults, or assumptions. Omit unknown fields or explicitly list them as missing.
- Respect the `do_not_send` list. Never forward student ID, full transcript, financial records, health details, private credentials, or unrelated personal information unless a future approved design explicitly authorizes it.
- The Router must filter a profile by task requirements before creating a handoff. It must never blindly inject a full profile.
- Institutional facts must come from verified knowledge sources, not user memory or inference.

Context selection is therefore:

```text
User profile → task requirements → allowed fields → minimum relevant context → handoff
```

## Missing data and errors

If a required field is absent, the target must not fabricate it. Return status `needs_user_input` and enumerate the exact missing fields. If the task is outside the target's scope, return `unsupported`. If processing fails, return `error` with a safe, actionable error message and no private data. Partial work is `partial` and must explain what remains uncertain.

Allowed response status values:

```text
success | partial | needs_user_input | unsupported | error
```

## Canonical handoff envelope

```json
{
  "handoff_version": "1.0",
  "from": "scholarship-matching-agent",
  "to": "gpa-academic-standing-agent",
  "reason": "Need GPA projection for scholarship eligibility",
  "user_request": "Original or minimally rewritten user request",
  "context": {
    "current_gpa": 3.25,
    "earned_credits": 65
  },
  "task": {
    "instruction": "Project GPA after next semester"
  },
  "expected_output": [
    "projected_gpa",
    "academic_status"
  ],
  "constraints": [
    "Use only user-provided academic data",
    "Do not assume SIS access"
  ]
}
```

`from`, `to`, and every `expected_output` item must match metadata in the directory/relationship graph. `reason` should identify why the target is needed, rather than restating the entire user request.

## Canonical target response envelope

```json
{
  "response_version": "1.0",
  "agent": "gpa-academic-standing-agent",
  "status": "success",
  "result": {},
  "sources": [],
  "assumptions": [],
  "missing_information": [],
  "limitations": []
}
```

`sources` must identify verified sources when institutional facts are used. `assumptions` and `limitations` must remain visible to the Aggregator. A result based only on user-provided data should say so in `limitations` or `assumptions` where useful.

## Role-specific behavior

### Router

The Router has global awareness of the agent directory and relationship graph. It identifies intent, may split a multi-intent request, and builds one minimum-context envelope per selected target. It does not answer specialist questions as though it had executed them.

For example, for “Tìm học bổng phù hợp với tôi”, the Router should forward only known relevant fields such as `major`, `academic_year`, `current_gpa`, and `earned_credits` to `scholarship-matching-agent`. It must not infer an unknown training score or invent scholarship details.

### Specialist

A specialist uses only its generated local relationship view to decide a normal handoff. It verifies data scope, requests missing fields explicitly, protects prohibited fields, and returns a structured response. It cannot claim a live call to another agent merely because a relationship exists in metadata.

### Aggregator

The Aggregator has global output awareness. It combines completed specialist envelopes into a coherent response, preserves source and limitation information, detects disagreement, and keeps unresolved questions visible. It should normally structure a multi-agent answer as: current status, gap analysis, recommendations/action plan, resources, next actions, and limitations.

## Provenance

Every institutional fact must be marked as either a verified official source or unavailable pending verification. User-confirmed data, official-source facts, agent inference, and recommendations are distinct categories; never present inference or recommendation as an official fact.
