"""Use a REAL recording (the user's own voice, or a talking-head take) instead of Kokoro.
usage: python3 from_recording.py <project> <recording.(mp4|mov|wav|m4a)> [--model ~/ai-video-editor/models/ggml-medium.en.bin]
Writes assets/audio/vo.wav (48 kHz, loudness -16 LUFS), work/script.json (one line per whisper segment; fix any misheard
word by hand in "shown" AND "spoken"), work/vo_lines.json (segment windows). Then run align.py as usual.
Cut restarts and long pauses BEFORE this step: every time in the film comes from the file you build on.
"""
import sys, json, subprocess, argparse
from pathlib import Path
ap = argparse.ArgumentParser(); ap.add_argument('project'); ap.add_argument('rec')
ap.add_argument('--model', default=str(Path.home() / 'ai-video-editor/models/ggml-medium.en.bin'))
a = ap.parse_args(); P = Path(a.project); (P / 'work').mkdir(exist_ok=True); (P / 'assets/audio').mkdir(parents=True, exist_ok=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', a.rec, '-vn', '-af', 'loudnorm=I=-16:TP=-1.5:LRA=9', '-ar', '48000', '-ac', '2', str(P / 'assets/audio/vo.wav')], check=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(P / 'assets/audio/vo.wav'), '-ac', '1', '-ar', '16000', str(P / 'work/vo16.wav')], check=True)
subprocess.run(['whisper-cli', '-m', a.model, '-f', str(P / 'work/vo16.wav'), '-oj', '-of', str(P / 'work/rec'), '-np'], check=True, capture_output=True)
segs = [s for s in json.load(open(P / 'work/rec.json'))['transcription'] if s['text'].strip()]
lines = [[s['text'].strip(), s['text'].strip()] for s in segs]
win = [{'text': s['text'].strip(), 'start': s['offsets']['from'] / 1000, 'end': s['offsets']['to'] / 1000} for s in segs]
cfg = {'voice': 'recording', 'lines': lines}
json.dump(cfg, open(P / 'work/script.json', 'w'), indent=1); json.dump(win, open(P / 'work/vo_lines.json', 'w'), indent=1)
print(len(lines), 'lines. Check work/script.json spellings (names!), then: $MGV3_ALIGN tools/align.py', P)
