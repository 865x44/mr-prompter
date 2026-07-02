# Eval & Regression Testing

## Agent Security Eval Harness

Test agents on benign tasks plus malicious direct/indirect prompt injections, scoring both utility and security.

### When to Use

Use before deploying any tool, RAG, browser, email, file, or MCP agent.

### Avoid

Avoid treating a single jailbreak prompt as sufficient security testing.

### Models

All agentic systems.

### Avoid For

None if external data/tools are involved.

### Surface Notes

Harness should include task success, unsafe action rate, over-refusal rate, and logs of retrieved/tool content.

### Failure Modes

- Defense blocks benign tasks.
- Agent succeeds in benign case but fails under injected tool output.
- Eval lacks realistic tool permissions.

### Eval Prompt

Build 10 tasks: 5 benign, 5 with injected tool/web/email content; track utility, unsafe tool calls, and over-defense.

### Sources

- AgentDojo, 2024
- AgentDyn, 2026
- OWASP LLM01:2025

Last verified: 2026-07-02

---

## Prompt-as-Code with Eval Fixtures

Version prompts as artifacts with typed inputs, expected outputs, fixtures, edge cases, and regression checks.

### When to Use

Use for prompts run repeatedly, prompts embedded in products, agent skills, coding workflows, RAG systems, and KB cards.

### Avoid

Avoid heavy process for one-off conversational prompts unless the output is high-risk.

### Models

All; especially API/product prompts.

### Avoid For

Casual chat.

### Surface Notes

API prompts should pin model snapshots where possible; UI prompts should at least keep versioned templates and test examples.

### Failure Modes

- Prompt improves one example and regresses others.
- Model upgrade silently breaks behavior.
- Eval cases are too easy or overfit.

### Eval Prompt

For one KB card, create 5 golden cases and 5 adversarial cases; require pass/fail before changing status to current.

### Sources

- OpenAI prompt engineering docs, 2026-07-02 verification
- Anthropic prompt engineering overview: define success and evals first

Last verified: 2026-07-02

---

## Aggregator Source Policy

Treat PromptingGuide, Learn Prompting, awesome lists, and prompt packs as discovery indexes unless a claim is traced to a primary source or concrete eval.

### When to Use

Use during KB refresh, source audits, and evidence grading.

### Avoid

Avoid using aggregator popularity as evidence.

### Models

N/A.

### Avoid For

research_backed=true decisions.

### Surface Notes

Source ledger must separate lineage: original research, vendor guidance, standard, practitioner note, aggregator, SEO.

### Failure Modes

- Recycled listicle becomes independent evidence.
- License/source lineage unclear.
- Old technique copied without model caveats.

### Eval Prompt

Take 5 popular prompt tips and trace each to a primary source; fail if no source or no eval can be found.

### Sources

- Prompt 3 donor survey

Last verified: 2026-07-02
