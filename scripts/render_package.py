#!/usr/bin/env python3
"""Fill assets/package.html into one review page.

--sample reads assets/sample_package.json, prints the page, and writes nothing.

Exit codes: 0 ok, 2 bad arguments or bad JSON.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "assets" / "package.html"
SAMPLE = ROOT / "assets" / "sample_package.json"
SECTION = re.compile(r"<section data-section=\"([a-z]+)\">.*?</section>\s*", re.DOTALL)


def fail(message: str, code: int) -> None:
    print(message, file=sys.stderr)
    sys.exit(code)


def load(path: Path) -> dict:
    try:
        data = json.loads(path.read_text())
    except (OSError, ValueError):
        fail("The package file is missing or is not JSON.", 2)
    if not isinstance(data, dict):
        fail("The package file must be a JSON object.", 2)
    return data


def items(pairs: list, left: str, right: str) -> str:
    rows = []
    for pair in pairs:
        if not isinstance(pair, dict):
            continue
        rows.append(f"<li>{html.escape(str(pair.get(left) or ''))}: {html.escape(str(pair.get(right) or ''))}</li>")
    if not rows:
        return ""
    return "<ul>\n" + "\n".join(rows) + "\n</ul>"


def text_block(value: str) -> str:
    return html.escape(value or "")


def render(data: dict) -> str:
    page = TEMPLATE.read_text()
    answers = items(data.get("answers") or [], "q", "a")
    fields = items(data.get("fields") or [], "label", "value")
    confirmation = str(data.get("confirmation") or "").strip()
    replacements = {
        "EMPLOYER": text_block(str(data.get("employer") or "")),
        "ROLE": text_block(str(data.get("role") or "")),
        "VERDICT": text_block(str(data.get("verdict") or "")),
        "QUOTE": text_block(str(data.get("quote") or "")),
        "SECTION": text_block(str(data.get("section") or "")),
        "LINK": text_block(str(data.get("link") or "")),
        "ANSWERS": answers,
        "RESUME": text_block(str(data.get("resume") or "")),
        "COVER": text_block(str(data.get("cover") or "")),
        "FIELDS": fields,
        "CONFIRMATION": text_block(confirmation),
    }
    for token, value in replacements.items():
        page = page.replace("{{" + token + "}}", value)

    drop = set()
    if not answers:
        drop.add("answers")
    if not str(data.get("resume") or "").strip():
        drop.add("resume")
    if not str(data.get("cover") or "").strip():
        drop.add("cover")
    if not fields:
        drop.add("fields")
    if not confirmation:
        drop.add("confirmation")

    def keep(match: re.Match) -> str:
        return "" if match.group(1) in drop else match.group(0)

    return SECTION.sub(keep, page)


def main() -> None:
    parser = argparse.ArgumentParser(description="Render the Job Ledger package page")
    parser.add_argument("--sample", action="store_true")
    parser.add_argument("--input", default="")
    parser.add_argument("--out", default="")
    args = parser.parse_args()
    if args.sample:
        page = render(load(SAMPLE))
        print(page)
        return
    if not args.input or not args.out:
        fail("Pass --input and --out, or --sample.", 2)
    page = render(load(Path(args.input)))
    destination = Path(args.out)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(page)
    print(json.dumps({"ok": True, "out": str(destination)}))


if __name__ == "__main__":
    main()
