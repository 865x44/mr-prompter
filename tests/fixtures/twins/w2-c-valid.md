# EXPECT: clean (0 violations)
# WHY: P2 verifies H1 against an EXTERNAL evidence source declared via
#   EVIDENCE, not against H1 alone. External grounding is what makes the
#   verification independent. USES resolves, EVIDENCE is declared.
P1: Conclude the single likeliest cause of the outage: H1 (expired cache
certificate). State the evidence chain used.
HANDOFF: H1
P2: Check H1 against the vendor incident log (external). If the log shows a
different cause, report the conflict with both quotes; do not certify.
EVIDENCE: ext-vendor-incident-log
USES: H1
