# Sourcing real material for MG V3 (free, local, with licences logged)

Write every source into the project's `SOURCES.md` (file, origin URL, licence, author). Show the sources table and the
flags to the person before rendering the final; credit CC BY images in the description and on the end card.

| need | where | how |
|---|---|---|
| photos of a person | Wikimedia Commons (API search, licence in `extmetadata`) — TechCrunch, government and event photos are often CC BY 2.0 / public domain | see `tools/commons.py` pattern in the worked example (`work/` notes): `action=query&list=search&srnamespace=6` then `prop=imageinfo&iiprop=url|size|extmetadata`; download ≥ 2600 px files through `/thumb/…/1920px-…` (the API refuses originals without a thumb size) |
| people with no free photo | the company's own official video (YouTube, the company channel) | `yt-dlp -f "bestvideo[height<=1080]"`, scan with a 1 frame / 15 s contact sheet, find each person by their lower-third name tag, grab one clean frame per person; cite "Anthropic (YouTube)" |
| cutouts | `npx hyperframes remove-background in.jpg -o out.png` (u2net human seg, CoreML, ~1 s) | crop the person first (one person per crop), then `tools/treat.py --keep x0,y0,x1,y1 --feather 0.1` drops tables/mugs at the bottom and fades the body so it can rise out of a card |
| real web pages / papers | `tools/capture.py out name URL --find "word|word"` (Playwright) | screenshots at 2× and saves the pixel box of every `--find` phrase, so the highlighter sweeps the exact real words |
| logos | Wikimedia Commons SVGs (`Anthropic logo.svg`, `Claude AI symbol.svg` …) | use as `<img>`; keep their colours |
| documents for puns | public-domain scans (Commons, Library of Congress, NASA) | grade `--look warm` |
| a small real clip | the official video above | `ffmpeg -ss … -t 3-4 … hue=s=0,eq=contrast=1.18` (pre-graded), shown in a small window on black |
| music | the user's own no-copyright track, saved as `assets/audio/music.mp3` (sound.json `bed.src`) | never generate harsh synth beds; no track = voice + effects only |
| sound effects | `kit/sfx/` (Pixabay licence + synthesised) | soft only |

## Fact-checking
Check every claim against two sources (Wikipedia + the primary: the company's page, the paper, a major outlet) while
sourcing the pictures. When sources disagree (e.g. "5 / 7 / 9 co-founders"), write a line that is true either way
("a handful of colleagues followed them"). Hedge what is unconfirmed ("Many believe it's named after Claude Shannon").
