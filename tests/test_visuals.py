#!/usr/bin/env python3
"""Checks for the visual layer. Run with the virtualenv that has Pillow."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import render_package  # noqa: E402
import render_visual  # noqa: E402
from visual_theme import connection_rows, safe_url  # noqa: E402

PYTHON = sys.executable


def run_script(*args: str, env: dict | None = None) -> subprocess.CompletedProcess[str]:
    merged = os.environ.copy()
    if env:
        merged.update(env)
    return subprocess.run(
        [PYTHON, *args],
        cwd=ROOT,
        env=merged,
        text=True,
        capture_output=True,
        check=False,
    )


class SafeLinks(unittest.TestCase):
    def test_schemes(self) -> None:
        self.assertEqual(safe_url("https://jobs.example/1"), "https://jobs.example/1")
        self.assertEqual(safe_url("mailto:maya@example.edu"), "mailto:maya@example.edu")
        self.assertEqual(safe_url("06-package.html"), "06-package.html")
        self.assertEqual(safe_url("javascript:alert(1)"), "")
        self.assertEqual(safe_url("data:text/html,hi"), "")
        self.assertEqual(safe_url("/etc/passwd"), "")
        self.assertEqual(safe_url("../secret.html"), "")
        self.assertEqual(safe_url("https://ok.example/a b"), "")


class Connections(unittest.TestCase):
    def test_selection_is_not_connected(self) -> None:
        rows = {row["key"]: row for row in connection_rows({"connectors": "email, linkedin", "connections": {}})}
        self.assertEqual(rows["email"]["status"], "Selected, not checked")
        self.assertFalse(rows["email"]["verified"])
        self.assertEqual(rows["notion"]["status"], "Not checked")
        self.assertNotIn("Connected", rows["linkedin"]["status"])

    def test_connected_needs_a_check_time(self) -> None:
        rows = {
            row["key"]: row
            for row in connection_rows({"connections": {"email": {"status": "connected"}}})
        }
        self.assertEqual(rows["email"]["status"], "Needs sign-in")
        self.assertFalse(rows["email"]["verified"])
        checked = connection_rows(
            {"connections": {"email": {"status": "connected", "checked_at": "2026-10-24T17:00:00-07:00"}}}
        )
        email = next(row for row in checked if row["key"] == "email")
        self.assertEqual(email["status"], "Connected")
        self.assertTrue(email["verified"])


class Index(unittest.TestCase):
    def test_connected_without_time_writes_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            env = {"HOME": str(Path(tmp) / "home"), "SKILL_DATA_DIR": tmp}
            result = run_script(
                "scripts/applications.py",
                "set-connection",
                "--name",
                "notion",
                "--status",
                "connected",
                env=env,
            )
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertFalse((Path(tmp) / "applications.json").exists())

    def test_applied_without_confirmation_still_exits_9(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            env = {"HOME": str(Path(tmp) / "home"), "SKILL_DATA_DIR": tmp}
            result = run_script(
                "scripts/applications.py",
                "upsert",
                "--employer",
                "Northwind Labs",
                "--namespace",
                "url",
                "--job-id",
                "1",
                "--status",
                "applied",
                env=env,
            )
            self.assertEqual(result.returncode, 9, result.stderr)
            self.assertFalse((Path(tmp) / "applications.json").exists())

    def test_sample_lookup_still_works(self) -> None:
        result = run_script(
            "scripts/applications.py",
            "--sample",
            "lookup",
            "--employer",
            "Stripe",
            "--namespace",
            "greenhouse",
            "--job-id",
            "4019283",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("applied", result.stdout)


class PackagePage(unittest.TestCase):
    def test_sample_package_keeps_stripe_and_drops_empty_form(self) -> None:
        page = render_package.render(render_package.load(render_package.SAMPLE))
        self.assertIn("Stripe", page)
        self.assertIn("Worth considering", page)
        self.assertIn("Resume text", page)
        self.assertNotIn('data-section="fields"', page)
        self.assertNotIn("<button", page.lower())
        self.assertNotIn("submit application", page.lower())

    def test_prepared_answers_stay_separate_from_observed_fields(self) -> None:
        data = render_visual.load_json(ROOT / "assets" / "demo" / "form_review.json")
        page = render_package.render(data)
        self.assertIn("Prepared answers", page)
        self.assertIn("Observed on the form", page)
        self.assertIn("Why this role?", page)
        self.assertIn("Review note. Not sent.", page)
        self.assertIn("resume-sheet", page)
        self.assertIn("Dear Northwind Labs team,", page)
        self.assertNotIn("maya.chen@example.edu</a>", page)
        self.assertIn(">Name<", page.replace(" ", "") or "Name")
        self.assertLess(page.index("Prepared answers"), page.index("Observed on the form"))
        self.assertIn("Filled, not submitted", page)
        self.assertNotIn("<button", page.lower())

    def test_user_text_and_bad_links_are_inert(self) -> None:
        employer = "Northwind <script>alert(1)</script> " + ("Labs " * 40)
        page = render_package.render(
            {
                "employer": employer,
                "role": "Intern",
                "link": "javascript:alert(1)",
                "resume": "line",
                "resume_url": "javascript:alert(1)",
            }
        )
        self.assertNotIn("<script>alert", page)
        self.assertIn("&lt;script&gt;", page)
        self.assertNotIn('href="javascript:', page)
        self.assertIn(employer.split("<")[0].strip(), page)

    def test_sample_and_user_reported_labels(self) -> None:
        sample = render_visual.card_html(
            render_visual.normalize_card(
                "confirmation",
                {
                    "demo": True,
                    "employer": "Northwind Labs",
                    "confirmation": "Application received. Reference NW-1842.",
                    "confirmation_source": "sample",
                },
            )
        )
        reported = render_visual.card_html(
            render_visual.normalize_card(
                "confirmation",
                {
                    "employer": "Northwind Labs",
                    "confirmation": "I saw the thank-you page.",
                    "confirmation_source": "user_reported",
                },
            )
        )
        self.assertIn("Sample data", sample)
        self.assertIn("does not record an application", sample)
        self.assertIn("User reported", reported)
        self.assertNotIn("Sample data", reported)


class DemoIsolation(unittest.TestCase):
    def test_demo_does_not_touch_the_index_and_renders_long_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "home"
            data = Path(tmp) / "skill-data"
            sentinel = {"sentinel": True, "roles": [{"employer": "Keep"}]}
            for folder in (home / ".config" / "job-ledger", data):
                folder.mkdir(parents=True)
                (folder / "applications.json").write_text(json.dumps(sentinel))
            out = Path(tmp) / "out"
            env = {"HOME": str(home), "SKILL_DATA_DIR": str(data)}
            result = run_script("scripts/render_visual.py", "demo", "--out", str(out), env=env)
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["mode"], "sample")
            self.assertFalse(payload["wrote_state"])
            for folder in (home / ".config" / "job-ledger", data):
                self.assertEqual(json.loads((folder / "applications.json").read_text()), sentinel)
            self.assertTrue((out / "05-opportunity.png").is_file())
            self.assertTrue((out / "06-package.html").is_file())
            self.assertTrue((out / "09-dashboard.html").is_file())
            dashboard = (out / "09-dashboard.html").read_text()
            self.assertIn("Sample data", dashboard)
            self.assertIn("Needs your action", dashboard)
            self.assertIn("Open package", dashboard)
            self.assertNotIn('href="javascript:', dashboard)

    def test_empty_dashboard_and_long_card(self) -> None:
        page = render_visual.render_dashboard({"roles": [], "generated_at": "2026-10-24T17:40:00-07:00"})
        self.assertIn("Nothing is waiting for review.", page)
        self.assertIn("Nothing is marked applied.", page)
        self.assertIn("snapshot", page)
        long_name = "VeryLongEmployerNameWithoutSpaces" * 8 + " <b>odd</b>"
        written_html = render_visual.card_html(
            render_visual.normalize_card(
                "opportunity",
                {"employer": long_name, "role": "Intern", "verdict": "Need to check", "reasons": [long_name]},
            )
        )
        self.assertIn("&lt;b&gt;", written_html)
        image = render_visual.draw_card(
            render_visual.normalize_card("opportunity", {"employer": long_name, "role": "Intern", "verdict": "Not a fit"})
        )
        self.assertLess(image.height, 5000)
        self.assertEqual(image.width, 780)


class ExistingSamples(unittest.TestCase):
    def test_tex_and_notion_samples(self) -> None:
        tex = run_script("scripts/tex_edit.py", "--sample")
        notion = run_script(
            "scripts/notion_hub.py",
            "--sample",
            "lookup",
            "--employer",
            "Stripe",
            "--namespace",
            "greenhouse",
            "--job-id",
            "4019283",
        )
        package = run_script("scripts/render_package.py", "--sample")
        self.assertEqual(tex.returncode, 0, tex.stderr)
        self.assertEqual(notion.returncode, 0, notion.stderr)
        self.assertEqual(package.returncode, 0, package.stderr)
        self.assertIn("Stripe", package.stdout)


if __name__ == "__main__":
    unittest.main()
