# Memory & State Hygiene

## Context Anchoring

### Silent Absorption ("Read" Mode)
Process information silently without generating responses unless explicit command given.

### Context_Anchor (Re-anchoring every N turns)
Generate 1-3 sentence internal summary of user's core profile, emotional state, and session goal inside `<Context_Anchor>` tag before each response.

### Story Bible + Macro Summary + Micro Context
```text
<STORY_BIBLE> [Character/world constants] </STORY_BIBLE>
<MACRO_SUMMARY> [Chapters 1-4 summary] </MACRO_SUMMARY>
<MICRO_CONTEXT> [Current immediate scene] </MICRO_CONTEXT>
```

## Memory and State Hygiene

Separate durable memory, session scratchpad, task state, user preferences, and stale/archived facts; retrieve only what is relevant to the current task.

### When to Use

Use for project assistants, coding agents, long-running research, personal assistants, and multi-session creative projects.

### Avoid

Avoid for stateless one-off prompts.

### Models

All agent/memory surfaces; local and API harnesses where state can be controlled.

### Avoid For

Automatic memory injection without relevance and staleness checks.

### Surface Notes

UI memory is opaque; custom harnesses should maintain typed stores: procedural, episodic, semantic, task state, exclusions, decisions.

### Failure Modes

- Stale memory overrides current instruction.
- Private/personal context appears unexpectedly.
- Agent writes hallucinated facts into durable memory.

### Eval Prompt

Run a 5-session scenario with changing project constraints; score whether the assistant retrieves current state and ignores archived/stale rules.

### Sources

- Lilian Weng agent memory taxonomy, 2023
- LangChain context engineering, 2025
- A Survey of Context Engineering, 2025

Last verified: 2026-07-02
