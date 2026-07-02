# Reasoning Techniques

## Native Reasoning Controls

Use exposed reasoning effort, thinking mode, thinking budget, or adaptive thinking controls instead of asking current reasoning models to reveal step-by-step reasoning.

### When to Use

Use for complex analysis, code review, planning, math, multi-step tool use, and ambiguous decisions on models with native reasoning controls.

### Avoid

Avoid on models/surfaces with no exposed reasoning controls; use concise plan-first prompting instead.

### Models

- OpenAI reasoning/GPT-5 series APIs with reasoning effort
- Claude thinking/effort surfaces where exposed
- Gemini thinking
- DeepSeek V4 thinking mode
- Qwen Thinking where configured

### Avoid For

- Visible chain-of-thought demands
- Low-latency bulk extraction
- Consumer UI surfaces where controls are unavailable

### Surface Notes

API can expose parameters; UI may expose a mode toggle or no control; local Qwen/DeepSeek behavior depends on runner template.

### Failure Modes

- User asks for hidden chain-of-thought.
- Effort set high for cheap classification and cost explodes.
- Reasoning control assumed available in UI when only API supports it.

### Eval Prompt

Compare three variants on 20 reasoning tasks: visible CoT prompt, reasoning-effort parameter with concise rationale, and no reasoning control. Track accuracy, latency, and output-token count.

### Sources

- OpenAI reasoning and prompt engineering docs, 2026-07-02 verification
- Anthropic model capability/tool docs, 2026-07-02 verification
- Google Gemini thinking docs, Prompt 2 verification
- DeepSeek V4/R1 docs, Prompt 2 verification

Last verified: 2026-07-02

---

## Concise Rationale with Hidden Reasoning

Ask the model to reason internally and output only the conclusion plus a short rationale, assumptions, and checks.

### When to Use

Use when the user needs trustable reasoning signals without verbose private reasoning traces.

### Avoid

Avoid when the task requires a full proof, derivation, audit trail, or educational step-by-step solution.

### Models

Most current frontier models; especially native reasoning models.

### Avoid For

- Legacy small models where explicit decomposition materially improves accuracy
- Formal proofs needing full derivation

### Surface Notes

Works in chat UI and API; do not request private chain-of-thought; use explicit sections such as Answer / Rationale / Assumptions / Checks.

### Failure Modes

- Rationale becomes post-hoc rationalization.
- Model hides uncertainty behind polished wording.
- Too short for high-risk decisions.

### Eval Prompt

Ask for answers to ambiguous decision cases; compare rationale-only outputs against full CoT requests for correctness, calibration, and leakage of unsupported claims.

### Sources

- OpenAI reasoning and prompt engineering docs, 2026-07-02 verification
- Prompt 2 model-behavior matrix

Last verified: 2026-07-02

---

## Legacy Chain-of-Thought Fallback

Use explicit stepwise reasoning only for older, weaker, or small/local models where decomposition demonstrably improves task performance.

### When to Use

Use for math, logic, or multi-step tasks on models without native reasoning controls, especially when an eval shows improvement.

### Avoid

Avoid as a universal instruction; avoid with native reasoning models unless asking for an educational explanation rather than hidden reasoning.

### Models

- Small/local instruct models
- Older GPT-style non-reasoning models
- Unverified models after eval

### Avoid For

- OpenAI reasoning models
- Claude extended/adaptive thinking surfaces
- DeepSeek/Qwen thinking modes
- High-volume low-latency calls

### Surface Notes

In UI, prefer "briefly explain" or "show the derivation" only when user-facing explanation is the product. In API, prefer reasoning controls where available.

### Research

- Wei et al. 2022 Chain-of-Thought Prompting
- The Prompt Report, 2024
- OpenAI reasoning-model guidance, 2026-07-02 verification

Evidence grade: A for older CoT literature; B/C for modern model fit.

### Failure Modes

- Token bloat.
- Plausible but wrong reasoning.
- Private reasoning request on surfaces that should not expose it.

### Eval Prompt

Run exact same reasoning set with no scaffold, brief plan-first, and full CoT; keep only if accuracy gain exceeds token/latency cost.

### Snippet

```text
For complex tasks:
- first create a solution plan (briefly),
- then give the final answer.
If speed is needed, think "silently" and output only the result with brief justification.
```

---

## Tree of Thought (ToT)

Force the model to explore multiple reasoning paths simultaneously, evaluate them, and prune unpromising ones.

**When to Apply**: Puzzles, planning, strategic reasoning, combinatorial tasks.

**3-Experts Prompt (Zero-Shot)**:
```text
Imagine three different experts are answering this question. All experts will
write down 1 step of their thinking, then share it with the group. Then all
experts will go on to the next step, etc. If any expert realizes they're wrong
at any point then they leave. The question is...
```

**Research**: Game of 24 — **74% vs 4%** (CoT baseline) (Yao et al., 2023).

---

## Step-Back Prompting

Two-phase: retrieve underlying principles BEFORE solving. Published by Zheng et al. (2023, Google DeepMind, ICLR 2024).

**Gains**: +7% MMLU Physics, +11% Chemistry, +27% TimeQA.

---

## Least-to-Most Prompting

Two-phase decomposition: break into simplest sub-problems, solve sequentially, chain solutions. SCAN benchmark: **16% -> 99%**.

**Key difference from CoT**: Strict phase isolation — decomposition and solving are fully separate.

---

## Self-Consistency

Generate multiple independent reasoning approaches, compare conclusions, select most reliable via consensus.

**Research**: Wang et al. (2022, ICLR 2023): **+3.9% to +17.9%** over standard CoT.

---

## Multi-Agent Debate

Simulate multiple LLM instances debating to converge on better answers.

**Research**: Du et al. (2023, ICML 2024), MIT/Google Brain: **+8% on GSM8K**.

---

## Source-Grounded Verification

Verify factual claims against external or provided sources, not merely against the model's own draft.

### When to Use

Use for factual research, legal/medical/financial-adjacent summaries, model roster updates, citations, and KB maintenance.

### Avoid

Avoid when no source access exists and the task only needs internal consistency; in that case label uncertainty explicitly.

### Models

Any model with web/file/RAG access; especially research agents and API systems with retrieval.

### Avoid For

Closed-book tasks where retrieval is unavailable and citation is required.

### Surface Notes

Deep Research/research agents should cite; API systems should retain source IDs; UI chat should distinguish sourced vs inferred claims.

### Failure Modes

- Model verifies against its own draft.
- Citations do not support the claim.
- Retrieved source is stale or low authority.

### Eval Prompt

Give five claims with mixed true/false/stale support and a small source set; require supported/unsupported/unclear labels with citations.

### Sources

- Chain-of-Verification paper, 2023/2024
- OWASP LLM01 groundedness / output validation guidance, 2025
- Anthropic reduce hallucinations docs, Prompt 3 donor survey

Last verified: 2026-07-02

---

## Single-Response Self-Check

Add a short final check for missing requirements, contradictions, unsupported claims, or format failures before the answer is emitted.

### When to Use

Use for structured outputs, audits, reports, and high-constraint prompts where omissions are common.

### Avoid

Avoid for very short answers or ultra-low-latency tasks.

### Models

General.

### Avoid For

Native reasoning models when implemented as verbose visible reflection; use concise checklist instead.

### Surface Notes

In API, this can be hidden in developer prompt; in UI, ask for a "final compliance check" only when useful to the user.

### Failure Modes

- Checklist becomes ceremonial and misses real errors.
- Adds boilerplate to user-facing output.

### Eval Prompt

Use 10 prompts with hidden format traps; compare omission rate with/without a final compliance checklist.

### Sources

- Reflexion paper lineage
- Existing KB diagnostic framework

Last verified: 2026-07-02
