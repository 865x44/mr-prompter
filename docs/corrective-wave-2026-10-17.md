# Corrective wave — review report (2026-10-17)

Branch `vnext/preflight-2026-10-17`. Planner REQUEST CHANGES accepted;
6 acceptance conditions binding. OMP slices (no Sol-Pi).

## Commits (4, same branch, no push/PR/merge)

| Slice | Commit | Content | Suite |
|---|---|---|---|
| A contradictions | `5c57391` | Gate K1-first (mandates deleted); CLI `Static lint PASS/WARN/FAIL`, Production-Ready forbidden standalone; model notes conditioned (5 groups) + test asserts conditioned form; contract-core→task contract; Onboarding/EXTRACT sync; gains bound to era | 27/27 at commit |
| B Fusion smoke | `352bbf9` | BLOCKED-as-subagent (5 verbatim blockers, no simulation) + human-transfer vs Fusion-ready split + `[PASTE` regression test | 28/28 |
| C semantic probes | `d04b128` | 16/16 pairs: defective findings with body quotes, valid silence with reasons + `test_semantic_probes.py` (4 tests) | 32/32 |
| D evidence repair | `6fb086c` | 3/6 recount (FAILs stay FAIL; thinking-OFF=HYPOTHESIS); real JSON map; `06-k1k2-evidence.md` (raw outputs, quality-gated choice); `07-r4a-trace.md`; `08-smoke-log.md`; CONDITIONAL-GO | 32/32 |
| Live smoke (Primary) | appended to `04-fusion-smoke.md`, UNCOMMITTED at report time — commit with this report | P1→P2 same persistent lane, no substitution, PASS (exclusion + consumption quoted) | 32/32 |

## Per-condition verdict

1. Model-fit executable defaults — PASS. Zero unconditional family rules
   (grep-verified); test asserts conditioned form.
2. Fusion live P1→P2 — PASS (Primary-executed; subagent spawning is
   administratively impossible — recorded, not bypassed).
3. Semantic twins — PASS. 16/16 finding/quote/silence; runner green.
4. FQA evidence — PASS. 3/6 fixed; no retroactive upgrades; live/simulated
   split; JSON parses; K1K2 raw saved.
5. K=1/K=2 terms — PASS. `quality-gated choice`; NOT budget-matched stated.
6. Static-lint statuses — PASS. No bare Production-Ready in CLI/SKILL deliver.

## Honest remainders (P2 debts, not blockers)

- Fusion smoke is n=1 mechanism proof (not order-swap statistics).
- Smoke-log entries marked NON-RERUN (transcribed, not re-executed).
- W0/W1 roughness list intact (system-probe, Few-shot stub, Task-lint).
- Single non-human judge lineage persists from FQA (provisional status kept).

Verdict: CONDITIONAL-GO stands; all P1 defects closed. Ready for planner re-review.
