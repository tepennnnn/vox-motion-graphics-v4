# Sound of the three references (voice split from music with Demucs htdemucs, then measured)

| | mix | voice stem | music + FX stem | voice over bed | tempo | what the FX layer is |
|---|---|---|---|---|---|---|
| REF-A Jobs (20 s) | -16.6 LUFS, peak 0 dBFS | -20.1 | -16.7 (LRA 15.9) | bed as loud as the voice, it pumps | ~132 bpm | 21 onsets: a sub "boom/whoosh" on every world change (0.06, 4.52, 7.41, 12.11, 17.31 s land within 0.02 s of the cut), soft risers before the flash and the circle iris |
| REF-B Edison (17.5 s) | -18.2 LUFS | -18.7 | -26.2 | ~7.5 LU under | ~136 bpm | soft piano bed; a low thump-whoosh (energy 40-150 Hz, ~0.4 s tail) at EVERY scene change (~every 2.2 s); a quick tick train under the title (0-3 s); bright glints at the accelerating photo stack |
| REF-C Al Ries (35 s) | -14.3 LUFS | -15.0 | -22.5 | ~7.5 LU under | ~129 bpm | steady pulse bed; little FX: light shimmer on the leaks, one hit on the highlighter cut, a click pattern under the barcode glitch |

## Rules taken from it
- One sound per **world change** (a sub thump + air), not per word. Inside a world, only the moves that carry the story get a sound (cutout rising, highlighter sweep, number roll, name landing).
- The FX peak lands on the cut (≤ 1 frame late). `tools/mix.py` aligns each file's measured peak to picture + 1 frame.
- Bed 7–10 LU under the voice (this user likes it quieter: ~9 LU), no ducking needed because the bed is already low; dip it ~5 dB under the thesis line.
- No harsh ticks, no glitch noise (the user finds them painful — see memory carousel-sound-taste). Soft swishes, sub booms, one riser into the payoff, sparkles only on sheens/logos.
- Master: voice -16 LUFS, mix ≈ -15 LUFS, true peak ≤ -1 dBTP (limit the premix and mux it over the render).
