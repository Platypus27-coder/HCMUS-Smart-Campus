# 🎓 HCMUS Smart Campus
## AI University Life Hub

> **One Campus. One AI Gateway. Every Student Service.**

**HCMUS Smart Campus** is a student-built AI Agent Space prototype developed for the  
**2026 Global AI Agent Competition – Track A: Agent Building Competition** on the **Wesome AI** platform.

The project explores how a university can organize academic services, student support, administration, research assistance, and personal development into a unified multi-agent campus experience.

---

## 🏆 Competition

- **Competition:** 2026 Global AI Agent Competition
- **Track:** Track A – Agent Building Competition
- **Platform:** Wesome AI
- **Project:** HCMUS Smart Campus – AI University Life Hub
- **Domain:** Education & Lifelong Learning
- **Target Environment:** University / Smart Campus

Track A evaluates a complete **Agent Workspace** containing multiple independently usable Agents.  
The project is therefore organized as one Main Space with multiple functional Sub-spaces and specialized Agents.

---

## 💡 Project Overview

University information and services are often distributed across multiple channels such as:

- Academic affairs
- Student services
- University regulations
- Scholarships
- Library resources
- Clubs and activities
- Administrative procedures
- Teaching and research support
- Student well-being and personal development

HCMUS Smart Campus proposes a unified AI gateway where users can access these services through specialized Agents.

Conceptually:

```text
User Request
    ↓
Campus Router
    ↓
Specialized Agents
    ↓
Campus Aggregator
    ↓
Unified Response / Action Plan
```

The goal is not to replace official university departments, but to demonstrate how an AI-native university service layer could make campus information easier to access and navigate.

---

## 🏫 Space Architecture

```text
HCMUS SMART CAMPUS
│
├── 01. Academic & Training
│   ├── Schedule & Deadline Agent
│   ├── GPA & Academic Standing Agent
│   └── Academic Advisor Agent
│
├── 02. Student Services
│   ├── Scholarship Matching Agent
│   ├── Library Research Agent
│   └── Clubs & Activities Agent
│
├── 03. Administration & One-stop Services
│   ├── Administrative Procedure Agent
│   ├── Regulation Q&A Agent
│   └── Department Contact Agent
│
├── 04. Teaching & Research
│   ├── Teaching Material Assistant
│   ├── Research Assistant
│   └── Class Support Agent
│
├── 05. Student Life & Development
│   ├── Student Well-being Agent
│   └── Soft Skills Coach Agent
│
└── 06. Central Orchestration
    ├── Campus Router Agent
    └── Campus Aggregator Agent
```

---

## 📁 Repository Purpose

This repository is used to store and organize all resources required to build the Agents and Spaces on Wesome AI.

The repository mirrors the competition package structure shown in the official Agent Space setup materials.

Each Agent is stored independently so that its:

- Role information
- Q&A data
- Knowledge base
- Background assets
- Menu resources
- Space resources

can be managed separately.

---

## 🗂️ Repository Structure

```text
HCMUS-Smart-Campus/
│
├── README.md
│
├── main-space/
│   ├── info.docx
│   ├── agent/
│   ├── menu/
│   │   ├── pic/
│   │   ├── file/
│   │   ├── video/
│   │   └── url/
│   └── space/
│
├── subspaces/
│   │
│   ├── 01-academic-training/
│   │   ├── schedule-deadline-agent/
│   │   ├── gpa-academic-standing-agent/
│   │   └── academic-advisor-agent/
│   │
│   ├── 02-student-services/
│   │   ├── scholarship-matching-agent/
│   │   ├── library-research-agent/
│   │   └── clubs-activities-agent/
│   │
│   ├── 03-administration-one-stop/
│   │   ├── administrative-procedure-agent/
│   │   ├── regulation-qa-agent/
│   │   └── department-contact-agent/
│   │
│   ├── 04-teaching-research/
│   │   ├── teaching-material-assistant/
│   │   ├── research-assistant-agent/
│   │   └── class-support-agent/
│   │
│   ├── 05-student-life-development/
│   │   ├── student-wellbeing-agent/
│   │   └── soft-skills-coach-agent/
│   │
│   └── 06-central-orchestration/
│       ├── campus-router-agent/
│       └── campus-aggregator-agent/
│
└── template/
    └── agent-template/
        ├── info.docx
        ├── agent/
        │   ├── QA.xlsx
        │   ├── knowledge.docx
        │   └── background.png
        ├── menu/
        │   ├── pic/
        │   ├── file/
        │   ├── video/
        │   └── url/
        └── space/
```

---

## 🤖 Standard Agent Package

Every Agent follows the same package structure:

```text
agent-name/
├── info.docx
│
├── agent/
│   ├── QA.xlsx
│   ├── knowledge.docx
│   └── background.png
│
├── menu/
│   ├── pic/
│   ├── file/
│   ├── video/
│   └── url/
│
└── space/
```

### `info.docx`

Stores the Agent's general information, such as:

- Agent name
- Sub-space
- Role
- Target users
- Main responsibilities
- Communication style
- Capabilities
- Knowledge scope
- Limitations / boundaries

### `agent/`

Contains the core Agent resources.

```text
agent/
├── QA.xlsx
├── knowledge.docx
└── background.png
```

- **QA.xlsx** — Question & Answer dataset
- **knowledge.docx** — Main knowledge material
- **background.png** — Agent / room background asset

### `menu/`

Contains resources displayed or linked through the Agent menu.

```text
menu/
├── pic/
├── file/
├── video/
└── url/
```

- **pic/** — Images and visual materials
- **file/** — Documents and downloadable resources
- **video/** — Video materials
- **url/** — External reference links

### `space/`

Contains assets or configuration materials related to the Agent's Space / Room.

---

## 🧩 Sub-space Organization

Agents are grouped by functional Sub-space.

```text
subspaces/
└── 02-student-services/
    ├── scholarship-matching-agent/
    ├── library-research-agent/
    └── clubs-activities-agent/
```

Each Agent keeps its own knowledge and supporting resources instead of sharing a single duplicated knowledge package across the entire project.

This makes the repository easier to maintain and keeps each Agent independently understandable and usable.

---

## 🧱 Agent Template

The `template/agent-template/` directory is used as the starting point for every new Agent.

```text
template/
└── agent-template/
    ├── info.docx
    ├── agent/
    │   ├── QA.xlsx
    │   ├── knowledge.docx
    │   └── background.png
    ├── menu/
    │   ├── pic/
    │   ├── file/
    │   ├── video/
    │   └── url/
    └── space/
```

When creating a new Agent, copy this directory into the appropriate Sub-space and rename it using the Agent name.

Example:

```bash
cp -r template/agent-template \
subspaces/02-student-services/scholarship-matching-agent
```

---

## 🔗 Agent Coordination Artifacts

The repository contains coordination metadata that prepares the agent packages for a future orchestration runtime. These files do **not** mean that Router, Aggregator, inter-agent calls, persistent memory, or Wesome AI integration are already implemented.

```text
shared/agent-directory.yaml
    Global directory of all agents. Primarily for Campus Router and Campus Aggregator.

shared/agent-relationships.yaml
    Source-of-truth relationship graph: when an agent should use another agent,
    minimum context it may send, prohibited fields, and expected output.

shared/routing-rules.yaml
    Hard/soft candidate-generation rules for a future Router.

shared/routing-score-criteria.yaml
    Baseline deterministic scoring, thresholds, penalties, and ambiguity policy.

<agent>/agent/related-agents.yaml
    Generated local view of only that agent's outgoing relationships.

shared/handoff-protocol.md
    Standard handoff and response contract.

shared/user-profile.schema.json
    Schema for consent-aware runtime user context; it does not store real users.

shared/user-memory-policy.md
    Rules for handling user context and sharing it safely.

AGENT_FOR_REPO.md
    Tool-neutral working rules for Codex, Claude Code, Cursor, Copilot, and other coding agents.
```

Generate local relationship views after editing the source-of-truth graph:

```bash
python scripts/generate_related_agents.py
```

Validate source metadata and generated files:

```bash
python scripts/validate_agent_graph.py
python scripts/validate_routing_rules.py
python scripts/validate_user_schema.py
python scripts/simulate_routing.py examples/routing/single-intent.example.json
python -m unittest discover -s tests
```

`examples/runtime/profile-summary.example.json` is clearly labelled by its path as demo-only data. Do not commit real runtime profiles; common runtime profile paths are ignored by Git.

---

## 📝 Naming Convention

Use lowercase **kebab-case** for folders.

Examples:

```text
schedule-deadline-agent
academic-advisor-agent
scholarship-matching-agent
student-wellbeing-agent
campus-router-agent
```

Sub-spaces use numeric prefixes to keep their order stable:

```text
01-academic-training
02-student-services
03-administration-one-stop
04-teaching-research
05-student-life-development
06-central-orchestration
```

Avoid names such as:

```text
agent1
agent-final
agent-new
agent-v2-final
```

---

## 🔄 Recommended Team Workflow

1. Select the target Sub-space.
2. Copy the Agent template.
3. Complete `info.docx`.
4. Prepare the Agent knowledge base.
5. Build the Q&A dataset.
6. Prepare images, files, videos, and URLs.
7. Upload and configure the Agent on Wesome AI.
8. Test the Agent independently.
9. Add the Agent to its corresponding Space / Sub-space.
10. Commit the final package to this repository.

---

## 🌐 Wesome AI Mapping

```text
Repository                     Wesome AI

main-space/                 →  Main Agent Space
subspaces/                  →  Functional Sub-spaces
agent-name/                 →  AI Agent
info.docx                   →  Agent information / role configuration
agent/QA.xlsx               →  Q&A knowledge
agent/knowledge.docx        →  Knowledge base
agent/background.png        →  Background asset
menu/pic/                   →  Image resources
menu/file/                  →  File resources
menu/video/                 →  Video resources
menu/url/                   →  External links
space/                      →  Space / Room resources
```

---

## ⚠️ Disclaimer

**HCMUS Smart Campus** is a student-built prototype created for competition and educational purposes.

It is **not an official information system of the University of Science, VNU-HCM (HCMUS)** and does not represent an official service provided by the university.

Publicly available university information may be used as reference material.

Private student records, restricted university systems, and personal academic data are not accessed unless explicit authorization is available.

Synthetic or demonstration data should be used whenever private real-world data cannot be legally or appropriately accessed.

---

## 📌 Project Status

🚧 **In Development**

The Agent packages, knowledge bases, media resources, and Space configurations are being developed and refined for the competition submission.

---

## 📄 License

This repository is intended primarily for educational and competition purposes.

Third-party documents, images, videos, and external resources remain subject to their respective licenses and usage policies.
