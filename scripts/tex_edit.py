#!/usr/bin/env python3
"""Fill allowed LaTeX slots and refuse edits that invent or drop work.

Reads assets/resume-template.tex and assets/cover-letter-template.tex.
--sample uses assets/sample_edit.json, prints a short summary, and writes nothing.

Exit codes: 0 ok, 2 bad arguments or unknown slot, 11 the edit broke a guardrail.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = {
    "resume": ROOT / "assets" / "resume-template.tex",
    "cover": ROOT / "assets" / "cover-letter-template.tex",
}
SAMPLE = ROOT / "assets" / "sample_edit.json"
SLOT_PATTERN = re.compile(r"(%% SLOT ([A-Z_]+)\n)(.*?)(%% END SLOT \2\n)", re.DOTALL)
NUMBER = re.compile(r"\d+(?:\.\d+)?%?")
PROJECT_ITEM = re.compile(r"\\item\s+([^:\n]+):")
JOB_ITEM = re.compile(r"\\item\s+(.+?)\s+--\s+")
RESUME_SLOTS = {"NAME", "CONTACT", "SUMMARY", "EDUCATION", "EXPERIENCE", "PROJECTS"}
COVER_SLOTS = {"ROLE", "BODY"}


def fail(message: str, code: int) -> None:
    print(message, file=sys.stderr)
    sys.exit(code)


def slots_in(text: str) -> dict[str, str]:
    return {name: body for _, name, body, _ in SLOT_PATTERN.findall(text)}


def fill(template: str, replacements: dict[str, str], allowed: set[str]) -> str:
    unknown = set(replacements) - allowed
    if unknown:
        fail("Unknown slot: " + ", ".join(sorted(unknown)) + ".", 2)

    def replace(match: re.Match) -> str:
        name = match.group(2)
        if name not in replacements:
            return match.group(0)
        body = replacements[name]
        if not body.endswith("\n"):
            body += "\n"
        return match.group(1) + body + match.group(4)

    return SLOT_PATTERN.sub(replace, template)


def numbers_ok(text: str, source: str) -> str | None:
    for number in NUMBER.findall(text):
        if number not in source:
            return number
    return None


def check_keywords(resume_text: str, keywords: list[str], source: str) -> None:
    source_folded = source.casefold()
    resume_folded = resume_text.casefold()
    for keyword in keywords:
        phrase = keyword.strip()
        if not phrase:
            continue
        if phrase.casefold() not in source_folded:
            fail(f"Keyword {phrase} is not in the confirmed facts or the bank. Do not add it from the job post.", 11)
        if phrase.casefold() not in resume_folded:
            fail(f"Resume is missing the job keyword {phrase}, which the student can support.", 11)


def check_resume(filled_slots: dict[str, str], original: dict[str, str], facts: str, bank: list[str], keywords: list[str]) -> None:
    source = facts + "\n" + "\n".join(bank)
    check_keywords("\n".join(filled_slots.values()), keywords, source)
    for name, body in filled_slots.items():
        invented = numbers_ok(body, source)
        if invented:
            fail(f"Resume slot {name} uses {invented}, which is not in the confirmed facts or the bank.", 11)
    name = filled_slots.get("NAME", original["NAME"]).strip()
    if name != original["NAME"].strip() and name not in facts:
        fail("Resume name is not in the confirmed facts.", 11)
    projects = filled_slots.get("PROJECTS", "")
    for project in bank:
        if project not in projects:
            fail(f"Resume dropped the bank project {project}.", 11)
    for found in PROJECT_ITEM.findall(projects):
        title = found.strip()
        if title not in bank:
            fail(f"Resume names {title}, which is not in the bank.", 11)
    experience = filled_slots.get("EXPERIENCE", "")
    for employer in JOB_ITEM.findall(experience):
        if employer.strip() not in facts:
            fail(f"Resume names employer {employer.strip()}, which is not in the confirmed facts.", 11)


def check_cover(filled_slots: dict[str, str], facts: str, bank: list[str]) -> None:
    source = facts + "\n" + "\n".join(bank)
    for name, body in filled_slots.items():
        invented = numbers_ok(body, source)
        if invented:
            fail(f"Cover letter slot {name} uses {invented}, which is not in the confirmed facts or the bank.", 11)


def load_edit(path: Path) -> dict:
    try:
        data = json.loads(path.read_text())
    except (OSError, ValueError):
        fail("The edit file is missing or is not JSON.", 2)
    if not isinstance(data, dict):
        fail("The edit file must be a JSON object.", 2)
    return data


def main() -> None:
    parser = argparse.ArgumentParser(description="Fill Job Ledger LaTeX slots")
    parser.add_argument("--sample", action="store_true")
    parser.add_argument("--edit", default="")
    parser.add_argument("--out-dir", default="")
    args = parser.parse_args()

    edit_path = SAMPLE if args.sample or not args.edit else Path(args.edit)
    if not args.sample and not args.edit:
        fail("Pass --edit, or --sample.", 2)
    data = load_edit(edit_path)
    facts = str(data.get("allowed_facts") or "")
    bank = [str(name) for name in data.get("bank_projects") or []]
    keywords = [str(phrase) for phrase in data.get("must_include") or []]
    resume_slots = {str(key): str(value) for key, value in (data.get("resume_slots") or {}).items()}
    cover_slots = {str(key): str(value) for key, value in (data.get("cover_slots") or {}).items()}

    resume_template = TEMPLATES["resume"].read_text()
    cover_template = TEMPLATES["cover"].read_text()
    resume = fill(resume_template, resume_slots, RESUME_SLOTS)
    cover = fill(cover_template, cover_slots, COVER_SLOTS)
    check_resume(slots_in(resume), slots_in(resume_template), facts, bank, keywords)
    check_cover(slots_in(cover), facts, bank)

    if args.sample or not args.out_dir:
        print(json.dumps({
            "ok": True,
            "resume_slots": sorted(resume_slots),
            "cover_slots": sorted(cover_slots),
            "bank_projects": bank,
            "wrote": False,
        }, indent=2))
        return

    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "resume.tex").write_text(resume)
    (out / "cover-letter.tex").write_text(cover)
    print(json.dumps({"ok": True, "out_dir": str(out), "wrote": True}, indent=2))


if __name__ == "__main__":
    main()
