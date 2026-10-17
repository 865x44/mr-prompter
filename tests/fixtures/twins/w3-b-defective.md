# EXPECT: flagged (>=1 preflight violation)
# WHY: P2 claims independent verification ("independently verify", "certify")
#   but consumes only H1 and re-reads P1's decision — review, not
#   independent verification. No EVIDENCE source is declared. CHAIN Step 4
#   forbids verification without external evidence; USES resolves to H1
#   (no dangling reference), the defect is the fake verification claim.
P1: Decide whether to expand into the Brazilian market: H1 (enter, citing
growth) or H2 (wait, citing currency risk). State the deciding factor.
HANDOFF: H1
P2: Independently verify the P1 decision. Re-read it carefully and confirm
whether it is correct, then certify it as independently verified.
USES: H1
