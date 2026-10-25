#!/usr/bin/env python3
"""Shared colors, status labels, and safe HTML helpers for Job Ledger visuals."""

from __future__ import annotations

import base64
import html
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent
CSS_PATH = ROOT / "assets" / "visual.css"
FONTS = ROOT / "assets" / "fonts"
SANS_FONT = FONTS / "SourceSans3-Regular.ttf"
SERIF_FONT = FONTS / "SourceSerif4-Regular.ttf"

IVORY = (247, 243, 236)
PAPER = (255, 252, 247)
FOREST = (31, 77, 58)
FOREST_INK = (23, 60, 45)
SAGE = (228, 237, 230)
CHARCOAL = (28, 26, 23)
MUTED = (94, 88, 78)
LINE = (227, 219, 208)
AMBER = (138, 90, 18)
AMBER_BG = (246, 231, 208)
RED = (140, 47, 47)
RED_BG = (246, 228, 224)

CONNECTION_STATUSES = {
    "not_checked",
    "needs_sign_in",
    "connected",
    "verification_required",
    "unavailable",
    "skipped",
}

CONFIRMATION_SOURCES = {"employer", "user_reported", "sample"}

STAGES = {"background", "connections", "ready"}

KNOWN_CONNECTIONS = [
    ("email", "Email", "Discover roles from alerts."),
    ("drive", "Drive", "Import project evidence."),
    ("canvas", "Canvas", "Add coursework and project materials."),
    ("notion", "Notion", "Notion is optional. Your applications are still saved in Job Ledger."),
    ("overleaf", "Overleaf", "Overleaf needs browser verification. Your source files are ready."),
    ("linkedin", "LinkedIn", "Optional discovery or outreach."),
]

STATUS_LABELS = {
    "not_checked": "Not checked",
    "needs_sign_in": "Needs sign-in",
    "verification_required": "Verification required",
    "unavailable": "Unavailable",
    "skipped": "Skipped",
}

DASHBOARD_GROUPS = [
    ("ready", "Ready to review", "Nothing is waiting for review."),
    ("action", "Needs your action", "Nothing needs you right now."),
    ("progress", "In progress", "Nothing is in progress."),
    ("applied", "Applied", "Nothing is marked applied."),
    ("screened", "Screened", ""),
]


def esc(value: object) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def safe_url(url: object) -> str:
    raw = str(url or "").strip()
    if not raw or any(char in raw for char in "\n\r\t "):
        return ""
    parts = urlsplit(raw)
    scheme = parts.scheme.lower()
    if scheme in {"http", "https", "mailto"}:
        return raw
    if scheme or raw.startswith("/") or raw.startswith("//") or "\\" in raw:
        return ""
    if ".." in raw.split("/"):
        return ""
    if re.fullmatch(r"[A-Za-z0-9._/-]+", raw):
        return raw
    return ""


def link_html(url: object, label: object | None = None) -> str:
    text = esc(url if label is None else label)
    safe = safe_url(url)
    if not text:
        return ""
    if not safe:
        return f"<span>{text}</span>"
    return f'<a href="{esc(safe)}">{text}</a>'


def initials(name: object) -> str:
    parts = [part for part in re.split(r"[^A-Za-z0-9]+", str(name or "")) if part]
    if not parts:
        return "?"
    if len(parts) == 1:
        return parts[0][:2].upper()
    return (parts[0][0] + parts[1][0]).upper()


def selected_names(connectors: object) -> set[str]:
    if isinstance(connectors, list):
        raw = ",".join(str(item) for item in connectors)
    else:
        raw = str(connectors or "")
    return {part.strip().casefold() for part in raw.split(",") if part.strip()}


def stored_connections(setup: dict) -> dict:
    stored = setup.get("connections") if isinstance(setup, dict) else None
    if not isinstance(stored, dict):
        return {}
    normalized = {}
    for key, value in stored.items():
        normalized[str(key).strip().casefold()] = value if isinstance(value, dict) else {}
    return normalized


def is_verified(entry: dict | None) -> bool:
    entry = entry or {}
    return entry.get("status") == "connected" and str(entry.get("checked_at") or "").strip() != ""


def connection_label(entry: dict | None, selected: bool = False) -> str:
    entry = entry or {}
    status = str(entry.get("status") or "not_checked").strip().casefold()
    if status == "connected" and str(entry.get("checked_at") or "").strip():
        return "Connected"
    if status == "connected":
        return "Needs sign-in"
    label = STATUS_LABELS.get(status, "Not checked")
    if selected and status == "not_checked":
        return "Selected, not checked"
    return label


def connection_rows(setup: dict | None) -> list[dict]:
    setup = setup or {}
    stored = stored_connections(setup)
    selected = selected_names(setup.get("connectors"))
    catalog = list(KNOWN_CONNECTIONS)
    known = {item[0] for item in catalog}
    for key in stored:
        if key not in known:
            catalog.append((key, key[:1].upper() + key[1:], ""))
    rows = []
    for key, label, benefit in catalog:
        entry = stored.get(key) or {}
        rows.append(
            {
                "key": key,
                "label": label,
                "benefit": benefit,
                "status": connection_label(entry, key in selected),
                "verified": is_verified(entry),
            }
        )
    return rows


def has_confirmation(role: dict) -> bool:
    return str(role.get("confirmation") or "").strip() != ""


def presentation_stage(status: object, confirmation: object = "") -> str:
    name = str(status or "").strip().casefold()
    if name == "applied":
        return "Applied" if str(confirmation or "").strip() else "Unconfirmed"
    return {
        "need to check": "Screened",
        "not a fit": "Screened",
        "skipped": "Screened",
        "kit ready": "Package ready",
        "filled": "Form prepared",
        "outreach sent": "In progress",
        "replied": "In progress",
        "interview": "In progress",
        "rejected": "Screened",
        "offer": "In progress",
    }.get(name, "Screened" if name else "Not started")


def dashboard_group(role: dict) -> str | None:
    status = str(role.get("status") or "").strip().casefold()
    if status == "applied" and has_confirmation(role):
        return "applied"
    if status in {"need to check", "filled"} or (status == "applied" and not has_confirmation(role)):
        return "action"
    if status in {"outreach sent", "replied", "interview", "offer"}:
        return "progress"
    if status == "kit ready":
        return "ready"
    if status in {"not a fit", "skipped", "rejected"}:
        return "screened"
    return None


def action_reason(role: dict) -> str:
    status = str(role.get("status") or "").strip().casefold()
    if status == "need to check":
        return "A screening question is still open."
    if status == "filled":
        return "The form is filled. Submission is not approved."
    if status == "applied" and not has_confirmation(role):
        return "Applied was saved without confirmation text."
    return ""


def confirmation_label(source: object, demo: bool = False) -> str:
    name = str(source or "").strip().casefold()
    if demo or name == "sample":
        return "Sample data"
    if name == "user_reported":
        return "User reported"
    if name == "employer":
        return "Employer page"
    return ""


def load_json(path: Path) -> dict:
    try:
        data = json.loads(Path(path).read_text())
    except (OSError, ValueError) as error:
        raise ValueError("The file is missing or is not JSON.") from error
    if not isinstance(data, dict):
        raise ValueError("The file must be a JSON object.")
    return data


def inline_css() -> str:
    css = CSS_PATH.read_text()

    def replace(match: re.Match) -> str:
        font = FONTS / match.group(1)
        if not font.is_file():
            return match.group(0)
        encoded = base64.b64encode(font.read_bytes()).decode("ascii")
        return f'url("data:font/ttf;base64,{encoded}")'

    return re.sub(r'url\("fonts/([^"]+)"\)', replace, css)


def page(title: str, body: str, body_class: str = "") -> str:
    class_attr = f' class="{esc(body_class)}"' if body_class else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<style>
{inline_css()}
</style>
</head>
<body{class_attr}>
{body}
</body>
</html>
"""


def font_candidates(kind: str) -> list[Path]:
    bundled = SERIF_FONT if kind == "serif" else SANS_FONT
    if kind == "serif":
        system = [
            Path("/System/Library/Fonts/Supplemental/Georgia.ttf"),
            Path("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"),
            Path("/usr/share/fonts/dejavu/DejaVuSerif.ttf"),
        ]
    else:
        system = [
            Path("/System/Library/Fonts/Supplemental/Arial.ttf"),
            Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
            Path("/usr/share/fonts/dejavu/DejaVuSans.ttf"),
        ]
    return [bundled, *system]
