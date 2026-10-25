# Job Ledger launch film

43 seconds · 1080 × 1920 · 60 fps. A Remotion/React/TypeScript production project separate from the Job Ledger runtime. The storyline is an explicitly labeled illustrative demonstration, with one fictional student, one employer, and separate package/submission approvals.

**Brand asset status:** the supplied Cubbie logo is integrated in the Messages headers and closing card. The original JPEG is preserved byte-for-byte; the avatar is a lossless crop with a circular display mask. Geometry and colors are unchanged. See `public/brand/manifest.json`.

## Download and watch

On GitHub, select the `launch-film` branch and choose **Code → Download ZIP**. Extract the ZIP, then open `video/deliverables/job-ledger-launch-1080x1920.mp4` in your video player. No developer tools are needed to watch. The silent version is in the same folder.

## Install

Validated environment: Node 24.19.0, npm 11.9.0, Python 3.12.14, FFmpeg/ffprobe 7.1.5, system Chromium 154 at `/usr/bin/chromium`. Remotion packages all use 4.0.538. Exact npm versions are in the committed package-lock.json.

```bash
cd job-ledger/video
npm ci
npm run typecheck
```

All render assets are bundled in `public/`. No network connection or API key is needed during rendering. Adjust the browser path in `remotion.config.ts` and capture scripts if moving to another machine. Run `npx remotion browser ensure` if no supported system browser is installed. Keep TLS and artifact verification enabled.

The Job Ledger runtime is in the parent directory. Its fixture-generation Pillow environment is `../.venv/bin/python`. The video project has its own dependencies; students do not need to install them.

## Preview and render

```bash
npm run studio -- --no-open
npm run render:draft
npm run render:final
```

Studio lists `JobLedgerLaunch` (60 fps) and `JobLedgerDraft` (30 fps). `safeGuides: true` enables the social-safe overlay in props; keep it false for exports. The draft command writes a 540 × 960 animatic. The final command renders 2580 frames, converts to limited-range H.264/yuv420p, adds the mastered AAC score, sets MP4 fast start, and runs verification. It limits rendering to three workers for this five-CPU machine.

The existing prepared Studio process may need restarting in a new task; processes do not persist in environment snapshots. No service is required for CLI rendering.

## Deliverables

These are technically verified exports with the supplied Cubbie logo integrated. See `docs/delivery-report.md` for measured results and remaining limitations.

- `deliverables/job-ledger-launch-1080x1920.mp4` — score and sound design.
- `deliverables/job-ledger-launch-silent.mp4` — video-only silent version.
- `deliverables/job-ledger-poster.png` — full-resolution poster frame.
- `deliverables/job-ledger-storyboard.jpg` — eight-shot contact sheet.
- Editable source, fixtures, fonts, skills, and score stems are included directly in this `video/` directory. GitHub’s **Code → Download ZIP** downloads the complete branch; no separate source ZIP is needed.
- `deliverables/verification.json` / `audio-verification.json` — measured technical results.

No voiceover or subtitles were generated. All narrative essentials are already on screen; no redundant message captions are added.

## Three useful edits

1. **Copy:** `src/data/conversation.ts`, `src/data/sampleProfile.ts`, headline strings in `src/data/storyboard.ts`, and the end-card component. Preserve evidence and separate approvals.
2. **Pacing:** scene boundaries in `src/data/storyboard.ts`; message arrival/camera states in `src/scenes/ConversationScenes.tsx`; tailoring steps in `src/components/TailoringSequence.tsx`. All timing derives from frames/fps. If changing the total duration, update the Root registrations and final verification expectations.
3. **Audio:** `src/data/audio.json` contains tempo, gains, approval ducking, seed, and cue times. `scripts/synthesize-score.py` defines the score. Regenerate/master with `npm run audio`, then rerun `bash scripts/finish-film.sh` to update audio without rendering the video again.

To regenerate audio on a new machine:

```bash
python3 -m venv .audio-venv
.audio-venv/bin/pip install --no-cache-dir -r requirements-audio.txt
.audio-venv/bin/python scripts/synthesize-score.py
.audio-venv/bin/python scripts/master-audio.py
```

## Assets and QA

`docs/claims-ledger.md` maps marketing claims to code, workflow instructions, or external integrations. `docs/provenance.md` records fonts, original audio and fictional source material. `docs/research.md` records blocked reference access and the documented iOS 18-style reconstruction.

`python3 scripts/prepare-fixtures.py` recreates the supplied-document fixtures using the parent Job Ledger checkout and pdfLaTeX. `npm run capture` regenerates the actual HTML review screenshot via Playwright. `npm run stills` renders representative full-resolution frames. The original repository source remains unchanged.

The official Remotion skills are installed under `.agents/skills/`. Read `.agents/skills/remotion-best-practices/SKILL.md` and the relevant references before extending the film. All fonts/images are local and preloaded by Remotion. Animation is deterministic; there are no CSS transitions, wall-clock timers or unseeded visual randomness.

Nothing is published automatically. This project and the review exports are included on the user-authorized `launch-film` branch for download. The original supplied logo, prepared crop, and provenance are included.
