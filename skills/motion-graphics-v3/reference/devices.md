# MG V3 device library

Each device: what it is, where it was measured (reference + frames), and how to build it (kit.js call / v3lib.py helper).
All times are absolute seconds on the one paused timeline; word times come from `K.t(i)` / `F.t(i)` (forced-aligned).

## Worlds (backgrounds) — a film uses 3–5 of them and moves between them with a transition device
| world | class | from | notes |
|---|---|---|---|
| Paper | `w-paper` + `.grid` + `.blob`s | REF-A f47-130 (#E7E8E2) | faint 90 px grid, soft blurred grey spheres drifting; dark ink type |
| Paper + leaves | `w-paper` + `leaves.png` (multiply, .5) | REF-A NeXT f211-260 | palm-leaf shadows drifting 60 px over the scene |
| Satin | `w-satin` | REF-A f135-210 | white cloth light; script keyword |
| Grey | `w-grey` + faint document texture (.035) | REF-B (#BFBFBF, floor #55564F) | grey-on-grey type, gradient cards, tape |
| Ink | `w-ink` | REF-C f429-905 (#0E0D12) | thin light type, thin white strokes, echo rings |
| Black | `w-black` | REF-A f366-517 | label cards, small window clips, staircase captions |
| Real page | `page_plane()` | REF-C f216-330, f398-424 | a real web page/paper, tilted 7-9°, B&W, vignette, DOF |
| Photo | full-bleed B&W photo + dark gradient | REF-A f331-350 | for the big condensed stacked type |

## Arrivals
| device | call | from |
|---|---|---|
| word lands on its spoken onset (blur 10→0, 0.16 s) | `W(i,'text')` + `K.words('#sN')` | all three: every caption |
| word modes | `mode='rise'|'slideR'|'slideL'|'pop'|'letters'|'scramble'|'type'|'grey'|'cut'` | REF-B per-letter bounce, REF-C scramble "Categories", REF-B typewriter |
| hero word with RGB split from the side | `K.rgb(sel,t)` | REF-A "NOBODY" f7-12 |
| odometer roll (years, versions, money) | `odo('2010','2020',...)` + `K.odo(sel,t,dur)` | REF-C 1920→1970 f1-44 |
| bar → card mask | `K.barCard(sel,t)` | REF-A f47-60 |
| sliver → card | `K.sliver(sel,t)` | REF-B f292-300 |
| cutout rises out of its card (head breaks the top edge) | `.mask` (bottom = card bottom) + `K.rise(img,t)` | REF-B f1-10, REF-A f47-90 |
| cutout drops in from the top | `K.drop(img,t)` | REF-A Pixar f261-270 |
| cutout slides in behind another | `K.slide(img,t,dx)` | REF-A f61-80 |
| logo / mark focus-in | `K.blurIn(sel,t,0.35,22)` | REF-A NeXT cube |
| pen arrow / pen circle / underline drawing on | `pen_path(d,...)` + `K.draw(sel,t)` | REF-B f136-215, REF-A staircase underlines |
| handwritten label writing on | `.t-hand` + clip-path inset tween | REF-A signature f71-90 (never fake a real signature: write the NAME as a pen label) |
| highlighter sweep on the real word | `page_plane(..., hls)` + `K.hl(sel,t)` | REF-C f216-330 |
| black redaction bar under a caption | `.abs` black bar `scaleX 0→1` | REF-A f106-118 |
| echo rings on a stressed word | `.ring` + `K.pulse(sel,t)` | REF-C f571-620 |
| specular sheen across a disc / logo | `K.sheen(sel,t)` | REF-C Al Ries circle f337-397 |
| photo stack wiping up, faster each time | `.mask` per photo + `yPercent 100→0` | REF-B f341-419 |

## Layering (depth sandwich) — the signature of the style
ground → card/disc → **words** → **cutout** → captions → finish. The big name or heading sits BEHIND the person's
head, 30–55 % covered (REF-B "Daniela", REF-A "PIXAR", REF-C "Al Ries"). Put the words in the scene before the cutout's
`.mask`, and give the cutout's mask a higher z-index.

## Transitions (use 4–6 kinds per film; never crossfade worlds)
| device | call | from |
|---|---|---|
| light flash + anamorphic streak (open) | `K.flash('#flash','#streak',t)` | REF-A f1-5 |
| zoom-blur out / in | `K.zoomOut(cam,t,dur,s0)` / `K.zoomIn` | REF-A f45-46, REF-B f26-27 |
| whip pan | `K.whipOut` / `K.whipIn` | REF-C f241-260 |
| blur dissolve | `K.blurOut` / `K.blurIn` | REF-A f211-220 |
| colour flood (wipe) into the next world | clip-path inset tween on the scene | REF-C slab |
| circle iris portal (a shape on screen becomes the window) | `K.iris(scene,t)` | REF-A f358-370 |
| light-leak burn | `K.leak('#leak',t)` | REF-C f201-215 |
| skewed colour slabs | `#slab1/#slab2` xPercent | REF-C f425-430 |
| letterbox in | `K.letterbox(top,bot,t)` | REF-A f159-171 |
| bloom to white | `K.bloom('#flash',t)` | REF-A f517-525 |
| spin-out | rotation + blur on the cam | REF-C f391-397 |
| barcode stripe glitch | full-frame repeating stripes, 2-3 frames | REF-C f831-855 |
| slice glitch on a word (2 frames) | `.s-slice` clones + `K.slices(sel,t)` | REF-A f17-18 |

## Garnish (makes it read "editorial", REF-A)
tiny mono text block TL, italic serif index number TR ("001"), `+` crosshairs, a bottom ticket (rule + mono + barcode
+ mark), spec labels with barcodes / QR / hatch, tracked micro caps between cards (`.t-track`), source tags on real
pages (`.label` + `.t-mono`). Barcodes and QR are drawn deterministically by `barcode()` / `qr()`.

## V3.1 — devices measured off REF-D (Costco) — "objects that act"
| device | call | from |
|---|---|---|
| moving person cut-out (video + alpha, bottom fade) | `vcut(src, id, style, f0, f1, start=a, dur=b-a)` + `tools/vcut.sh` | the user's v1 note ("mundane") |
| letters fly in from scattered spots and assemble | `letters(text, cls)` + `K.assemble('.cls', t)` | REF-D 0.2-0.6 s |
| object flies in spinning, parks, keeps turning | `K.fly(sel, t, {y, rot, s0, dur, until, spin})` | REF-D cheese 25.7 s, money 33.7 s |
| extruded heavy type | `ext(depth, colour)` in a style + `font-family:'V3 Heavy'` | REF-D every headline |
| word slams in big → 1 with overshoot | `K.slam(sel, t)` | REF-D headline words |
| ribbon with a word riding it, swoops in/out | `ribbon_svg(id, d, colour, text)` + `K.ribbon('#id-p', '#id-t', t, {...})` | REF-D 12.6-15.2 s |
| word-search grid, bar finds the word | `wordsearch(word, row)` + bar `scaleX` + `.wsh` pop | REF-D 5.0-6.5 s |
| phone with a real page, snap zoom into the screen | `phone(x,y,w,h,inner)` + `K.snap(wrapper, t, 1, 1.75, {x1, y1})` | REF-D laptop 22-25.7 s |
| selection box with handles opens on a word | `selbox(x,y,w,h,inner)` + scaleX from a sliver | REF-D "RECIPROCITY" 15.3 s |
| ink blots bleed over the frame (transition) | `blots(id)` overlay + `K.blots('#id circle', t)` | REF-D 4.8 s |
| building / store rises from the bottom | mask + `y 1200 → 0`, expo.out 0.75 s | REF-D 0-0.6 s |
| chart line draws through real numbers, arrow out of the top | SVG path `pathLength=1` + `K.draw`, dots `stagger` | REF-D 9-12.6 s |
| silhouettes walk away (step bob while receding) | `K.walk(sel, t0, t1, {rate, bob})` + scale/y on a wrapper | v2 "walked out" |
| colour worlds | `w-clay`, `w-ivory`, `w-slate`, `w-kraft`, real sky photo, `grid-l`, `rays`, `glow` | REF-D |

Scenes are NOT timed clips in the root (a `<video>` with its own data-start cannot sit inside a timed wrapper): each
scene div is switched on/off with two timeline `set`s (v3lib does it) and every video carries its own start/duration.
