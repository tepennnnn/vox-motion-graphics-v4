#!/bin/bash
# Cut a MOVING person out of real footage (REF-A/B/C people are alive; stills read "mundane").
# usage: vcut.sh <video> <start_s> <dur_s> <crop_x0> <crop_x1> <out.webm> [--pingpong]
# Crops one person (full height), B&W + contrast, 30 fps, removes the background (u2net, CoreML, ~10 fps), and with
# --pingpong plays it forward then backward so a scene longer than the clip never freezes.
set -e
SRC="$1"; SS="$2"; DUR="$3"; X0="$4"; X1="$5"; OUT="$6"; PP="$7"
TMP="${OUT%.webm}_src.mp4"
ffmpeg -v error -y -ss "$SS" -t "$DUR" -i "$SRC" -an -vf "crop=$((X1-X0)):ih:$X0:0,scale=-2:1000,fps=30,hue=s=0,eq=contrast=1.16:gamma=0.96" -c:v libx264 -crf 14 -pix_fmt yuv420p "$TMP"
npx hyperframes remove-background "$TMP" -o "$OUT" --quality balanced >/dev/null 2>&1
if [ "$PP" = "--pingpong" ]; then
  ffmpeg -v error -y -c:v libvpx-vp9 -i "$OUT" -filter_complex "[0:v]split[a][b];[b]reverse[r];[a][r]concat=n=2:v=1[v]" -map "[v]" -c:v libvpx-vp9 -pix_fmt yuva420p -b:v 0 -crf 24 -row-mt 1 -auto-alt-ref 0 "${OUT%.webm}_pp.webm"
  echo "${OUT%.webm}_pp.webm"
fi
rm -f "$TMP"; echo "$OUT"
