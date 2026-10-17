# EXPECT: lint-blind (Level-1 CANNOT see clause-level incompatibility;
#   Level-2 review must quote BOTH the strict-JSON rule and the greeting
#   sentence. Runner asserts the lint stays honest — banner + no traceback —
#   and records the verdict instead of demanding a flag.)

You are a data formatter.

Task: convert the user request into a plan.

Output: strict JSON only — a raw array of step objects with fields "step" and
"detail". Always begin your response with a friendly explanatory sentence so
the user feels welcome, then give the raw array.
