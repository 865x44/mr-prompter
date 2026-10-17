# EXPECT: clean (0 violations)
# WHY: P3 consumes the declared artifact H1; the rejected alternative H2 is
#   preserved as TRACKED with its reason instead of silently dropped. Full
#   handoff preservation: every HANDOFF artifact is either consumed or tracked.
P1: Draft two candidate slogans: H1 (playful), H2 (formal). Note the
audience each fits.
HANDOFF: H1, H2
P2: Pick H1 for the young-audience campaign. State why H2 does not fit there.
USES: H1
TRACKED: H2 (rejected for this campaign: formal register mismatches a young
audience; keep for enterprise placements)
P3: Finalize H1 for print: tighten wording, keep the playful register, add
the compliance footer.
USES: H1
