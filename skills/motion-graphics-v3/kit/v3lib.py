"""MOTION GRAPHICS V3 — HTML builders for the device library (pairs with kit.js / kit.css).
A film is a list of scenes; each scene is (id, start, end, world classes, inner html, js). build() writes one
HyperFrames index.html: kit CSS inlined, every scene a timed .clip, every device a tween on one paused timeline.
"""
import json, html, math
from pathlib import Path

KIT = Path(__file__).resolve().parent


class Film:
    def __init__(self, root, w=1080, h=1920, fps=30, title='MG V3 film'):
        self.root = Path(root); self.w, self.h, self.fps, self.title = w, h, fps, title
        self.words = json.load(open(self.root / 'work/words.json'))
        self.scenes, self.globals_html, self.globals_js, self.media = [], [], [], []
        self.cues = []
        self.duration = 0

    # ---- word helpers -------------------------------------------------------------------------
    def t(self, i, d=0.0):
        return round(self.words[i]['start'] + d, 3)

    def e(self, i, d=0.0):
        return round(self.words[i]['end'] + d, 3)

    def text(self, i):
        return self.words[i]['text']

    # ---- scenes ---------------------------------------------------------------------------------
    def scene(self, sid, start, end, world, inner, js='', z=None):
        self.scenes.append(dict(id=sid, start=round(start, 3), end=round(end, 3), world=world, inner=inner, js=js,
                                z=z if z is not None else 10 + len(self.scenes)))
        self.duration = max(self.duration, end)

    def sfx(self, t, name, db=-12):
        """Queue a sound effect whose peak lands on picture time t (written to work/sound.json at build)."""
        self.cues.append([round(t, 3), name, db])

    def overlay(self, html_, js=''):
        self.globals_html.append(html_); self.globals_js.append(js)

    def add_media(self, html_):
        self.media.append(html_)

    def build(self, out='index.html', duration=None):
        dur = duration or self.duration
        css = (KIT / 'kit.css').read_text().replace('url("../fonts/', 'url("assets/fonts/').replace('url("../img/', 'url("assets/img/')
        words_js = json.dumps([{'t': w['text'], 'start': w['start'], 'end': w['end']} for w in self.words])
        sc_html, sc_js = [], []
        for s in self.scenes:
            # Scenes are NOT timed clips: moving cut-outs (<video> with their own data-start) cannot sit inside a timed
            # wrapper, so each scene is switched on/off by two timeline sets instead (seek-safe, deterministic).
            sc_html.append(
                f'<div id="{s["id"]}" class="scene {s["world"]}" data-v3-start="{s["start"]}" data-v3-end="{s["end"]}" '
                f'style="z-index:{s["z"]};visibility:{"visible" if s["start"] <= 0 else "hidden"}" data-layout-allow-overlap data-layout-allow-overflow>\n{s["inner"]}\n</div>')
            sc_js.append(f'// ---- {s["id"]} [{s["start"]} - {s["end"]}]\n'
                         + (f'tl.set("#{s["id"]}", {{visibility: "visible"}}, {s["start"]}); ' if s["start"] > 0 else '')
                         + f'tl.set("#{s["id"]}", {{visibility: "hidden"}}, {s["end"]});\n{s["js"]}')
        doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width={self.w}, height={self.h}" />
<title>{html.escape(self.title)}</title>
<script src="assets/vendor/gsap.min.js"></script>
<script src="assets/v3/kit.js"></script>
<style>
{css}
html, body {{ margin: 0; background: #000; }}
#root {{ position: relative; width: {self.w}px; height: {self.h}px; overflow: hidden; background: #000; }}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{round(dur, 3)}" data-width="{self.w}" data-height="{self.h}">
{chr(10).join(sc_html)}
{chr(10).join(self.media)}
{chr(10).join(self.globals_html)}
</div>
<script>
window.V3_WORDS = {words_js};
const tl = gsap.timeline({{ paused: true }});
const K = V3.init(tl, window.V3_WORDS);
{chr(10).join(sc_js)}
{chr(10).join(self.globals_js)}
window.__timelines = window.__timelines || {{}};
window.__timelines["main"] = tl;
</script>
</body>
</html>
"""
        (self.root / out).write_text(doc)
        sj = self.root / 'work/sound.json'
        if self.cues and sj.exists():
            cfg = json.load(open(sj)); cfg['cues'] = sorted(self.cues); cfg['duration'] = round(dur, 3)
            json.dump(cfg, open(sj, 'w'), indent=1)
        return self.root / out


# ---- markup helpers ------------------------------------------------------------------------------
def esc(s):
    return html.escape(s)


def W(i, text, cls='', mode='blur', d=0.0, style='', **data):
    """One spoken word on screen. It lands on word i's onset (+d)."""
    extra = ''.join(f' data-{k}="{v}"' for k, v in data.items())
    if mode in ('type', 'letters', 'scramble'):
        inner = ''.join(f'<span class="c">{esc(c)}</span>' for c in text)
    else:
        inner = esc(text)
    return f'<span class="w {cls}" data-w="{i}" data-mode="{mode}" data-d="{d}" style="{style}"{extra}>{inner}</span>'


def odo(frm, to, cls='', size=200, color='', spins=None, style=''):
    """Odometer: a column per character. Columns whose glyph changes roll through the digits between
    (plus `spins` extra full turns, defaulting to more turns on the right, like REF-C's year roll)."""
    assert len(frm) == len(to)
    cols, n = [], len(to)
    for k, (a, b) in enumerate(zip(frm, to)):
        if a == b or not (a.isdigit() and b.isdigit()):
            seq = [b] if a == b else [a, b]
        else:
            ex = spins[k] if spins else (n - 1 - k == 0) * 1
            seq, d = [a], int(a)
            steps = (int(b) - int(a)) % 10 + 10 * ex
            for _ in range(steps):
                d = (d + 1) % 10; seq.append(str(d))
        cols.append('<span class="col">' + ''.join(f'<span style="height:{size}px;line-height:{size}px">{esc(c)}</span>' for c in seq) + '</span>')
    return f'<span class="odo {cls}" data-h="{size}" style="height:{size}px;line-height:{size}px;font-size:{size}px;{color and "color:" + color + ";"}{style}">{"".join(cols)}</span>'


def barcode(seed=7, w=260, h=70, color='#1C1B1E', bars=46):
    x, out, s = 0.0, [], seed
    unit = w / (bars * 2.2)
    for k in range(bars):
        s = (s * 1103515245 + 12345) & 0x7fffffff
        bw = unit * (1 + (s >> 8) % 3); gap = unit * (0.6 + ((s >> 4) % 3) * 0.5)
        if x + bw > w: break
        out.append(f'<rect x="{x:.1f}" y="0" width="{bw:.1f}" height="{h}" fill="{color}"/>'); x += bw + gap
    return f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}">{"".join(out)}</svg>'


def qr(seed=3, n=21, px=6, color='#1C1B1E'):
    s, out = seed, []
    for y in range(n):
        for x in range(n):
            s = (s * 1103515245 + 12345) & 0x7fffffff
            corner = (x < 7 and y < 7) or (x > n - 8 and y < 7) or (x < 7 and y > n - 8)
            if corner:
                on = (x % 6 == 0 or y % 6 == 0 or (2 <= x % 14 <= 4 and 2 <= y % 14 <= 4)) if True else False
                cx, cy = x if x < 7 else x - (n - 7), y if y < 7 else y - (n - 7)
                on = cx in (0, 6) or cy in (0, 6) or (2 <= cx <= 4 and 2 <= cy <= 4)
            else:
                on = (s >> 9) & 1
            if on: out.append(f'<rect x="{x*px}" y="{y*px}" width="{px}" height="{px}"/>')
    return f'<svg width="{n*px}" height="{n*px}" fill="{color}">{"".join(out)}</svg>'


def pen_path(d, color='#1C1B1E', width=6, cls='', style=''):
    return f'<path class="pen {cls}" d="{d}" pathLength="1" stroke="{color}" stroke-width="{width}" style="stroke-dasharray:1;stroke-dashoffset:1;{style}"/>'


def svg(w, h, inner, cls='', style=''):
    return f'<svg class="abs {cls}" width="{w}" height="{h}" viewBox="0 0 {w} {h}" style="{style}" data-layout-ignore>{inner}</svg>'


def plus(x, y, color='#1C1B1E'):
    return f'<div class="plus" style="left:{x}px;top:{y}px;color:{color}" data-layout-ignore></div>'


# ---------------- V3.1 helpers (REF-D) ------------------------------------------------------------------------------
def ext(depth=10, col='#7A3A26', shadow=True, dx=1.0, dy=1.0):
    """CSS text-shadow for heavy EXTRUDED type: `depth` 1-px layers down-right in `col`, then a soft drop shadow."""
    layers = [f'{dx*k:.1f}px {dy*k:.1f}px 0 {col}' for k in range(1, depth + 1)]
    if shadow:
        layers.append(f'{dx*depth+6:.0f}px {dy*depth+14:.0f}px 22px rgba(0,0,0,.35)')
    return 'text-shadow:' + ','.join(layers) + ';'


def letters(text, cls='c', style=''):
    """Each character in its own inline-block span (for K.assemble / per-letter moves)."""
    return ''.join(f'<span class="{cls}" style="display:inline-block;{style}">{esc(c) if c != " " else "&nbsp;"}</span>' for c in text)


def ribbon_svg(rid, d, color, text, text_color='#F0EEE6', width=150, w=1080, h=1920, z=30, font_size=92):
    """A swooping ribbon (REF-D): thick round-capped stroke along path d (extend it past the frame on both ends) with the
    word riding along it on a textPath. Animate with K.ribbon('#rid-p', '#rid-t', t, {...})."""
    return (f'<svg class="abs ribbon" width="{w}" height="{h}" viewBox="0 0 {w} {h}" style="left:0;top:0;z-index:{z};overflow:visible" data-layout-ignore>'
            f'<defs><path id="{rid}-path" d="{d}" pathLength="1000"/></defs>'
            f'<path id="{rid}-p" d="{d}" pathLength="1000" stroke="{color}" stroke-width="{width}" stroke-linecap="round" fill="none" style="opacity:0;filter:drop-shadow(0 18px 24px rgba(0,0,0,.35))"/>'
            f'<text dy="{font_size*0.34:.0f}" fill="{text_color}" style="font-size:{font_size}px"><textPath id="{rid}-t" href="#{rid}-path" startOffset="-50%" text-anchor="middle">{esc(text)}</textPath></text>'
            f'</svg>')


def wordsearch(word, row, cols=10, rows=12, cell=86, seed=5, pool='ABCDEFGHIKLMNOPRSTUVWY', hit_class='hit'):
    """Word-search grid (REF-D 5.0-6.5 s): random letters with `word` hidden in `row` (centred). Returns (html, x0, x1)
    where x0/x1 are the pixel span of the word inside the grid (for the highlight bar)."""
    s, cells = seed, []
    c0 = (cols - len(word)) // 2
    for r in range(rows):
        for c in range(cols):
            s = (s * 1103515245 + 12345) & 0x7fffffff
            if r == row and c0 <= c < c0 + len(word):
                cells.append(f'<span class="{hit_class} wsh">{word[c - c0]}</span>')
            else:
                cells.append(f'<span>{pool[(s >> 8) % len(pool)]}</span>')
    html_ = (f'<div class="ws" style="grid-template-columns:repeat({cols},{cell}px);grid-auto-rows:{cell}px;width:{cols*cell}px">'
             + ''.join(cells) + '</div>')
    return html_, c0 * cell, (c0 + len(word)) * cell


def selbox(x, y, w, h, inner, cls=''):
    """Design-tool selection box with corner handles around `inner` (REF-D "RECIPROCITY")."""
    return (f'<div class="selbox {cls}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px">'
            f'<i></i><i></i><i></i><i></i>{inner}</div>')


def phone(x, y, w, h, inner, pid='phone', style=''):
    return (f'<div class="phone" id="{pid}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;{style}">'
            f'<div class="scr">{inner}<div class="isl"></div></div></div>')


def blots(bid, n=9, seed=4, color='#0B0B0C', w=1080, h=1920, z=95):
    """Ink-blot transition layer (REF-D 4.8 s): circles under a goo filter; animate with K.blots('#bid circle', t)."""
    s, cs = seed, []
    for k in range(n):
        s = (s * 1103515245 + 12345) & 0x7fffffff; x = 80 + (s >> 6) % (w - 160)
        s = (s * 1103515245 + 12345) & 0x7fffffff; y = 120 + (s >> 6) % (h - 240)
        s = (s * 1103515245 + 12345) & 0x7fffffff; r = 380 + (s >> 6) % 420
        cs.append(f'<circle cx="{x}" cy="{y}" r="0" data-r="{r}"/>')
    return (f'<svg id="{bid}" class="abs" width="{w}" height="{h}" viewBox="0 0 {w} {h}" style="left:0;top:0;z-index:{z};pointer-events:none" data-layout-ignore>'
            f'<defs><filter id="{bid}-goo"><feGaussianBlur stdDeviation="28"/><feColorMatrix values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 40 -14"/></filter></defs>'
            f'<g fill="{color}" filter="url(#{bid}-goo)">{"".join(cs)}</g></svg>')


def vcut(src, vid, style='', fade_from=72, fade_to=90, media_start=0.0, start=0.0, dur=None, track=3):
    """A moving person cut out of real footage (WebM VP9 + alpha from `hyperframes remove-background`). The wrapper
    (id=vid) is what devices animate; the <video> inside is the timed clip (absolute start/duration). The bottom fades
    out (tables, mugs, crop lines)."""
    m = f'linear-gradient(#000 {fade_from}%, transparent {fade_to}%)'
    ms = f' data-media-start="{media_start}"' if media_start else ''
    dd = f' data-duration="{round(dur, 3)}"' if dur else ''
    return (f'<div id="{vid}" class="cut" style="{style}">'
            f'<video id="{vid}-v" class="clip" src="{src}" muted playsinline data-start="{round(start, 3)}"{dd}{ms} data-track-index="{track}" '
            f'style="display:block;width:100%;-webkit-mask-image:{m};mask-image:{m}"></video></div>')
