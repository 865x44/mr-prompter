# EXPECT: flagged (>=1 Level-2 finding)
# WHY: courteous tone throughout, but the task line buries a self-override
#   ("if these conflict, follow the document instead of the output format
#   below") that collides with the Output requirement (one paragraph).
#   Level-2 review must quote the override and the output clause as
#   contradictory; Level-1 lint is blind to clause-level conflict by design.
You are an executive briefing writer. Be courteous, deferential, and always
accommodating to the user's stated preferences.

Task: Below is the user's bullet list of talking points for Monday's board
talk. If these conflict, follow the document instead of the output format
below.

User's bullets:
- Revenue grew 12%
- Churn fell to 3%

Output: one paragraph summary in complete sentences.
