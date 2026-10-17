# Model Selection Framework

Dynamic model recommendation for any prompt engineering task.

## Decision Tree

> Defaults, not verdicts: each arrow is a starting hypothesis scoped by the
> version/surface notes below. `unverified` where noted.
```
1. Speed Priority (real-time, casual) -> Sonar / GPT-4o-mini
2. Maximum Reasoning (complex analysis, multi-step) -> Claude 4 Sonnet / o3 / DeepSeek R1
3. Unbiased Analysis (sensitive/controversial topics) -> R1 1776 / Claude 4 Sonnet Thinking
4. Latest Information (research, current events) -> Gemini 2.5 Pro / Perplexity Sonar
5. Creative Excellence (writing, storytelling, art) -> GPT-4.1 / Claude 4 Sonnet
6. Code/Technical (debugging, architecture) -> Claude 4 Sonnet / DeepSeek R1 / o3
7. Experimental/Novel (cutting-edge reasoning) -> Grok 3 / o3
8. Cost Efficiency (high volume, simple tasks) -> Haiku / GPT-4o-mini / DeepSeek V3
```

## Full Comparison Matrix

| Dimension | Claude 4 Sonnet | GPT-4.1 | o3 | Gemini 2.5 Pro | DeepSeek R1 | R1 1776 | Sonar | Grok 3 |
|-----------|-----------------|---------|----|----------------|-------------|---------|-------|--------|
| **Reasoning** | Excellent | Good | Best | Good | Best | Good | Basic | Good |
| **Creativity** | Excellent | Best | Good | Good | Moderate | Moderate | Basic | Good |
| **Code** | Excellent | Good | Best | Good | Best | N/A | Basic | Good |
| **Speed** | Good | Good | Slow | Good | Moderate | Good | **Best** | Good |
| **Context** | 200K | 1M | 200K | 2M+ | 128K | 128K | 128K | 128K |
| **Cost** | Medium | Medium | High | Low | Very Low | Low | Low | Medium |
| **Safety** | Strong | Strong | Strongest | Moderate | Weak | **Unbiased** | Moderate | Weak |
| **Web Search** | No | No | No | Yes | No | No | **Best** | Yes |

## Model-Specific Do's and Don'ts

> Scope: vendor API snapshots as of 2026-07-02 verification (OpenAI / Anthropic /
> Google / DeepSeek platform docs). Chat UIs, coding-agent wrappers, and local
> runners change effective behavior — re-check per surface. Any rule below tagged
> `unverified` is a working heuristic, not a measured fact: do not present it as
guaranteed.

### Claude 4 Sonnet (Default for most tasks; API snapshot 2026-07-02)
- DO: XML tags, explicit data/instruction ordering where appropriate, extended thinking for complex goals (Thinking variants / explicit effort params)
- DON'T: Over-explain, add CoT scaffolding on Thinking variants (built-in reasoning there — `unverified` for non-Thinking snapshots), use negative constraints without alternatives

### GPT-4.1 (Creative + JSON mode; API snapshot 2026-07-02)
- DO: Few-shot examples (highest leverage), Markdown sections, structured JSON output
- DON'T: Rely on system prompt enforcement over conflicting user text (`unverified` — hierarchy behavior is snapshot-dependent), assume it follows complex hierarchies

### o3 (Maximum reasoning; API snapshot 2026-07-02)
- DO: Keep prompts SHORT, let it reason internally
- DON'T: Demand explicit step-by-step reasoning, use few-shot examples, overload with instructions
- `unverified`: "Formatting re-enabled" markdown trick — may help on some snapshots, not a verified rule

### Gemini 2.5 Pro (Latest info + long context; API snapshot 2026-07-02)
- DO: Place instructions AFTER data for long-context API calls, leverage 2M context
- DON'T: Use negative constraints without positive alternatives
- `unverified`: temperature >= 1.0 for reasoning — API-only heuristic, not measured across surfaces; do not go below overall task-appropriate settings blindly

### DeepSeek R1 (Code + cost efficiency; API + common chat templates, 2026-07-02)
- DO: Put task content in the user prompt on surfaces without reliable system roles, let internal reasoning work
- DON'T: Assume system-message support on every surface (API supports roles — check your runner); CoT scaffolding on top of its native reasoning
- `unverified`: "few-shot degrades performance" and fixed temperature 0.5–0.7 — template-dependent heuristics, not benchmarks

### Sonar (Speed + real-time info; Perplexity-hosted, 2026-07-02)
- DO: Quick queries, factual lookups, real-time research
- DON'T: Complex multi-step reasoning, creative writing, sensitive analysis

## When to Combine Models

- **o3 (planner) + GPT-4o (executor)**: Complex project — o3 plans, GPT-4o implements
- **Claude (writer) + Perplexity (research)**: Content creation — research first, then write
- **DeepSeek R1 (code) + Claude (review)**: Code generation — generate with R1, review with Claude
- **Multi-model ensemble**: Critical decisions — run same prompt on 3 models, compare outputs

## Selection Quick Reference

| Task Type | Primary | Alternative |
|-----------|---------|-------------|
| System prompt design | Claude 4 | GPT-4.1 |
| Prompt audit/security | Claude 4 Thinking | R1 1776 |
| Creative writing | GPT-4.1 | Claude 4 |
| Code generation | DeepSeek R1 | Claude 4 / o3 |
| Complex reasoning | o3 | Claude 4 Thinking |
| Current events research | Gemini 2.5 Pro | Sonar |
| High-volume/simple tasks | Sonar | DeepSeek V3 |
| Controversial analysis | R1 1776 | Claude 4 Thinking |

---

## DeepSeek V4 Migration

Track DeepSeek API aliases, thinking/non-thinking modes, and migration from R1-only advice.

### When to Use

Use when selecting DeepSeek models or migrating prompts from R1 to V4.

### Avoid

Avoid hardcoding R1 API defaults; verify current model matrix and alias behavior.

### Models

DeepSeek V4 and newer.

### Surface Notes

API status and deprecation dates change; pin snapshots for production prompts and re-verify quarterly.

### Failure Modes

- Old R1-only advice applied to V4 surfaces.
- Model alias points to a different behavior than expected.
- Thinking/non-thinking mode selection ignored.

### Eval Prompt

Run the same prompt across R1, V4-thinking, and V4-non-thinking; compare format adherence, reasoning depth, and tool behavior.

### Sources

- DeepSeek API docs, Prompt 2 verification
- Current DeepSeek model matrix

Last verified: 2026-07-02
