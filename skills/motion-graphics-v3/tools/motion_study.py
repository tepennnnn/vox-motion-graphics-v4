"""Measure HOW MUCH and WHAT KIND of motion a video has, frame by frame (dense optical flow, OpenCV).
usage: python motion_study.py <video> <name> [--out analysis/motion]
Per frame pair: the global camera move fitted to the flow (zoom %/s, pan px/s in 1080-wide units, rotation deg/s),
the LOCAL motion left after removing the camera (things moving inside the frame), and the share of the frame moving.
Writes <name>_motion.tsv, <name>_motion.png (timeline) and prints a summary to compare a build against references.
"""
import sys, argparse, json
import numpy as np, cv2
ap = argparse.ArgumentParser(); ap.add_argument('video'); ap.add_argument('name'); ap.add_argument('--out', default='analysis/motion')
a = ap.parse_args()
import os; os.makedirs(a.out, exist_ok=True)
cap = cv2.VideoCapture(a.video); fps = cap.get(cv2.CAP_PROP_FPS) or 30
W, H = 180, 320; k = 1080 / W          # flow measured at 180x320, reported in 1080-wide pixels
ys, xs = np.mgrid[8:H - 8:6, 8:W - 8:6]; P = np.stack([xs.ravel(), ys.ravel()], 1).astype(np.float32)
rows, prev = [], None
while True:
    ok, fr = cap.read()
    if not ok: break
    g = cv2.cvtColor(cv2.resize(fr, (W, H), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2GRAY)
    if prev is not None:
        fl = cv2.calcOpticalFlowFarneback(prev, g, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        v = fl[P[:, 1].astype(int), P[:, 0].astype(int)]
        M, inl = cv2.estimateAffinePartial2D(P, P + v, method=cv2.RANSAC, ransacReprojThreshold=0.6)
        if M is None: M = np.array([[1, 0, 0], [0, 1, 0]], np.float32)
        s = float(np.hypot(M[0, 0], M[1, 0])); rot = float(np.degrees(np.arctan2(M[1, 0], M[0, 0])))
        # camera-predicted flow at each point; residual = local motion
        pred = (P @ M[:, :2].T + M[:, 2]) - P
        res = np.linalg.norm(v - pred, axis=1)
        mag = np.linalg.norm(v, axis=1)
        cx, cy = W / 2, H / 2
        centre_shift = (np.array([cx, cy]) @ M[:, :2].T + M[:, 2]) - np.array([cx, cy])
        diff = float(np.abs(g.astype(np.float32) - prev.astype(np.float32)).mean())
        rows.append(dict(f=len(rows) + 1, t=round((len(rows) + 1) / fps, 3), zoom=(s - 1) * 100 * fps,
                         pan=float(np.linalg.norm(centre_shift)) * k * fps, rot=rot * fps,
                         local=float(np.mean(res)) * k, moving=float((mag > 0.35).mean()), diff=diff))
    prev = g
cap.release()
Z = np.array([[r['zoom'], r['pan'], r['rot'], r['local'], r['moving'], r['diff']] for r in rows])
cut = Z[:, 5] > 28                        # hard cuts/flashes: excluded from the motion stats
m = Z[~cut]
dead = (np.abs(m[:, 0]) < 0.6) & (m[:, 1] < 12) & (m[:, 3] < 0.6)       # no camera move AND nothing moving
cam = (np.abs(m[:, 0]) >= 0.6) | (m[:, 1] >= 12) | (np.abs(m[:, 2]) >= 0.3)
summary = dict(name=a.name, seconds=round(len(rows) / fps, 1), cuts=int(cut.sum()),
               dead_pct=round(100 * dead.mean(), 1), camera_moving_pct=round(100 * cam.mean(), 1),
               zoom_abs_median=round(float(np.median(np.abs(m[:, 0]))), 2), pan_median=round(float(np.median(m[:, 1])), 1),
               local_median=round(float(np.median(m[:, 3])), 2), local_p90=round(float(np.percentile(m[:, 3], 90)), 2),
               moving_share_median=round(float(np.median(m[:, 4])), 3))
# longest run of dead frames (seconds)
run = best = 0
for d in dead:
    run = run + 1 if d else 0; best = max(best, run)
summary['longest_dead_s'] = round(best / fps, 2)
with open(f'{a.out}/{a.name}_motion.tsv', 'w') as fh:
    fh.write('f\tt\tzoom%/s\tpan_px/s\trot_deg/s\tlocal_px\tmoving\tdiff\n')
    for r in rows: fh.write('\t'.join(str(round(r[c], 3)) for c in ('f', 't', 'zoom', 'pan', 'rot', 'local', 'moving', 'diff')) + '\n')
json.dump(summary, open(f'{a.out}/{a.name}_motion.json', 'w'), indent=1)
try:
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    t = [r['t'] for r in rows]
    fig, ax = plt.subplots(4, 1, figsize=(20, 9), sharex=True)
    ax[0].plot(t, Z[:, 0]); ax[0].set_ylabel('zoom %/s'); ax[0].set_ylim(-60, 60)
    ax[1].plot(t, Z[:, 1]); ax[1].set_ylabel('pan px/s'); ax[1].set_ylim(0, 1500)
    ax[2].plot(t, Z[:, 3]); ax[2].set_ylabel('local px'); ax[2].set_ylim(0, 12)
    ax[3].plot(t, Z[:, 4]); ax[3].set_ylabel('moving share')
    for x in np.array(t)[cut]:
        for aa in ax: aa.axvline(x, color='r', lw=.6, alpha=.5)
    ax[0].set_title(f"{a.name}: {summary}", fontsize=8)
    plt.tight_layout(); plt.savefig(f'{a.out}/{a.name}_motion.png', dpi=70)
except Exception as e:
    print('plot skipped', e)
print(json.dumps(summary))
