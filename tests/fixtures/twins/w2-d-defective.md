# EXPECT: flagged (>=1 typed-link violation)
# WHY: P3 consumes H4, which no earlier HANDOFF declares — a dangling
#   reference across the P1->P2->P3 handoff. H2 is additionally dropped
#   without TRACKED. Deterministic link errors, not judgment calls.
P1: Draft two candidate slogans: H1 (playful), H2 (formal). Note the
audience each fits.
HANDOFF: H1, H2
P2: Pick H1 for the young-audience campaign. State why H2 does not fit there.
USES: H1
P3: Finalize H4 for print: tighten wording, keep the formal register, add
the compliance footer.
USES: H4
