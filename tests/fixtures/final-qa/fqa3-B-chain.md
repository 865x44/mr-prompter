# FQA-3 · Lane B — vendor-comparison chain (CHAIN, T4 brief)

> Blind label: **Lane B**. (Mapping sealed in `_blind-map.json`.)

## K justification (deletion test)
- K=1 (single prompt: read blurbs + recommend) fails because the scoring
  step needs a checkable artifact: without a frozen evidence pack, the
  recommendation can silently drift from the vendor facts (the exact
  failure the hard constraint guards against).
- K=3 (evidence → blind-spots → decision) fails the deletion test: the
  blind-spot pass restates P1 facts without a consumer — P2 already scores
  migration/admin/exit explicitly. Deleted.
- **K=2**: P1 evidence pack (criteria + quoted vendor facts) → P2 scored
  decision consuming exactly that pack. No phase without a consumer.

## P1 — Evidence pack (authoring contract)
Consumes: the two frozen vendor blurbs (pasted below). Produces HANDOFF E1:
criteria table (cost/yr, deployment model, seats, SSO, admin load) with
every cell QUOTED from the blurbs, plus Q1: the verbatim hard constraint.
Completion: every criterion has a quote or is marked UNKNOWN. Failure:
any recommendation, ranking, or unquoted cell in P1 output.

```
Extract a criteria table for AcmeFind vs BetaSeek: price/yr, deployment
model (on-prem vs cloud — quote the exact words), seats, SSO, admin load.
Every cell = verbatim quote or UNKNOWN. Then quote the hard constraint
from the brief. No recommendation. No ranking.

<vendors>
VENDOR-A "AcmeFind": on-prem index, $4k/yr, supports 40 seats, no SSO.
VENDOR-B "BetaSeek": cloud-hosted index only, $2.5k/yr, SSO included.
Team: 40 people. HARD CONSTRAINT: "no cloud-hosted index this year."
SSO is nice-to-have.
</vendors>
```
HANDOFF E1: criteria table + quoted constraint.

## P2 — Scored decision (authoring contract)
Consumes: HANDOFF E1 only. Produces: 1–5 scores per criterion, exclusion
check against the quoted constraint FIRST, one recommendation, decisive
reason, 2 follow-ups. USES: E1. Completion: exclusion check cites the
quoted constraint before any scoring. Failure: recommending a vendor the
constraint excludes.

```
From evidence pack E1 (pasted below): FIRST apply the quoted hard
constraint as an exclusion filter and say which vendor it excludes.
Then score the remaining vendor(s) 1–5 on cost / deployment fit /
admin load, recommend one with the single decisive reason, and list 2
follow-up questions. If the constraint excludes every vendor, say so
instead of recommending.

[PASTE E1 HERE]
```

## Semantic preflight (before delivery)
- Information loss: P2 consumes all E1 cells (scores touch every row);
  nothing silently dropped — no blind-spot phase needed.
- Premature convergence: P1 contains no ranking, so P2 cannot inherit one.
- Fake verification: no external benchmark is cited as proof; the vendor's
  own relevance claim is scored as vendor-claim, not evidence.

## Fusion handoff
Authoring pack complete: K=2 justified above; per-step contracts with
completion/failure tests; no judge/repair loop requested.
