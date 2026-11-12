"""Sound study of one reference: onsets in the music/SFX stem vs visual cuts vs words.
usage: python sound_study.py <name> <fps>   (run from analysis/audio)
Writes <name>_sound.png (spectrogram + markers) and <name>_sound.txt (onset list, tempo, stats).
"""
import sys, json
import numpy as np
import librosa, librosa.display
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

name, fps = sys.argv[1], float(sys.argv[2])
nv, sr = librosa.load(f"sep/htdemucs/{name}/no_vocals.wav", sr=22050, mono=True)
vo, _ = librosa.load(f"sep/htdemucs/{name}/vocals.wav", sr=22050, mono=True)

# words
words = []
for seg in json.load(open(f"{name}.words.json"))["transcription"]:
    w = seg["text"].strip()
    if w:
        words.append((seg["offsets"]["from"] / 1000, w))

# visual cut candidates from frame diff
cuts = []
rows = [l.split("\t") for l in open(f"../sheets/{name[0]}_diff.tsv").read().strip().split("\n")[1:]]
for r in rows:
    if float(r[2]) > 28:
        cuts.append(float(r[1]))

onset_env = librosa.onset.onset_strength(y=nv, sr=sr, hop_length=256)
on = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr, hop_length=256, units="time", backtrack=False, delta=0.25)
strength = {round(t, 3): float(onset_env[librosa.time_to_frames(t, sr=sr, hop_length=256)]) for t in on}
tempo, beats = librosa.beat.beat_track(y=nv, sr=sr, hop_length=256)
cent = librosa.feature.spectral_centroid(y=nv, sr=sr).mean()
rms_nv = librosa.feature.rms(y=nv, hop_length=256)[0]

with open(f"{name}_sound.txt", "w") as fh:
    fh.write(f"tempo~{float(np.atleast_1d(tempo)[0]):.1f} bpm, music/sfx centroid {cent:.0f} Hz, onsets {len(on)} in {len(nv)/sr:.1f}s\n")
    fh.write("visual cuts (diff>28): " + ", ".join(f"{c:.2f}" for c in cuts) + "\n")
    fh.write("onset t / strength / nearest cut dt / nearest word\n")
    for t in on:
        dc = min(cuts, key=lambda c: abs(c - t)) if cuts else None
        dw = min(words, key=lambda w: abs(w[0] - t))
        fh.write(f"{t:6.2f}  {strength[round(t,3)]:5.1f}  cut {('%+.2f' % (t - dc)) if dc is not None else '-':>6}  word '{dw[1]}' {t - dw[0]:+.2f}\n")

S = librosa.amplitude_to_db(np.abs(librosa.stft(nv, n_fft=2048, hop_length=256)), ref=np.max)
fig, ax = plt.subplots(3, 1, figsize=(22, 10), sharex=True, gridspec_kw={"height_ratios": [3, 1, 1]})
librosa.display.specshow(S, sr=sr, hop_length=256, x_axis="time", y_axis="log", ax=ax[0], cmap="magma")
for c in cuts:
    ax[0].axvline(c, color="cyan", lw=1, alpha=.8)
ax[0].set_title(f"{name}: music+SFX stem (cyan = visual cuts)")
t = librosa.times_like(onset_env, sr=sr, hop_length=256)
ax[1].plot(t, onset_env, lw=.8)
for o in on:
    ax[1].axvline(o, color="red", lw=.6, alpha=.6)
ax[1].set_ylabel("onset")
tv = librosa.times_like(rms_nv, sr=sr, hop_length=256)
ax[2].plot(tv, librosa.amplitude_to_db(rms_nv + 1e-6), lw=.8, label="music/sfx")
ax[2].plot(tv, librosa.amplitude_to_db(librosa.feature.rms(y=vo, hop_length=256)[0] + 1e-6), lw=.8, label="voice")
for tw, w in words:
    ax[2].text(tw, -10, w, fontsize=7, rotation=90)
ax[2].legend(loc="lower right")
plt.tight_layout()
plt.savefig(f"{name}_sound.png", dpi=80)
print(open(f"{name}_sound.txt").read()[:3000])
