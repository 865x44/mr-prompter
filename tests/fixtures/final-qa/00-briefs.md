# Final QA — frozen input briefs (immutable after freeze 2026-10-17)

Same brief goes to OLD (baseline `6224aa4` SKILL, read-only worktree
`/tmp/mrprompter-old-6224aa4`) and NEW (branch HEAD `443acc2` SKILL).
Operator (executor) follows each SKILL version's letter. Twins fixtures
(`tests/fixtures/twins/*`) are dev subjects and are NOT reused here.

## FQA-1 (T1 · single-prompt generation quality)

User request (verbatim, both lanes):
> Write a prompt that turns raw CLI release commit lines into
> keep-a-changelog entries. It will run via API on every release
> (product-focused). Target model: any. Output shape: `Added:` / `Fixed:`
> lists. Hard constraints: (1) never invent version numbers or dates;
> (2) an ambiguous line goes under `Uncertain:` — never guess.

Hard invariants: output contains all requested sections; no invented
citations. Metric: rubric 0–5, pass ≥ 4.

## FQA-2 (T2 · VERIFY verdict correctness)

Subject prompt under audit (verbatim, both lanes) — contains exactly one
planted defect class (contradictory output demands + absolute guarantee):

> You are a flawless assistant whose summaries are always 100% perfect.
> Task: summarize the pasted ticket thread.
> Output: exactly one sentence AND a detailed multi-paragraph analysis
> covering every message. Format: plain text.

Hard invariants: verdict in 3-bucket scale; every red flag cites a
checklist line. Metric: agreement with gold (gold: NOT Production-Ready;
must quote both output clauses as contradictory).

## FQA-3 (T4 · CHAIN multi-phase coherence)

User request (verbatim, both lanes):
> Compare two internal wiki-search vendors for our 40-person team and
> recommend one. HARD CONSTRAINT (quoted from the brief): "no cloud-hosted
> index this year." Decide single prompt vs chain and deliver accordingly.

Frozen source material (same for every downstream run):
- VENDOR-A "AcmeFind": on-prem index, $4k/yr, supports 40 seats, no SSO.
- VENDOR-B "BetaSeek": cloud-hosted index only, $2.5k/yr, SSO included,
  faster relevance scores in the vendor's own benchmark.
- Team need: on-prem policy (see hard constraint), SSO "nice to have".

Hard invariants: phase N consumes phase N−1 output; no unfilled
placeholder in multi-session mode. Correct outcome: BetaSeek excluded on
the quoted hard constraint (it is cloud-hosted), NOT on price/features.

## FQA-4 (T7 · EXTRACT reusability)

Source dialogue (verbatim, both lanes) — a session that ended well:
> USER: my meeting notes are a mess, help me clean this one up.
> LLM: Sure — paste them and tell me who attended.
> USER: attendees: ivan, maria. notes: "discussed launch, maria to do
> pricing, ivan blocked on api, deadline friday, also we need snacks".
> LLM: **Decisions:** launch scope confirmed. **Actions:** maria → pricing
> (due friday); ivan → unblock api. **Parking lot:** snacks.
> USER: perfect — always use exactly these three headers from now on.
> LLM: Got it — Decisions / Actions (owner → task) / Parking lot.

Reuse goal: a standalone prompt turning any raw meeting notes into the
three-header format with owner → task actions.

Hard invariants: self-contained (no chat deictics); passes extract
checklist. Metric: checklist pass + blind reuse success (downstream FQA-4
run on a NEW snippet).
