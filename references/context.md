# Prompt Engineer Skill — Overview

A production-ready prompt engineering skill. Provides seven modes (**Generate**, **Verify**, **Improve**, **Chain**, **Model Select**, **Diagnose**, **Extract**) backed by **28 techniques**, **13 failure patterns**, **58 ready-to-use prompts**, **6 model profiles**, and **10 research-backed citations**.

## Stats (verified)

- **28 techniques** across reasoning, system, creative, and analytic categories
- **10 research-backed** with explicit citations (CoT: 13% → 41%, ToT: 4% → 74%, CoV: hallucinations ↓80%)
- **58 ready-to-use prompts** (system, task, chain, template, meta)
- **6 model profiles** with platform-specific rules (Claude, GPT-4.1, o3, Gemini, DeepSeek, Sonar)
- **13 failure patterns** for session diagnostics (codes I01-T02)
- **6 session archetypes** (Death by Corrections, Works Once Breaks Twice, Scope Creep Spiral, Format Jenga, The Yes-Man, Ghost Instructions)
- **5 extraction patterns** for capturing successful sessions
- **8 anti-patterns** with fixes
- **Security-first assessment** in every mode

## Knowledge Base Structure

```
references/
  context.md      # Overview, stats, platform rules
  meta.md         # Principles, mistakes, model cheat sheet, emergency fixes
  system.md       # Architecture, hierarchy, safety, injection defense, mode patterns
  reasoning.md    # CoT, ToT, CoV, Reflexion, Metacognition, Strategic Chain
  analytic.md     # Anti-sycophancy, epistemic humility, Socratic, MECE
  creative.md     # Negative prompting, archetypes, entropy, sampling, Neurotexts templates
  cases.md        # Documented failure modes with root cause and fix
  models.md       # Model selection framework, decision tree, comparison matrix
  diagnose.md     # Session diagnostics: analyze conversation logs, find failure points, produce patches
  extract.md      # Extract reusable prompts from successful conversation logs
scripts/
  prompt_engineer.py  # Search, retrieve, verify, assemble CLI
knowledge/
  index.json      # Searchable index of all techniques
```

## Platform Rules (CRITICAL)

| Platform | Key Rule |
|----------|----------|
| **Claude 4 Sonnet** | XML tags natively; documents at TOP, query at BOTTOM (+30% quality). Extended thinking for high-level goals. |
| **GPT-4.1** | Few-shot examples highest-leverage. Markdown sections. |
| **o3** | SHORT prompts only. **NO CoT scaffolding** — built-in reasoning. Add "Formatting re-enabled" for markdown. |
| **Gemini 2.5 Pro** | Instructions AFTER data for long contexts. Avoid negation without alternative. Temperature >= 1.0 for reasoning. |
| **DeepSeek R1** | **NO system message** — user prompt only. **NO few-shot examples** — degrades performance. Temperature 0.5-0.7. Internal reasoning in `<think>`. |

## Model Selection Quick Reference

Read `references/models.md` for full framework. Quick decision tree:

| Need | Go To |
|------|-------|
| Maximum reasoning | Claude 4 Sonnet Thinking, o3, DeepSeek R1 |
| Creative writing | GPT-4.1, Claude 4 Sonnet |
| Code generation | DeepSeek R1, Claude 4 Sonnet, o3 |
| Latest information | Gemini 2.5 Pro, Sonar |
| Speed | Sonar, GPT-4o-mini |
| Unbiased analysis | R1 1776, Claude 4 Sonnet Thinking |
| Cost efficiency | DeepSeek V3, Sonar, Haiku |

## Adjacent Skills

- `text-craft` — for post-processing Russian prose output (word choice, formality, double-negatives, AI-translation fixes).
