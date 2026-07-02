# System Techniques

## Surface-Aware Model Rules

Route every technique through model family, model ID/snapshot, and surface before recommending it.

### When to Use

Use whenever a card mentions model behavior, instruction hierarchy, tool use, context window, or reasoning controls.

### Avoid

Avoid treating this as a model leaderboard; it is a compatibility layer, not a benchmark.

### Model Notes

- **API**: supports explicit roles, parameters, tools, and reasoning controls.
- **Consumer UI**: may hide system/developer controls or expose them as mode toggles.
- **Deep Research / coding agents**: add orchestration layers that change effective behavior.
- **Local runners**: vary by template, quantization, and snapshot.

### Surface Notes

- API supports explicit roles/params/tools.
- Consumer UI may hide system/developer controls.
- Deep Research and coding agents add orchestration.
- Local runners vary by template and quantization.

### Failure Modes

- Static model cheat sheet survives in another file.
- API advice is applied to UI or local runner.
- Model alias/deprecation is missed.

### Eval Prompt

Run the same prompt in API, chat UI, coding agent, and local runner; score format adherence, instruction priority, tool behavior, and token cost.

### Sources

- OpenAI Prompt Engineering docs, 2026-07-02 verification
- Anthropic Claude Platform docs, 2026-07-02 verification
- Google Gemini API docs, 2026-07-02 verification
- DeepSeek API docs, 2026-07-02 verification

Last verified: 2026-07-02

## Instruction Mechanics

### "Because" Causality Connector
Linking instructions with "because" activates more complex neural pathways for logic processing.

### Parenthetical Clarification Priority
Parenthetical remarks are interpreted as high-priority clarifications. Double parentheses further amplify importance: `((essential in two sentences))`.

### If/When Verb Switching
Replace "if" with "when" to increase instruction confidence. "When" is a statement of fact; "if" is background noise.

## Mode Patterns

### Skeptic Mode / Devil's Advocate
Three-phase self-critique: generate -> critique -> rewrite with critique incorporated.

### Constitutional Self-Critique
Skeptic Mode with explicit principles. Model generates a response, critiques it against a defined list, then rewrites.


## Few-Shot Specialization

Use examples only for a defined purpose: format, behavior, counterexample, edge case, or eval fixture.

### When to Use

Use for extraction, classification, style control, formatting, and edge-case disambiguation.

### Avoid

Avoid as a universal default; avoid examples that bias reasoning search or conflict with instructions.

### Models

General; especially GPT-style explicit-instruction models and smaller extraction models. Needs eval for reasoning models.

### Avoid For

- Native reasoning tasks where examples cause anchoring
- DeepSeek/Qwen local runners without testing
- Low-context budgets

### Surface Notes

API: keep examples in developer/instructions or input schema as appropriate. UI: concise examples. Agent harness: examples can be selected by retrieval.

### Failure Modes

- Examples override task.
- All examples are easy/positive; edge cases fail.
- Examples consume context that should hold source data.

### Eval Prompt

Run zero-shot, format-shot, behavior-shot, and counterexample-shot on 20 extraction cases; compare accuracy and schema adherence.

### Sources

- The Prompt Report, 2024
- OpenAI prompt engineering docs, examples guidance
- Google Gemini prompting guidance, Prompt 3 donor survey

Last verified: 2026-07-02
