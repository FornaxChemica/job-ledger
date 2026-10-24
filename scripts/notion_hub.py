#!/usr/bin/env python3
"""Notion hub: one checklist page plus one row per job id.

Uses the student's NOTION_API_KEY. The command must name that variable so Cubbie
can pass it. --sample reads assets/sample_applications.json, contacts nothing,
and writes nothing.

Exit codes: 0 ok, 2 bad arguments, 3 key missing, 4 Notion unreachable,
5 key rejected, 6 page not shared or hub not set up, 7 other Notion error.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

API = "https://api.notion.com/v1"
SAMPLE = Path(__file__).resolve().parent.parent / "assets" / "sample_applications.json"
HEX = re.compile(r"[0-9a-fA-F]")


def fail(message: str, code: int) -> None:
    print(message, file=sys.stderr)
    sys.exit(code)


def config_path() -> Path:
    root = Path(os.environ.get("SKILL_DATA_DIR") or Path.home() / ".config" / "job-ledger")
    return root / "notion.json"


def load_config() -> dict:
    path = config_path()
    try:
        data = json.loads(path.read_text())
    except FileNotFoundError:
        return {}
    except (OSError, ValueError):
        fail("Could not read notion.json. It was left untouched.", 6)
    return data if isinstance(data, dict) else {}


def save_config(data: dict) -> None:
    path = config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = json.dumps(data, indent=2) + "\n"
    json.loads(raw)
    temporary = path.with_suffix(".json.tmp")
    temporary.write_text(raw)
    json.loads(temporary.read_text())
    temporary.replace(path)


def page_id(value: str) -> str:
    raw = "".join(HEX.findall(value.split("?")[0]))
    if len(raw) < 32:
        fail("That Notion link has no page id.", 2)
    raw = raw[-32:].lower()
    return f"{raw[0:8]}-{raw[8:12]}-{raw[12:16]}-{raw[16:20]}-{raw[20:32]}"


def key_or_fail() -> str:
    key = os.environ.get("NOTION_API_KEY", "").strip()
    if not key:
        fail("NOTION_API_KEY is not set. Ask the student to save their Notion integration key.", 3)
    return key


def api(method: str, path: str, body: dict | None, key: str) -> dict:
    payload = None if body is None else json.dumps(body).encode()
    request = urllib.request.Request(
        API + path,
        data=payload,
        method=method,
        headers={
            "Authorization": f"Bearer {key}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as exc:
        if exc.code == 401:
            fail("Notion rejected the API key.", 5)
        if exc.code == 404:
            fail("Notion could not see that page. Share the parent page with the integration.", 6)
        fail(f"Notion returned HTTP {exc.code}.", 7)
    except urllib.error.URLError:
        fail("Could not reach Notion. Try again later.", 4)


def rich(value: str) -> dict:
    return {"rich_text": [{"type": "text", "text": {"content": (value or "")[:1900]}}]}


def paragraph(text: str) -> dict:
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {"rich_text": [{"type": "text", "text": {"content": text[:1900]}}]},
    }


def emit(payload: dict) -> None:
    print(json.dumps(payload, indent=2))


def sample_roles() -> list[dict]:
    data = json.loads(SAMPLE.read_text())
    return list(data.get("roles") or [])


def command_lookup(args: argparse.Namespace) -> None:
    if args.sample:
        found = next(
            (
                role for role in sample_roles()
                if role.get("namespace") == args.namespace and str(role.get("job_id")) == args.job_id
            ),
            None,
        )
        if found is None:
            emit({"ok": True, "found": False, "sample": True})
        else:
            emit({
                "ok": True,
                "found": True,
                "sample": True,
                "status": found.get("status"),
                "employer": found.get("employer"),
                "namespace": found.get("namespace"),
                "job_id": found.get("job_id"),
            })
        return

    config = load_config()
    database_id = config.get("database_id")
    if not database_id:
        fail("Notion hub is not set up. Run init, or tell the student the hub is off.", 6)
    result = api(
        "POST",
        f"/databases/{database_id}/query",
        {
            "filter": {
                "and": [
                    {"property": "Job ID", "rich_text": {"equals": args.job_id}},
                    {"property": "Namespace", "rich_text": {"equals": args.namespace}},
                ]
            },
            "page_size": 1,
        },
        key_or_fail(),
    )
    rows = result.get("results") or []
    if not rows:
        emit({"ok": True, "found": False})
        return
    props = rows[0].get("properties") or {}

    def plain(prop: dict) -> str:
        chunks = prop.get("rich_text") or []
        return "".join(chunk.get("plain_text", "") for chunk in chunks)

    emit({
        "ok": True,
        "found": True,
        "status": plain(props.get("Status") or {}),
        "employer": "".join(
            chunk.get("plain_text", "") for chunk in (props.get("Employer") or {}).get("title") or []
        ),
        "namespace": plain(props.get("Namespace") or {}),
        "job_id": plain(props.get("Job ID") or {}),
    })


def properties(args: argparse.Namespace) -> dict:
    props = {
        "Employer": {"title": [{"type": "text", "text": {"content": args.employer[:1900]}}]},
        "Job ID": rich(args.job_id),
        "Namespace": rich(args.namespace),
        "Status": rich(args.status),
    }
    if args.url:
        props["Link"] = {"url": args.url}
    if args.quote:
        props["Quote"] = rich(args.quote)
    if args.package_url:
        props["Package"] = {"url": args.package_url}
    if args.overleaf_url:
        props["Overleaf"] = {"url": args.overleaf_url}
    if args.confirmation:
        props["Confirmation"] = rich(args.confirmation)
    return props


def command_upsert(args: argparse.Namespace) -> None:
    if args.status == "applied" and not (args.confirmation or "").strip():
        fail("Applied requires the confirmation text the employer page showed.", 2)
    if args.sample:
        emit({"ok": True, "sample": True, "wrote": False, "status": args.status, "job_id": args.job_id})
        return
    config = load_config()
    database_id = config.get("database_id")
    if not database_id:
        fail("Notion hub is not set up. Run init, or tell the student the hub is off.", 6)
    key = key_or_fail()
    existing = api(
        "POST",
        f"/databases/{database_id}/query",
        {
            "filter": {
                "and": [
                    {"property": "Job ID", "rich_text": {"equals": args.job_id}},
                    {"property": "Namespace", "rich_text": {"equals": args.namespace}},
                ]
            },
            "page_size": 1,
        },
        key,
    )
    rows = existing.get("results") or []
    props = properties(args)
    if rows:
        api("PATCH", f"/pages/{rows[0]['id']}", {"properties": props}, key)
        emit({"ok": True, "updated": True, "job_id": args.job_id})
        return
    api(
        "POST",
        "/pages",
        {"parent": {"database_id": database_id}, "properties": props},
        key,
    )
    emit({"ok": True, "created": True, "job_id": args.job_id})


def hub_lines(args: argparse.Namespace) -> list[str]:
    return [
        f"Cadence: {args.cadence or 'not set'}",
        f"Referral: {args.referral or 'not set'}",
        f"Package format: {args.package_format or 'html'}",
        f"School: {args.school or 'not set'}",
        f"Connectors: {args.connectors or 'not set'}",
        f"Resume tool: {args.resume_tool or 'not set'}",
        f"Overleaf: {args.overleaf or 'not set'}",
        f"Resume: {args.resume_url or 'not set'}",
        f"Cover letter: {args.cover_url or 'not set'}",
        f"LaTeX source: {args.tex_url or 'not set'}",
        f"Story bank: {args.bank or 'not set'}",
    ]


def command_init(args: argparse.Namespace) -> None:
    parent = page_id(args.parent)
    if args.sample:
        emit({"ok": True, "sample": True, "wrote": False, "parent": parent, "would_create": ["Hub", "Applications"]})
        return
    key = key_or_fail()
    hub = api(
        "POST",
        "/pages",
        {
            "parent": {"page_id": parent},
            "properties": {"title": {"title": [{"type": "text", "text": {"content": "Job Ledger hub"}}]}},
            "children": [paragraph("Hub created. Setup fields are written here.")],
        },
        key,
    )
    database = api(
        "POST",
        "/databases",
        {
            "parent": {"type": "page_id", "page_id": parent},
            "title": [{"type": "text", "text": {"content": "Applications"}}],
            "properties": {
                "Employer": {"title": {}},
                "Job ID": {"rich_text": {}},
                "Namespace": {"rich_text": {}},
                "Status": {"rich_text": {}},
                "Link": {"url": {}},
                "Quote": {"rich_text": {}},
                "Package": {"url": {}},
                "Overleaf": {"url": {}},
                "Confirmation": {"rich_text": {}},
            },
        },
        key,
    )
    save_config({
        "parent_page_id": parent,
        "hub_page_id": hub.get("id"),
        "hub_url": hub.get("url"),
        "database_id": database.get("id"),
        "database_url": database.get("url"),
    })
    emit({"ok": True, "hub_url": hub.get("url"), "database_url": database.get("url")})


def command_hub_set(args: argparse.Namespace) -> None:
    lines = hub_lines(args)
    if args.sample:
        emit({"ok": True, "sample": True, "wrote": False, "lines": lines})
        return
    config = load_config()
    hub_id = config.get("hub_page_id")
    if not hub_id:
        fail("Notion hub is not set up. Run init, or tell the student the hub is off.", 6)
    key = key_or_fail()
    children = api("GET", f"/blocks/{hub_id}/children?page_size=100", None, key)
    for block in children.get("results") or []:
        api("DELETE", f"/blocks/{block['id']}", None, key)
    api("PATCH", f"/blocks/{hub_id}/children", {"children": [paragraph(line) for line in lines]}, key)
    emit({"ok": True, "updated": True})


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Job Ledger Notion hub")
    parser.add_argument("--sample", action="store_true")
    sub = parser.add_subparsers(dest="command", required=True)

    lookup = sub.add_parser("lookup")
    lookup.add_argument("--employer", required=True)
    lookup.add_argument("--namespace", required=True)
    lookup.add_argument("--job-id", required=True)

    upsert = sub.add_parser("upsert")
    upsert.add_argument("--employer", required=True)
    upsert.add_argument("--namespace", required=True)
    upsert.add_argument("--job-id", required=True)
    upsert.add_argument("--status", required=True)
    upsert.add_argument("--url", default="")
    upsert.add_argument("--quote", default="")
    upsert.add_argument("--package-url", default="")
    upsert.add_argument("--overleaf-url", default="")
    upsert.add_argument("--confirmation", default="")

    init = sub.add_parser("init")
    init.add_argument("--parent", required=True)

    hub = sub.add_parser("hub-set")
    hub.add_argument("--cadence", default="")
    hub.add_argument("--referral", default="")
    hub.add_argument("--package-format", default="")
    hub.add_argument("--school", default="")
    hub.add_argument("--connectors", default="")
    hub.add_argument("--resume-tool", default="")
    hub.add_argument("--overleaf", default="")
    hub.add_argument("--resume-url", default="")
    hub.add_argument("--cover-url", default="")
    hub.add_argument("--tex-url", default="")
    hub.add_argument("--bank", default="")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "lookup":
        command_lookup(args)
    elif args.command == "upsert":
        command_upsert(args)
    elif args.command == "init":
        command_init(args)
    elif args.command == "hub-set":
        command_hub_set(args)


if __name__ == "__main__":
    main()
