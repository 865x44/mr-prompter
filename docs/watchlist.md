# Watchlist

Cards and topics that need follow-up evidence, model-refresh, or local evals before promotion to `current`.

## Model/Value Refresh (user-owned donor research)

- **DeepSeek V4 migration** — alias/deprecation behavior, thinking/non-thinking modes, API surface changes.
- **Gemini preview models** — stability of thinking controls, long-context behavior, function calling updates.
- **Local runners** — Qwen, Mistral, Llama default chat templates and quantization effects on prompt behavior.
- **OpenAI GPT-5.5 / GPT-5.6 / o-series** — reasoning-effort surfaces and API behavior changes.
- **Anthropic Fable / Sonnet / Opus / thinking surfaces** — model IDs, effort controls, tool-use behavior.

## Technique Follow-Ups

- **Tool retrieval / overload control** — needs local harness eval.
- **Context compression with provenance** — needs multi-session workflow eval.
- **Native reasoning controls vs concise rationale** — compare across target models.
- **Creative anti-cliché patterns** — needs user writing-pipeline eval.
- **Agent security eval harness** — needs real MCP / OpenCode-style tooling eval.
- **Anti-sycophancy** — operationally important but lacks independent empirical source; retain `watch` until sourced.

## Cadence

- Re-verify model roster and surface-specific advice **monthly** or before any release.
- Re-run target prompts on actual surfaces: API, Chat UI, coding agent, local runner.
- Review `docs/eval-gauntlet.md` fixtures quarterly; promote `watch` cards only after a passing local run.
