# MG V3 look — measured, then turned into rules

## Colour
- **Monochrome first.** REF-B is 97 % low-saturation frames, REF-A 55 %. Every photo and page is graded B&W
  (`tools/treat.py --look mono|mono_soft|warm|paper|ink`) before the build; the render never grades.
- **One accent per film**, used only where it carries meaning: highlighter, the key number, a pen circle, a CTA word.
  Default accent = the subject's brand colour if it has one (Anthropic clay #D97757 = also the user's own accent);
  otherwise #D97757.
- Tokens: paper #E9E7E1 · satin #F3F2EF · grey #BEBEBC / floor #55564F · ink #0F0E13 · cream labels #F2EEE4 ·
  dark type #1C1B1E · grey type #6F6E6A · light type #EDEBE6.

## Type (five tiers, REF-A) — fonts are OFL, shipped in kit/fonts
| tier | class | use | 9:16 size |
|---|---|---|---|
| connector words | `.t-thin` Inter 300 | the small words of the line, one per spoken word | 46–58 px |
| key word | `.t-bold` Inter 800 / `.t-head` Inter 900 caps | names, places, the noun the line is about | 96–210 px |
| emotional keyword | `.t-ital` Playfair italic · `.t-script` Pinyon · `.t-black` blackletter | the feeling word (born, research, different way, story) | 100–180 px |
| thesis / stat | `.t-cond` Anton caps | huge stacked white words over a photo, the number | 118–380 px |
| micro | `.t-track` tracked caps · `.t-mono` JetBrains Mono | labels, sources, between label cards | 18–34 px |
Mix two tiers in one line (thin + bold, thin + italic). Never more than one hero word per beat.

## Rhythm (measured)
- **Worlds hold 2–4 s; elements arrive inside them.** REF-A has 9 hard cuts in 20 s; REF-B 10 in 17.5 s; REF-C
  one world every ~2.5 s. Pace comes from words landing on their onsets (every 0.2–0.4 s) and cutouts/cards arriving,
  not from cutting.
- Only ~22 % of frames have big motion (diff > 4): long held layouts with small moves. The camera always drifts
  (push 1.0→1.05 per world, page planes drift and rotate).
- Payoff accelerates: REF-B's photo stack goes 0.5 → 0.45 → 0.35 → 0.3 s per photo.
- Transitions take 0.15–0.45 s. Exits are shorter than entrances.

## Shorts (9:16, 1080×1920) vs long form (16:9, 1920×1080)
- 9:16: keep words between y 200 and 1480; the bottom 400 px is ticket/label/source decoration only.
- 16:9 (`Film(root, w=1920, h=1080)`): same worlds, cards move to the left or right third with the type on the other
  side; hero words 140–260 px; captions ride above the lower third. Hook and every chapter open at short-form pace
  (a world every 2–3 s), the body lets a world hold 4–6 s with more elements arriving inside it (a page being
  highlighted line by line, a photo stack, a label card filling in).
- Over a talking head (long form): the face is one more "world" (cut out with the matte, standing in front of a
  paper/grey world with the heading behind the head, REF-A Pixar template), ~25–35 % of runtime.

## Real material, always (the user's rule)
The person's real photos (cut out), the company's real pages and papers (captured, highlighted), real logos, real
product UI, a real clip in a small window. Metaphor objects (a door for "walked out", a trophy for "wins", the 1787
constitution for "constitution") are welcome on top — puns are part of all three references.
