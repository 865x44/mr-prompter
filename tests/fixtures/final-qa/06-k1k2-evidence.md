# Final QA — 06 K=1 challenger vs K=2 reference (FQA-3 vendor case)

Case: new prompter recommends K>1 (FQA-3 Lane B: E1 evidence pack → P2
scored decision). Challenger: ONE strong single prompt (K=1) doing the
whole comparison in one call. Budgets were NOT matched (K=1 $0.00096 vs
K=2 $0.00145 — different totals), so this is NOT called budget-matched.
Term: `quality-gated choice`, NEVER Pareto dominance.

Verdict line: K=2 preferred on evidence discipline at higher measured
cost (sub-cent delta buys the quoted-evidence artifact + refusal-to-score
honesty; K=1 fails the no-worse-quality gate despite winning on cost).

## K=1 prompt (compact, verbatim as run, 678 bytes)

```text
Compare two wiki-search vendors for our 40-person team and recommend one. Vendor facts: VENDOR-A "AcmeFind": on-prem index, $4k/yr, supports 40 seats, no SSO. VENDOR-B "BetaSeek": cloud-hosted index only, $2.5k/yr, SSO included. Team: 40 people. HARD CONSTRAINT: "no cloud-hosted index this year." SSO is nice-to-have. FIRST quote the hard constraint and apply it as an exclusion filter, naming which vendor it excludes. Then score each remaining vendor 1-5 on cost / deployment fit / admin load, recommend one with the single decisive reason, and list 2 follow-up questions. Every scored cell must quote the vendor fact or be marked UNKNOWN. Never recommend an excluded vendor.
```

Run: `omp -p <prompt> --no-session --mode json --no-rules --no-skills
--no-extensions --no-title --hide-thinking --no-tools --model
opencode-go/muse-spark-1.3-contributor`; model resolved:
muse-spark-1.3-contributor (preferred tier, reachable; no fallback).

## K=1 verbatim output (full, untrimmed)

```text
"no cloud-hosted index this year."

Exclusion filter: This excludes VENDOR-B "BetaSeek" because it is "cloud-hosted index only".

Remaining vendor scores:

| Vendor | Cost (1-5) | Deployment fit (1-5) | Admin load (1-5) |
|---|---|---|---|
| VENDOR-A "AcmeFind" | 4/5 — "$4k/yr" | 5/5 — "on-prem index" | 2/5 — "no SSO" |

Recommendation: VENDOR-A "AcmeFind"

Decisive reason: It is the only vendor with "on-prem index" that passes the hard constraint.

Follow-up questions:
1. What hardware/ops is needed to run the "on-prem index" for 40 people?
2. Can team accept "no SSO" given SSO is nice-to-have, and what is the manual provisioning plan for "supports 40 seats"?
```

Exclusion verdict: PASS. K=1 quotes the hard constraint verbatim, applies
it FIRST as an exclusion filter, names BetaSeek as excluded ON the
deployment fact (not on price/SSO/features), never recommends the
excluded vendor, recommends AcmeFind with the decisive reason = sole
constraint passer. Matches the K=2 outcome. Difference vs K=2: no frozen
quoted evidence pack, no per-step contracts; single call.

## K=1 telemetry (fresh live run, same model, same BASE flags)

- model arg `opencode-go/muse-spark-1.3-contributor`, resolved
  `muse-spark-1.3-contributor`, stop=stop, no error
- prompt 678 bytes; input 6034 / output 1797 / totalTokens 7944 /
  reasoningTokens 1522 / cacheRead 113
- cost input $0.0006034 + output $0.0003594 = TOTAL $0.000963026
  (provider-reported)
- wall 12.94s (harness-measured, includes spawn/transport), provider
  duration 10441.38ms, ttft 1265.03ms

## K=2 reference — E1 prompt (verbatim, 518 bytes)

```text
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

## K=2 reference — P2 prompt (verbatim, 710 bytes incl. verbatim E1 paste)

```text
From evidence pack E1 (pasted below): FIRST apply the quoted hard
constraint as an exclusion filter and say which vendor it excludes.
Then score the remaining vendor(s) 1–5 on cost / deployment fit /
admin load, recommend one with the single decisive reason, and list 2
follow-up questions. If the constraint excludes every vendor, say so
instead of recommending.

E1 (verbatim, from P1):
| Criterion | AcmeFind | BetaSeek |
|---|---|---|
| price/yr | "$4k/yr" | "$2.5k/yr" |
| deployment model | "on-prem index" | "cloud-hosted index only" |
| seats | "supports 40 seats" | UNKNOWN |
| SSO | "no SSO" | "SSO included" |
| admin load | UNKNOWN | UNKNOWN |

Hard constraint: "no cloud-hosted index this year."
```

## K=2 reference — E1 verbatim output (reused, not re-measured)

```text
| Criterion | AcmeFind | BetaSeek |
|---|---|---|
| price/yr | "$4k/yr" | "$2.5k/yr" |
| deployment model | "on-prem index" | "cloud-hosted index only" |
| seats | "supports 40 seats" | UNKNOWN |
| SSO | "no SSO" | "SSO included" |
| admin load | UNKNOWN | UNKNOWN |

Hard constraint: "no cloud-hosted index this year."
```

## K=2 reference — P2 verbatim output (reused, not re-measured)

```text
Hard constraint as exclusion filter: "no cloud-hosted index this year."

This excludes **BetaSeek** — E1 lists its deployment model as "cloud-hosted index only".

Remaining vendor: **AcmeFind**

Scores for AcmeFind, from E1 only:
- cost: cannot score 1-5 — price is "$4k/yr" but E1 provides no budget threshold to anchor it
- deployment fit: 5/5 — "on-prem index" directly satisfies the hard constraint
- admin load: cannot score 1-5 — listed as UNKNOWN in E1

Recommendation: **AcmeFind** — it is the only vendor that passes the hard constraint.

2 follow-up questions:
1. What is the actual admin load for AcmeFind's on-prem index?
2. Is AcmeFind's "no SSO" acceptable, and is "supports 40 seats" sufficient?
```

## K=2 telemetry (REUSED recorded FQA-3 Lane B runs, same single-tier model; NOT re-measured)

Source: `/tmp/fqa34/B-p1.rec.json` + `/tmp/fqa34/B-p2.rec.json`
(executor-local; provider-reported usage in `turn_end` messages).

- E1 prompt 518 bytes: input 3681 / output 1534 / total 5328 /
  reasoning 1392 / cost $0.000675126 / wall 9.68s / duration 6198.15ms /
  stop=stop
- P2 prompt 710 bytes: input 3724 / output 2029 / total 5866 /
  reasoning 1763 / cost $0.000778426 / wall 11.90s / duration 8943.33ms /
  stop=stop
- K=2 TOTALS: prompt bytes 1228; input 7405 / output 3563 /
  totalTokens 11194 / reasoningTokens 3155 / COST $0.001453552 /
  wall 21.58s (sequential sum) / duration 15141.48ms (sum)

## The two disputed cells

Both runs exclude BetaSeek ON the quoted constraint and recommend AcmeFind
(outcome parity). The dispute is evidence discipline on the scored cells:

1. **cost cell** — K=1 scored cost 4/5 citing "$4k/yr" with NO budget
   threshold to anchor it (unanchored inference). K=2 REFUSED to score
   cost ("cannot score 1-5 — E1 provides no budget threshold to anchor
   it") — refusal-to-score honesty the per-step contract requires.
2. **admin-load cell** — K=1 scored admin load 2/5 citing "no SSO" (an SSO
   fact reused as an admin-load score — mild cross-cell drift the K=2
   contracts forbid). K=2 REFUSED to score admin load ("listed as
   UNKNOWN in E1") — UNKNOWN honesty from the frozen quoted pack.

K=1 follow-ups are operationally sharper, but on the graded invariant
(constraint-first exclusion + factual grounding) K=2 is strictly cleaner.

## Reasoning-visibility

EXACT (provider-reported `usage.reasoningTokens` in `turn_end` for all
three runs; no estimation). Approximation flags: (a) wall_s includes local
harness spawn/transport overhead, not pure model latency — use provider
duration_s for model-side comparison; (b) K=1 input tokens (6034) exceed
either K=2 leg (~3700) despite shorter prompt bytes — input count includes
provider-side system/preamble tokens that vary run to run, so cost
comparison is on provider-reported cost, not prompt bytes; (c) K=2 is
honest-recorded telemetry from the 2026-10-17 FQA-3 runs, not a same-hour
re-run — provider preamble drift possible; (d) single K=1 sample, no
retries, no judge loop.

## Quality-gated choice (NOT Pareto, NOT budget-matched)

K=2 wins on evidence discipline (quoted E1 artifact, no unanchored scores,
refusal-to-score honesty) with identical correct exclusion/recommendation.
Measured cost delta: K=1 cheaper ($0.000963 vs $0.001454, K=1 saves
$0.000491 ≈ 34% less; tokens 7944 vs 11194; wall 12.94s vs 21.58s
sequential). Prefer K=2: the saving is sub-cent and buys the exact failure
the hard constraint guards against (silent drift from vendor facts via
unanchored scoring). Under the quality gate (smaller K wins ONLY at
no-worse quality + invariants + measured lower cost), K=1 fails the
no-worse-quality gate despite winning on cost.
