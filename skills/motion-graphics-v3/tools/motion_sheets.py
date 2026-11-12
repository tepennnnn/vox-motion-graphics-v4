"""Contact sheets that SHOW where the motion is: each tile = the frame with its optical-flow magnitude painted on it
(red = moving), plus the camera numbers. usage: python motion_sheets.py <video> <out_prefix> [--step 3] [--start 0] [--end 999]
"""
import argparse
import numpy as np, cv2
ap = argparse.ArgumentParser(); ap.add_argument('video'); ap.add_argument('out')
ap.add_argument('--step', type=int, default=3); ap.add_argument('--start', type=float, default=0); ap.add_argument('--end', type=float, default=999)
a = ap.parse_args()
cap = cv2.VideoCapture(a.video); fps = cap.get(cv2.CAP_PROP_FPS) or 30
W, H = 216, 384; tiles, prev, n = [], None, 0
while True:
    ok, fr = cap.read()
    if not ok: break
    n += 1; t = (n - 1) / fps
    small = cv2.resize(fr, (W, H), interpolation=cv2.INTER_AREA); g = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
    if prev is not None and a.start <= t <= a.end and n % a.step == 0:
        fl = cv2.calcOpticalFlowFarneback(prev, g, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        mag = np.linalg.norm(fl, axis=2) * (1080 / W)          # px per frame at 1080 wide
        heat = np.clip(mag / 12, 0, 1)
        tile = small.astype(np.float32)
        tile[..., 2] = np.clip(tile[..., 2] * (1 - heat) + 255 * heat, 0, 255)
        tile[..., 1] *= (1 - heat * 0.7); tile[..., 0] *= (1 - heat * 0.7)
        tile = tile.astype(np.uint8)
        share = (mag > 2).mean()
        cv2.rectangle(tile, (0, 0), (W, 34), (0, 0, 0), -1)
        cv2.putText(tile, f'{n} {t:.2f}s', (3, 14), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 255), 1)
        cv2.putText(tile, f'mov {share*100:.0f}% max {mag.max():.0f}px', (3, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        tiles.append(tile)
    prev = g
cols, rows = 10, 3; per = cols * rows
for s in range(0, len(tiles), per):
    sheet = np.zeros((rows * H, cols * W, 3), np.uint8)
    for i, tl in enumerate(tiles[s:s + per]):
        sheet[(i // cols) * H:(i // cols + 1) * H, (i % cols) * W:(i % cols + 1) * W] = tl
    cv2.imwrite(f'{a.out}_{s // per + 1:02d}.jpg', sheet, [cv2.IMWRITE_JPEG_QUALITY, 80])
print(len(tiles), 'tiles')
