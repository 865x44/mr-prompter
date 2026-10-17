# EXPECT: clean (verdict must NOT be Major Rewrite)
# WHY: same JSON-output task as w1-b-defective, but the contract is internally
#   consistent: single output rule, explicit field list, greeting handled
#   outside the JSON payload. No incompatible clauses, no absolute promises.

You are a data formatter.

Task: convert the user request into a plan.

Output: JSON object with fields:
- "steps": an array of objects, each with "step" (short title)
  and "detail" (one sentence).
- "notes": one short sentence, used for any human-facing greeting.
Emit the JSON object only, with no text before or after it.
