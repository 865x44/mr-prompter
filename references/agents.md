# Tool-Use & Agent Loops

## Agent Retry / Reflection Loop

In an agent harness, run evaluate → diagnose → patch/retry loops using explicit success criteria and state, rather than one-shot self-reflection prose.

### When to Use

Use for code agents, research agents, multi-step tool workflows, and tasks with executable or inspectable outcomes.

### Avoid

Avoid when no external success signal exists or retries would cause side effects without rollback.

### Models

Tool-capable frontier models; coding agents; local agents with tests.

### Avoid For

- Single-shot chat answers
- State-changing tools without sandbox/checkpoint

### Surface Notes

Agent harness should log actions, tool results, errors, retry reason, and diff. UI chat can only approximate this.

### Failure Modes

- Agent loops indefinitely.
- Reflection writes bad memory.
- Retry repeats same failing strategy.

### Eval Prompt

Give a failing unit-test task; compare one-shot fix vs loop with test-run, error diagnosis, and one retry.

### Sources

- Reflexion, Shinn et al. 2023
- OpenAI agent prompting guidance, 2026-07-02 verification
- LangChain context engineering field guide, 2025

Last verified: 2026-07-02

---

## Strategic Prompt Chain

A 4-phase sequential prompt chain for deep topic analysis. Context accumulates across phases.

**Default chain**: Phase 1 (Analytical Perspectives) -> Phase 2 (360 Blind Spots) -> Phase 3 (Distillation)
**Optional**: +Phase 2B (Ecosystem Scout), +Phase 4 (Master Synthesis for multi-AI runs)

### Phase 1 — Analytical Perspectives
Generate 2-4 domain-specific lenses. Each perspective:
- Role = expert who has seen this specific type of failure
- Task = 3 specific questions with named entities
- Cognitive forcing: Step-Back / Adversarial Gate / Formulation Invariance (one per perspective)
- Constraints: FACT/CONCLUSION/HYPOTHESIS labeling, max 250-350 words, no preamble, first word = diagnosis
- Format: Diagnosis -> Q1 -> Q2 -> Q3 -> Three actions

### Phase 2 — 360 Blind Spots
Find what all analysts missed:
1. Hidden assumptions — what did all analyses take for granted?
2. Untouched angles — what aspects were never mentioned?
3. Contradictions between analyses
4. One non-obvious idea — practically applicable right now

### Phase 3 — Distillation
Six-step knowledge extraction:
1. Inventory all ideas from session
2. Thematic map
3. Contradictions (don't resolve — describe)
4. Detailed action plan with horizons (now / this week / later)
5. Open questions
6. Pre-mortem (3 failure reasons visible now)

### Phase 4 — Master Synthesis (multi-AI runs)
Five-step synthesis of multiple AI distillation documents:
1. Consensus map (ideas in 2+ docs = high confidence)
2. Unique findings (only in one doc — often valuable)
3. Contradictions between AIs
4. AI source evaluation
5. Master document (structured like Phase 3)

---

## Agent Loop Rubric and TODO Control

Give long-running agents a small explicit TODO/rubric and require progress checks at meaningful boundaries, not every token.

### When to Use

Use for multi-step coding, research, migration, file editing, and tool workflows where partial completion is likely.

### Avoid

Avoid for one-shot responses or models already managed by an external orchestrator with equivalent state tracking.

### Models

OpenAI/Claude/Gemini/DeepSeek/Grok tool agents; local coding agents.

### Avoid For

Simple extraction/classification.

### Surface Notes

API agent should store TODO state separately; UI chat can show brief progress; coding agents can use checklist files.

### Failure Modes

- TODO list becomes performative.
- Agent keeps going past safe scope.
- Checklist is not updated after tool results.

### Eval Prompt

Give a 7-step repo task with two hidden blockers; compare plain agent vs rubric/TODO agent on missed steps and unnecessary actions.

### Sources

- OpenAI agent prompting guidance, 2026-07-02 verification
- Existing KB DIAGNOSE/VERIFY mode patterns

Last verified: 2026-07-02

---

## Multi-Agent Debate

Simulate multiple LLM instances debating to converge on better answers.

**Research**: Du et al. (2023, ICML 2024), MIT/Google Brain: **+8% on GSM8K**.

---

## Tool Contract Design

Define tools with precise schema, trigger boundary, permission level, error behavior, and expected tool-result format.

### When to Use

Use whenever a model can call functions, web tools, file tools, shell, MCP, browser, or external APIs.

### Avoid

Avoid exposing tools for tasks that can be answered from context or where tool output is untrusted and unvalidated.

### Models

Claude tool use; OpenAI tools/function calling/Agents; Gemini function calling/code execution/search; DeepSeek V4 tools; xAI/Grok tools; local harnesses.

### Avoid For

- Plain chat surfaces without tools
- State-changing tools without approval

### Surface Notes

API tool contracts should be machine-validated; UI tools may be implicit; MCP clients require additional security review.

### Failure Modes

- Ambiguous tool descriptions cause wrong calls.
- Tool result is treated as instruction.
- Tool schema too broad; model gets excess agency.

### Eval Prompt

Give three overlapping tools and one malformed tool result; score correct tool choice, schema validity, and refusal to follow tool-output instructions.

### Sources

- Anthropic Tool Use docs, 2026-07-02 verification
- OpenAI tool/function/agent docs, 2026-07-02 verification
- Google Gemini function calling docs, Prompt 3 donor survey

Last verified: 2026-07-02
