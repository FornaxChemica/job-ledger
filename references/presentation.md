# How Job Ledger shows its work

This file is for Cubbie, not for a student text. Student texts stay short and plain. A card is a picture. A review page is a file the student opens. Neither one can update the index, connect an account, or approve a submission. The student does that by replying.

## When to send something

Send a card only at a milestone. Do not send a new picture after every answer.

- Welcome, once, when they first ask for help and setup has no stage.
- Profile, once, after a resume or confirmed background is read and before they confirm it.
- Connections, once, after the profile is confirmed.
- Ready, once, when stage is `ready` and the first role has not been screened.
- Opportunity, once per new role, with the verdict.
- Package page, when status becomes `kit ready`.
- The same page again, when the employer form has been filled and is waiting for a submit yes.
- Confirmation card, only after `applied` is saved with the confirmation text.
- Dashboard, when they ask what is in progress, or after a confirmation if they want the list. Do not attach it to every role.

A normal application is five beats, plus questions only when a fact would change the package:

1. Opportunity card, one line, official link on its own line.
2. Questions, in one message, only if something material is unknown.
3. Package page when the kit is ready.
4. Package page again when the form is filled, asking whether to submit.
5. Confirmation card after the confirmation quote is saved.

Errors and a missing account can add a message. Do not drop a required check to keep the count down.

## Companion text

One idea. No headings, tables, or Markdown. The picture already holds the detail, so the text does not repeat it.

Opportunity: "Worth considering. The card has the evidence." Then the official link alone on the next line. Ask "Apply to this one?" only for Worth considering, or Need to check when their answer could make it worth considering. For Not a fit, do not pitch it.

Package: "Your review page is ready." Deliver the HTML file. Do not invent a URL for it.

Filled form: "The form is filled and not submitted. Okay to submit?" Deliver the new HTML file.

Confirmation: quote the confirmation in one line. The card says whether it came from the employer page, the student, or sample data.

If `image` is null, send the HTML path from the same command and say the picture could not be drawn. Continue the task.

## Commands

Cards and the dashboard do not write the application index. `mode` is `sample` only when the input says `demo` or the confirmation source is `sample`. `wrote_state` is false.

```bash
python3 scripts/render_visual.py card --kind welcome --input welcome.json --out welcome.png
python3 scripts/render_visual.py card --kind profile --input profile.json --out profile.png
python3 scripts/render_visual.py card --kind connections --input connections.json --out connections.png
python3 scripts/render_visual.py card --kind ready --input ready.json --out ready.png
python3 scripts/render_visual.py card --kind opportunity --input opportunity.json --out opportunity.png
python3 scripts/render_visual.py card --kind confirmation --input confirmation.json --out confirmation.png
python3 scripts/render_package.py --input package.json --out package.html
python3 scripts/render_visual.py dashboard --input index.json --out dashboard.html --generated-at "<ISO time>"
```

`--out` for a card is a `.png` path. The command also writes the `.html` card beside it. Send the PNG when `image` is set. Send the HTML when it is not. The package command writes only the HTML page. The dashboard command writes only HTML.

Run cards with the Job Ledger virtualenv when the system Python has no Pillow:

```bash
python3 -m venv ~/.local/share/venvs/job-ledger
~/.local/share/venvs/job-ledger/bin/pip install "Pillow==13.0.0"
~/.local/share/venvs/job-ledger/bin/python scripts/render_visual.py card --kind opportunity --input opportunity.json --out opportunity.png
```

Pillow is a pip wheel. It does not need apt or a browser. HTML-to-PNG is not available in Cubbie. This machine can draw PNGs with Pillow 13.0.0. A run inside Cubbie is still required before calling the image path proven there. The HTML card is the fallback either way.

The package page and the dashboard do not need Pillow.

## Card JSON

Every card accepts `demo: true` and an optional `reply`. Sample surfaces must show "Sample data". Do not turn that flag on for a real student.

Welcome, connections, and ready can use:

- `stage`, `value`, `confirmed` (list of strings), `next`
- Connections also reads `connectors` and `connections` from `show-setup`

Profile reads `profile`:

- `name`, `education`, `targets`, `location`, `skills` (list)
- `evidence`: list of `{name, did, result}`
- `missing`: list of strings

Do not put work authorization, sponsorship, a metric, or a project outcome in the profile unless the student or a document stated it.

Opportunity:

- `employer`, `role`, `location`, `source`, `verdict`, `status`
- `reasons`: two or three strings grounded in evidence
- `gap`: one uncertainty, or omit it
- `verdict` is Worth considering, Need to check, or Not a fit

No match percentage, salary, deadline, or logo unless that exact fact was verified. The card uses initials.

Confirmation:

- `employer`, `role`, `confirmation`
- `confirmation_source`: `employer`, `user_reported`, or `sample`

The card does not mark the role applied. Saving `applied` is still the upsert command, and it still requires the confirmation text.

## Package JSON

The old fields still work: `employer`, `role`, `verdict`, `quote`, `section`, `link`, `answers`, `resume`, `cover`, `fields`, `confirmation`. Empty sections are left out.

Optional fields:

- `status`, `location`, `deadline`, `updated`, `demo`
- `fit`: list of `{requirement, state, evidence, source, blocking}`
- `state` is `supported`, `needs_confirmation`, or `missing`. Red is only for `missing` with `blocking: true`.
- `resume_url`, `cover_url`, `changes`, `source_files`
- `prepared_answers`: `{q, a, note}` list. When this key is present it replaces `answers`. `note` is a review hold and is not an answer to send.
- `resume_doc` and `cover_doc` typeset the resume and letter. A plain `resume` or `cover` string is still rendered when the document object is absent.
- `fields`: values observed on the employer form. Do not copy prepared answers into `fields`.
- `attachments`, `missing`, `approval`, `return_copy`, `confirmation_source`

Resume and cover text are labeled as text. Do not call that block a PDF preview. A download link is rendered only for `http`, `https`, or `mailto`. Any other scheme is shown as text, not as a link.

The page never contains a submit button. The last line tells the student what to reply in the conversation. Default copy:

- Package: `Return to Cubbie and reply 'use this package'.`
- Filled form: `Return to Cubbie and reply yes to submit, or no to stop.`

## Dashboard JSON

Pass the index from the local file, or a JSON object with `roles` in that same shape. Optional `generated_at` and `demo`.

```bash
python3 scripts/applications.py show-setup
```

The dashboard groups stored statuses. "Needs your action" is a label, not a new status.

- Ready to review: `kit ready`
- Needs your action: `need to check`, `filled`, or `applied` without confirmation text
- In progress: `outreach sent`, `replied`, `interview`, `offer`
- Applied: `applied` with confirmation text
- Screened, only when a row exists: `not a fit`, `skipped`, `rejected`

`need to check` means a screening question is still open. `filled` means the form is filled and submission is not approved. `applied` without confirmation text is shown as unconfirmed, not Applied.

Each row shows the employer, the role when `role` was saved, the stage, `updated` when present, and a package or posting link only when the URL is http, https, or a same-folder relative name such as `06-package.html`. Do not invent a host. A path on disk is not turned into a link.

The page says when it was generated and that it is a snapshot. Filters work in the file itself. Notion is not required.

## Setup that the pictures read

`connectors` is what the student wants to use. `connections` is what was checked. Show Connected only when status is `connected` and `checked_at` is set. A name in `connectors` without that check is "Selected, not checked".

```bash
python3 scripts/applications.py save-setup --stage background --notifications off --referral off --package-format html --profile-file profile.json
python3 scripts/applications.py set-connection --name notion --status skipped
python3 scripts/applications.py set-connection --name email --status connected --checked-at "<ISO time>"
python3 scripts/applications.py show-setup
```

Stages are `background`, `connections`, and `ready`. Notifications are `off` or `on`. `connected` without `--checked-at` is rejected and nothing is written.

On the next conversation, read `show-setup` and continue from the saved stage. Do not ask answered questions again.

Create a check-in only after they choose a cadence and notifications are on. The check-in text, worded so it still makes sense later: "Job Ledger check-in. Search the connected email alerts and boards. Look each job id up in the local index and the Notion hub before texting. Send one new role in a single message."

## Demo

Demo files live in `assets/demo`. Output goes where `--out` points. The command does not read or write `~/.config/job-ledger` or `SKILL_DATA_DIR`.

```bash
python3 scripts/render_visual.py demo --out output/demo
```

The result says `"mode": "sample"` and `"wrote_state": false`. Sample connections are skipped. The sample confirmation says it does not record an application. Do not describe that recording as a real submission or a real sign-in.
