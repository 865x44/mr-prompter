# Meta-Layer: Principles, Mistakes, Model Cheat Sheet

## Top Principles

1. **Always match technique to model**: Check `avoid_for` in index before applying.
2. **Prefer positive patterns**: "Do X" + example beats "Don't do Y" alone.
3. **Start minimal**: 200-600 token core, expand only for specific failure modes.
4. **Containerize data**: Any user input or document gets `<documents>` or similar wrapper.
5. **Assume injection**: Every prompt that processes external data needs untrusted boundary.
6. **Version and test**: Prompts are engineering artifacts — define success criteria and eval set.
7. **No blind copy-paste**: Adapt every snippet to user's specific task, model, constraints.

## Common Mistakes (Anti-Patterns)

| # | Mistake | Fix |
|---|---------|-----|
| 1 | Instruction-following ambiguity | Add explicit hierarchy, positive patterns |
| 2 | Sycophancy vulnerability | Inject anti-sycophancy module |
| 3 | Missing output format spec | Always specify format with example |
| 4 | Scope creep invitation | Define boundaries, include "what NOT to do" |
| 5 | Safety bypass surface | Mark untrusted data boundaries explicitly |
| 6 | Negation without alternative | "Don't do X" -> "Do Y instead" + example |
| 7 | Over-wide prohibitions | "Do not infer" -> "Infer only from provided text" |
| 8 | AI-isms in output | Negative prompting: ban list + positive replacement |

## Research Foundation

Key peer-reviewed sources behind techniques in this knowledge base:

- **Chain-of-Thought**: Wei et al. (2022), "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models" — https://arxiv.org/abs/2201.11903
- **Tree-of-Thought**: Yao et al. (2023), "Tree of Thoughts: Deliberate Problem Solving with Large Language Models" — Game of 24: 74% vs 4% (CoT baseline)
- **Chain-of-Verification**: Dhuliawala et al. (2023), Meta AI, ACL 2024 — >2x precision, hallucinated entities: 2.95 -> 0.68 per response
- **Reflexion**: Shinn et al. (2023), NeurIPS — significant improvement across 9 LLMs (p < 0.001)
- **Metacognitive Protocol**: Wang et al. (2023), NAACL 2024 — surpassed all baselines on 10 NLU datasets
- **Step-Back Prompting**: Zheng et al. (2023), Google DeepMind, ICLR 2024 — +7% Physics, +11% Chemistry, +27% TimeQA
- **Least-to-Most**: Zhou et al. (2023) — SCAN benchmark: 16% -> 99%
- **Self-Consistency**: Wang et al. (2022), ICLR 2023 — +3.9% to +17.9% over CoT
- **Multi-Agent Debate**: Du et al. (2023), ICML 2024, MIT/Google Brain — +8% on GSM8K
- **The Prompt Report**: Schulhoff et al. (2024) — comprehensive survey of 200+ techniques — https://arxiv.org/abs/2406.06608

Full reference list: 200+ sources available at `ai-prompt-engineering-assistant-guide-reference-urls.md` (Urbans collection).

## Conversational vs Product-Focused Mode

### Conversational Mode
- How most people interact with LLMs daily (ChatGPT, Claude)
- Short, iterative back-and-forth: "Write email" -> "Make it more formal" -> "Add a joke"
- Simple prompts work: "Write email", "Make better" can be effective
- Focus: speed, convenience, interactive refinement

### Product-Focused Mode
- Crafting prompts run thousands/millions of times in a product
- Must be highly optimized and robust — users don't see every output
- Requires rigorous testing, edge-case handling, version control
- Focus: consistency, reliability, performance metrics

**Decision rule**: If the prompt will run >100 times or serve end-users without supervision -> Product-Focused. If one-off or interactive -> Conversational.

## Emergency Response & Troubleshooting

### Common Failure Patterns
- Model ignores instructions or follows wrong ones
- Output format doesn't match specification
- Safety filters trigger on legitimate requests
- Hallucinations in factual sections
- Performance degrades with longer prompts

### Rapid Response Procedure
1. **Identify**: What exactly failed? Instruction ignored? Format wrong? Hallucination?
2. **Isolate**: Which section of the prompt caused it? Remove sections one by one.
3. **Fix**: Apply surgical fix — don't rewrite the whole prompt:
   - Instruction ignored -> Add hierarchy marker, move instruction higher, use XML tags
   - Format wrong -> Add explicit schema example, use JSON mode
   - Hallucination -> Add Chain-of-Verification, constrain to provided data only
   - Safety misfire -> Rephrase without trigger words, add context
4. **Validate**: Test the fix with 2-3 edge cases
5. **Log**: If novel failure -> `python scripts/prompt_engineer.py case --new --slug <pattern>`

### Quick-Fix Cheat Sheet

| Symptom | Immediate Fix |
|---------|---------------|
| Ignores formatting | Add "CRITICAL: Respond ONLY in [format]. No explanation." |
| Too verbose | Add "Max 100 words. No filler." |
| Hallucinates facts | Add "Use ONLY provided documents. If unsure, say 'Not in data'." |
| Inconsistent output | Add 2-3 few-shot examples with exact format |
| Ignores constraints | Move constraints to beginning, wrap in `<constraints>` tags |
| Sycophantic/agreeable | Inject anti-sycophancy module from `references/analytic.md` |

## Model Cheat Sheet Quick Reference

### Claude 4 Sonnet
- Native strength: XML tags. Use `<section>` containers liberally.
- Order: Documents at TOP, query at BOTTOM (up to 30% quality gain).
- Extended thinking: Give high-level goals, NOT step-by-step instructions.
- Default: Concise. Ask explicitly for detail if needed.

### GPT-4.1
- Highest leverage: Few-shot examples with consistent markup.
- Structure: Markdown sections work well.
- Developer message: Use for system rules; user message for task specifics.

### o1 / o3
- CRITICAL: Do NOT add "think step by step" or CoT scaffolding.
- Length: SHORT. They handle reasoning internally.
- Tip: Add `"Formatting re-enabled"` as first line of developer message for markdown output.

### Gemini 2.5 Pro
- Order: Place instructions AFTER data for long contexts.
- Constraints: Avoid negative constraints ("do not X"). State what TO do.
- Temperature: Don't go below 1.0 for reasoning — can cause looping.

### DeepSeek R1
- CRITICAL: NO system message. All instructions in user prompt ONLY.
- CRITICAL: NO few-shot examples — consistently degrades performance.
- Temperature: 0.5-0.7 (0.6 recommended).
- Internal reasoning: Model reasons in `<think>` tags automatically.
- Efficiency hack: "Think step by step, but only keep a minimum draft for each step, 5 words or fewer per step." Cuts tokens ~50%.
