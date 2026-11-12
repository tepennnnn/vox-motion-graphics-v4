---
name: motion-graphics-v3
description: >-
  "Motion graphics V3" (also "MG V3", "motion graphic V3", "the V3 style", "the Steve Jobs / Edison / Al Ries style") — the
  user's editorial story motion-graphics style for SHORTS (9:16) and LONG FORM (16:9): a narrated story (a founder, a
  company, an invention, an idea) told as full motion graphics built on REAL material — the real people as B&W cut-outs
  (background removed) rising out of cards with their name behind their head, the real web pages / papers tilted with
  an orange highlighter on the exact words, real logos focusing in, real product UI on streetwear label cards, a real
  clip in a small window — on paper / grey / ink worlds with grids, tape, pen arrows, barcodes and crosshairs, every
  spoken word landing on screen on its onset in mixed type (thin sans + bold + italic serif + script), odometer years,
  huge condensed stacked type for the stat, light-leak / iris / zoom-blur / whip transitions, soft sub-thump sound on
  each world change. Learned frame by frame from three Pinterest reels (Sharoz Media "Steve Jobs", Rida Visual "Thomas
  Edison", Rivinity "Al Ries") and EarnEdits "Costco free samples" (colour worlds, objects that act). Free and local: Kokoro voice, wav2vec2 word alignment, HyperFrames render. Use whenever
  the user says motion graphics V3 / MG V3, gives a story or topic to tell this way, or wants a faceless story short,
  a founder/company origin story, or an editorial "cut-out photos + real pages" explainer.
---

# MOTION GRAPHICS V3 — the editorial story edit

The voice tells a story; the screen shows the evidence. Every line is one **world** held 2–4 s in which things
**arrive on the words**: the person's real photo cut out and rising out of a card, the line's words landing one by one
in mixed type, a pen arrow, a highlighter on the real page. Monochrome everywhere, one accent colour.

> **Where it comes from.** `reference/REF-A_jobs.md` (20 s, 601 frames), `REF-B_edison.md` (17.5 s, 419 frames),
> `REF-C_ries.md` (35 s, 1050 frames): every frame looked at on labelled contact sheets, cuts measured by frame diff,
> the voice split from the music (Demucs) and the sound measured on its own (`reference/SOUND.md`).
> `REF-D_costco.md` (50 s, 1509 frames) adds the "fire" layer: colour worlds every 2–3 s, real objects that ACT over the
> words, heavy extruded type. Motion was measured with dense optical flow (`tools/motion_study.py`) on all four.
> Worked example: `example/build.py` — "How Claude was born" v2 (49 s, 16 scenes, 2026-10-26).

**Read before building:** `reference/devices.md` (the library + which call builds each device) · `reference/look.md`
(colour, type tiers, rhythm, 9:16 vs 16:9) · `reference/sourcing.md` (real images, cut-outs, pages, licences) ·
`reference/SOUND.md` · `NOTES.md` (the user's own rules, they win) · `example/build.py`.

## ⭐ What makes it V3 (the things a first draft gets wrong)
0. **Read NOTES.md first.** Demo v1 was called "mundane" and "AI sounds strange": both are now rules there, with
   measured targets (dead frames ≤ 30 %, camera moving ≥ 50 %, local motion ≥ 0.8 px) that `tools/motion_study.py`
   checks on every render.
1. **Held worlds, busy insides.** Not a cut every second (that is Editor V1). A world holds 2–4 s; inside it a new
   element lands every 0.2–0.5 s on the words. ~22 % of frames have big motion in the references.
2. **Real people as cut-outs, layered — and MOVING.** B&W, high contrast, rising out of a card / dropping in from
   the top, the head breaking the card's top edge; two or three cut-outs stacked (siblings, eras, the team). When any
   footage of the person exists, cut them out as VIDEO (`tools/vcut.sh … --pingpong`, `vcut()` in v3lib) so they
   talk and turn. Stills only for archive people. Rectangles are for taped photo stacks and small window clips.
3. **The depth sandwich.** ground → card/disc → the big word → the cut-out. The name or heading sits BEHIND the head,
   30–55 % covered ("Daniela", "PIXAR", "Al Ries").
4. **Every spoken word is on screen at its onset** — as design, not subtitles: thin connectors + one bold key word +
   one italic/script feeling word. Word times are forced-aligned (`tools/align.py`), never guessed.
5. **Real pages with a highlighter.** Capture the real page (`tools/capture.py --find`), tilt it 7–9°, B&W, vignette,
   depth of field, and sweep the accent highlighter over the EXACT words (their pixel boxes come from the capture).
6. **Objects that act (REF-D).** Every scene has one physical action: the mark spins up and parks in front of the
   word (`K.fly`), letters assemble from all sides (`K.assemble`), a building rises from the bottom, words ride
   swooping ribbons (`ribbon_svg` + `K.ribbon`), a phone slides in on a tilted colour card and the camera snap-zooms
   into its screen (`phone()` + `K.snap`), a word is found in a word-search (`wordsearch()`), a chart line draws through
   the real numbers, banknotes spin in under BILLION, ink blots bleed into the next world (`blots()` + `K.blots`),
   silhouettes walk into a door of light (`K.walk`).
7. **Puns on top of the facts.** "walked out" → a doorway of light with their silhouettes; "constitution" → the 1787
   "We the People" parchment before Anthropic's real one. Names, dates and numbers are always the real thing.
8. **Transitions with a cause, 4–6 kinds per film** (flash streak, zoom-blur, whip, iris from a shape, light leak,
   colour slabs, bloom to white, barcode glitch). Worlds never crossfade.
9. **Colour worlds + ONE accent.** Photos stay B&W, but the WORLDS change colour scene to scene (clay `w-clay`, ivory
   `w-ivory`, slate `w-slate`, a real sky photo, black, grey). Headlines are heavy extruded type (`ext()`).
10. **Garnish**: mono micro text, italic index numbers, crosshairs, a bottom ticket with a barcode, spec labels.
11. **Sound**: one soft sub thump/whoosh per world change, a few soft accents, one riser into the payoff; bed ~9 LU
    under the voice, dip under the thesis line. No harsh ticks or glitch noise.

## ⛔ Hard rules
- Real material on every beat; fact-check each claim against two sources while sourcing (`reference/sourcing.md`);
  hedge what is unconfirmed. Never fake a real person's signature, document or quote.
- Log every image/clip with its licence in `SOURCES.md`; credit on the end card / description.
- The render never grades: treat stills with `tools/treat.py` first. GSAP only animates wrappers/children, never a
  CSS-transformed element; every reveal is seek-safe (kit.js handles it — use the kit calls).
- Show the person the script + sources before the final render when they asked for a plan; otherwise cook and deliver.
- Publish nothing.

## Workflow
Every step: `source ~/.claude/skills/motion-graphics-v3/tools/env.sh` (picks the local Python envs; on a fresh machine run
`tools/setup.sh` once). `SK=~/.claude/skills/motion-graphics-v3`.

0. **Project:** `bash $SK/tools/new_film.sh <dir> 9x16` (or `16x9` for long form).
1. **Story + script** (`work/script.json`): 12–18 short lines, one beat each, ~2.5 words/s; hook line first ("Nobody
   tells you how … was born"), thesis line near the end ("Sometimes, walking away is the start."), one-line CTA.
   `shown` is what appears; `spoken` is how Kokoro should say it ("Dario Ahmo-day", "twenty_twenty"; `_` joins spoken
   words that make ONE shown word, so the counts match). Acronyms stay plain (`AI`, `OpenAI`, `GPT-3`): never `A.I.`.
   - **Narrated (default):** `$MGV3_TTS $SK/tools/vo.py <dir>` (Kokoro am_michael ×1.08) → `assets/audio/vo.wav` + line windows.
   - **His own recording:** `python3 $SK/tools/from_recording.py <dir> <file>` (cut flubs first).
   Then `$MGV3_ALIGN $SK/tools/align.py <dir>` → `work/words.json` (exact onsets, every shown word).
2. **Source** (`reference/sourcing.md`): moving cut-outs from real footage (`tools/vcut.sh`), photos (Wikimedia Commons API with licences; the company's official video for
   people with no free photo — find each person by their lower-third), cut-outs (`npx hyperframes remove-background`
   + `$MGV3_IMG $SK/tools/treat.py --keep … --feather 0.1`), pages (`$MGV3_IMG $SK/tools/capture.py … --find "word|word"`
   then `treat.py --look paper --maxh 6000` so the boxes stay valid), logos (Commons SVG), one small real clip.
   Make a contact sheet of the cut-outs and LOOK at it.
3. **Plan the beats:** one scene per line, each a device from `reference/devices.md`, worlds alternating
   (dark hook → paper → page → grey → black → paper+leaves → ink → document → page → black labels → satin → paper →
   photo → black → paper CTA in the example). Pick 4–6 transition kinds.
4. **Build** `build.py` (start from `build.example.py`): `F.scene(id, start, end, world, html, js)`; words with
   `W(i, 'text', mode=…)`, devices with `K.*`. Times from `F.t(i)` (word onsets). `python3 build.py` → `index.html`.
5. **Check:** `npx hyperframes check --json` (0 errors), then `npx hyperframes snapshot . --no-end -o work/snaps --at …`
   at every beat and LOOK: text clipped at the frame edge, words over busy textures, a cut-out's crop edge showing,
   something visible before its entrance, a pen mark on the wrong word.
6. **Sound:** write `work/sound.json` (cues on the picture times, see the example) → `python3 $SK/tools/mix.py <dir>`.
7. **Render:** `npx hyperframes render . -o renders/v1.mp4 -q delivery` (~1 min for 50 s), then master and mux:
   `ffmpeg -i vo -i bed -i sfx amix … alimiter … loudnorm=I=-15:TP=-1.2` → `-c:v copy` (see example notes).
   Contact-sheet the RENDER at 5 fps (`tools/sheets.py`) and look again; re-transcribe the final to prove no word is masked;
   run `tools/motion_study.py render.mp4 NAME` and compare with NOTES.md targets (and `tools/motion_sheets.py` to SEE
   where the motion is). Fix and re-render until it passes.
8. Deliver to the Desktop as `<Title>_MG-V3.mp4` with a 3-line note (length, what's real, sources).

## Long form (16:9)
`Film(root, w=1920, h=1080)`. Same worlds and devices; cards on one third with the words on the other; hook and each
chapter open at short-form pace, the body holds a world 4–6 s with more arrivals inside it. Over a talking head: his
recording is the voice (`from_recording.py`); his face is one more world (matte him with `remove-background` on the
video and stand him in front of a paper world with the chapter heading behind his head) ~25–35 % of runtime.

## Learning another reference into V3
Download it (`yt-dlp`), dump every frame, `tools/sheets.py frames fps out` (labelled sheets + frame-diff TSV), read every
sheet, write `reference/REF-X.md` (frames · time · what · device), split the sound
(`$MGV3_AUDIO -m demucs --two-stems=vocals`) and run `tools/sound_study.py`. Add new devices to `kit.js`/`devices.md`.

## Files
`SKILL.md` · `NOTES.md` (user rules) · `reference/` (REF-A/B/C, SOUND, devices, look, sourcing) · `kit/` (`kit.css`,
`kit.js`, `v3lib.py`, OFL fonts, grain + leaf-shadow textures, soft SFX kit, gsap) · `tools/` (`env.sh`, `setup.sh`,
`new_film.sh`, `vo.py`, `from_recording.py`, `align.py`, `capture.py`, `treat.py`, `vcut.sh`, `mix.py`, `sheets.py`,
`motion_study.py`, `motion_sheets.py`, `sound_study.py`) · `example/` (the approved Anthropic demo: `build.py`, `script.json`, `sound.json`).
