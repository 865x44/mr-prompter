# Reasoning Techniques

## Chain of Thought (CoT)

Request model to perform multi-step reasoning. Improves complex reasoning.

**When to Apply**: Math, logic, multi-factor decisions. **Do NOT use** with reasoning models (o1/o3, DeepSeek R1, Claude extended thinking).

**Snippet**:
```text
For complex tasks:
- first create a solution plan (briefly),
- then give the final answer.
If speed is needed, think "silently" and output only the result with brief justification.
```

**Research**: GSM8K: 13% -> 41% (zero-shot). CoT can be plausible but deceptive (Anthropic research).

**Model Notes**:
- Claude: Use `<thinking>` tags or extended thinking mode
- GPT-4o: "Think step by step" works well
- o1/o3, DeepSeek R1: **DO NOT use** — built-in reasoning
- Gemini: Supported; for lower latency use thinking level LOW

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

## Chain of Verification (CoV)

Fact-checking technique: model drafts answer -> plans verification questions -> answers them independently -> revises original.

**When to Apply**: Factual accuracy critical, hallucination-prone domains.

**Snippet**:
```text
STEP 1 — Draft Response: Generate your initial answer.

STEP 2 — Verification Planning: Generate 3-5 specific verification questions
that would confirm or deny the key factual claims.

STEP 3 — Independent Verification: Answer each verification question
independently. Do NOT refer back to your draft answer.

STEP 4 — Final Verified Response: Compare verification answers against your
draft. Remove or correct any claims that were contradicted.
```

**Research**: Dhuliawala et al. (2023), Meta AI: **>2x precision**, hallucinated entities slashed from 2.95 to 0.68 per response.

---

## Reflexion

Self-reflection: model explicitly reviews its own reasoning, detects mistakes, and corrects before final output.

**Snippet**:
```text
Reason through the query inside <thinking> tags, then provide final response
inside <output> tags. If you detect a mistake at any point, correct yourself
inside <reflection> tags.
```

**Research**: Shinn et al. (2023, NeurIPS): general self-reflection significantly improves performance across 9 LLMs (p < 0.001).

---

## Metacognitive Protocol

Five-stage explicit reasoning: comprehend -> preliminary judgment -> critical reflection -> final judgment -> confidence assessment.

**Snippet**:
```text
1. COMPREHEND: Read and interpret. State your understanding explicitly.
2. PRELIMINARY JUDGMENT: First-pass answer.
3. CRITICAL REFLECTION: Could I be interpreting differently? What assumptions? Biases? Alternatives?
4. FINAL JUDGMENT: Synthesize into revised, well-justified answer.
5. CONFIDENCE ASSESSMENT: Rate 0-100% and explain factors.
```

**Research**: Wang et al. (2023), NAACL 2024: peer-reviewed across **10 NLU datasets**, "notably surpassed other prompting baselines."

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

## Reasoning Upgrade Insert

Injection that activates "thinking" mode in weak prompts:
```text
For complex tasks:
- first create a plan (briefly),
- then give the final answer.
If speed is needed, think "silently" and output only result + brief justification.
```

**Avoid with reasoning models** (o1/o3, DeepSeek R1) — they handle reasoning internally.

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
