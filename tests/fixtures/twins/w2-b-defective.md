# EXPECT: flagged (>=1 typed-link violation)
# WHY: P2 references a step LABEL ("P1-findings") instead of the declared
#   artifact (H1), and its body ("analyse deeper") adds no new input,
#   operation, or criterion. A USES entry must name a HANDOFF artifact from
#   an earlier step — a pseudo-dependency on a label is a typed-link error.
P1: Produce a cost breakdown of the support backlog: H1 (table: ticket class
x hours x cost driver).
HANDOFF: H1
P2: Go deeper on the P1-findings. Analyse them more thoroughly and produce
deeper insights about what they really mean.
USES: P1-findings
