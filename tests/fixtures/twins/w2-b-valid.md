# EXPECT: clean (0 violations)
# WHY: same P1 artifact as w2-b-defective, but P2 names the real artifact H1
#   and applies a NEW operation with a verifiable criterion (top-2 drivers by
#   cost share). Real consumption, not "go deeper".
P1: Produce a cost breakdown of the support backlog: H1 (table: ticket class
x hours x cost driver).
HANDOFF: H1
P2: From the cost table, compute each class's share of total cost and keep
only the top-2 drivers; drop the rest with the computed shares quoted.
Completion: a ranked 2-row table. Failure: any row without a computed share.
USES: H1
