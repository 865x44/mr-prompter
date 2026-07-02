# Context Engineering

## Progressive Disclosure

Three-layer context retrieval for agents: Index -> Search -> Deep Dive. Instead of loading all context blindly, the model decides what to fetch at each layer. Result: 35,000 tokens (6% relevant) -> 920 tokens (100% relevant).

```text
Your attention budget is strictly limited. Do NOT ingest all context at once.

LAYER 1 — INDEX: Retrieve compact metadata table of available documents
(ID, Date, Type, Title, Token Count).

LAYER 2 — SEARCH: Based on the index, identify which documents are relevant.

LAYER 3 — DEEP DIVE: Fetch full text ONLY for documents absolutely critical
for the current reasoning step.

ROI RULE: Small items are cheap. Large logs require strong justification.
If in doubt — stay at Layer 2.
```
*Edge case: for static, always-needed context a hybrid preload (partial pre-fetch at Layer 1) may reduce latency.*

## Retrieval and Context Selection

Select the smallest sufficient, relevant, and source-traceable context before generation.

### When to Use

Use for long documents, codebases, KB QA, research, and any task with more candidate context than the model needs.

### Avoid

Avoid when the whole input is tiny and source order is already clear.

### Models

All; mandatory for long-context models when precision matters.

### Avoid For

Marketing demos that equate context window size with reliability.

### Surface Notes

RAG systems should track chunk IDs and source quality; UI workflows should manually list included/excluded files; code agents should use grep/AST/file search before reading everything.

### Failure Modes

- Retriever misses the decisive chunk.
- High-similarity but low-authority chunk dominates.
- Exclusion rule is not propagated.

### Eval Prompt

Inject relevant, irrelevant, contradictory, and excluded chunks; score whether output uses only eligible evidence.

### Sources

- A Survey of Context Engineering for Large Language Models, 2025
- LangChain Context Engineering for Agents, 2025

Last verified: 2026-07-02

---

## Long Context Is Not Usable Context

Treat official context windows as capacity limits, not accuracy guarantees.

### When to Use

Use whenever a prompt uses large files, many docs, long chat history, or 1M-token model claims.

### Avoid

Do not use as an excuse to ignore long-context capabilities; use it to force selection/evals.

### Models

All long-context models.

### Avoid For

None; warning should be universal.

### Surface Notes

API can measure token usage and retrieval ablations; UI users should not assume uploaded files were equally attended.

### Practical Guidance

- Start with a "short contractual core" (200-600 tokens), add only what eliminates specific failure modes.
- As tokens grow, extraction accuracy falls. Prefer a minimal set of high-signal tokens.
- For long-document tasks, place the query after the data only when the selected context is already small and relevant.

### Failure Modes

- Needle/exclusion lost in middle.
- Low-signal context distracts from task.
- Conflicting context produces synthesis sludge.

### Eval Prompt

Place a critical instruction, a contradiction, and an exclusion at different positions in a long pack; score recall and correct exclusion propagation.

### Sources

- A Survey of Context Engineering for Large Language Models, 2025
- Vendor context-window docs from Prompt 2

Last verified: 2026-07-02

---

## Context Engineering: Write / Select / Compress / Isolate

Manage the context window as an engineered working set: write state outside the window, select relevant pieces, compress safely, and isolate context by subtask/tool/agent.

### When to Use

Use for long-running agents, RAG, codebase work, multi-document analysis, and memory-enabled assistants.

### Avoid

Avoid turning it into ceremony for tiny one-shot prompts.

### Models

All long-context and agentic models; especially Claude/Gemini/OpenAI/DeepSeek/Grok large-context APIs and local agents.

### Avoid For

Blind stuffing into 1M context without retrieval/provenance.

### Surface Notes

API/agent harnesses can implement state schemas, retrievers, compaction, and subagents; UI chat usually needs manual summaries and file selection.

### Failure Modes

- Summaries drop exclusions or decisions.
- Retrieval pulls irrelevant stale memory.
- Tool output poisons context.

### Eval Prompt

Give a 100k-token mixed corpus with one exclusion rule and one target answer; compare full stuffing vs selected context vs compressed context.

### Sources

- A Survey of Context Engineering for Large Language Models, arXiv 2025
- LangChain Context Engineering for Agents, 2025-07-02

Last verified: 2026-07-02

---

## Context Compression with Provenance

Compress context only if the summary preserves source links, decisions, exclusions, unresolved questions, and confidence.

### When to Use

Use for long agent loops, research chains, multi-session work, codebase summaries, and handoffs.

### Avoid

Avoid for high-risk domains if source traceability cannot be retained.

### Models

All; especially agent harnesses with compaction.

### Avoid For

Summaries that replace evidence without preserving pointers.

### Surface Notes

Agent harness should store summary plus source map; UI chat should produce handoff packets with "kept/dropped/unknown" fields.

### Failure Modes

- Compression erases the rationale for a decision.
- Old summary carries stale rule forward.
- Citation/source IDs are dropped.

### Eval Prompt

Summarize a 20-turn agent trace with decisions, exclusions, and unresolved items; test whether a new model can continue without violating prior constraints.

### Sources

- LangChain Context Engineering for Agents, 2025
- Agentic Context Engineering, Prompt 3 donor survey

Last verified: 2026-07-02

---

## Tool Retrieval and Overload Control

Retrieve or select only relevant tool descriptions for the current task instead of exposing every available tool.

### When to Use

Use when an agent has many tools, overlapping tools, plugin marketplaces, MCP servers, or large schemas.

### Avoid

Avoid when the agent has a tiny fixed toolset and selection overhead exceeds benefit.

### Models

Tool-using agents across vendors.

### Avoid For

Hard real-time workflows where retrieval adds unacceptable latency.

### Surface Notes

Implement as semantic/keyword retrieval over tool specs plus allowlist by task/permission; log selected vs withheld tools.

### Failure Modes

- Retriever hides the needed tool.
- Similar tools confuse model.
- High-risk tool is retrieved for low-risk task.

### Eval Prompt

Run 30 tool-selection tasks with all tools vs retrieved tools; compare tool-choice accuracy, token use, and unsafe tool exposure.

### Sources

- LangChain Context Engineering for Agents, 2025

Last verified: 2026-07-02
