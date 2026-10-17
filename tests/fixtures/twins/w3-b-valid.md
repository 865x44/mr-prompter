# EXPECT: clean (0 preflight violations)
# WHY: same P1 and same verification surface as w3-b-defective, but P2
#   checks H1 against a declared EXTERNAL evidence source (the central
#   bank's published currency-stability report) with an explicit
#   contradiction protocol. External grounding makes the verification
#   independent; USES resolves, EVIDENCE is declared. Silence is earned.
P1: Decide whether to expand into the Brazilian market: H1 (enter, citing
growth) or H2 (wait, citing currency risk). State the deciding factor.
HANDOFF: H1
P2: Check H1 against the central bank's published currency-stability
report (external). If the report contradicts the currency-risk assessment,
report the conflict with both quotes; do not certify.
EVIDENCE: ext-bcb-currency-report
USES: H1
