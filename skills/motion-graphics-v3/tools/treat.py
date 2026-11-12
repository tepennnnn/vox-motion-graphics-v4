"""MG V3 still treatments (the references' looks), applied before the build so the render never grades.
usage: python treat.py <in> <out.png> [--look mono|mono_soft|warm|paper|ink] [--keep 0,0,1,0.8] [--feather 0.12] [--grain 6]
       [--maxh 1600]
- Cutouts (RGBA in): the alpha is kept, trimmed to its box; --keep x0,y0,x1,y1 (fractions) crops first (e.g. drop a table at
  the bottom); --feather fades the bottom edge so a body can rise out of a card without a hard cut line.
- mono       hard B&W, lifted blacks, crisp (REF-A Jobs / REF-B Edison portraits)
- mono_soft  softer B&W, lower contrast (REF-B grey world)
- warm       B&W with a warm paper tint (REF-C paper)
- paper      page captures: desaturated, slightly warm, contrast up (REF-C article page)
- ink        dark-world variant: B&W, crushed, for navy scenes
"""
import argparse
import numpy as np
from PIL import Image, ImageFilter

ap = argparse.ArgumentParser()
ap.add_argument('src'); ap.add_argument('out')
ap.add_argument('--look', default='mono'); ap.add_argument('--keep', default='')
ap.add_argument('--feather', type=float, default=0.0); ap.add_argument('--grain', type=float, default=5)
ap.add_argument('--maxh', type=int, default=1700)
a = ap.parse_args()

im = Image.open(a.src).convert('RGBA')
if a.keep:
    x0, y0, x1, y1 = [float(v) for v in a.keep.split(',')]
    W, H = im.size
    im = im.crop((int(x0 * W), int(y0 * H), int(x1 * W), int(y1 * H)))
arr = np.asarray(im).astype(np.float32) / 255
rgb, al = arr[..., :3], arr[..., 3]
lum = rgb @ np.array([0.299, 0.587, 0.114], dtype=np.float32)

def curve(x, lo, hi, gamma):
    x = np.clip((x - lo) / (hi - lo), 0, 1)
    return x ** gamma

if a.look == 'mono':
    y = curve(lum, 0.06, 0.92, 1.05); y = 0.07 + 0.9 * (y * y * (3 - 2 * y) * 0.55 + y * 0.45)
    out = np.stack([y, y, y], -1)
elif a.look == 'mono_soft':
    y = 0.16 + 0.7 * curve(lum, 0.04, 0.96, 0.95); out = np.stack([y, y, y], -1)
elif a.look == 'warm':
    y = 0.08 + 0.86 * curve(lum, 0.05, 0.95, 1.0); out = np.stack([y * 1.0, y * 0.975, y * 0.93], -1)
elif a.look == 'paper':
    s = 0.12; y = curve(lum, 0.10, 0.97, 1.15)
    out = np.clip(rgb * s + np.stack([y, y, y], -1) * (1 - s), 0, 1) * np.array([1.0, 0.985, 0.95])
elif a.look == 'ink':
    y = 0.04 + 0.8 * curve(lum, 0.10, 0.90, 1.25); out = np.stack([y, y, y], -1)
else:
    out = rgb
if a.grain:
    rng = np.random.default_rng(7)
    out = np.clip(out + rng.normal(0, a.grain / 255, out.shape[:2])[..., None], 0, 1)

if a.feather > 0:
    H = al.shape[0]; f = int(H * a.feather)
    ramp = np.ones(H, np.float32); ramp[H - f:] = np.linspace(1, 0, f) ** 1.4
    al = al * ramp[:, None]
res = Image.fromarray((np.dstack([out, al]) * 255).astype(np.uint8), 'RGBA')
bb = res.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox()
if bb: res = res.crop(bb)
if res.size[1] > a.maxh:
    res = res.resize((int(res.size[0] * a.maxh / res.size[1]), a.maxh), Image.LANCZOS)
if a.out.endswith('.jpg'):
    res.convert('RGB').save(a.out, quality=90)
else:
    res.save(a.out, optimize=True)
print(a.out, res.size)
