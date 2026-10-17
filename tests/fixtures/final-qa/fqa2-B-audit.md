# FQA-2 · Lane B — audit report (VERIFY, T2 subject)

> Blind label: **Lane B**. (Mapping sealed in `_blind-map.json`.)

## Security Assessment
- No injection vectors: subject processes pasted ticket threads (first-party
  data assumed); no exfiltration instruction present.
- Note: "flawless / 100% perfect" self-claim lowers user skepticism — a
  trust-surface issue worth one warning.

## Audit Score
- Manual: **8/10** dimensions passed (warnings: D7 examples absent, D8 tone
  contract implicit only).
- Automated (`prompt_engineer.py verify`, baseline build): **8/10,
  0 critical → PRODUCTION-READY**.
- Overall verdict: **Needs Fixes** (automation passes; manual review escalates
  on the output-clause conflict below).

## Top Issues
1. (Critical) Contradictory output demands — "Output: exactly one sentence
   AND a detailed multi-paragraph analysis covering every message." A model
   cannot satisfy both; one clause will be silently violated on every run.
2. (Warning) Unverifiable self-guarantee — "a flawless assistant whose
   summaries are always 100% perfect" promises infallibility; sets no
   uncertainty behavior.
3. (Info) No failure/uncertainty behavior for empty or contradictory threads.

## Suggested Fixes
- Before: "Output: exactly one sentence AND a detailed multi-paragraph
  analysis covering every message."
- After: "Output: one shape per request — a single sentence when asked for a
  confirmation; a short multi-paragraph analysis when asked for coverage.
  Never both in one answer."
- Before: "a flawless assistant whose summaries are always 100% perfect".
- After: remove; add "If a message is ambiguous, quote it and mark the
  summary tentative."
- KB: `negative-prompting` (negation with alternative), output-schema
  discipline.

## Model-Fit Analysis
- Prompt is model-agnostic short-form; no CoT scaffolding present (good for
  o-series/R1 targets). No model switch recommended; the defect is
  model-independent.

## Clarifying Questions
1. Who consumes the summary — triage rotation or audit trail?
2. Should long threads be truncated or chunked at some message count?
3. Have you seen the model pick the wrong output shape in practice?

## Memory Integration
- Should I track this single-vs-full summary pattern for future audits?
- Want me to remember your team's plain-text-only style preference?
