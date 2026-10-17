# Final QA — repair matrix (2 subjects × 3 variants, NEW CLI verify)

All 6 verdicts independently reproduced by Primary (sha256 match, same CLI).
Negative flip: w1-d-valid → Needs Fixes, 0 critical, clean expectation met.

| Subject | Variant | Chars (Δ) | CLI verdict | Target defect fixed? |
|---|---|---|---|---|
| w1-a (contra-clauses+guarantee+override) | generic rewrite | 269 (+21) | Production-Ready (0c/1w) | YES — but see ruling |
| w1-a | scoped | 103 (−145, −58%) | Needs Fixes (0c/4w) | YES |
| w1-a | scoped+subtractive | 75 (−173, −70%) | Needs Fixes (0c/5w) | YES |
| w2-a (dropped H1–H3) | generic rewrite | 379 (+0, new text) | Needs Fixes — chain contract destroyed | NO |
| w2-a | scoped (+USES/TRACKED) | 449 (+70) | Needs Fixes, 0 link violations | YES |
| w2-a | scoped+subtractive (−tone fluff) | 411 (+32) | Needs Fixes, 0 link violations | YES, cheapest |

RULING on w1-a generic → Production-Ready (Primary, not worker claim):
reproduced byte-identical. Reading: the rewrite deleted ALL THREE lexical
triggers (guarantee phrase, ignore-above clause, yes-vs-explain conflict —
the rewrite kept only "explain in full detail" + a fielded JSON schema).
So the lint is working AS DESIGNED (lexical layer): no triggers → no
criticals. This is NOT a lint bypass — a bypass would keep the defect while
dodging the wording. It IS a cost finding: generic reached clean only by
spending +21 chars and discarding the original task shape (yes-only
requirement vanished — the "fix" changed the task, not just the defect).
Scoped (−58%) and subtractive (−70%) fixed the same defect cheaper while
preserving task shape. Winner w1-a: scoped+subtractive (fix + economy).
Winner w2-a: scoped+subtractive (0 violations, +32 chars vs +70).
Generic rewrite loses on chains: it cannot see typed-link contracts at all.

Recommendation: scoped+subtractive wins both subjects (fix × economy);
generic is admissible for single prompts but wasteful and chain-blind.
