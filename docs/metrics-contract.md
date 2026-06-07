# Mr. Prompter Metrics Contract

> Version: maintenance-release
> Date: 2026-06-07
>
> This contract defines every exact number that may appear in published claims.
> Claims not listed here must not use exact numbers.

---

## Retained Metrics

| Metric | Definition | Authoritative Source | Current Value |
|--------|-----------|----------------------|---------------|
| `techniques` | Number of objects in `knowledge/index.json["techniques"]` | `knowledge/index.json` | 31 |
| `research_backed` | Number of technique entries with `"research_backed": true` | `knowledge/index.json` | 12 |
| `patterns` | Number of objects in `knowledge/index.json["patterns"]` | `knowledge/index.json` | 5 |
| `templates` | Number of objects in `knowledge/index.json["templates"]` | `knowledge/index.json` | 3 |
| `anti_patterns` | Number of objects in `knowledge/index.json["anti_patterns"]` | `knowledge/index.json` | 8 |
| `failure_patterns` | Number of coded diagnostic patterns in `references/diagnose.md` | `references/diagnose.md` | 13 |
| `session_archetypes` | Number of archetype sections under "Common Session Failure Archetypes" in `references/diagnose.md` | `references/diagnose.md` | 6 |
| `extraction_patterns` | Number of pattern sections under "Common Patterns" in `references/extract.md` | `references/extract.md` | 5 |
| `model_profiles` | Number of model-specific profile sections under "Model-Specific Do's and Don'ts" in `references/models.md` | `references/models.md` | 6 |
| `modes` | Number of operational modes documented in the skill | `SKILL.md` mode list | 7 |
| `prompt_markdown_files` | Number of `.md` files under `prompts/` (including index and archive) | `prompts/` directory | 58 |

## Rules

1. **Technique count** is the length of the `techniques` array. It is the single source of truth for "how many techniques."
2. **Research-backed count** is the count of `research_backed: true` flags. It is NOT a verified claim about independent research quality.
3. **Mode count** is 7 wherever an exact mode count is stated.
4. **Prompt files** counts Markdown files, not "ready-to-use prompts." The phrase "ready-to-use prompts" must not be paired with an exact number unless a separate deterministic rule for prompt entries is defined and enforced.
5. **Failure patterns, session archetypes, extraction patterns, and model profiles** are counted from their canonical reference files, not from `index.json.stats`. `index.json.stats` must match these counts.

## Exclusions

The following are explicitly out of scope for exact numeric claims:

- "Ready-to-use prompt entries" — ambiguous boundary between standalone files, archive entries, and navigation rows.
- "Research-backed citations" — requires independent verification of citation quality, not just flag counting.
- "Models in comparison matrix" — matrix columns differ from profile sections and are not a user-facing metric.
