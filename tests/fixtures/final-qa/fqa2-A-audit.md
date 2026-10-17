# FQA-2 · Lane A — audit report (VERIFY, T2 subject)

> Blind label: **Lane A**. (Mapping sealed in `_blind-map.json`.)

## Level 1 — structural/deterministic (CLI, current build)

```
AUDIT RESULT: 10/13 passed — 1 critical, 2 warnings
[WARNING]  Task: explicit instruction or goal present
[WARNING]  Style: explicit tone or voice contract
[CRITICAL] No unverifiable guarantees (never/100%/infallible)
Verdict: Needs Fixes
```

No scores beyond the lint counts above. Automated layer catches the
lexical guarantee; it does NOT adjudicate the clause conflict (lexical
by design).

## Level 2 — semantic review (quote-level findings, no scores)

- **Finding S1 (output-clause contradiction).** The prompt demands both
  "exactly one sentence" AND "a detailed multi-paragraph analysis covering
  every message". Evidence: the single Output sentence contains both
  clauses joined by AND. Either the sentence constraint or the coverage
  constraint fails on every non-trivial thread — this is SAT-unsatisfiable
  as written, not a style preference.
- **Finding S2 (absolute guarantee, confirms L1 critical).** "a flawless
  assistant whose summaries are always 100% perfect" asserts infallibility
  with no uncertainty behavior. If the thread is ambiguous, the model has
  no licensed move except confabulation.
- **Non-finding (explicitly checked, not flagged).** Short length and plain-
  text format are authorial choices for a triage summary, not defects.

## Verdict: Needs Fixes

Not Production-Ready (S1 reproduces on every run — confirmed live in the
downstream arm). Not Major Rewrite (single conflict + guarantee removal
repair it; structure is otherwise sound).

## Suggested repair (scoped, minimal)

> Task: summarize the pasted ticket thread.
> Output: one shape per request — a single sentence for confirmations, a
> short multi-paragraph analysis for coverage requests. Never both at once.
> If a message is ambiguous, quote it and mark the summary tentative.
> Format: plain text.
