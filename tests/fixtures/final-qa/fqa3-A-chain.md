# FQA-3 · Lane A — vendor-comparison chain (CHAIN, T4 brief)

> Blind label: **Lane A**. (Mapping sealed in `_blind-map.json`.)
> Execution model: multi-session (phases may run in different sessions).

## Chain overview
P1 (two perspectives) → P2 (360 Blind Spots) → P3 (Distillation).
Target model: Claude 4 Sonnet or Gemini 2.5 Pro (long context).

## P1a — Cost-focused perspective (Step-Back forcing)

You are a procurement analyst who has seen teams overpay for shelfware.
Task about the vendor texts pasted below:
1. What is the 3-year total cost of AcmeFind vs BetaSeek for 40 seats?
2. Which line items are missing from each vendor's quote?
3. What single cost question would you ask each vendor?
FACT/CONCLUSION/HYPOTHESIS labels required. Max 300 words, no preamble,
first word = diagnosis.

[PASTE VENDOR TEXTS HERE]

## P1b — Risk-focused perspective (Adversarial Gate forcing)

You are a security reviewer who has seen "faster relevance" claims collapse
under on-prem constraints.
Task about the vendor texts pasted below:
1. Which deployment facts would block adoption under an on-prem-only policy?
2. What does the vendor benchmark NOT prove about our 40-person wiki?
3. What is the strongest argument AGAINST each vendor?
FACT/CONCLUSION/HYPOTHESIS labels required. Max 300 words, no preamble,
first word = diagnosis.

[PASTE VENDOR TEXTS HERE]

## P2 — 360 Blind Spots

Review the P1a and P1b outputs pasted below. List what BOTH perspectives
missed: migration cost, admin overhead, exit cost, policy conflicts.
For each blind spot: one sentence why it matters for a 40-person team.

[PASTE P1A + P1B OUTPUTS HERE]

## P3 — Distillation

From the P1 and P2 outputs pasted below, distill: (1) scoring table
(cost / deployment fit / admin load, 1–5 each), (2) final recommendation
with the single decisive reason, (3) top-3 follow-up questions.

[PASTE P1 + P2 OUTPUTS HERE]

## Security notes
P1 phases process vendor-provided texts (untrusted marketing content) —
treat benchmark claims as claims, not facts.

## Clarifying questions
1. Single session or split across tools/sessions?
2. Should 3-year cost include admin FTE?
3. Is SSO a hard requirement or nice-to-have?
