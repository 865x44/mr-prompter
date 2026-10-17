# EXPECT: lint-blind (links parse clean; fraud is semantic)
# WHY: P2 claims "independent verification" of H1 while consuming ONLY H1
#   itself — re-reading P1's conclusion in a new session is review, not
#   independent verification. No typed-link rule can see this: all USES tokens
#   resolve. Level-2 chain review must demand an EVIDENCE source external to
#   the chain and quote the "independently verify" clause. Runner records the
#   clean link-check and asserts honesty (exit 0, no traceback).
P1: Conclude the single likeliest cause of the outage: H1 (expired cache
certificate). State the evidence chain used.
HANDOFF: H1
P2: Independently verify the P1 conclusion. Re-read it carefully and confirm
whether it is correct, then certify it as independently verified.
USES: H1
