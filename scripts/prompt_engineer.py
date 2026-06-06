#!/usr/bin/env python3
"""
Prompt Engineer CLI — search, retrieve, verify, and assemble prompts
from the structured knowledge base.

Usage:
    python prompt_engineer.py search <query> [--category X] [--model Y] [--tag Z]
    python prompt_engineer.py get <technique_id>
    python prompt_engineer.py verify --prompt-file <file>
    python prompt_engineer.py assemble --goal <file> --model <model> --category <cat>
    python prompt_engineer.py list [--category X]
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path


def get_kb_dir() -> Path:
    """Resolve knowledge base directory relative to script location."""
    script_dir = Path(__file__).resolve().parent
    kb_dir = script_dir.parent / "knowledge"
    if not kb_dir.exists():
        for parent in script_dir.resolve().parents:
            candidate = parent / "knowledge"
            if candidate.exists() and (candidate / "index.json").exists():
                return candidate
        raise FileNotFoundError("Knowledge base directory not found")
    return kb_dir


def load_index(kb_dir: Path) -> dict:
    with open(kb_dir / "index.json", "r", encoding="utf-8") as f:
        return json.load(f)


def score_search(entry: dict, query: str, category: str | None, model: str | None, tag: str | None) -> int:
    score = 0
    q_lower = query.lower()
    name = entry.get("name", "").lower()
    desc = entry.get("when_to_use", "").lower()
    tags = [t.lower() for t in entry.get("tags", [])]
    models = [m.lower() for m in entry.get("models", [])]
    entry_cat = entry.get("category", "").lower()

    if q_lower in name:
        score += 10
    if q_lower in desc:
        score += 5
    for t in tags:
        if q_lower in t:
            score += 8

    if category and entry_cat == category.lower():
        score += 20
    if model:
        if any(model.lower() == m for m in models):
            score += 15
        elif model.lower() in entry.get("avoid_for", []):
            score -= 50
    if tag and tag.lower() in tags:
        score += 12

    return score


def cmd_search(args):
    kb_dir = get_kb_dir()
    index = load_index(kb_dir)
    query = args.query
    category = args.category
    model = args.model
    tag = args.tag

    results = []
    for item_type in ["techniques", "patterns", "templates"]:
        for entry in index.get(item_type, []):
            s = score_search(entry, query, category, model, tag)
            if s > 0:
                results.append((s, item_type, entry))

    results.sort(key=lambda x: x[0], reverse=True)

    if not results:
        print("No results found.")
        return

    print(f"{'Score':<6} {'Type':<12} {'ID':<30} {'Name':<40}")
    print("-" * 100)
    for score, item_type, entry in results[:20]:
        print(f"{score:<6} {item_type:<12} {entry['id']:<30} {entry.get('name', '')[:39]:<40}")


def cmd_get(args):
    kb_dir = get_kb_dir()
    index = load_index(kb_dir)
    target_id = args.technique_id

    for item_type in ["techniques", "patterns", "templates", "anti_patterns"]:
        for entry in index.get(item_type, []):
            if entry["id"] == target_id:
                # Map to references/ directory
                ref_dir = kb_dir.parent / "references"
                file_map = {
                    "reasoning": "reasoning.md",
                    "system": "system.md",
                    "creative": "creative.md",
                    "analytic": "analytic.md",
                    "meta": "meta.md",
                }
                cat = entry.get("category", "")
                ref_file = file_map.get(cat)
                if ref_file and (ref_dir / ref_file).exists():
                    print(f"--- {entry['name']} ---")
                    print(f"Category: {cat}")
                    print(f"When to use: {entry.get('when_to_use', 'N/A')}")
                    if entry.get('gain_reported'):
                        print(f"Research gain: {entry['gain_reported']}")
                    print(f"Models: {', '.join(entry.get('models', []))}")
                    if entry.get('avoid_for'):
                        print(f"Avoid for: {', '.join(entry['avoid_for'])}")
                    print()
                    # Show relevant section from reference file
                    content = (ref_dir / ref_file).read_text(encoding="utf-8")
                    # Find section by name
                    pattern = re.compile(rf"^## .*?{re.escape(entry['name'])}.*?(?=^## |\Z)", re.MULTILINE | re.DOTALL | re.IGNORECASE)
                    match = pattern.search(content)
                    if match:
                        print(match.group(0)[:3000])
                    else:
                        print(f"See references/{ref_file} for full details.")
                else:
                    print(f"Entry found: {entry['name']}")
                    print(f"When to use: {entry.get('when_to_use', 'N/A')}")
                return

    print(f"Technique/pattern/template not found: {target_id}")


def cmd_list(args):
    kb_dir = get_kb_dir()
    index = load_index(kb_dir)
    category = args.category

    print(f"{'ID':<30} {'Name':<40} {'Category'}")
    print("-" * 90)
    for item_type in ["techniques", "patterns", "templates"]:
        for entry in index.get(item_type, []):
            if not category or entry.get("category", "").lower() == category.lower():
                print(f"{entry['id']:<30} {entry.get('name', '')[:39]:<40} {entry.get('category', '')}")


def cmd_verify(args):
    prompt_text = Path(args.prompt_file).read_text(encoding="utf-8") if args.prompt_file else ""
    if not prompt_text and args.prompt_text:
        prompt_text = args.prompt_text
    if not prompt_text:
        print("No prompt provided. Use --prompt-file or --prompt-text")
        return

    pl = prompt_text.lower()
    issues = []
    greens = 0
    yellows = 0
    reds = 0

    def has(pattern, text=None):
        return bool(re.search(pattern, text or pl))

    checks = [
        ("Identity: role or persona defined",
         "yellow",
         has(r'\byou are\b|\bты\b|<role>|\bact as\b|your role|твоя роль|ты —|you\'re a\b')),

        ("Task: explicit instruction or goal present",
         "yellow",
         has(r'your task|задача[:]\s|твоя задача|\bgenerate\b|\banalyze\b|\bwrite\b|\bcreate\b|создай|напиши|проанализируй|your job|твоя работа')),

        ("Output: format explicitly specified",
         "green",
         has(r'\bjson\b|\bmarkdown\b|\bxml\b|format:|output format|формат:|вывод:|таблиц|список|bullet|numbered|пункт')),

        ("CRITICAL: No CoT scaffold for built-in-reasoning models (o1/o3/DeepSeek R1)",
         "red",
         not (has(r'\bo1\b|\bo3\b|deepseek.?r1') and
              has(r'step by step|chain of thought|think step|шаг за шагом|пошаговo|цепочка рассуждений'))),

        ("Structure: external data isolated from instructions",
         "yellow",
         len(prompt_text) < 600 or
         any(marker in prompt_text for marker in
             ['<documents>', '<context>', '<user_input>', '<data>', '<text>', '```', '---\n', '===\n'])),

        ("Anti-pattern: prohibitions paired with alternatives",
         "yellow",
         len(re.findall(r"\bdon't\b|\bdo not\b|\bнельзя\b", pl)) < 3 or
         has(r'\binstead\b|\bвместо\b|\brather\b|\balternatively\b|use\b|замените')),

        ("Style: explicit tone or voice contract",
         "yellow",
         has(r'tone[:]\s|тон[:]\s|style[:]\s|стиль[:]\s|voice:|голос[:]\s|тональн|register:|register is')),

        ("Length: output length guidance present",
         "yellow",
         has(r'\bwords?\b|\btokens?\b|\bsentences?\b|\bconcise\b|\bbrief\b|кратко|подробно|\bparagraphs?\b|абзац|\bshort\b|\blong\b')),

        ("Scope: no edge-case laundry list (>25 bullet points)",
         "yellow",
         prompt_text.count('\n- ') + prompt_text.count('\n* ') + prompt_text.count('\n• ') < 25),

        ("CRITICAL: Injection defense when processing external input",
         "red",
         not has(r'user input|user message|пользовательский|user_input|user content|external input') or
         has(r'untrusted|prompt injection|не следуй инструкциям|sandbox|do not follow instructions|ignore instructions in')),
    ]

    for name, severity, passed in checks:
        if passed:
            greens += 1
        else:
            if severity == "red":
                reds += 1
                issues.append(f"[CRITICAL] {name}")
            else:
                yellows += 1
                issues.append(f"[WARNING]  {name}")

    total = len(checks)
    print(f"\n{'='*52}")
    print(f"AUDIT RESULT: {greens}/{total} passed")
    print(f"  Pass: {greens}   Warning: {len([i for i in issues if 'WARNING' in i])}   Critical: {reds}")
    print(f"{'='*52}\n")

    if issues:
        print("Issues found:")
        for issue in issues:
            print(f"  {issue}")
    else:
        print("No issues found. Prompt looks solid!")

    print(f"\nVerdict: ", end="")
    if reds > 0:
        print("NEEDS FIXES before production")
    elif yellows > 2:
        print("GOOD — minor improvements recommended")
    else:
        print("PRODUCTION-READY")


def cmd_assemble(args):
    kb_dir = get_kb_dir()
    index = load_index(kb_dir)
    model = args.model.lower() if args.model else "claude"
    category = args.category.lower() if args.category else "system"

    goal_text = ""
    if args.goal:
        goal_text = Path(args.goal).read_text(encoding="utf-8")

    patterns = [p for p in index.get("patterns", []) if p["category"] == category]
    if not patterns:
        patterns = index.get("patterns", [])[:1]
    selected_pattern = patterns[0] if patterns else None

    techniques = [t for t in index.get("techniques", []) if t["category"] == category]
    if not techniques:
        techniques = [t for t in index.get("techniques", []) if category in t.get("tags", [])]
    if not techniques:
        techniques = index.get("techniques", [])[:3]

    compatible = []
    for t in techniques:
        avoid = [a.lower() for a in t.get("avoid_for", [])]
        if model not in avoid:
            compatible.append(t)

    selected_techniques = compatible[:3]

    print(f"# Prompt Assembly Scaffold")
    print(f"\n**Goal:** {goal_text[:200] if goal_text else '(not specified)'}")
    print(f"**Target Model:** {model}")
    print(f"**Category:** {category}")
    if selected_pattern:
        print(f"\n## Recommended Structure: {selected_pattern['name']}")
    print(f"\n## Suggested Techniques:")
    for t in selected_techniques:
        print(f"\n### {t['name']}")
        print(f"- **When:** {t['when_to_use']}")
        print(f"- **Tags:** {', '.join(t.get('tags', []))}")
        if t.get('gain_reported'):
            print(f"- **Gain:** {t['gain_reported']}")

    print(f"\n## Model-Specific Notes:")
    if model in ["claude", "claude-4"]:
        print("- Use XML tags for structure")
        print("- Place documents at TOP, queries at BOTTOM")
        print("- Enable extended thinking for complex tasks")
    elif model in ["gpt-4o", "gpt-4"]:
        print("- Use Markdown sections + few-shot examples")
        print("- Clear, structured instructions work best")
    elif model in ["o1", "o3"]:
        print("- **SHORT prompts only**")
        print("- **NO explicit CoT instructions** — built-in reasoning")
        print("- Add 'Formatting re-enabled' if needed")
    elif model in ["gemini", "gemini-3"]:
        print("- Short, direct instructions")
        print("- Place data BEFORE instructions for long context")
        print("- Avoid negative constraints, use positive framing")
    elif model in ["deepseek-r1", "deepseek"]:
        print("- **NO system message** — everything in user prompt")
        print("- **NO few-shot examples** — degrades performance")
        print("- Temperature 0.5-0.7, minimal prompt length")


def main():
    parser = argparse.ArgumentParser(prog="prompt_engineer", description="Prompt Engineer CLI")
    subparsers = parser.add_subparsers(dest="command")

    search_parser = subparsers.add_parser("search", help="Search the knowledge base")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("--category", help="Filter by category")
    search_parser.add_argument("--model", help="Filter by model compatibility")
    search_parser.add_argument("--tag", help="Filter by tag")

    get_parser = subparsers.add_parser("get", help="Get a technique by ID")
    get_parser.add_argument("technique_id", help="Technique/pattern/template ID")

    list_parser = subparsers.add_parser("list", help="List all entries")
    list_parser.add_argument("--category", help="Filter by category")

    verify_parser = subparsers.add_parser("verify", help="Verify a prompt against checklist")
    verify_parser.add_argument("--prompt-file", help="Path to prompt file")
    verify_parser.add_argument("--prompt-text", help="Prompt text directly")

    assemble_parser = subparsers.add_parser("assemble", help="Assemble a prompt scaffold")
    assemble_parser.add_argument("--goal", help="Goal description file")
    assemble_parser.add_argument("--model", default="claude", help="Target model")
    assemble_parser.add_argument("--category", default="system", help="Prompt category")

    args = parser.parse_args()

    if args.command == "search":
        cmd_search(args)
    elif args.command == "get":
        cmd_get(args)
    elif args.command == "list":
        cmd_list(args)
    elif args.command == "verify":
        cmd_verify(args)
    elif args.command == "assemble":
        cmd_assemble(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
