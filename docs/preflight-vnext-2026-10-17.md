# Preflight vNext — 2026-10-17

Branch: `vnext/preflight-2026-10-17` (from `main@6224aa4`). Sole artifact of this wave.
Downstream pilot NOT run. Authoring smoke probes NOT run (gate W1/W2).

## 1. Verified facts (command → observation)

**P1 baseline.**
`git rev-parse HEAD` → `6224aa472ca867b04b14ea2cbe0d706022160185`. `git status --short --branch` → clean tree on `## vnext/preflight-2026-10-17`, untracked only `docs/salvage-matrix.md`, `docs/salvage-summary.md`, `review/` (preexisting dirt, untouched). `git diff --stat` → empty. `main...origin/main` shows no ahead/behind (upstream == 6224aa4 per wave brief; offline, taken as stated).
`bash scripts/check.sh` → `Ran 17 tests ... OK`, `All checks passed.` (17/17 PASS, reproduced in-wave).

**Canon counts.** `knowledge/index.json`: techniques **39**, categories **10**, files under `references/` **15** (agents, analytic, cases, context, context-engineering, creative, diagnose, evals, extract, memory, meta, models, reasoning, security, system), `research_backed=true` **21**, evidence grades A:21/B:9/C:6/D:3.

**P1 conflicts (stale numbers).** `docs/metrics-contract.md:15-16` still pins `techniques=31`, `research_backed=12` — **STALE vs KB 39/21** (contract predates KB restructure `853aba3`). No other `31` hits in SKILL./scripts/tests (only date `2026-05-31` in prompts archive + historical `.ai/tasks`, `AUDIT_REPORT.md`). SKILL frontmatter/description already say 39 techniques / 21 flags. **Fix direction (recorded, not executed): contract under KB** — update metrics-contract to 39/21, keep `index.json` as single source of truth.
**4 exempt techniques.** `tests/test_prompt_engineer_cli.py:83` exempt set = `{forced-domain-shift, toggle-mode-pattern, injection-defense, progressive-disclosure}`, but only **2 of 4 IDs exist** in index.json (`forced-domain-shift` creative, `progressive-disclosure` context); `toggle-mode-pattern`, `injection-defense` are dead entries. Both existing ones DO have reference sections (`references/creative.md:251`, `references/context-engineering.md:3`) — audit `check_technique_reference_sections` passes with zero missing. **Decision for W0 (recorded, not executed):** delete the 2 dead IDs from the exempt set; keep-or-drop the remaining 2 only if a real gap appears (currently they pass both audit and `get` — `get forced-domain-shift` rc=0). Alternatively give audit an explicit exemption list mirroring the test; owner picks.
**Verdict scale mismatch.** SKILL VERIFY (`SKILL.md:218`) promises `Production-Ready / Needs Fixes / Major Rewrite`; CLI (`scripts/prompt_engineer.py:258-264`) prints `PRODUCTION-READY / NEEDS FIXES before production / GOOD — minor improvements recommended`. Third bucket differs in name and threshold (yellows>2). **Fix only synchronously SKILL+CLI+tests (W0).**
**Placeholders/stale routing.** No TODO/FIXME/lorem/TBD in SKILL.md, references/, index.json (only legitimate `[PASTE PHASE N OUTPUT HERE]` chain placeholders + `agent-loop-rubric-todo` technique, both intentional). 7-mode → reference routing intact (`references/context.md:3` names all 7 modes + 39/21 counts; SKILL mode table + per-mode `Read references/...` directives verified by grep). CLI help exposes `search/get/list/verify/assemble`, consistent with SKILL usage snippets.
**Model rules.** GENERATE asks target model among Claude 4 / GPT-4.1 / o3 / Gemini 2.5 Pro / DeepSeek R1; `references/models.md` matrix covers 8 models incl. R1 1776 / Sonar / Grok 3 — plausible-current, flagged as assumption to re-verify in W1 (see §2).

**P3 live Fusion contract** (`~/.omp/agent/managed-skills/omp-fusion/SKILL.md`, RUNTIME-VERIFIED 2026-10-16, OMP 18.11.0, smoke `smoke-20261016-a` 7/7 §8 PASS; archival PRE-FIX DRAFT ignored). What Fusion demands of a CHAIN pack:
- Sequential release P1..PK per lane, same agent ID continued; step complete only after full output read + immutable snapshot (`local://fusion-<run>-<lane>-s<i>.md`) + manifest (`.json`) saved and structurally gated — only then P(i+1). Blind lanes: no future prompt text in shared files (hashes/IDs only).
- Per-step JSON STEP MANIFEST fields: `step`, `claims[]` (`id,text,support,depends_on,status∈supported|tentative|disputed`), `assumptions[]` (`id,text,status∈accepted|uncertain|revised`), `open_questions[]`, `unique_leads[]`, `invariants[]` (`id,status∈met|violated|unknown,why`). Claim IDs namespaced `<lane>:S<i>:C<n>/A<n>`.
- Run manifest fields: `run_id, goal, released_prompts, future_prompt_ids_or_hashes, invariants, evidence_policy, source_refs, lanes[], steps[], judge_status, decision, missing, warnings`.
- One fresh-context judge (strict JSON schema: `decision∈select|augment|synthesize|preserve_alternatives|insufficient_evidence`, `baseLane, rationale, stepFindings, selectedClaimIds, rejectedClaimIds, unresolved, repairNeeded, finalizationInstructions`); orchestrator validates ID-existence + dependency closure (unknown ID = hard failure); repair OFF by default, max 1 branch, never splice into stale downstream.
- Verified limits: §8.6 manifest-membership only, lane identity from spawn pins; repair/quorum-fail/`preserve_alternatives` NOT runtime-verified.

**P4 anthropics/skills.** `find / -maxdepth 8 -name {prompt-audit,eval-hillclimb,agent-design}.md` → **no hits**; `~/.agents/skills/` has no such files. → **Unavailable; zero new mechanisms absorbed; scope unchanged.** License note: no LICENSE file in repo; upstream GitHub `license:null` per wave brief — no verbatim imports made (this doc contains no upstream text).

**P5 READY reference.** Parent-session READY verdict not separately retrievable from this fresh session; wave-embedded mandatory fixes (§1: canon=39/contract-under-KB, exempt-4 fate, verdict-scale sync) used as authority and recorded above. No verdict invented beyond wave text.

## 2. Assumptions (to re-verify, not facts)
A1. Model matrix currency (A2-model names, context sizes e.g. "Claude 200K") — W1 check.
A2. `origin/main == 6224aa4` taken from wave brief (offline session).
A3. 15 reference files / 58 prompt files / 13 failure patterns countsSpot-checked via contract stats, not independently recounted.

## 3. Changes vs 6224aa4
None. `git diff --stat` empty; only new file is this doc. Untracked dirt preexisting, untouched.

## 4. Baseline
SHA `6224aa4`, `scripts/check.sh` 17/17 PASS (reproduced 2026-10-17, ~3.5s). KB 39/10/15.

## 5. Blockers / open (owner decides, waves do NOT)
B1. Model set + budget for Final QA runs (unresolved product decision).
B2. W0 choice: prune 2 dead exempt IDs vs explicit audit exemption list.
B3. metrics-contract rewrite wording (values fixed: 39/21).
No technical blockers for W0.

## 6. Approved scope + frozen Final QA task list (holdout)

Scope: Wave 0 (contract/exempt/verdict-sync fixes) → W1 authoring gates → W2 Final QA on frozen tasks below → report. No pilot, no SKILL/KB semantic changes beyond W0 fixes, no dep installs.
Holdout: task CASES (inputs/expected judgments) are held by the generator (Primary/owner) and were never shown to this executor; only names, hard invariants and metrics are frozen here.

| # | Task (diverse type) | Hard invariants | Metrics |
|---|---|---|---|
| T1 | Single-prompt generation quality | Output contains all requested sections; no invented citations | Human/LLM-judge rubric 0–5; pass ≥4 |
| T2 | VERIFY verdict correctness | Verdict ∈ 3-bucket scale; every red flag cites a checklist line | Verdict agreement vs gold ≥90% |
| T3 | Adversarial twin discrimination (defective vs near-identical admissible) | Twins differ in exactly the planted defect; judge must split them | Split accuracy 4/4 pairs |
| T4 | CHAIN multi-phase coherence | Phase N consumes Phase N−1 output; no placeholder left unfilled in multi-session mode | Phase-linkage checklist 100% |
| T5 | MODEL SELECT rationale grounding | Recommendation cites matrix row from models.md; no off-matrix model | Grounded-rationale rate 100% |
| T6 | DIAGNOSE taxonomy mapping | Every failure maps to a real pattern code in diagnose.md | Code-precision ≥90% |
| T7 | EXTRACT reusability | Output is self-contained prompt (no chat deictics); passes extract checklist | Checklist pass + blind reuse success |
| T8 | CLI–SKILL consistency (regression) | `check.sh` 17/17 + metrics-contract == KB counts + verdict strings identical | Binary pass/fail |

Frozen 2026-10-17. Any add/drop/reword requires owner approval + new preflight rev.
