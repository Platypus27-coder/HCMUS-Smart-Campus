# User Context and Memory Policy

## Scope

This policy governs future runtime handling of user context. It does not create persistent memory or authorize storage. Runtime user data must never be committed to this repository; `.gitignore` excludes common runtime profile paths.

## Core rules

1. Information stated in one conversation is not automatically permanent memory.
2. Store or reuse user context only after explicit consent and only for the stated purpose.
3. Share only the minimum fields needed for a target agent's task, as defined by `agent-relationships.yaml`.
4. A user can review, correct, or request removal of stored context in a future runtime implementation.
5. Unknown means unknown. `null` is not zero, false, empty, or an invitation to infer a value.
6. Do not forward sensitive or unrelated information during handoff. This includes student IDs, full transcripts, health details, financial records, credentials, and private communications.
7. HCMUS institutional facts must come from verified knowledge sources, not from user profile memory.

## Data labels

Each meaningful datum should be distinguishable by origin:

| Label | Meaning | Example |
|---|---|---|
| `user_confirmed` | The user explicitly supplied or approved it. | `major: Information Technology` |
| `official_source` | It is supported by a verified institutional source. | A cited public procedure document |
| `agent_inference` | It is a reasoned, non-authoritative conclusion. | A possible study-plan risk |
| `recommendation` | It is proposed action, not a fact. | Prepare a document checklist |

Never relabel an inference or recommendation as an official-source fact.

## Examples

### Permitted minimum context

For a GPA simulation, a Router can send `current_gpa`, `earned_credits`, `planned_courses`, and `expected_grades` when the user has provided them. It should not send club interests or a display name.

### Unknown value

If `training_score` is `null`, the Scholarship Matching Agent must say that it needs the score or must qualify its result. It must not treat `null` as `0` or assume eligibility.

### Consent-aware summary

Before a future runtime saves context, it can ask: “Bạn đã cho biết ngành Công nghệ thông tin và GPA 3.25/4. Bạn có muốn lưu các thông tin này để dùng cho lần sau không?” A refusal means the data remains session-only.

### Sensitive wellbeing context

The Student Well-being Agent may use a user's immediate concern to provide support in the current exchange. It must not pass health details to Department Contact Agent merely to find a public contact channel; the handoff should contain only `request_topic` and a preferred contact channel.
