# Final QA — authoring judgment (BLIND, Lane A/B only)

Judge: single non-human judge (executor). Status: **provisional**.
Scales are STRICTLY separate (§5 wave brief): structural / semantic /
live success / cost-latency / hard-constraint regressions /
judge selection / fusion. A good-looking chain wins nothing by itself.

Gold references: T1 (sections present, no invented citations, rubric≥4);
T2 (verdict ≠ Production-Ready + both output clauses quoted);
T4 (phase linkage, no unfilled placeholders); T7 (self-contained,
checklist pass).

## Structural pass (new CLI verify on prompt bodies)

| Artifact | Result |
|---|---|
| FQA-1 A | 9/13 Needs Fixes |
| FQA-1 B | 7/13 Needs Fixes |
| FQA-4 A | 8/13 Needs Fixes |
| FQA-4 B | 9/13 Needs Fixes |
| FQA-2 subject (old CLI) | 8/10 PRODUCTION-READY (automation false-pass) |
| FQA-2 subject (new CLI) | 10/13, 1 critical → Needs Fixes |

No artifact hits Production-Ready or Major Rewrite at the structural
layer alone. The FQA-2 automation split (old passes / new flags) is the
sharpest structural difference in the pilot.

## Semantic findings (blind)

- **FQA-1.** Both prompts cover all requested sections, both carry the two
  hard constraints verbatim, neither invents citations. A adds: 5 few-shot
  examples (only the Uncertain behavior is non-obvious — the other four
  restate the declarative shape), 5 clarifying questions, memory-integration
  boilerplate, gain numbers with a soft caveat. B adds: explicit empty-input
  behavior, applicability note with unknowns marked, 1 minimal example, no
  gain numbers. Semantic edge to **B** on token economy (805 vs 1529 chars
  prompt body) with equal constraint coverage; no quality loss observed in A,
  only ritual overhead.
- **FQA-2.** A: automation (L1) already refuses Production-Ready (lexical
  guarantee critical), L2 quotes both output clauses as jointly
  unsatisfiable, verdict Needs Fixes, scoped repair attached. B: automation
  PASSES the subject (8/10 PRODUCTION-READY) and only the manual 10-dim
  layer escalates to Needs Fixes on the clause conflict. Both final verdicts
  match gold. Edge to **A** on defense-in-depth (two layers agree); B's
  automation false-pass is recorded as a weakness of the old build, NOT as
  a wrong final verdict (criterion: final verdict vs gold).
- **FQA-3.** A: default K=3 (2 perspectives + blind spots + distillation),
  no K-justification, no per-step completion tests, placeholders for
  multi-session (acceptable), vendor texts pasted per phase. B: K=2 with an
  explicit deletion test (K=1 loses checkable evidence; K=3's blind-spot
  pass has no consumer), per-step contracts with failure tests, frozen
  vendor data embedded, preflight naming premature-convergence and
  fake-verification risks. Edge to **B** on auditability (every phase has a
  consumer and a failure test); whether K=2 beats K=3 live is decided in
  the downstream arm, not here.
- **FQA-4.** Both self-contained, both pass the extract checklist
  (three-header rule, owner rule, no-invention rule, format example).
  A adds: WHY marks on load-bearing constraints, variable/constant split,
  what-was-removed list, `unvalidated draft` status stated plainly.
  B adds: 3 full examples (session instances retained, heavier), anti-
  patterns, no validation status (reads as proven — it is not). Edge to
  **A** on honesty labeling and token economy.

## Judge selection (authoring only — live outcome pending downstream)

FQA-1: B. FQA-2: A. FQA-3: B (auditability; live TBD). FQA-4: A.
Tally: A-lane 1, B-lane 3 — **provisional, authoring only, n=4, NOT a
superiority claim** (8 tasks ≠ proof; 4 tasks even less so).

## Limitations of this judgment
Single non-human judge; same operator authored both lanes (procedure, not
personnel, was varied); labels alternated per task but the judge held the
map file (weak blinding — recorded honestly). Live task success and
cost-latency scales are filled in `02-downstream-results.md`.
