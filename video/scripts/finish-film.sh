#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
mkdir -p deliverables
ffmpeg -hide_banner -loglevel warning -y -i output/render-master.mp4 -vf 'scale=in_range=auto:out_range=tv,format=yuv420p' -an -c:v libx264 -preset slow -crf 17 -pix_fmt yuv420p -color_range tv -color_primaries bt709 -color_trc bt709 -colorspace bt709 -movflags +faststart deliverables/job-ledger-launch-silent.mp4
ffmpeg -hide_banner -loglevel warning -y -i deliverables/job-ledger-launch-silent.mp4 -i public/audio/launch-master.wav -map 0:v:0 -map 1:a:0 -c:v copy -af volume=-0.3dB -c:a aac -b:a 256k -ar 48000 -t 43 -movflags +faststart deliverables/job-ledger-launch-1080x1920.mp4
python3 scripts/verify-exports.py
