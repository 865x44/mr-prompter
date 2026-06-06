# Model Selection Framework

Dynamic model recommendation for any prompt engineering task.

## Decision Tree

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

### Claude 4 Sonnet (Default for most tasks)
- DO: XML tags, documents-at-top-query-at-bottom, extended thinking for complex goals
- DON'T: Over-explain, add CoT scaffolding (it has built-in reasoning), use negative constraints without alternatives

### GPT-4.1 (Best for creative + JSON mode)
- DO: Few-shot examples (highest leverage), Markdown sections, structured JSON output
- DON'T: Rely on system prompt enforcement (weak vs user message), assume it follows complex hierarchies

### o3 (Best for maximum reasoning)
- DO: Keep prompts SHORT, let it reason internally, add "Formatting re-enabled" for markdown
- DON'T: Add explicit "think step by step", use few-shot examples, overload with instructions

### Gemini 2.5 Pro (Best for latest info + long context)
- DO: Place instructions AFTER data, use temperature >= 1.0 for reasoning, leverage 2M context
- DON'T: Use negative constraints without positive alternatives, go below 1.0 temperature

### DeepSeek R1 (Best for code + cost efficiency)
- DO: Put EVERYTHING in user prompt (no system message), temperature 0.5-0.7, let `<think>` tags work
- DON'T: Use system messages, few-shot examples (degrades performance), or CoT scaffolding

### Sonar (Best for speed + real-time info)
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
