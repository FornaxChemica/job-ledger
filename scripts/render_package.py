#!/usr/bin/env python3
"""Fill assets/package.html into one review page.

--sample reads assets/sample_package.json, prints the page, and writes nothing.

Exit codes: 0 ok, 2 bad arguments or bad JSON.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from visual_theme import confirmation_label, esc, inline_css, link_html, presentation_stage, safe_url

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "assets" / "package.html"
SAMPLE = ROOT / "assets" / "sample_package.json"
SECTION = re.compile(r"<section\b[^>]*\bdata-section=\"([a-z]+)\"[^>]*>.*?</section>\s*", re.DOTALL)
FIT_STATES = {"supported", "needs_confirmation", "missing"}


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


def pretty_time(value: str) -> str:
    match = re.match(r"(\d{4})-(\d{2})-(\d{2})", value.strip())
    if not match:
        return value.strip()
    months = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
    year, month, day = match.groups()
    return f"{months[int(month) - 1]} {int(day)}, {year}"


def text_of(data: dict, *keys: str) -> str:
    for key in keys:
        value = str(data.get(key) or "").strip()
        if value:
            return str(data.get(key) or "")
    return ""


def verdict_class(verdict: str) -> str:
    name = verdict.casefold()
    if "not a fit" in name:
        return "pill pill-quiet"
    if "need to check" in name:
        return "pill pill-amber"
    return "pill"


def fit_label(state: str) -> str:
    return {
        "supported": "Supported",
        "needs_confirmation": "Needs confirmation",
        "missing": "Missing",
    }.get(state, "Needs confirmation")


def section_heading(number: str, title: str, hint: str) -> str:
    return (
        f"<h2><span class=\"index\">{esc(number)}</span> {esc(title)}</h2>"
        f"<p class=\"section-hint\">{esc(hint)}</p>"
    )


def qa_list(pairs: object, left: str, right: str, caption: str) -> str:
    if not isinstance(pairs, list):
        return ""
    rows = []
    for pair in pairs:
        if not isinstance(pair, dict):
            continue
        question = str(pair.get(left) or "").strip()
        answer = str(pair.get(right) or "").strip()
        if not question and not answer:
            continue
        note = str(pair.get("note") or "").strip()
        answer_html = f"<p class=\"answer\">{esc(answer)}</p>" if answer else ""
        note_html = (
            f"<aside class=\"hold\"><p class=\"caption\">Review note. Not sent.</p><p>{esc(note)}</p></aside>"
            if note
            else ""
        )
        rows.append(
            "<article class=\"qa\">"
            f"<h3>{esc(question)}</h3>"
            f"<p class=\"caption\">{esc(caption)}</p>"
            f"{answer_html}{note_html}"
            "</article>"
        )
    return "\n".join(rows)


def render_fit(rows: object, number: str) -> str:
    if not isinstance(rows, list):
        return ""
    blocks = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        state = str(row.get("state") or "needs_confirmation")
        if state not in FIT_STATES:
            state = "needs_confirmation"
        blocking = bool(row.get("blocking")) and state == "missing"
        evidence = str(row.get("evidence") or "").strip()
        source = str(row.get("source") or "").strip()
        open_gap = state in {"needs_confirmation", "missing"}
        body = ""
        note = ""
        if open_gap:
            note_label = "Blocking" if blocking else "Still open"
            note_class = "hold hold-blocking" if blocking else "hold"
            note = (
                f"<aside class=\"{note_class}\"><p class=\"caption\">{note_label}</p>"
                f"<p>{esc(evidence or 'This requirement is still open.')}</p></aside>"
            )
        elif evidence:
            body = f"<p>{esc(evidence)}</p>"
        source_html = f"<p class=\"meta\">{esc(source)}</p>" if source else ""
        state_class = "caption state-blocking" if blocking else "caption"
        blocks.append(
            "<article class=\"qa\">"
            f"<h3>{esc(row.get('requirement') or 'Requirement')}</h3>"
            f"<p class=\"{state_class}\">{esc(fit_label(state))}</p>"
            f"{body}{source_html}{note}"
            "</article>"
        )
    if not blocks:
        return ""
    heading = section_heading(
        number,
        "Evidence",
        "Each requirement sits next to a confirmed fact, or a gap that is still open.",
    )
    return heading + "\n".join(blocks)


def sheet_line(left: object, right: object = "", muted: bool = False) -> str:
    main = str(left or "").strip()
    side = str(right or "").strip()
    if not main and not side:
        return ""
    kind = " entry-sub" if muted else ""
    side_html = f"<span>{esc(side)}</span>" if side else ""
    return f"<p class=\"entry-line{kind}\"><strong>{esc(main)}</strong>{side_html}</p>"


def sheet_bullets(items: object) -> str:
    if not isinstance(items, list):
        return ""
    rows = [f"<li>{esc(item)}</li>" for item in items if str(item or "").strip()]
    if not rows:
        return ""
    return "<ul class=\"sheet-bullets\">" + "".join(rows) + "</ul>"


def resume_sheet(doc: dict) -> str:
    contact = str(doc.get("contact") or "").strip()
    contact_html = f"<p class=\"paper-contact\">{esc(contact)}</p>" if contact else ""
    sections = []
    for section in doc.get("sections") or []:
        if not isinstance(section, dict):
            continue
        title = str(section.get("title") or "").strip()
        body = []
        for line in section.get("lines") or []:
            text = str(line or "").strip()
            if text:
                body.append(f"<p class=\"skill-line\">{esc(text)}</p>")
        for entry in section.get("entries") or []:
            if not isinstance(entry, dict):
                continue
            body.append(sheet_line(entry.get("title"), entry.get("aside")))
            body.append(sheet_line(entry.get("subtitle"), entry.get("when"), muted=True))
            body.append(sheet_bullets(entry.get("bullets")))
        body_html = "".join(part for part in body if part)
        if not title and not body_html:
            continue
        heading = f"<h4>{esc(title)}</h4>" if title else ""
        sections.append(f"<section class=\"sheet-section\">{heading}{body_html}</section>")
    name = str(doc.get("name") or "").strip()
    name_html = f"<p class=\"paper-name\">{esc(name)}</p>" if name else ""
    return f"<div class=\"paper resume-sheet\">{name_html}{contact_html}{''.join(sections)}</div>"


def letter_sheet(doc: dict) -> str:
    left = str(doc.get("contact_left") or "").strip()
    right = str(doc.get("contact_right") or "").strip()
    name = str(doc.get("name") or "").strip()
    head = (
        "<header class=\"letter-head\">"
        f"<p class=\"letter-side\">{esc(left)}</p>"
        f"<p class=\"paper-name\">{esc(name)}</p>"
        f"<p class=\"letter-side right\">{esc(right)}</p>"
        "</header>"
    )
    date = str(doc.get("date") or "").strip()
    date_html = f"<p class=\"letter-date\">{esc(date)}</p>" if date else ""
    salutation = str(doc.get("salutation") or "").strip()
    salutation_html = f"<p>{esc(salutation)}</p>" if salutation else ""
    paragraphs = "".join(
        f"<p>{esc(paragraph)}</p>" for paragraph in (doc.get("paragraphs") or []) if str(paragraph or "").strip()
    )
    close = str(doc.get("close") or "").strip()
    signature = str(doc.get("signature") or "").strip()
    close_html = f"<p class=\"letter-close\">{esc(close)}</p>" if close else ""
    signature_html = f"<p class=\"letter-sign\">{esc(signature)}</p>" if signature else ""
    return (
        f"<div class=\"paper letter\">{head}{date_html}{salutation_html}"
        f"{paragraphs}{close_html}{signature_html}</div>"
    )


def document_block(title: str, text: str, url: object, link_label: str) -> str:
    link = ""
    if str(url or "").strip() and safe_url(url):
        link = f"<p class=\"doc-link\">{link_html(url, link_label)}</p>"
    lines = text.replace("\r\n", "\n").split("\n")
    first = lines[0].strip() if lines else ""
    rest = "\n".join(lines[1:]).strip("\n")
    name_html = ""
    body = text
    if first and len(first) <= 48 and ":" not in first and len(lines) > 1:
        name_html = f"<p class=\"paper-name\">{esc(first)}</p>"
        body = rest
    return (
        f"<article class=\"doc\"><h3>{esc(title)}</h3>{link}"
        f"<div class=\"paper\">{name_html}<pre class=\"paper-body\">{esc(body)}</pre></div></article>"
    )


def render_documents(data: dict, number: str) -> str:
    chunks = []
    resume_doc = data.get("resume_doc")
    cover_doc = data.get("cover_doc")
    if isinstance(resume_doc, dict) and (resume_doc.get("sections") or resume_doc.get("name")):
        link = ""
        if safe_url(data.get("resume_url")):
            link = f"<p class=\"doc-link\">{link_html(data.get('resume_url'), 'Open resume file')}</p>"
        chunks.append(f"<article class=\"doc\"><h3>Resume text</h3>{link}{resume_sheet(resume_doc)}</article>")
    else:
        resume = text_of(data, "resume", "resume_text")
        if resume.strip():
            chunks.append(document_block("Resume text", resume, data.get("resume_url"), "Open resume file"))
    if isinstance(cover_doc, dict) and (cover_doc.get("paragraphs") or cover_doc.get("name")):
        link = ""
        if safe_url(data.get("cover_url")):
            link = f"<p class=\"doc-link\">{link_html(data.get('cover_url'), 'Open cover letter file')}</p>"
        chunks.append(f"<article class=\"doc\"><h3>Cover letter text</h3>{link}{letter_sheet(cover_doc)}</article>")
    else:
        cover = text_of(data, "cover", "cover_text")
        if cover.strip():
            chunks.append(document_block("Cover letter text", cover, data.get("cover_url"), "Open cover letter file"))
    changes = str(data.get("changes") or "").strip()
    if changes:
        chunks.append(f"<aside class=\"hold\"><p class=\"caption\">What changed</p><p>{esc(changes)}</p></aside>")
    links = []
    sources = data.get("source_files") or []
    if isinstance(sources, list):
        for item in sources:
            if isinstance(item, str) and safe_url(item):
                links.append(f"<li>{link_html(item, item)}</li>")
            elif isinstance(item, dict) and safe_url(item.get("url")):
                links.append(f"<li>{link_html(item.get('url'), item.get('name') or item.get('url'))}</li>")
    if links:
        chunks.append("<div class=\"doc\"><h3>Source files</h3><ul class=\"clean\">" + "".join(links) + "</ul></div>")
    if not chunks:
        return ""
    heading = section_heading(
        number,
        "Documents",
        "Resume and cover letter as text. A file link appears only when one was provided.",
    )
    return heading + "\n".join(chunks)


def string_list(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item or "").strip()]


def default_approval(data: dict, fields_html: str) -> dict:
    confirmation = str(data.get("confirmation") or "").strip()
    source = str(data.get("confirmation_source") or "").strip().casefold()
    if confirmation and source == "sample":
        return {
            "package": "Sample",
            "form": "Sample",
            "submit": "Not a real submission",
            "confirmed": "Sample data",
        }
    if confirmation and source == "user_reported":
        return {
            "package": "Approved",
            "form": "Filled",
            "submit": "User reported",
            "confirmed": "User reported",
        }
    if confirmation:
        confirmed = "Employer page" if source == "employer" else "Confirmation text is present"
        return {
            "package": "Approved",
            "form": "Filled",
            "submit": "Approved",
            "confirmed": confirmed,
        }
    if fields_html:
        return {
            "package": "Approved",
            "form": "Filled, not submitted",
            "submit": "Not approved",
            "confirmed": "No",
        }
    return {
        "package": "Waiting for you",
        "form": "Not filled",
        "submit": "Not approved",
        "confirmed": "No",
    }


def default_return(data: dict, fields_html: str) -> str:
    explicit = str(data.get("return_copy") or "").strip()
    if explicit:
        return explicit
    source = str(data.get("confirmation_source") or "").strip().casefold()
    if str(data.get("confirmation") or "").strip() and source == "sample":
        return "This page is sample data. Return to Cubbie. It does not submit an application."
    if str(data.get("confirmation") or "").strip():
        return "Return to Cubbie and reply status to see the dashboard."
    if fields_html:
        return "Return to Cubbie and reply yes to submit, or no to stop."
    return "Return to Cubbie and reply 'use this package'."


def render_review(data: dict, fields_html: str, number: str) -> str:
    approval = data.get("approval") if isinstance(data.get("approval"), dict) else None
    if approval is None:
        approval = default_approval(data, fields_html)
    rows = []
    for key, label in (
        ("package", "Package"),
        ("form", "Employer form"),
        ("submit", "Submission"),
        ("confirmed", "Confirmation"),
    ):
        if str(approval.get(key) or "").strip():
            rows.append(f"<div><dt>{esc(label)}</dt><dd>{esc(approval.get(key))}</dd></div>")
    attachments = string_list(data.get("attachments"))
    missing = string_list(data.get("missing"))
    confirmation = str(data.get("confirmation") or "").strip()
    source = str(data.get("confirmation_source") or "").strip().casefold()
    if confirmation and source == "sample":
        hold = "This confirmation is sample data. It does not record an application."
    elif fields_html:
        hold = "The form is filled and has not been submitted."
    else:
        hold = "Nothing has been submitted. This page is for review."
    parts = [
        section_heading(
            number,
            "Before you decide",
            "What is ready, what is still open, and the reply that moves this forward.",
        ),
        f"<aside class=\"hold\"><p class=\"caption\">Preparation</p><p>{esc(hold)}</p></aside>",
    ]
    if rows:
        parts.append("<dl class=\"facts-row\">" + "".join(rows) + "</dl>")
    if attachments:
        parts.append("<h3>Attachments</h3><ul class=\"clean\">" + "".join(f"<li>{esc(item)}</li>" for item in attachments) + "</ul>")
    if missing:
        parts.append(
            "<aside class=\"hold\"><p class=\"caption\">Still open</p><ul class=\"clean\">"
            + "".join(f"<li>{esc(item)}</li>" for item in missing)
            + "</ul></aside>"
        )
    parts.append(f"<p class=\"next-step\"><span class=\"caption\">Next</span> {esc(default_return(data, fields_html))}</p>")
    return "\n".join(parts)


def render_overview(data: dict, number: str) -> str:
    parts = [
        section_heading(
            number,
            "The role",
            "What the posting says, and where this application stands.",
        )
    ]
    verdict = str(data.get("verdict") or "").strip()
    if verdict:
        parts.append(f"<p class=\"{verdict_class(verdict)}\">{esc(verdict)}</p>")
    quote = str(data.get("quote") or "").strip()
    if quote:
        section = str(data.get("section") or "").strip()
        section_html = f"<p class=\"meta\">{esc(section)}</p>" if section else ""
        parts.append(f"<blockquote><p>{esc(quote)}</p>{section_html}</blockquote>")
    link = data.get("link") if str(data.get("link") or "").strip() else data.get("url")
    if str(link or "").strip():
        parts.append(f"<p class=\"posting\">{link_html(link)}</p>")
    facts = []
    if str(data.get("status") or "").strip() or str(data.get("confirmation") or "").strip():
        facts.append(("Stage", presentation_stage(data.get("status"), data.get("confirmation"))))
    if str(data.get("deadline") or "").strip():
        facts.append(("Deadline", str(data.get("deadline"))))
    if facts:
        parts.append(
            "<dl class=\"facts-row\">"
            + "".join(f"<div><dt>{esc(label)}</dt><dd>{esc(value)}</dd></div>" for label, value in facts)
            + "</dl>"
        )
    if len(parts) == 1:
        parts.append("<p>No posting details were provided.</p>")
    return "\n".join(parts)


def render_confirmation(data: dict, number: str) -> str:
    confirmation = str(data.get("confirmation") or "").strip()
    if not confirmation:
        return ""
    label = confirmation_label(data.get("confirmation_source"), bool(data.get("demo")))
    label_html = f"<p class=\"caption\">{esc(label)}</p>" if label else ""
    return (
        section_heading(number, "Confirmation", "The words that recorded the outcome, and where they came from.")
        + label_html
        + f"<div class=\"paper\"><pre class=\"paper-body\">{esc(confirmation)}</pre></div>"
    )


def render(data: dict) -> str:
    page = TEMPLATE.read_text()
    demo = bool(data.get("demo")) or str(data.get("confirmation_source") or "").strip().casefold() == "sample"
    employer = str(data.get("employer") or "Application")
    role = str(data.get("role") or "")
    if "prepared_answers" in data:
        prepared = data.get("prepared_answers") or []
    else:
        prepared = data.get("answers") or []
    answers = qa_list(prepared, "q", "a", "Prepared for review. Not read off the employer form.")
    fields = qa_list(data.get("fields") or [], "label", "value", "Seen on the employer form.")
    confirmation = render_confirmation(data, "0")
    present = [
        ("overview", "The role", True),
        ("fit", "Evidence", bool(data.get("fit"))),
        ("documents", "Documents", bool(render_documents(data, "0"))),
        ("answers", "Prepared answers", bool(answers)),
        ("fields", "Observed on the form", bool(fields)),
        ("review", "Before you decide", True),
        ("confirmation", "Confirmation", bool(confirmation)),
    ]
    # fit and documents need a real emptiness check. render_documents("") still returns heading if chunks exist.
    # Recompute documents and fit once with final numbers below.
    visible_keys = []
    for key, _label, show in present:
        if key == "fit":
            show = bool(render_fit(data.get("fit") or [], "0"))
        if show:
            visible_keys.append(key)
    numbers = {key: str(index) for index, key in enumerate(visible_keys, start=1)}
    fit = render_fit(data.get("fit") or [], numbers.get("fit", ""))
    documents = render_documents(data, numbers.get("documents", ""))
    answers_html = ""
    if answers:
        answers_html = section_heading(
            numbers["answers"],
            "Prepared answers",
            "Written for the form. These are not values read off the employer page.",
        ) + answers
    fields_html = ""
    if fields:
        fields_html = section_heading(
            numbers["fields"],
            "Observed on the form",
            "Values seen on the filled employer form.",
        ) + fields
    confirmation = render_confirmation(data, numbers.get("confirmation", ""))
    nav = '<nav class="packet-nav" aria-label="On this page">' + "".join(
        f'<a href="#{key}">{esc(label)}</a>'
        for key, label, _show in present
        if key in numbers
    ) + "</nav>"
    subtitle_bits = [part for part in (role, str(data.get("location") or "").strip()) if part]
    updated = str(data.get("updated") or "").strip()
    top_bits = []
    if demo:
        top_bits.append("<span class=\"sample\">Sample data</span>")
    if updated:
        top_bits.append(esc(pretty_time(updated)))
    title = employer if not role else f"{employer} — {role}"
    replacements = {
        "STYLE": inline_css(),
        "TITLE": esc(title),
        "TOPMETA": " ".join(top_bits),
        "NAV": nav,
        "EMPLOYER": esc(employer),
        "SUBTITLE": esc(" · ".join(subtitle_bits)),
        "OVERVIEW": render_overview(data, numbers["overview"]),
        "FIT": fit,
        "DOCUMENTS": documents,
        "ANSWERS": answers_html,
        "FIELDS": fields_html,
        "REVIEW": render_review(data, fields, numbers["review"]),
        "CONFIRMATION": confirmation,
    }
    for token, value in replacements.items():
        page = page.replace("{{" + token + "}}", value)

    drop = {key for key, _label, _show in present if key not in numbers}

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
        print(render(load(SAMPLE)))
        return
    if not args.input or not args.out:
        fail("Pass --input and --out, or --sample.", 2)
    incoming = load(Path(args.input))
    destination = Path(args.out)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(render(incoming))
    mode = "sample" if incoming.get("demo") or str(incoming.get("confirmation_source") or "") == "sample" else "real"
    print(json.dumps({"ok": True, "mode": mode, "wrote_state": False, "out": str(destination)}))


if __name__ == "__main__":
    main()
