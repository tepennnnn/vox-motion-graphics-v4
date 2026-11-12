"""MG V3 sound: music bed + an effects track laid from a cue list, each effect's PEAK landing one frame after its
picture (light arrives before sound). Writes assets/audio/bed.wav and assets/audio/sfx.wav (48 kHz stereo).
usage: python3 mix.py <project>     (reads <project>/work/sound.json)
sound.json: {"duration": 50, "bed": {"src": "...", "offset": 2.0, "gain_db": -14, "fade_in": 0.4, "fade_out": 1.4,
             "dips": [[start, end, db], ...]},
             "sfx_dir": "...", "cues": [[t, "file", gain_db], ...]}
"""
import sys, json, subprocess
from pathlib import Path
import numpy as np

SR = 48000
P = Path(sys.argv[1]); cfg = json.load(open(P / 'work/sound.json'))
D = cfg['duration']; N = int(D * SR)


def load(path, ss=0.0, dur=None):
    cmd = ['ffmpeg', '-v', 'error', '-ss', str(ss), '-i', str(path)] + (['-t', str(dur)] if dur else []) + ['-f', 'f32le', '-ac', '2', '-ar', str(SR), '-']
    a = np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, dtype=np.float32)
    return a.reshape(-1, 2).copy()


def write(path, a):
    a = np.clip(a, -1, 1)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-i', '-', '-c:a', 'pcm_s16le', str(path)],
                   input=a.astype(np.float32).tobytes(), check=True)


db = lambda x: 10 ** (x / 20)

# ---- bed
b = cfg.get('bed') or {}
src = b.get('src') and (Path(b['src']) if Path(b['src']).is_absolute() else P / b['src'])
if src and src.exists():
    bed = load(str(src), b.get('offset', 0), D)
else:
    print('no music bed (put your own no-copyright track at', b.get('src', 'assets/audio/bed.mp3'), ') → silence under the voice')
    bed = np.zeros((N, 2), np.float32)
bed = np.vstack([bed, np.zeros((max(0, N - len(bed)), 2), np.float32)])[:N]
g = np.full(N, db(b.get('gain_db', -14)), np.float32)
fi, fo = int(b.get('fade_in', 0.3) * SR), int(b.get('fade_out', 1.2) * SR)
g[:fi] *= np.linspace(0, 1, fi); g[N - fo:] *= np.linspace(1, 0, fo)
for s, e, d in b.get('dips', []):           # smooth 0.25 s ramps into and out of each dip
    env = np.ones(N, np.float32); i0, i1, r = int(s * SR), int(e * SR), int(0.25 * SR)
    env[i0:i1] = db(d)
    env[max(0, i0 - r):i0] = np.linspace(1, db(d), i0 - max(0, i0 - r))
    env[i1:min(N, i1 + r)] = np.linspace(db(d), 1, min(N, i1 + r) - i1)
    g *= env
write(P / 'assets/audio/bed.wav', bed * g[:, None])

# ---- effects
sfx = np.zeros((N, 2), np.float32); cache = {}
for t, f, gdb in cfg['cues']:
    if f not in cache:
        a = load(Path(cfg['sfx_dir']) / f)
        env = np.abs(a).max(1); k = int(0.01 * SR)
        sm = np.convolve(env, np.ones(k) / k, mode='same')
        cache[f] = (a, int(np.argmax(sm)))
    a, pk = cache[f]
    start = int((t + 1 / 30) * SR) - pk
    a0 = max(0, -start); start = max(0, start)
    seg = a[a0:a0 + N - start] * db(gdb)
    sfx[start:start + len(seg)] += seg
write(P / 'assets/audio/sfx.wav', sfx * db(cfg.get('sfx_gain_db', 0)))
print('bed + sfx written', len(cfg['cues']), 'cues')
