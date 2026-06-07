#!/usr/bin/env python3
"""
Consistency audit for mr-prompter.
Exits non-zero if mechanically countable facts diverge from published claims.
"""

import json
import os
import re
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(
    os.environ.get("AUDIT_REPO_ROOT", Path(__file__).resolve().parent.parent)
).resolve()

errors = []
warnings = []


def fail(msg):
    errors.append(msg)
    print(f"FAIL: {msg}")


def warn(msg):
    warnings.append(msg)
    print(f"WARN: {msg}")


def load_index():
    path = REPO_ROOT / "knowledge" / "index.json"
    override = os.environ.get("AUDIT_INDEX_OVERRIDE")
    if override:
        path = REPO_ROOT / "knowledge" / override
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _count_section_headers(md_path, section_title_regex, header_regex=r"^### "):
    """Count markdown headers under a matched section."""
    if not md_path.exists():
        return None
    content = md_path.read_text(encoding="utf-8")
    section_match = re.search(section_title_regex, content, re.DOTALL | re.MULTILINE)
    if not section_match:
        return None
    return len(re.findall(header_regex, section_match.group(0), re.MULTILINE))


def _count_coded_patterns(md_path):
    """Count coded diagnostic patterns like **I01**, **F01**, etc. in tables."""
    if not md_path.exists():
        return None
    content = md_path.read_text(encoding="utf-8")
    return len(re.findall(r"^\|\s*\*\*[A-Z]\d+\*\*", content, re.MULTILINE))


def _compute_modes_from_skill():
    """Count data rows in the canonical SKILL.md Mode Selection table."""
    skill_path = REPO_ROOT / "SKILL.md"
    if not skill_path.exists():
        return None
    skill = skill_path.read_text(encoding="utf-8")
    m = re.search(r"## Mode Selection\s*\n\n\|[^\n]+\|\n\|[-:| ]+\|\n((?:\|[^\n]+\|\n?)+)", skill)
    return len(m.group(1).strip().splitlines()) if m else None


def compute_metrics(index):
    """Compute the retained metrics from their canonical repository sources."""
    ref_dir = REPO_ROOT / "references"
    prompts_dir = REPO_ROOT / "prompts"
    return {
        "techniques": len(index.get("techniques", [])),
        "patterns": len(index.get("patterns", [])),
        "templates": len(index.get("templates", [])),
        "anti_patterns": len(index.get("anti_patterns", [])),
        "research_backed": sum(1 for t in index.get("techniques", []) if t.get("research_backed")),
        "failure_patterns": _count_coded_patterns(ref_dir / "diagnose.md"),
        "session_archetypes": _count_section_headers(
            ref_dir / "diagnose.md",
            r"## Common Session Failure Archetypes.*?(?=^## |\Z)",
            r"^### Archetype",
        ),
        "extraction_patterns": _count_section_headers(
            ref_dir / "extract.md",
            r"## Common Patterns.*?(?=^## |\Z)",
            r"^### Pattern",
        ),
        "model_profiles": _count_section_headers(
            ref_dir / "models.md",
            r"## Model-Specific Do\'s and Don\'ts.*?(?=^## |\Z)",
            r"^### ",
        ),
        "modes": _compute_modes_from_skill(),
        "prompt_files": len(list(prompts_dir.rglob("*.md"))) if prompts_dir.exists() else None,
    }


def check_index_stats(index):
    """Verify stored stats match computed array lengths and reference-file counts."""
    stats = index.get("stats", {})
    computed = compute_metrics(index)
    stored_keys = {
        "techniques",
        "patterns",
        "templates",
        "anti_patterns",
        "research_backed",
        "failure_patterns",
        "session_archetypes",
        "extraction_patterns",
        "model_profiles",
        "prompt_files",
    }
    for key in stored_keys:
        value = computed[key]
        if value is None:
            fail(f"Could not compute required metric: {key}")
        elif key not in stats:
            fail(f"index.json stats.{key} is missing (required by metrics contract)")
        elif stats[key] != value:
            fail(f"index.json stats.{key}={stats[key]} != computed {value}")


def check_unique_ids(index):
    """Verify IDs are unique across all collections."""
    all_ids = []
    for collection_name in ["techniques", "patterns", "templates", "anti_patterns"]:
        for item in index.get(collection_name, []):
            all_ids.append(item.get("id"))

    dupes = {k: v for k, v in Counter(all_ids).items() if v > 1}
    if dupes:
        for dup_id, count in dupes.items():
            fail(f'Duplicate ID "{dup_id}" appears {count} times')


def check_technique_categories(index):
    """Verify technique categories are valid."""
    valid = {"system", "reasoning", "creative", "analytic", "meta"}
    for t in index.get("techniques", []):
        cat = t.get("category", "")
        if cat not in valid:
            tid = t.get("id")
            fail(f'Technique "{tid}" has invalid category "{cat}"')


DEFERRED_MISSING_SECTIONS = {
    "forced-domain-shift",
    "toggle-mode-pattern",
    "injection-defense",
    "progressive-disclosure",
}


def check_technique_reference_sections(index):
    """Verify each technique maps to a reference section.

    The four known missing sections are documented deferred exemptions.
    Any additional missing mapping is treated as a failure.
    """
    ref_dir = REPO_ROOT / "references"
    file_map = {
        "reasoning": "reasoning.md",
        "system": "system.md",
        "creative": "creative.md",
        "analytic": "analytic.md",
        "meta": "meta.md",
    }

    missing = []
    for t in index.get("techniques", []):
        cat = t.get("category", "")
        ref_file = file_map.get(cat)
        if not ref_file:
            tid = t.get("id")
            fail(f'Technique "{tid}" has unknown category "{cat}"')
            continue

        ref_path = ref_dir / ref_file
        if not ref_path.exists():
            fail(f"Missing reference file: {ref_file}")
            continue

        content = ref_path.read_text(encoding="utf-8")
        name = t.get("name", "")
        pattern = re.compile(
            rf"^## [^\n]*{re.escape(name)}[^\n]*$",
            re.MULTILINE | re.IGNORECASE,
        )
        if not pattern.search(content):
            missing.append(t.get("id"))

    deferred = [m for m in missing if m in DEFERRED_MISSING_SECTIONS]
    unexpected = [m for m in missing if m not in DEFERRED_MISSING_SECTIONS]

    if deferred:
        warn(
            f"Deferred missing reference sections: {', '.join(sorted(deferred))}"
        )
    if unexpected:
        fail(
            f"Techniques with no matching reference section: {', '.join(sorted(unexpected))}"
        )


def check_referenced_files_exist(index):
    """Verify local files referenced by the knowledge base exist."""
    refs = [
        REPO_ROOT / "references" / "context.md",
        REPO_ROOT / "references" / "meta.md",
        REPO_ROOT / "references" / "system.md",
        REPO_ROOT / "references" / "reasoning.md",
        REPO_ROOT / "references" / "analytic.md",
        REPO_ROOT / "references" / "creative.md",
        REPO_ROOT / "references" / "cases.md",
        REPO_ROOT / "references" / "models.md",
        REPO_ROOT / "references" / "diagnose.md",
        REPO_ROOT / "references" / "extract.md",
        REPO_ROOT / "scripts" / "prompt_engineer.py",
    ]
    for path in refs:
        if not path.exists():
            fail(f"Referenced file does not exist: {path.relative_to(REPO_ROOT)}")


def check_adapters():
    """Verify adapters do not contain stale exact counts."""
    adapters_dir = REPO_ROOT / "adapters"
    if not adapters_dir.exists():
        return

    for adapter_path in adapters_dir.iterdir():
        if not adapter_path.is_file():
            continue
        content = adapter_path.read_text(encoding="utf-8")

        stale_claims = [
            ("75+", "research-backed techniques claim"),
            ("Six modes", "six modes claim"),
            ("six modes", "six modes claim"),
        ]
        for claim, desc in stale_claims:
            if claim in content:
                fail(f'Adapter "{adapter_path.name}" contains stale {desc}: "{claim}"')


def check_published_claims():
    """Verify exact published claims match the metrics contract.

    This compares parsed retained claims in README.md, SKILL.md,
    references/context.md, and adapters against computed metrics from
    the current repository to enforce docs/metrics-contract.md.
    """
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    skill = (REPO_ROOT / "SKILL.md").read_text(encoding="utf-8")
    context = (REPO_ROOT / "references" / "context.md").read_text(encoding="utf-8")

    index = load_index()
    metrics = compute_metrics(index)
    techniques = metrics["techniques"]
    rb_count = metrics["research_backed"]
    modes = metrics["modes"]
    prompt_md_count = metrics["prompt_files"]
    if modes is None:
        fail("Could not compute mode count from SKILL.md")
        modes = 0

    # README stats table
    readme_table_match = re.search(
        r"\|\s*Techniques \(total\)\s*\|\s*(\d+)\s*\|", readme
    )
    if readme_table_match:
        claimed = int(readme_table_match.group(1))
        if claimed != techniques:
            fail(f"README.md claims {claimed} techniques in stats table (computed {techniques})")

    readme_rb_match = re.search(
        r"\|\s*Research-backed.*\|\s*(\d+)\s*\|", readme
    )
    if readme_rb_match:
        claimed = int(readme_rb_match.group(1))
        if claimed != rb_count:
            fail(f"README.md claims {claimed} research-backed in stats table (computed {rb_count})")

    readme_prompt_match = re.search(
        r"\|\s*Prompt Markdown files\s*\|\s*(\d+)\s*\|", readme
    )
    if readme_prompt_match:
        claimed = int(readme_prompt_match.group(1))
        if claimed != prompt_md_count:
            fail(f"README.md claims {claimed} prompt Markdown files (computed {prompt_md_count})")

    # README retained metric table claims (exact counts)
    for label, computed_val, pattern in [
        ("failure_patterns", metrics["failure_patterns"], r"\|\s*Failure patterns.*?\|\s*(\d+)\s*\|"),
        ("session_archetypes", metrics["session_archetypes"], r"\|\s*Session archetypes.*?\|\s*(\d+)\s*\|"),
        ("extraction_patterns", metrics["extraction_patterns"], r"\|\s*Extraction patterns.*?\|\s*(\d+)\s*\|"),
        ("model_profiles", metrics["model_profiles"], r"\|\s*Model profiles.*?\|\s*(\d+)\s*\|"),
    ]:
        m = re.search(pattern, readme)
        if m:
            claimed = int(m.group(1))
            if computed_val is None:
                fail(f"README.md table claims {claimed} {label} but index.json stat is missing")
            elif claimed != computed_val:
                fail(f"README.md table claims {claimed} {label} (computed {computed_val})")

    # README bullet claims (exact counts)
    for label, computed_val, pattern in [
        ("failure_patterns", metrics["failure_patterns"], r"(?i)(\d+)\s+coded\s+failure\s+patterns"),
    ]:
        m = re.search(pattern, readme)
        if m:
            claimed = int(m.group(1))
            if computed_val is None:
                fail(f"README.md bullet claims {claimed} {label} but index.json stat is missing")
            elif claimed != computed_val:
                fail(f"README.md bullet claims {claimed} {label} (computed {computed_val})")

    header_match = re.search(r"> \*\*Prompt engineering toolkit:\*\* (\d+) specialized modes", readme)
    if header_match:
        claimed = int(header_match.group(1))
        if claimed != modes:
            fail(f"README.md header claims {claimed} modes (computed {modes})")

    skill_fm_match = re.search(r"(\d+) techniques with (\d+) research-backed flags", skill)
    if skill_fm_match:
        claimed_tech = int(skill_fm_match.group(1))
        claimed_rb = int(skill_fm_match.group(2))
        if claimed_tech != techniques:
            fail(f"SKILL.md frontmatter claims {claimed_tech} techniques (computed {techniques})")
        if claimed_rb != rb_count:
            fail(f"SKILL.md frontmatter claims {claimed_rb} research-backed (computed {rb_count})")

    for match in re.finditer(r"\b(\d+|Six|Seven|six|seven) (?:distinct tasks|modes)\b", skill):
        words = {"six": 6, "seven": 7}
        token = match.group(1)
        claimed = int(token) if token.isdigit() else words[token.lower()]
        if claimed != modes:
            fail(f"SKILL.md claims {claimed} modes/tasks (computed {modes})")

    ctx_tech_match = re.search(r"backed by \*\*(\d+) techniques\*\*", context)
    if ctx_tech_match:
        claimed = int(ctx_tech_match.group(1))
        if claimed != techniques:
            fail(f"references/context.md claims {claimed} techniques (computed {techniques})")

    ctx_rb_match = re.search(r"\*\*(\d+) research-backed flags\*\*", context)
    if ctx_rb_match:
        claimed = int(ctx_rb_match.group(1))
        if claimed != rb_count:
            fail(f"references/context.md claims {claimed} research-backed (computed {rb_count})")

    ctx_prompt_match = re.search(r"\*\*(\d+) prompt Markdown files\*\*", context)
    if ctx_prompt_match:
        claimed = int(ctx_prompt_match.group(1))
        if claimed != prompt_md_count:
            fail(f"references/context.md claims {claimed} prompt Markdown files (computed {prompt_md_count})")

    # Context retained metric bullet claims (exact counts)
    for label, computed_val, pattern in [
        ("failure_patterns", metrics["failure_patterns"], r"\*\*(\d+) failure patterns\*\*"),
        ("session_archetypes", metrics["session_archetypes"], r"\*\*(\d+) session archetypes\*\*"),
        ("extraction_patterns", metrics["extraction_patterns"], r"\*\*(\d+) extraction patterns\*\*"),
        ("model_profiles", metrics["model_profiles"], r"\*\*(\d+) model profiles\*\*"),
        ("anti_patterns", metrics["anti_patterns"], r"\*\*(\d+) anti-patterns\*\*"),
    ]:
        m = re.search(pattern, context)
        if m:
            claimed = int(m.group(1))
            if computed_val is None:
                fail(f"references/context.md claims {claimed} {label} but computed stat is missing")
            elif claimed != computed_val:
                fail(f"references/context.md claims {claimed} {label} (computed {computed_val})")

    ctx_modes_match = re.search(r"Provides (?:\*\*)?(\w+) modes", context, re.IGNORECASE)
    if ctx_modes_match:
        token = ctx_modes_match.group(1)
        words = {"six": 6, "seven": 7}
        claimed = int(token) if token.isdigit() else words.get(token.lower())
        if claimed is None or claimed != modes:
            fail(f"references/context.md claims {token} modes (computed {modes})")

    if "75+ research-backed" in skill:
        fail("SKILL.md frontmatter contains \"75+ research-backed techniques\"")

    if "58 ready-to-use prompts" in readme:
        fail("README.md uses ambiguous exact count \"58 ready-to-use prompts\"")

    if "58 ready-to-use prompts" in context:
        fail("references/context.md uses ambiguous exact count \"58 ready-to-use prompts\"")

    if "Stats (verified)" in context:
        fail("references/context.md uses misleading \"Stats (verified)\" label")

    adapters_dir = REPO_ROOT / "adapters"
    if adapters_dir.exists():
        for adapter_path in adapters_dir.iterdir():
            if not adapter_path.is_file():
                continue
            content = adapter_path.read_text(encoding="utf-8")
            for match in re.finditer(r"(\d+)\s+[Mm]odes", content):
                claimed = int(match.group(1))
                if claimed != modes:
                    fail(
                        f'Adapter "{adapter_path.name}" claims {claimed} modes '
                        f"(computed {modes})"
                    )


def check_python_syntax():
    """Verify Python files compile."""
    py_files = [
        REPO_ROOT / "scripts" / "prompt_engineer.py",
        REPO_ROOT / "scripts" / "audit_consistency.py",
    ]
    for path in py_files:
        if path.exists():
            try:
                compile(path.read_text(encoding="utf-8"), str(path), "exec")
            except SyntaxError as e:
                fail(f"Syntax error in {path.relative_to(REPO_ROOT)}: {e}")


def main():
    print("=" * 60)
    print("Mr. Prompter Consistency Audit")
    print("=" * 60)

    index = load_index()

    check_index_stats(index)
    check_unique_ids(index)
    check_technique_categories(index)
    check_technique_reference_sections(index)
    check_referenced_files_exist(index)
    check_adapters()
    check_published_claims()
    check_python_syntax()

    print("\n" + "=" * 60)
    if errors:
        print(f"RESULT: {len(errors)} error(s), {len(warnings)} warning(s)")
        print("Audit FAILED")
        sys.exit(1)
    else:
        print(f"RESULT: 0 errors, {len(warnings)} warning(s)")
        print("Audit PASSED")
        sys.exit(0)


if __name__ == "__main__":
    main()
