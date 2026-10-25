# Render and verification report

Both exports include the original supplied Cubbie logo in the Messages headers and closing card. The white avatar circle, symbol geometry, and colors are preserved. Source and crop provenance are recorded in `public/brand/manifest.json`.

| Check | Result |
|---|---|
| Duration | 43.000 seconds, both exports |
| Dimensions | 1080 × 1920, vertical 9:16 |
| Frame rate / count | 60 fps / 2580 frames |
| Video | H.264, yuv420p, limited range, Rec.709 metadata |
| Music export audio | AAC, stereo, 48 kHz, 256 kb/s target |
| Silent export audio | No audio stream |
| MP4 fast start | moov precedes mdat, verified |
| Decode | Full video/audio decode passed for both files |
| Audio integrated loudness | −14.31 LUFS after AAC encoding |
| Audio true peak | −1.51 dBTP after AAC encoding |
| Black detection | None at the 0.10-second threshold |
| First/last frames | Exact frames 0 and 2579 extracted; both present and nonblack |
| TypeScript | Passed |
| Dependencies | Remotion packages all 4.0.538; exact lockfile |
| Runtime network | None required for rendering |
| Product runtime | Existing files unchanged; production project added under `video/` |

Visual inspection covered the full draft and final timeline at half-second intervals, representative 1080p frames, and phone-size contact sheets. Corrected font fallback, review-page scroll framing, native time labels, and attachment-origin continuity. The signature sequence traces Python from the role to supplied evidence to resume wording. Package approval and submission approval are separate; sample receipt precedes the Applied dashboard row. No simulated login, invented score, guaranteed outcome, contact information or grades appear.

The logo update was checked in eight representative full-resolution frames, including the opening and end card, then rerendered at 1080 × 1920 / 60 fps. The original logo and prepared crop were inspected visually and compared pixel-for-pixel.

The opening hook and Cubbie context are visible immediately. The resolved final brand/CTA holds from approximately 38.85 to 43 seconds. No cursor, Android navigation, permanent in-thread dashboard, unseeded animation or final safe-guide overlay is present. Phone cropping in the opening is intentional.

Music and sound effects are original procedural synthesis. Audio was measured and decoded; an audio-audition channel was not available, so a subjective listening review is not claimed. A first AAC encode peaked at −0.99 dBTP; the delivered encode includes 0.3 dB additional headroom and passes the requested ceiling.

## Remaining limitations

- YouTube references, Apple references and live Remotion docs were blocked by the network proxy. The videos were not watched. UI is an explicitly documented iOS 18-style reconstruction, not verified latest-release iOS.
- No suitable natural licensed voice was available. No optional voiceover export or SRT was generated.
- The user subsequently authorized transfer through a separate `launch-film` GitHub branch. This directory and the exports are included on that branch; existing runtime files are unchanged.

Primary edits: copy in `src/data/conversation.ts` / `sampleProfile.ts`, pacing in `src/data/storyboard.ts` and scene timings, audio in `src/data/audio.json`. See README for install, preview, draft, final, and regeneration commands.
