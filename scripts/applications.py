#!/usr/bin/env python3
"""Local index of roles, setup, and the story bank.

Lookup is by employer plus a namespaced job id. A title is never a key.
Sample mode reads assets/sample_applications.json and writes nothing.

Exit codes: 0 ok, 2 bad arguments, 9 applied status without a confirmation,
10 the saved file is corrupt and was left untouched.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

STATUSES = {
    "skipped",
    "not a fit",
    "need to check",
    "kit ready",
    "filled",
    "applied",
    "outreach sent",
    "replied",
    "interview",
    "rejected",
    "offer",
}
SKIP = {"skipped", "not a fit", "applied"}
SAMPLE = Path(__file__).resolve().parent.parent / "assets" / "sample_applications.json"


def fail(message: str, code: int) -> None:
    print(message, file=sys.stderr)
    sys.exit(code)


def empty_state() -> dict:
    return {"roles": [], "setup": {}, "bank": []}


def state_path() -> Path:
    root = Path(os.environ.get("SKILL_DATA_DIR") or Path.home() / ".config" / "job-ledger")
    return root / "applications.json"


def load_file(path: Path) -> dict:
    try:
        data = json.loads(path.read_text())
    except FileNotFoundError:
        return empty_state()
    except (OSError, ValueError):
        fail(f"Could not read {path.name}. The last saved file was left untouched.", 10)
    if not isinstance(data, dict):
        fail(f"{path.name} is not a saved index. It was left untouched.", 10)
    data.setdefault("roles", [])
    data.setdefault("setup", {})
    data.setdefault("bank", [])
    return data


def save_file(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = json.dumps(data, indent=2) + "\n"
    json.loads(raw)
    temporary = path.with_suffix(".json.tmp")
    temporary.write_text(raw)
    json.loads(temporary.read_text())
    temporary.replace(path)


def key_of(role: dict) -> tuple[str, str, str]:
    return (
        str(role.get("employer") or "").casefold(),
        str(role.get("namespace") or "").casefold(),
        str(role.get("job_id") or ""),
    )


def find_role(state: dict, employer: str, namespace: str, job_id: str) -> dict | None:
    wanted = (employer.casefold(), namespace.casefold(), job_id)
    for role in state["roles"]:
        if key_of(role) == wanted:
            return role
    return None


def company_count(state: dict, employer: str) -> int:
    name = employer.casefold()
    return sum(1 for role in state["roles"] if str(role.get("employer") or "").casefold() == name)


def emit(payload: dict) -> None:
    print(json.dumps(payload, indent=2))


def command_lookup(args: argparse.Namespace, state: dict) -> None:
    role = find_role(state, args.employer, args.namespace, args.job_id)
    count = company_count(state, args.employer)
    if role is None:
        emit({"action": "ask", "same_company_count": count, "role": None})
        return
    status = role.get("status")
    action = "skip" if status in SKIP else "resume"
    emit({"action": action, "same_company_count": count, "role": role})


def command_upsert(args: argparse.Namespace, state: dict) -> None:
    if args.status not in STATUSES:
        fail("Status must be one of: " + ", ".join(sorted(STATUSES)) + ".", 2)
    if args.status == "applied" and not (args.confirmation or "").strip():
        fail("Applied requires the confirmation text the employer page showed.", 9)
    role = find_role(state, args.employer, args.namespace, args.job_id)
    if role is None:
        role = {
            "employer": args.employer,
            "namespace": args.namespace,
            "job_id": args.job_id,
        }
        state["roles"].append(role)
    role["status"] = args.status
    if args.url:
        role["url"] = args.url
    if args.quote:
        role["quote"] = args.quote
    if args.section:
        role["section"] = args.section
    if args.package_url:
        role["package_url"] = args.package_url
    if args.overleaf_url:
        role["overleaf_url"] = args.overleaf_url
    if args.confirmation is not None:
        role["confirmation"] = args.confirmation
    if args.updated:
        role["updated"] = args.updated
    emit({"saved": True, "role": role, "same_company_count": company_count(state, args.employer)})


def command_save_setup(args: argparse.Namespace, state: dict) -> None:
    setup = state["setup"]
    for field in ("cadence", "referral", "package_format", "school", "connectors", "resume_tool"):
        value = getattr(args, field)
        if value:
            setup[field] = value
    emit({"saved": True, "setup": setup})


def command_show_setup(state: dict) -> None:
    emit(state.get("setup") or {})


def command_save_bank(args: argparse.Namespace, state: dict) -> None:
    try:
        incoming = json.loads(Path(args.file).read_text())
    except (OSError, ValueError):
        fail("The bank file is missing or is not JSON.", 2)
    if isinstance(incoming, dict):
        incoming = incoming.get("bank", incoming.get("projects"))
    if not isinstance(incoming, list) or any(not isinstance(item, dict) or "name" not in item for item in incoming):
        fail("The bank file must be a list of objects with a name.", 2)
    state["bank"] = incoming
    emit({"saved": True, "count": len(incoming)})


def command_show_bank(state: dict) -> None:
    emit({"bank": state.get("bank") or []})


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Local Job Ledger index")
    parser.add_argument("--sample", action="store_true", help="Read the bundled sample and write nothing")
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
    upsert.add_argument("--section", default="")
    upsert.add_argument("--package-url", default="")
    upsert.add_argument("--overleaf-url", default="")
    upsert.add_argument("--confirmation", default=None)
    upsert.add_argument("--updated", default="")

    setup = sub.add_parser("save-setup")
    setup.add_argument("--cadence", default="")
    setup.add_argument("--referral", default="")
    setup.add_argument("--package-format", default="")
    setup.add_argument("--school", default="")
    setup.add_argument("--connectors", default="")
    setup.add_argument("--resume-tool", default="")

    sub.add_parser("show-setup")

    bank = sub.add_parser("save-bank")
    bank.add_argument("--file", required=True)

    sub.add_parser("show-bank")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.sample:
        state = load_file(SAMPLE)
    else:
        path = state_path()
        state = load_file(path)

    if args.command == "lookup":
        command_lookup(args, state)
        return
    if args.command == "show-setup":
        command_show_setup(state)
        return
    if args.command == "show-bank":
        command_show_bank(state)
        return

    if args.sample:
        if args.command == "upsert":
            command_upsert(args, state)
        elif args.command == "save-setup":
            command_save_setup(args, state)
        elif args.command == "save-bank":
            command_save_bank(args, state)
        print("Sample mode wrote nothing.", file=sys.stderr)
        return

    if args.command == "upsert":
        command_upsert(args, state)
    elif args.command == "save-setup":
        command_save_setup(args, state)
    elif args.command == "save-bank":
        command_save_bank(args, state)
    save_file(path, state)


if __name__ == "__main__":
    main()
