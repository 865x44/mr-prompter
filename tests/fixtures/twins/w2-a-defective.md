# EXPECT: flagged (>=1 typed-link violation)
# WHY: P1 produces three hypotheses, P2 silently drops all of them — no USES,
#   no TRACKED, no stated filter reason. This is information loss, not
#   filtering. (Executable step text is the source of truth; SUMMARY-style
#   metadata claims are ignored by the checker.)
P1: List three falsifiable hypotheses for why signup conversion dropped in
June: H1 (price-page friction), H2 (slow mobile checkout), H3 (broken referral
attribution). For each: one observable prediction.
HANDOFF: H1, H2, H3
P2: Write a confident action plan to fix signup conversion. Recommend a full
price-page redesign and a new referral program. Do not revisit alternatives.
