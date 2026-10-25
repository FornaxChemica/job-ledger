#!/usr/bin/env python3
"""Conversation cards and the application dashboard.

Cards are phone-width PNGs drawn with Pillow. If Pillow cannot be imported,
the same command still writes an HTML card and reports that the image failed.
The demo command reads only assets/demo and writes only the folder you pass.
It does not read or write the application index.

Exit codes: 0 ok, 2 bad arguments or bad JSON.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from render_package import render as render_package
from visual_theme import (
    AMBER,
    AMBER_BG,
    CHARCOAL,
    DASHBOARD_GROUPS,
    FOREST,
    FOREST_INK,
    IVORY,
    LINE,
    MUTED,
    PAPER,
    SAGE,
    action_reason,
    confirmation_label,
    connection_rows,
    dashboard_group,
    esc,
    font_candidates,
    initials,
    link_html,
    load_json,
    page,
    presentation_stage,
    safe_url,
)

ROOT = Path(__file__).resolve().parent.parent
DEMO = ROOT / "assets" / "demo"
WIDTH = 780
PAD = 52
CARD_KINDS = {"welcome", "profile", "connections", "ready", "opportunity", "confirmation"}


def fail(message: str, code: int) -> None:
    print(message, file=sys.stderr)
    sys.exit(code)


def as_list(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item or "").strip()]


def clean(value: object) -> str:
    return " ".join(str(value or "").split())


def default_reply(kind: str, data: dict) -> str:
    if kind == "welcome":
        return "Reply with your resume and a job link."
    if kind == "profile":
        return "Reply with any corrections, or say this looks right."
    if kind == "connections":
        return "Reply with a connection to add, or say continue."
    if kind == "ready":
        return "Reply with a job link to review the first role."
    if kind == "opportunity":
        verdict = str(data.get("verdict") or "").casefold()
        if "not a fit" in verdict:
            return "Reply skip to leave this one."
        if "need to check" in verdict:
            return "Reply with the missing fact, or say skip."
        return "Reply prepare to build your package."
    if confirmation_label(data.get("confirmation_source"), bool(data.get("demo"))) == "Sample data":
        return "This is sample data. It does not record an application."
    return "Reply status to see the dashboard."


def line_pairs(pairs: list[tuple[str, object]]) -> list[dict]:
    rows = []
    for label, value in pairs:
        text = clean(value)
        if text:
            rows.append({"label": label, "value": text})
    return rows


def evidence_lines(items: object) -> list[str]:
    lines = []
    if not isinstance(items, list):
        return lines
    for item in items:
        if isinstance(item, dict):
            name = clean(item.get("name"))
            rest = [part for part in (clean(item.get("did")), clean(item.get("result"))) if part]
            detail = ". ".join(rest)
            text = f"{name}: {detail}" if name and detail else name or detail
        else:
            text = clean(item)
        if text:
            lines.append(text)
    return lines


def normalize_card(kind: str, data: dict) -> dict:
    if kind not in CARD_KINDS:
        raise ValueError("Card kind must be welcome, profile, connections, ready, opportunity, or confirmation.")
    demo = bool(data.get("demo"))
    model = {
        "kind": kind,
        "kicker": "Job Ledger",
        "title": "",
        "subtitle": "",
        "demo": demo,
        "initials": "",
        "pills": [],
        "lines": [],
        "bullets_label": "",
        "bullets": [],
        "empty_note": "",
        "note": None,
        "reply": str(data.get("reply") or default_reply(kind, data)),
    }
    if kind == "welcome":
        confirmed = as_list(data.get("confirmed"))
        model.update(
            {
                "title": "Your job search, one role at a time.",
                "lines": line_pairs(
                    [
                        ("What this does", data.get("value") or "Screen a role, prepare one package, and submit only after you approve it."),
                        ("Stage", data.get("stage") or "Your background"),
                        ("Next", data.get("next") or "Send a resume and a job link."),
                    ]
                ),
                "bullets_label": "Already confirmed" if confirmed else "",
                "bullets": confirmed,
                "empty_note": "" if confirmed else "Nothing is confirmed yet.",
            }
        )
    elif kind == "profile":
        profile = data.get("profile") if isinstance(data.get("profile"), dict) else data
        skills = as_list(profile.get("skills"))
        missing = as_list(profile.get("missing"))
        model.update(
            {
                "title": clean(profile.get("name")) or "Profile",
                "subtitle": "Confirm what Job Ledger will rely on.",
                "lines": line_pairs(
                    [
                        ("Education", profile.get("education")),
                        ("Target roles", profile.get("targets")),
                        ("Location", profile.get("location")),
                        ("Skills", ", ".join(skills)),
                    ]
                ),
                "bullets_label": "Evidence",
                "bullets": evidence_lines(profile.get("evidence")),
                "empty_note": "" if profile.get("evidence") else "No projects or experience are confirmed yet.",
                "note": {"label": "Still missing", "value": "; ".join(missing), "tone": "amber"} if missing else None,
            }
        )
    elif kind == "connections":
        model.update(
            {
                "title": "Optional connections",
                "subtitle": "Continue without connecting. A selection is not a sign-in.",
                "lines": line_pairs(
                    [(row["label"], f"{row['status']}. {row['benefit']}".strip()) for row in connection_rows(data)]
                ),
            }
        )
    elif kind == "ready":
        confirmed = as_list(data.get("confirmed"))
        model.update(
            {
                "title": "Ready for the first role.",
                "lines": line_pairs(
                    [
                        ("Stage", data.get("stage") or "Ready"),
                        ("Next", data.get("next") or "Review the first role."),
                    ]
                ),
                "bullets_label": "Saved",
                "bullets": confirmed,
            }
        )
    elif kind == "opportunity":
        verdict = clean(data.get("verdict"))
        status = str(data.get("status") or "").strip()
        if data.get("status_label"):
            stage = clean(data.get("status_label"))
        elif status:
            stage = presentation_stage(status, "")
        elif verdict:
            stage = "Screened"
        else:
            stage = "Not started"
        tone = "good"
        if "need to check" in verdict.casefold():
            tone = "amber"
        elif "not a fit" in verdict.casefold():
            tone = "quiet"
        gap = clean(data.get("gap"))
        model.update(
            {
                "title": clean(data.get("employer")) or "Role",
                "subtitle": clean(data.get("role")),
                "initials": initials(data.get("employer")),
                "pills": [{"text": verdict, "tone": tone}] if verdict else [],
                "lines": line_pairs(
                    [
                        ("Location", data.get("location")),
                        ("Source", data.get("source")),
                        ("Status", stage),
                    ]
                ),
                "bullets_label": "Why" if as_list(data.get("reasons")) else "",
                "bullets": as_list(data.get("reasons"))[:3],
                "note": {"label": "Still open", "value": gap, "tone": "amber"} if gap else None,
            }
        )
    else:
        label = confirmation_label(data.get("confirmation_source"), demo)
        confirmation = clean(data.get("confirmation"))
        if label == "Sample data":
            title = "Sample confirmation"
        elif label == "User reported":
            title = "You reported this confirmation"
        elif confirmation:
            title = "Submission confirmed"
        else:
            title = "No confirmation yet"
        model.update(
            {
                "title": title,
                "subtitle": clean(data.get("employer")),
                "lines": line_pairs(
                    [
                        ("Role", data.get("role")),
                        ("Confirmation", confirmation or "None recorded"),
                        ("How we know", label),
                    ]
                ),
            }
        )
    return model


def card_html(model: dict) -> str:
    pills = []
    for pill in model["pills"]:
        tone = pill.get("tone")
        css = "pill"
        if tone == "amber":
            css = "pill pill-amber"
        elif tone == "quiet":
            css = "pill pill-quiet"
        pills.append(f"<p class=\"{css}\">{esc(pill.get('text'))}</p>")
    lines = []
    for row in model["lines"]:
        lines.append(f"<li><span class=\"label\">{esc(row['label'])}</span> {esc(row['value'])}</li>")
    bullets = "".join(f"<li>{esc(item)}</li>" for item in model["bullets"])
    bullet_block = ""
    if model["bullets_label"] or bullets:
        label = f"<h2>{esc(model['bullets_label'])}</h2>" if model["bullets_label"] else ""
        bullet_block = f"{label}<ul class=\"clean\">{bullets}</ul>" if bullets else label
    empty = f"<p class=\"meta\">{esc(model['empty_note'])}</p>" if model["empty_note"] else ""
    note = ""
    if model["note"]:
        css = "note note-red" if model["note"].get("tone") == "red" else "note"
        note = f"<div class=\"{css}\"><p class=\"label\">{esc(model['note']['label'])}</p><p>{esc(model['note']['value'])}</p></div>"
    mark = f"<div class=\"mark\">{esc(model['initials'])}</div>" if model["initials"] else ""
    sample = "<p class=\"sample\">Sample data</p>" if model["demo"] else ""
    subtitle = f"<p class=\"role\">{esc(model['subtitle'])}</p>" if model["subtitle"] else ""
    body = f"""
<a class="skip" href="#card">Skip to the summary</a>
<main>
  <article class="sheet" id="card">
    <div class="sheet-body">
      <p class="brand">{esc(model["kicker"])}</p>
      {sample}
      {mark}
      <h1>{esc(model["title"])}</h1>
      {subtitle}
      {"".join(pills)}
      <ul class="facts">{"".join(lines)}</ul>
      {bullet_block}
      {empty}
      {note}
    </div>
    <p class="reply-band">{esc(model["reply"])}</p>
  </article>
</main>
"""
    return page(model["title"] or "Job Ledger", body, "card-page")


def load_font(kind: str, size: int):
    from PIL import ImageFont

    for path in font_candidates(kind):
        if path.is_file():
            try:
                return ImageFont.truetype(str(path), size=size)
            except OSError:
                continue
    return ImageFont.load_default(size=size)


def wrap_text(text: str, font, width: int, max_lines: int = 8) -> list[str]:
    raw = clean(text)
    if not raw:
        return []
    pieces: list[str] = []
    for word in raw.split(" "):
        if font.getlength(word) <= width:
            pieces.append(word)
            continue
        buf = ""
        for char in word:
            trial = buf + char
            if font.getlength(trial) <= width:
                buf = trial
            else:
                if buf:
                    pieces.append(buf)
                buf = char
        if buf:
            pieces.append(buf)
    lines: list[str] = []
    current = ""
    for piece in pieces:
        trial = piece if not current else f"{current} {piece}"
        if font.getlength(trial) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = piece
    if current:
        lines.append(current)
    if len(lines) <= max_lines:
        return lines
    kept = lines[:max_lines]
    last = kept[-1].rstrip("…")
    while last and font.getlength(last + "…") > width:
        last = last[:-1]
    kept[-1] = (last or "").rstrip() + "…"
    return kept


def text_block_height(lines: list[str], font, gap: int) -> int:
    if not lines:
        return 0
    return len(lines) * (font.size + gap) - gap


def draw_card(model: dict):
    from PIL import Image, ImageDraw

    title_font = load_font("serif", 54)
    body_font = load_font("sans", 32)
    small_font = load_font("sans", 28)
    content_width = WIDTH - PAD * 2
    gap = 10
    operations: list[tuple] = []
    y = 28

    def add_text(text: str, font, fill, max_lines: int = 8, space_after: int = 18, label: str = ""):
        nonlocal y
        lines = wrap_text(text, font, content_width, max_lines)
        if not lines:
            return
        height = text_block_height(lines, font, gap)
        operations.append(("text", y, lines, font, fill))
        y += height + space_after

    def add_label_value(label: str, value: str):
        nonlocal y
        add_text(label, small_font, MUTED, max_lines=2, space_after=4)
        add_text(value, body_font, CHARCOAL, max_lines=6, space_after=18)

    if model["demo"]:
        add_text("Sample data", small_font, AMBER, max_lines=1, space_after=16)
    add_text("JOB LEDGER", small_font, FOREST, max_lines=1, space_after=12)
    if model["initials"]:
        operations.append(("circle", y, model["initials"]))
        y += 100
    add_text(model["title"], title_font, CHARCOAL, max_lines=4, space_after=12)
    if model["subtitle"]:
        add_text(model["subtitle"], body_font, MUTED, max_lines=3, space_after=16)
    for pill in model["pills"]:
        operations.append(("pill", y, pill))
        y += 64
    for row in model["lines"]:
        add_label_value(row["label"], row["value"])
    if model["bullets_label"]:
        add_text(model["bullets_label"], small_font, MUTED, max_lines=1, space_after=8)
    for bullet in model["bullets"]:
        add_text("–  " + bullet, body_font, CHARCOAL, max_lines=4, space_after=12)
    if model["empty_note"]:
        add_text(model["empty_note"], body_font, MUTED, max_lines=3, space_after=12)
    if model["note"]:
        note_lines = wrap_text(model["note"]["value"], body_font, content_width - 36, 5)
        label_lines = wrap_text(model["note"]["label"], small_font, content_width - 36, 1)
        note_height = 28 + text_block_height(label_lines, small_font, 6) + 8 + text_block_height(note_lines, body_font, gap) + 28
        operations.append(("note", y, note_height, label_lines, note_lines, model["note"].get("tone")))
        y += note_height + 8

    reply_lines = wrap_text(model["reply"], body_font, content_width, 4) or ["Reply if you want to change something."]
    reply_height = 36 + text_block_height(reply_lines, body_font, gap) + 36
    height = max(y + reply_height, 420)
    if height > 4200:
        height = 4200
    image = Image.new("RGB", (WIDTH, height), IVORY)
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, WIDTH, 16), fill=FOREST)
    for op in operations:
        kind = op[0]
        if kind == "text":
            _, top, lines, font, fill = op
            cursor = top
            for line in lines:
                if cursor > height - reply_height - 8:
                    break
                draw.text((PAD, cursor), line, font=font, fill=fill)
                cursor += font.size + gap
        elif kind == "circle":
            _, top, letters = op
            draw.ellipse((PAD, top, PAD + 84, top + 84), fill=FOREST)
            draw.text((PAD + 42, top + 42), letters, font=small_font, fill=PAPER, anchor="mm")
        elif kind == "pill":
            _, top, pill = op
            text = clean(pill.get("text"))
            tone = pill.get("tone")
            fill = SAGE if tone == "good" else AMBER_BG if tone == "amber" else PAPER
            ink = FOREST_INK if tone == "good" else AMBER if tone == "amber" else CHARCOAL
            text_width = small_font.getlength(text)
            box = (PAD, top, PAD + text_width + 36, top + 48)
            draw.rounded_rectangle(box, radius=24, fill=fill, outline=LINE)
            draw.text((PAD + 18, top + 24), text, font=small_font, fill=ink, anchor="lm")
        elif kind == "note":
            _, top, note_height, label_lines, note_lines, tone = op
            fill = AMBER_BG if tone != "red" else (246, 228, 224)
            draw.rounded_rectangle((PAD, top, WIDTH - PAD, top + note_height), radius=16, fill=fill)
            cursor = top + 24
            for line in label_lines:
                draw.text((PAD + 18, cursor), line, font=small_font, fill=AMBER)
                cursor += small_font.size + 6
            cursor += 6
            for line in note_lines:
                draw.text((PAD + 18, cursor), line, font=body_font, fill=CHARCOAL)
                cursor += body_font.size + gap
    band_top = height - reply_height
    draw.rectangle((0, band_top, WIDTH, height), fill=SAGE)
    cursor = band_top + 32
    for line in reply_lines:
        draw.text((PAD, cursor), line, font=body_font, fill=FOREST_INK)
        cursor += body_font.size + gap
    return image


def write_card(kind: str, data: dict, png_path: Path) -> dict:
    model = normalize_card(kind, data)
    html_path = png_path.with_suffix(".html")
    html_path.parent.mkdir(parents=True, exist_ok=True)
    html_path.write_text(card_html(model))
    image_path = None
    image_error = None
    try:
        draw_card(model).save(png_path, "PNG")
        image_path = str(png_path)
    except Exception as error:
        image_error = f"Image rendering failed ({error.__class__.__name__}: {error}). The HTML card is the fallback."
        if png_path.exists():
            png_path.unlink()
    return {
        "ok": True,
        "mode": "sample" if data.get("demo") else "real",
        "wrote_state": False,
        "html": str(html_path),
        "image": image_path,
        "image_error": image_error,
    }


def role_bits(role: dict, demo_page: bool) -> str:
    status = presentation_stage(role.get("status"), role.get("confirmation"))
    bits = [esc(status)]
    source = confirmation_label(role.get("confirmation_source"), False)
    if str(role.get("status") or "").casefold() == "applied" and source:
        bits.append(esc(source))
    elif demo_page and str(role.get("confirmation_source") or "") == "sample":
        bits.append("Sample data")
    if str(role.get("updated") or "").strip():
        bits.append("Updated " + esc(role.get("updated")))
    return " · ".join(bits)


def render_dashboard(data: dict, generated_at: str = "") -> str:
    when = str(generated_at or data.get("generated_at") or "").strip() or "not recorded"
    demo = bool(data.get("demo"))
    roles = data.get("roles") if isinstance(data.get("roles"), list) else []
    grouped = {key: [] for key, _label, _empty in DASHBOARD_GROUPS}
    for role in roles:
        if not isinstance(role, dict):
            continue
        group = dashboard_group(role)
        if group in grouped:
            grouped[group].append(role)
    sections = []
    for key, label, empty in DASHBOARD_GROUPS:
        rows = grouped[key]
        if key == "screened" and not rows:
            continue
        blocks = []
        for role in rows:
            title = str(role.get("employer") or "Unknown employer")
            role_name = clean(role.get("role"))
            role_html = f"<p class=\"role\">{esc(role_name)}</p>" if role_name else ""
            reason = action_reason(role)
            reason_html = f"<p>{esc(reason)}</p>" if reason else ""
            links = []
            if safe_url(role.get("package_url")):
                links.append(link_html(role.get("package_url"), "Open package"))
            if safe_url(role.get("url")):
                links.append(link_html(role.get("url"), "Posting"))
            link_html_row = f"<p>{' · '.join(links)}</p>" if links else ""
            blocks.append(
                "<article class=\"row\">"
                f"<h3>{esc(title)}</h3>{role_html}"
                f"<p class=\"meta\">{role_bits(role, demo)}</p>"
                f"{reason_html}{link_html_row}</article>"
            )
        body = "\n".join(blocks) if blocks else f"<p class=\"empty\">{esc(empty)}</p>"
        sections.append(f"<section class=\"group\" data-group=\"{key}\"><h2>{esc(label)}</h2>{body}</section>")
    sample = "<p class=\"sample\">Sample data</p>" if demo else ""
    filters = [
        ("view-all", "All"),
        ("view-ready", "Ready to review"),
        ("view-action", "Needs your action"),
        ("view-progress", "In progress"),
        ("view-applied", "Applied"),
    ]
    inputs = []
    labels = []
    for index, (ident, label) in enumerate(filters):
        checked = " checked" if index == 0 else ""
        inputs.append(f'<input class="view-input" type="radio" name="view" id="{ident}"{checked}>')
        labels.append(f'<label for="{ident}">{esc(label)}</label>')
    body = f"""
{"".join(inputs)}
<div class="frame">
  <header class="mast">
    <p class="brand">Job Ledger</p>
    {sample}
    <h1>Applications</h1>
    <p class="snapshot">Generated {esc(when)}. This is a snapshot. Changes appear after Job Ledger builds this page again.</p>
  </header>
  <div class="filter-bar">{"".join(labels)}</div>
</div>
<main>
  {"".join(sections)}
</main>
"""
    return page("Job Ledger applications", body)


def result_payload(**payload: object) -> None:
    print(json.dumps({"wrote_state": False, **payload}, indent=2))


def command_card(kind: str, source: Path, destination: Path) -> None:
    if kind not in CARD_KINDS:
        fail("Card kind must be welcome, profile, connections, ready, opportunity, or confirmation.", 2)
    if destination.suffix.lower() != ".png":
        fail("Card --out must be a .png path. HTML is written beside it.", 2)
    try:
        data = load_json(source)
    except ValueError as error:
        fail(str(error), 2)
    result_payload(**write_card(kind, data, destination))


def command_dashboard(source: Path, destination: Path, generated_at: str) -> None:
    try:
        data = load_json(source)
    except ValueError as error:
        fail(str(error), 2)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(render_dashboard(data, generated_at))
    result_payload(
        ok=True,
        mode="sample" if data.get("demo") else "real",
        html=str(destination),
        image=None,
    )


def command_demo(destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    files = []
    cards = [
        ("welcome", "01-welcome.png"),
        ("profile", "02-profile.png"),
        ("connections", "03-connections.png"),
        ("ready", "04-setup-ready.png"),
        ("opportunity", "05-opportunity.png"),
        ("confirmation", "08-confirmation.png"),
    ]
    for kind, name in cards:
        try:
            data = load_json(DEMO / f"{kind}.json")
        except ValueError as error:
            fail(str(error), 2)
        written = write_card(kind, data, destination / name)
        files.append({"kind": kind, "html": written["html"], "image": written["image"], "image_error": written["image_error"]})
    for source_name, out_name in (("package.json", "06-package.html"), ("form_review.json", "07-form-review.html")):
        try:
            data = load_json(DEMO / source_name)
        except ValueError as error:
            fail(str(error), 2)
        target = destination / out_name
        target.write_text(render_package(data))
        files.append({"kind": source_name, "html": str(target), "image": None, "image_error": None})
    try:
        index = load_json(DEMO / "index.json")
    except ValueError as error:
        fail(str(error), 2)
    dashboard = destination / "09-dashboard.html"
    dashboard.write_text(render_dashboard(index))
    files.append({"kind": "dashboard", "html": str(dashboard), "image": None, "image_error": None})
    result_payload(ok=True, mode="sample", out=str(destination), files=files)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Render Job Ledger cards and the dashboard")
    sub = parser.add_subparsers(dest="command", required=True)

    card = sub.add_parser("card")
    card.add_argument("--kind", required=True)
    card.add_argument("--input", required=True)
    card.add_argument("--out", required=True)

    dashboard = sub.add_parser("dashboard")
    dashboard.add_argument("--input", required=True)
    dashboard.add_argument("--out", required=True)
    dashboard.add_argument("--generated-at", default="")

    demo = sub.add_parser("demo")
    demo.add_argument("--out", default="output/demo")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "card":
        command_card(args.kind, Path(args.input), Path(args.out))
    elif args.command == "dashboard":
        command_dashboard(Path(args.input), Path(args.out), args.generated_at)
    elif args.command == "demo":
        command_demo(Path(args.out))


if __name__ == "__main__":
    main()
