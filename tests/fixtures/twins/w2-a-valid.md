# EXPECT: clean (0 violations)
# WHY: same P1 as w2-a-defective, but P2 consumes H1 and H3 and explicitly
#   filters H2 against a quoted hard constraint, preserving it as TRACKED
#   (rejected-but-tracked). Filtering with a stated reason is legitimate.
P1: List three falsifiable hypotheses for why signup conversion dropped in
June: H1 (price-page friction), H2 (slow mobile checkout), H3 (broken referral
attribution). For each: one observable prediction.
HANDOFF: H1, H2, H3
P2: HARD CONSTRAINT (quoted from the brief): "no mobile-app changes this
quarter." H2 (slow mobile checkout) requires an app release, so exclude it.
Build the remediation plan from the remaining hypotheses.
USES: H1, H3
TRACKED: H2 (rejected: needs app release, blocked this quarter)
