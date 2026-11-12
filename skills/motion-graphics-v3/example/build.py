"""WORKED EXAMPLE (demo v2, 2026-10-26). Copy the patterns, not the content.
HOW CLAUDE WAS BORN — Motion Graphics V3 demo, v2 (9:16, 1080x1920, 30 fps).
v1 measured "mundane" against the references (tools/motion_study.py): cameras barely moved, nobody in frame moved, no
object ever acted, one monochrome palette, flat type. v2 adds, per scene: a camera that pans 40-120 px/s, real people
MOVING (video cut-outs), an object or the type doing one big physical thing (REF-D), colour worlds, extruded type.
python3 build.py  ->  index.html (+ work/sound.json cues)
"""
import sys, json, math
from pathlib import Path
import os
sys.path.insert(0, str(Path(os.environ.get('MGV3', Path(__file__).resolve().parents[1])) / 'kit'))
from v3lib import (Film, W, odo, barcode, qr, pen_path, svg, plus, esc, ext, letters, ribbon_svg, wordsearch, selbox,
                   phone, blots, vcut)

ROOT = Path(__file__).resolve().parent
F = Film(ROOT, title='How Claude Was Born')
t, e = F.t, F.e
LINES = json.load(open(ROOT / 'work/vo_lines.json'))
END = round(LINES[-1]['end'] + 1.45, 2)
ACC, IV, INK, CLAYD = '#D97757', '#F0EEE6', '#141413', '#9A4A2E'


def SB(k, lead=0.14, tail=0.04):
    """Scene k's window: from just before its line to just past the next line's start (the next scene covers it)."""
    s = 0.0 if k == 0 else LINES[k]['start'] - lead
    en = END if k + 1 >= len(LINES) else LINES[k + 1]['start'] - lead + tail
    return round(s, 3), round(en, 3)


def page_plane(sid, img, boxes_json, focus, s, rot, hls, cx=540, cy=900, mask='ellipse 62% 30% at 50% 47%'):
    boxes = json.load(open(ROOT / boxes_json))
    pw, ph = boxes['w'] * s, boxes['h'] * s
    fx, fy = focus[0] * s, focus[1] * s
    plane = (f'left:{cx - fx:.0f}px;top:{cy - fy:.0f}px;width:{pw:.0f}px;height:{ph:.0f}px;'
             f'transform-origin:{fx:.0f}px {fy:.0f}px;transform:rotate({rot}deg)')
    hl_html = ''
    for k, (text, nth) in enumerate(hls):
        b = [b for b in boxes['boxes'] if b['text'] == text][nth]
        hl_html += (f'<div class="hl {sid}-hl{k}" style="left:{b["x"]*s-6:.0f}px;top:{b["y"]*s-2:.0f}px;'
                    f'width:{b["w"]*s+12:.0f}px;height:{b["h"]*s+4:.0f}px"></div>')
    blur_img = img.replace('.jpg', '_blur.jpg')
    return f'''
  <div class="fill" style="background:#1d1d1d">
    <div class="abs pcam" style="{plane}"><img src="{blur_img}" style="width:100%;height:100%;display:block" alt=""></div>
  </div>
  <div class="fill" style="-webkit-mask-image:radial-gradient({mask}, #000 55%, transparent 100%);mask-image:radial-gradient({mask}, #000 55%, transparent 100%)">
    <div class="abs pcam" style="{plane}"><img src="{img}" style="width:100%;height:100%;display:block" alt="">{hl_html}</div>
  </div>
  <div class="vignette"></div>'''


def page_shift(s, rot, frm, to):
    dx, dy = (to[0] - frm[0]) * s, (to[1] - frm[1]) * s
    r = math.radians(rot)
    return -(dx * math.cos(r) - dy * math.sin(r)), -(dx * math.sin(r) + dy * math.cos(r))


def box(boxes_json, text, nth=0):
    b = [b for b in json.load(open(ROOT / boxes_json))['boxes'] if b['text'] == text][nth]
    return (b['x'] + b['w'] / 2, b['y'] + b['h'] / 2)


HEAVY_IV = f"font-family:'V3 Heavy';text-transform:uppercase;color:{IV};{ext(12, CLAYD)}"
HEAVY_INK = f"font-family:'V3 Heavy';text-transform:uppercase;color:{INK};{ext(10, ACC)}"
CUT = 'position:absolute;left:0;top:0;width:1px;height:1px;opacity:0'

# ================================================================================================================
# S1 HOOK — ink world + god rays; "CLAUDE" extruded letters fly in from everywhere and assemble (REF-D 0.2 s); the
# real Claude mark spins up from below and parks IN FRONT of the word, still turning (REF-D cheese 25.7 s)
a, b = SB(0)
F.scene('s1', a, b, 'w-slate', f'''
  <div class="cam" id="s1-cam">
    <div class="rays" id="s1-rays"></div>
    <div class="glow" style="left:40px;top:430px;width:1000px;height:1000px"></div>
    <div class="abs center-x t-thin light" style="top:470px;font-size:54px">{W(0,'Nobody ')}{W(1,'tells ')}{W(2,'you ')}{W(3,'how')}</div>
    <div class="abs center-x" style="top:610px;font-size:205px;line-height:1;white-space:nowrap;{HEAVY_IV}">{letters('CLAUDE', 's1-l')}</div>
    <img id="s1-spark" class="abs" src="assets/img/Claude_AI_symbol.svg" style="left:330px;top:760px;width:420px;height:420px;filter:drop-shadow(0 30px 40px rgba(0,0,0,.5))" alt="">
    <div class="abs center-x light" style="top:1215px"><span class="t-ital" style="font-size:132px">{W(5,'was ')}{W(6,'born.', cls='acc')}</span></div>
    <div class="abs t-mono light" style="left:70px;top:210px;opacity:.7;font-size:20px" id="s1-hud1">ANTHROPIC<br>THE ORIGIN FILE<br>SAN FRANCISCO · 2021</div>
    <div class="abs light" style="right:70px;top:196px;font:italic 500 64px 'V3 Serif';opacity:.85" id="s1-hud2">001</div>
    <div class="abs" id="s1-ticket" style="left:70px;right:70px;top:1470px;height:150px;border-top:2px solid rgba(237,235,230,.45);color:{IV}">
      <div class="abs t-mono" style="left:0;top:22px;font-size:20px;opacity:.8">THE STORY OF<br>CLAUDE · EST. 2023</div>
      <div class="abs" style="left:330px;top:24px;opacity:.85">{barcode(11, 300, 64, IV)}</div>
      <div class="abs" style="right:0;top:14px;font:900 64px 'V3 Sans';letter-spacing:-.04em">A\\</div>
    </div>
  </div>
  <div class="w" data-w="4" data-mode="cut" style="{CUT}"></div>''', f'''
K.assemble('#s1 .s1-l', 0.0, {{r: 700, dur: 0.5, stagger: 0.03}});
K.cam('#s1-rays', {a}, {b}, {{rotation: 0}}, {{rotation: 24}});
K.cam('#s1-cam', {a}, {b}, {{scale: 1.0, y: 0}}, {{scale: 1.08, y: -60}}, 'power1.out');
K.fly('#s1-spark', 0.55, {{y: 1000, rot: -300, s0: 0.3, dur: 0.6, until: {b}, spin: 40}});
K.in('#s1-hud1, #s1-hud2, #s1-ticket', 0.4, {{blur: 6, dur: 0.2}});
K.words('#s1');
K.slam('#s1 .s1-l', {t(4)}, {{s0: 1.18, dur: 0.22, stagger: 0.02}});
K.zoomOut('#s1-cam', {b - 0.2}, 0.2, 1.08);
''')
F.sfx(0.0, 'subboom_1.wav', -9); F.sfx(0.05, 'whoosh.mp3', -13); F.sfx(0.62, 'swish_1.wav', -14)
F.sfx(1.12, 'sparkle.mp3', -18); F.sfx(t(4), 'impact_2.wav', -17); F.sfx(b - 0.18, 'whoosh.mp3', -12)

# ================================================================================================================
# S2 2020 · DARIO — ivory paper; extruded year rolls 2010 -> 2020; bar -> card; Dario (MOVING, real footage) rises out
# of the card, OPENAI slams in behind his head and the real logo spins in; camera pans 40 px/s
a, b = SB(1)
F.scene('s2', a, b, 'w-ivory', f'''
  <div class="cam" id="s2-cam">
    <div class="grid"></div>
    <div class="blob" id="s2-b1" style="left:-180px;top:1260px;width:560px;height:560px;filter:blur(18px)"></div>
    <div class="blob" id="s2-b2" style="left:780px;top:120px;width:420px;height:420px;filter:blur(22px)"></div>
    <div class="abs" id="s2-year" style="left:0;right:0;top:560px;text-align:center;transform-origin:50% 50%">
      <div class="t-thin dark" style="font-size:54px;margin-bottom:6px">{W(7,'In')}</div>
      {odo('2010', '2020', '', 330, style=HEAVY_INK)}
    </div>
    <div class="card" id="s2-card" style="left:170px;top:640px;width:740px;height:740px;z-index:1"></div>
    <div class="abs" id="s2-head" style="left:0;right:0;top:360px;text-align:center;font-size:200px;white-space:nowrap;line-height:1;z-index:2;{HEAVY_INK}">OPENAI</div>
    <div class="mask" style="left:0;right:0;top:140px;height:1240px;z-index:3">
      {vcut('assets/video/dario_pp.webm', 's2-dario', 'left:150px;bottom:0;width:780px', 70, 96, start=a, dur=b - a)}
    </div>
    <img id="s2-oai" class="abs" src="assets/img/OpenAI_logo_2025_symbol.svg" style="left:790px;top:1180px;width:170px;height:170px;z-index:5;background:{IV};border-radius:50%;padding:18px" alt="">
    <div class="abs t-hand" id="s2-label" style="left:430px;top:1165px;font-size:88px;color:{IV};transform:rotate(-6deg);clip-path:inset(0 100% 0 0);z-index:5">Dario Amodei</div>
    {svg(1080, 1920, pen_path('M580 1165 C 560 1115, 556 1070, 570 1020', IV, 5, 's2-arrow') + pen_path('M552 1044 L570 1014 L592 1040', IV, 5, 's2-arrow'), style='left:0;top:0;z-index:5')}
    <div class="abs center-x" style="top:1420px;z-index:4">
      <span class="t-thin dark">{W(11,'was ')}{W(12,'running ')}</span><span class="t-ital dark" style="font-size:118px">{W(13,'research', mode='slideR')}</span><span class="t-thin dark"> {W(14,'at')}</span>
    </div>
    <div class="abs t-mono dark" style="left:70px;top:1590px;opacity:.6">VP OF RESEARCH · OPENAI · 2016—2020</div>
  </div>''', f'''
K.blurIn('#s2-cam', {a}, 0.18, 14);
K.in('#s2 .odo', {t(8, -0.06)}, {{blur: 8, dur: 0.14}});
K.odo('#s2 .odo', {t(8)}, 0.62);
K.cam('#s2-year', {t(9, -0.35)}, {t(9, -0.02)}, {{y: 0, scale: 1, opacity: 1}}, {{y: -330, scale: 0.4, opacity: 0}}, 'expo.inOut', false);
K.barCard('#s2-card', {t(9, -0.3)}, {{dur: 0.42}});
K.rise('#s2-dario', {t(9, -0.2)}, 820, 0.62);
K.fromTo('#s2-label', {{clipPath: 'inset(0 100% 0 0)'}}, {{clipPath: 'inset(0 0% 0 0)', duration: 0.55, ease: 'power1.inOut'}}, {t(10)});
K.draw('#s2 .s2-arrow', {t(10, 0.1)}, 0.35);
K.cam('#s2-b1', {a}, {b}, {{x: 0, y: 0}}, {{x: 80, y: -60}});
K.cam('#s2-b2', {a}, {b}, {{x: 0, y: 0}}, {{x: -70, y: 40}});
K.words('#s2');
K.out('#s2-label, #s2 .s2-arrow', {t(15, -0.25)}, {{dur: 0.18}});
K.slam('#s2-head', {t(15)}, {{s0: 1.6, dur: 0.3}});
K.fly('#s2-oai', {t(15, 0.12)}, {{x: 300, y: 200, rot: 200, s0: 0.3, dur: 0.5}});
K.cam('#s2-cam', {a}, {b}, {{x: 90, scale: 1.0}}, {{x: -90, scale: 1.07}});
K.whipOut('#s2-cam', {b - 0.16}, -1000, 0.16);
''')
F.sfx(a, 'whoosh.mp3', -14); F.sfx(t(8), 'swish_1.wav', -17); F.sfx(t(9, -0.3), 'swish_1.wav', -15)
F.sfx(t(9, -0.2), 'subboom_1.wav', -15); F.sfx(t(15), 'impact_2.wav', -13); F.sfx(t(15, 0.15), 'pop.mp3', -9)
F.sfx(b - 0.16, 'whoosh.mp3', -11)

# ================================================================================================================
# S3 GPT-2 / GPT-3 — the real GPT-3 paper; the camera travels across the author list (REF-C page: 300 px/s pans with a
# -4 %/s zoom) lighting up each future co-founder; GPT-2 slams, rolls to 3 with a snap punch
GP = 'assets/img/page_gpt3.json'; S_, ROT = 0.9, -8
f_dario = box(GP, 'Dario Amodei')
sx_tom, sy_tom = page_shift(S_, ROT, f_dario, box(GP, 'Tom B. Brown'))
a, b = SB(2)
F.scene('s3', a, b, '', f'''
  <div class="cam" id="s3-cam">
    {page_plane('s3', 'assets/img/page_gpt3.jpg', GP, f_dario, S_, ROT,
                [('Dario Amodei', 0), ('Tom B. Brown', 0), ('Benjamin Mann', 0), ('Jared Kaplan', 0), ('Jack Clark', 0), ('Sam McCandlish', 0)])}
  </div>
  <div class="fill" id="s3-scrim" style="background:rgba(10,10,12,.82);opacity:0"></div>
  <div class="abs" id="s3-bar" style="left:200px;top:300px;width:680px;height:92px;background:#0E0E10;transform-origin:0 50%"></div>
  <div class="abs center-x t-thin light" style="top:318px;font-size:50px">{W(16,'He ')}{W(17,'helped ')}{W(18,'build')}</div>
  <div class="abs center-x" id="s3-gpt" style="top:690px;font-size:260px;line-height:1;{HEAVY_IV}">
    <span class="w" data-w="19" data-mode="pop">GPT-{odo('2', '3', '', 260, style=HEAVY_IV)}</span>
  </div>
  <div class="abs center-x t-thin light" style="top:1000px">{W(20,'and')}</div>
  <div class="label" id="s3-src" style="left:70px;top:1400px;padding:14px 20px;border:2px solid #1C1B1E;opacity:0"><span class="t-mono" style="font-size:21px">ARXIV 2005.14165 · MAY 2020<br>6 OF ITS AUTHORS LATER FOUNDED ANTHROPIC</span></div>''', f'''
K.whipIn('#s3-cam', {a}, 1000, 0.26);
K.cam('#s3 .pcam', {a}, {t(19, -0.1)}, {{scale: 1.22, x: 40, y: 0}}, {{scale: 1.12, x: -60, y: 10}}, 'power1.out');
K.hl('#s3 .s3-hl0', {a + 0.3}, 0.34);
K.fromTo('#s3-bar', {{scaleX: 0}}, {{scaleX: 1, duration: 0.28, ease: 'expo.out'}}, {t(16, -0.12)});
K.fromTo('#s3-scrim', {{opacity: 0}}, {{opacity: 1, duration: 0.18}}, {t(19, -0.12)});
K.words('#s3');
K.odo('#s3-gpt .odo', {t(21, -0.04)}, 0.3, {{stagger: false}});
K.snap('#s3-gpt', {t(21, -0.04)}, 1, 1.14, {{dur: 0.16, blur: 6}});
K.snap('#s3-gpt', {t(21, 0.14)}, 1.14, 1, {{dur: 0.2, blur: 0}});
K.fromTo('#s3-scrim', {{opacity: 1}}, {{opacity: 0, duration: 0.22, immediateRender: false}}, {t(21, 0.5)});
K.out('#s3 [data-w="16"], #s3 [data-w="17"], #s3 [data-w="18"], #s3 [data-w="20"], #s3-bar', {t(21, 0.45)}, {{dur: 0.15}});
K.cam('#s3-gpt', {t(21, 0.5)}, {t(21, 0.82)}, {{y: 0, scale: 1}}, {{y: -470, scale: 0.4}}, 'expo.inOut', false);
K.cam('#s3 .pcam', {t(21, 0.5)}, {t(21, 0.95)}, {{scale: 1.12, x: -60, y: 10}}, {{scale: 0.96, x: {sx_tom:.0f}, y: {sy_tom + 140:.0f}}}, 'expo.inOut', false);
K.hl('#s3 .s3-hl1, #s3 .s3-hl2, #s3 .s3-hl3, #s3 .s3-hl4, #s3 .s3-hl5', {t(21, 0.75)}, 0.2);
K.cam('#s3 .pcam', {t(21, 0.95)}, {b}, {{scale: 0.96, x: {sx_tom:.0f}, y: {sy_tom + 140:.0f}}}, {{scale: 0.92, x: {sx_tom - 160:.0f}, y: {sy_tom + 120:.0f}}}, 'none', false);
K.in('#s3-src', {t(21, 0.8)}, {{blur: 6, dur: 0.18}});
K.blurOut('#s3-cam, #s3-gpt, #s3-src', {b - 0.16}, 0.16, 20);
''')
F.sfx(a, 'whoosh.mp3', -12); F.sfx(a + 0.3, 'swish_1.wav', -19); F.sfx(t(19), 'impact-bass-1.mp3', -17)
F.sfx(t(21), 'pop.mp3', -8); F.sfx(t(21, 0.5), 'whoosh.mp3', -15); F.sfx(t(21, 0.75), 'swish_1.wav', -18)

# ================================================================================================================
# S4 DANIELA — clay world; two ink cards; Dario and Daniela MOVING (real footage) rise out of them; "Daniela" slams
# behind her head; "a different way" rides two RIBBONS that swoop across and out (REF-D 12.6 s)
a, b = SB(3)
F.scene('s4', a, b, 'w-clay', f'''
  <div class="cam" id="s4-cam">
    <div class="grid-l" style="opacity:.5"></div>
    <div class="card" id="s4-card1" style="left:50px;top:700px;width:420px;height:520px;z-index:1"></div>
    <div class="mask" style="left:0;top:330px;width:540px;height:890px;z-index:2">{vcut('assets/video/dario_pp.webm', 's4-dario', 'left:28px;bottom:0;width:470px', 70, 96, media_start=2.0, start=a, dur=b - a)}</div>
    <div class="abs t-thin dark" style="left:70px;top:236px;font-size:56px;color:{INK}">{W(22,'But ')}{W(23,'he ')}{W(24,'and')}</div>
    <div class="abs" style="left:66px;top:300px;font-size:112px;line-height:1;{HEAVY_IV}">{W(25,'his ')}{W(26,'sister')}</div>
    <div class="card" id="s4-card2" style="left:450px;top:640px;width:580px;height:700px;z-index:3"></div>
    <div class="abs" style="left:190px;top:478px;font-size:150px;line-height:1;white-space:nowrap;z-index:4;{HEAVY_INK}">{W(27,'Daniela', mode='rise')}</div>
    <div class="mask" style="left:420px;top:280px;width:660px;height:1060px;z-index:5">{vcut('assets/video/daniela_pp.webm', 's4-dani', 'left:20px;bottom:0;width:620px', 68, 94, start=a, dur=b - a)}</div>
    <div class="abs center-x" style="top:1385px;z-index:6"><span class="t-thin" style="font-size:58px;color:{INK}">{W(28,'wanted ')}{W(29,'AI ')}{W(30,'built')}</span></div>
  </div>
  {ribbon_svg('s4ra', 'M -400 1800 C 200 1740, 520 1500, 1500 1450', INK, 'A different', IV, 168, z=40, font_size=96)}
  {ribbon_svg('s4rb', 'M -420 1930 C 250 1925, 700 1860, 1520 1720', IV, 'way.', INK, 168, z=41, font_size=110)}
  <div class="w" data-w="31" data-mode="cut" style="{CUT}"></div>
  <div class="w" data-w="32" data-mode="cut" style="{CUT}"></div>
  <div class="w" data-w="33" data-mode="cut" style="{CUT}"></div>''', f'''
K.blurIn('#s4-cam', {a}, 0.2, 16);
K.sliver('#s4-card1', {a + 0.06}, 0.34);
K.rise('#s4-dario', {t(23, -0.05)}, 620, 0.55);
K.words('#s4');
K.sliver('#s4-card2', {t(26, -0.16)}, 0.36);
K.rise('#s4-dani', {t(26)}, 820, 0.6);
K.ribbon('#s4ra-p', '#s4ra-t', {t(31, -0.06)}, {{seg: 700, tin: 0.4, hold: 0.55, tout: 0.32, park: 150}});
K.ribbon('#s4rb-p', '#s4rb-t', {t(33, -0.1)}, {{seg: 520, tin: 0.36, hold: {max(0.1, b - t(33, -0.1) - 0.36 - 0.28):.2f}, tout: 0.28, park: 220}});
K.cam('#s4-cam', {a}, {b}, {{scale: 1.0, y: 30, rotation: -0.6}}, {{scale: 1.07, y: -60, rotation: 0.8}});
''')
F.sfx(a, 'whoosh.mp3', -13); F.sfx(a + 0.06, 'swish_1.wav', -16); F.sfx(t(23), 'subboom_1.wav', -16)
F.sfx(t(26, -0.16), 'swish_1.wav', -16); F.sfx(t(26), 'subboom_1.wav', -14); F.sfx(t(31, 0.05), 'whoosh.mp3', -10)
F.sfx(t(33), 'whoosh.mp3', -11)

# ================================================================================================================
# S5 WALKED OUT — black; a doorway of light opens; their silhouettes WALK into it (step bob, receding); letterbox
a, b = SB(4)
F.scene('s5', a, b, 'w-black', f'''
  <div class="cam" id="s5-cam">
    <div class="abs" id="s5-spill" style="left:0;right:0;top:1180px;height:740px;background:linear-gradient(180deg, rgba(255,236,206,.55), rgba(255,236,206,0) 80%);clip-path:polygon(40% 0, 60% 0, 100% 100%, 0 100%);opacity:0"></div>
    <div class="abs" id="s5-door" style="left:400px;top:560px;width:280px;height:620px;background:linear-gradient(180deg,#FFF8EC,#FFE3BC);box-shadow:0 0 140px 40px rgba(255,226,180,.5);clip-path:inset(0 100% 0 0)"></div>
    <div class="abs" id="s5-w1" style="left:150px;top:900px;width:430px"><img class="cut" id="s5-sil1" src="assets/img/sil_daniela.png" style="position:relative;width:430px" alt=""></div>
    <div class="abs" id="s5-w2" style="left:520px;top:880px;width:470px"><img class="cut" id="s5-sil2" src="assets/img/sil_dario_film.png" style="position:relative;width:470px" alt=""></div>
    <div class="abs center-x t-thin light" style="top:236px;font-size:54px">{W(34,'So ')}{W(35,'they')}</div>
    <div class="abs center-x light" style="top:300px"><span class="t-script" style="font-size:190px">{W(36,'walked ')}{W(37,'out.')}</span></div>
  </div>
  <div class="bar" id="s5-top" style="left:0;right:0;top:0;height:0"></div>
  <div class="bar" id="s5-bot" style="left:0;right:0;bottom:0;height:0"></div>''', f'''
K.fromTo('#s5-door', {{clipPath: 'inset(0 100% 0 0)'}}, {{clipPath: 'inset(0 0% 0 0)', duration: 0.4, ease: 'power2.inOut'}}, {t(34, -0.05)});
K.fromTo('#s5-spill', {{opacity: 0}}, {{opacity: 1, duration: 0.4}}, {t(34, 0.05)});
K.cam('#s5-w1', {a}, {b}, {{scale: 1.0, x: 0, y: 0}}, {{scale: 0.72, x: 90, y: -150}}, 'power1.in');
K.cam('#s5-w2', {a}, {b}, {{scale: 1.0, x: 0, y: 0}}, {{scale: 0.72, x: -90, y: -150}}, 'power1.in');
K.walk('#s5-sil1', {a + 0.1}, {b}, {{rate: 3.4, bob: 16}});
K.walk('#s5-sil2', {a + 0.25}, {b}, {{rate: 3.2, bob: 14}});
K.letterbox('#s5-top', '#s5-bot', {a + 0.05}, 210, 0.35);
K.words('#s5');
K.cam('#s5-cam', {a}, {b}, {{scale: 1.0}}, {{scale: 1.1}});
K.blurOut('#s5-cam', {b - 0.14}, 0.14, 16);
''')
F.sfx(t(34, -0.05), 'subboom_1.wav', -10); F.sfx(t(36), 'sweepdown_1.wav', -20)

# ================================================================================================================
# S6 A HANDFUL OF COLLEAGUES — ivory; five co-founders (MOVING footage) drop in one per beat with name tags; pan
a, b = SB(5)
crew = [  # name, video, left, mask bottom, width, z, drop delay
    ('JARED KAPLAN', 'jared_pp', -20, 1090, 430, 1, 0.00),
    ('SAM McCANDLISH', 'sam', 320, 1090, 440, 1, 0.20),
    ('TOM BROWN', 'tom', 660, 1090, 440, 1, 0.40),
    ('CHRIS OLAH', 'chris', 20, 1700, 520, 2, 0.62),
    ('JACK CLARK', 'jack', 520, 1700, 540, 2, 0.84, 56, 76),
]
t_drop = t(40, -0.05)
crew_html, crew_js = '', []
for k, (nm, vid, l, bt, w, z, dd, *fd) in enumerate(crew):
    f0, f1 = fd if fd else (66, 92)
    crew_html += (f'<div class="mask" style="left:0;right:0;top:420px;height:{bt-420}px;z-index:{z}">'
                  + vcut(f'assets/video/{vid}.webm', f's6-p{k}', f'left:{l}px;bottom:0;width:{w}px', f0, f1, start=a, dur=b - a) + '</div>'
                  f'<div class="abs t-mono s6-tag{k}" style="z-index:5;left:{l + w/2 - 125:.0f}px;width:250px;text-align:center;top:{bt - 64}px;'
                  f'background:{INK};color:{IV};padding:8px 0;font-size:19px;letter-spacing:.12em">{nm}</div>')
    crew_js.append(f"K.drop('#s6-p{k}', {t_drop + dd:.3f}, -1150, 0.5); K.in('#s6 .s6-tag{k}', {t_drop + dd + 0.3:.3f}, {{blur: 4, dur: 0.14}});")
    F.sfx(t_drop + dd + 0.22, 'pop.mp3', -12 - (k % 2) * 2)
F.scene('s6', a, b, 'w-ivory', f'''
  <div class="cam" id="s6-cam">
    <div class="grid"></div>
    <div class="abs" style="left:70px;top:200px"><span class="t-thin dark" style="font-size:56px">{W(38,'And ')}{W(39,'a ')}</span><span style="font-size:132px;line-height:1;{HEAVY_INK}">{W(40,'handful', mode='pop')}</span></div>
    <div class="abs t-thin dark" style="left:76px;top:350px;font-size:56px">{W(41,'of ')}{W(42,'colleagues')}</div>
    <div class="abs dark" style="left:560px;top:328px"><span class="t-ital" style="font-size:90px">{W(43,'followed ')}{W(44,'them.', cls='acc')}</span></div>
    {crew_html}
    <div class="abs t-mono dark" style="left:70px;top:1770px;opacity:.6;z-index:6">CO-FOUNDERS · ALL FORMERLY OPENAI · 2021</div>
  </div>''', '\n'.join(crew_js) + f'''
K.blurIn('#s6-cam', {a}, 0.2, 14);
K.words('#s6');
K.cam('#s6-cam', {a}, {b}, {{scale: 1.0, x: 70}}, {{scale: 1.05, x: -70}});
K.blurOut('#s6-cam', {b - 0.2}, 0.2, 18);
''')
F.sfx(a, 'whoosh.mp3', -14)

# ================================================================================================================
# S7 2021 · ANTHROPIC — ivory + leaf shadows; the year rolls 2020 -> 2021; the HQ RISES from the bottom (REF-D store
# rise); the real wordmark slams above the roof; spec label slides in
a, b = SB(6)
b = round(b + 0.42, 3)
F.scene('s7', a, b, 'w-ivory', f'''
  <div class="cam" id="s7-cam">
    <div class="grid"></div>
    <div class="abs" id="s7-hq" style="left:-60px;right:-60px;top:820px;height:1180px;overflow:hidden;box-shadow:0 -30px 60px rgba(0,0,0,.18)">
      <img id="s7-hqimg" src="assets/img/hq.jpg" style="width:100%;display:block;margin-top:-80px" alt="">
    </div>
    <div class="abs" id="s7-year" style="left:0;right:0;top:330px;text-align:center">
      <div class="t-thin dark" style="font-size:54px;margin-bottom:6px">{W(45,'In')}</div>
      {odo('2020', '2021', '', 330, style=HEAVY_INK)}
    </div>
    <div class="abs center-x t-thin dark" style="top:400px;font-size:58px">{W(47,'they ')}{W(48,'started')}</div>
    <img id="s7-logo" class="abs" src="assets/img/Anthropic_logo.svg" style="left:110px;top:560px;width:860px;opacity:0;filter:drop-shadow(0 12px 18px rgba(0,0,0,.25))" alt="">
    <div class="w" data-w="49" data-mode="cut" style="{CUT}"></div>
    <div class="label" id="s7-spec" style="left:70px;right:70px;top:1360px;height:200px;border:2px solid #1C1B1E;z-index:4">
      <div class="abs t-mono" style="left:24px;top:22px;font-size:21px;line-height:1.5">ANTHROPIC, PBC<br>EST. JANUARY 2021<br>SAN FRANCISCO, CA<br>AI SAFETY &amp; RESEARCH</div>
      <div class="abs" style="right:24px;top:30px">{barcode(5, 330, 96)}</div>
      <div class="abs t-mono" style="right:24px;top:140px;font-size:18px">NO. 0001 — PUBLIC BENEFIT CORP.</div>
    </div>
  </div>
  <img class="abs" id="s7-leaves" src="assets/img/leaves.png" style="left:-120px;top:-60px;width:1400px;height:2000px;mix-blend-mode:multiply;opacity:.45" alt="">''', f'''
K.blurIn('#s7-cam', {a}, 0.28, 18);
K.cam('#s7-leaves', {a}, {b}, {{x: -70, y: 0}}, {{x: 40, y: 30}});
K.words('#s7');
K.odo('#s7 .odo', {t(46, 0.05)}, 0.5);
K.out('#s7-year', {t(47, -0.18)}, {{dur: 0.18, y: -60}});
K.fromTo('#s7-hq', {{y: 1200}}, {{y: 0, duration: 0.75, ease: 'expo.out'}}, {t(47, -0.1)});
K.cam('#s7-hqimg', {t(47, -0.1)}, {b}, {{scale: 1.12}}, {{scale: 1.0}});
K.slam('#s7-logo', {t(49, -0.04)}, {{s0: 1.7, dur: 0.32}});
K.fromTo('#s7-logo', {{opacity: 0}}, {{opacity: 1, duration: 0.08, immediateRender: false}}, {t(49, -0.04)});
K.fromTo('#s7-spec', {{x: -1100}}, {{x: 0, duration: 0.42, ease: 'expo.out'}}, {t(49, 0.3)});
K.cam('#s7-cam', {a}, {b}, {{scale: 1.0, y: 0}}, {{scale: 1.05, y: -40}});
''')
F.sfx(a, 'whoosh.mp3', -14); F.sfx(t(46), 'swish_1.wav', -17); F.sfx(t(47, -0.1), 'subboom_1.wav', -11)
F.sfx(t(49, -0.04), 'impact-bass-1.mp3', -14); F.sfx(t(49, 0.3), 'swish_1.wav', -16)

# ================================================================================================================
# S8 SAFETY — colour flood to clay; a tilted word-search grid; on "Safety" a bar sweeps one row and finds S-A-F-E-T-Y,
# snap zoom onto it (REF-D word-search 5.0 s); ink blots bleed into the next scene
a, b = SB(7)
ws_html, wx0, wx1 = wordsearch('SAFETY', 6, cols=10, rows=12, cell=88, seed=9)
F.scene('s8', a, b, 'w-clay', f'''
  <div class="cam" id="s8-cam">
    <div class="abs" style="left:70px;top:210px"><span class="t-thin light" style="font-size:58px">{W(50,'A ')}{W(51,'company ')}{W(52,'with')}</span></div>
    <div class="abs" style="left:66px;top:285px;font-size:108px;line-height:1;{HEAVY_IV}">{W(53,'one ')}{W(54,'obsession.')}</div>
    <div class="abs" style="left:0;top:440px;width:1080px;height:1300px;perspective:1600px">
      <div class="abs" id="s8-plane" style="left:100px;top:120px;width:880px;transform-origin:50% 50%">
        <div class="abs" id="s8-bar" style="left:{wx0 - 10}px;top:{6*88 + 8}px;width:{wx1 - wx0 + 20}px;height:72px;background:{INK};border-radius:40px;transform-origin:0 50%;opacity:.92"></div>
        <div class="abs" style="left:0;top:0">{ws_html}</div>
      </div>
    </div>
  </div>
  <div class="w" data-w="55" data-mode="cut" style="{CUT}"></div>''', f'''
K.fromTo('#s8', {{clipPath: 'inset(100% 0 0 0)'}}, {{clipPath: 'inset(0% 0 0 0)', duration: 0.36, ease: 'power2.inOut'}}, {a});
K.words('#s8');
K.fromTo('#s8-plane', {{rotationX: 34, rotationZ: -11, y: 260, opacity: 0}}, {{rotationX: 20, rotationZ: -7, y: 0, opacity: 1, duration: 0.6, ease: 'expo.out'}}, {a + 0.1});
K.cam('#s8-plane', {a + 0.7}, {t(55, -0.05)}, {{rotationX: 20, rotationZ: -7}}, {{rotationX: 16, rotationZ: -4}}, 'none', false);
K.fromTo('#s8-bar', {{scaleX: 0}}, {{scaleX: 1, duration: 0.34, ease: 'power2.inOut'}}, {t(55, -0.05)});
K.fromTo('#s8 .wsh', {{scale: 1, color: 'rgba(255,250,240,.9)'}}, {{scale: 1.28, color: '{IV}', duration: 0.18, ease: 'back.out(3)', stagger: 0.04}}, {t(55, 0.05)});
K.snap('#s8-plane', {t(55, 0.2)}, 1, 1.22, {{y1: -60, dur: 0.3, blur: 6}});
K.cam('#s8-cam', {a}, {b}, {{x: 40, y: 0}}, {{x: -40, y: -50}});
K.blots('#blots circle', {b - 0.32}, 0.6);
''')
F.sfx(a, 'whoosh.mp3', -12); F.sfx(t(55, -0.05), 'swish_1.wav', -14); F.sfx(t(55, 0.1), 'impact_2.wav', -12)
F.sfx(b - 0.3, 'sweepdown_1.wav', -16)

# ================================================================================================================
# S9 CONSTITUTION (pun) — the 1787 parchment flies in tumbling and lands; caption in a redaction bar; the word stamps
# in blackletter with a clay underline drawing on; light-leak burn out
a, b = SB(8)
F.scene('s9', a, b, 'w-black', f'''
  <div class="cam" id="s9-cam">
    <img class="abs" id="s9-doc" src="assets/img/us_constitution.jpg" style="left:-140px;top:150px;width:1360px;box-shadow:0 40px 90px rgba(0,0,0,.6)" alt="">
    <div class="vignette"></div>
  </div>
  <div class="abs" id="s9-bar" style="left:70px;top:1120px;height:92px;width:940px;background:#0E0E10;transform-origin:0 50%"></div>
  <div class="abs t-thin light" style="left:100px;top:1138px;font-size:50px">{W(56,'They ')}{W(57,'even ')}{W(58,'gave ')}{W(59,'their ')}{W(60,'AI ')}{W(61,'a')}</div>
  <div class="abs center-x" style="top:1215px;color:#1A1714"><span class="t-black" style="font-size:196px;text-shadow:0 3px 0 rgba(255,250,235,.7)">{W(62,'constitution.', mode='pop')}</span></div>
  {svg(1080, 1920, pen_path('M150 1440 C 380 1428, 700 1430, 930 1418', ACC, 9, 's9-u'), style='left:0;top:0')}''', f'''
K.fly('#s9-doc', {a + 0.02}, {{y: 1500, rot: 28, s0: 1.4, dur: 0.6, r1: 3}});
K.cam('#s9-cam', {a}, {b}, {{scale: 1.0, x: 50, y: 0}}, {{scale: 1.1, x: -50, y: -60}});
K.fromTo('#s9-bar', {{scaleX: 0}}, {{scaleX: 1, duration: 0.3, ease: 'expo.out'}}, {t(56, -0.12)});
K.words('#s9');
K.draw('#s9 .s9-u', {t(62, 0.2)}, 0.36);
K.leak('#leak', {b - 0.35}, 0.5);
''')
F.sfx(a + 0.02, 'whoosh.mp3', -11); F.sfx(a + 0.55, 'subboom_1.wav', -16); F.sfx(t(62), 'impact_2.wav', -11)
F.sfx(b - 0.3, 'swish_1.wav', -17)

# ================================================================================================================
# S10 PRINCIPLES — Anthropic's real constitution page; highlighter on the term, a 0.35 s whip-pan down the page to
# "principles", then a slow zoom-out drift (REF-C 7.2-11 s)
CP = 'assets/img/page_constitution.json'; S10_, R10 = 0.95, 7
f_cai = box(CP, 'Constitutional AI', 3); f_pr = box(CP, 'principles')
sx2, sy2 = page_shift(S10_, R10, f_cai, f_pr)
a, b = SB(9)
F.scene('s10', a, b, '', f'''
  <div class="cam" id="s10-cam">
    {page_plane('s10', 'assets/img/page_constitution.jpg', CP, f_cai, S10_, R10, [('Constitutional AI', 3), ('principles', 0)], cy=820)}
  </div>
  <div class="label abs" id="s10-tag" style="left:70px;top:230px;padding:16px 22px;border:2px solid #1C1B1E"><span class="t-mono" style="font-size:22px">ANTHROPIC.COM · CLAUDE'S CONSTITUTION</span></div>
  <div class="abs" style="left:0;right:0;top:1330px;text-align:center">
    <span class="abs" id="s10-bar" style="left:120px;right:120px;top:0;height:96px;background:#0E0E10;transform-origin:0 50%;display:block"></span>
    <span class="t-thin light" style="position:relative;top:18px;font-size:50px">{W(63,'A ')}{W(64,'written ')}{W(65,'list ')}{W(66,'of ')}</span>
  </div>
  <div class="abs center-x" style="top:1440px;color:#F2EEE4"><span class="t-ital" style="font-size:96px;text-shadow:0 6px 30px rgba(0,0,0,.6)">{W(68,'it ')}{W(69,'has ')}{W(70,'to ')}{W(71,'follow.')}</span></div>
  <div class="w" data-w="67" data-mode="cut" style="{CUT}"></div>''', f'''
K.whipIn('#s10-cam', {a}, -900, 0.26);
K.cam('#s10 .pcam', {a}, {t(67, -0.36)}, {{scale: 1.2, x: 60, y: 0}}, {{scale: 1.1, x: -40, y: 0}}, 'power1.out');
K.hl('#s10 .s10-hl0', {a + 0.3}, 0.36);
K.in('#s10-tag', {a + 0.3}, {{blur: 6, y: -30, dur: 0.25, ease: 'expo.out'}});
K.cam('#s10 .pcam', {t(67, -0.36)}, {t(67, -0.02)}, {{scale: 1.1, x: -40, y: 0}}, {{scale: 1.12, x: {sx2 - 40:.0f}, y: {sy2 + 300:.0f}}}, 'power3.inOut', false);
K.hl('#s10 .s10-hl1', {t(67, 0.02)}, 0.34);
K.cam('#s10 .pcam', {t(67, -0.02)}, {b}, {{scale: 1.12, x: {sx2 - 40:.0f}, y: {sy2 + 300:.0f}}}, {{scale: 1.02, x: {sx2 - 140:.0f}, y: {sy2 + 280:.0f}}}, 'none', false);
K.fromTo('#s10-bar', {{scaleX: 0}}, {{scaleX: 1, duration: 0.3, ease: 'expo.out'}}, {t(63, -0.12)});
K.words('#s10');
K.fromTo('#slab1', {{xPercent: -110}}, {{xPercent: 110, duration: 0.22, ease: 'power2.inOut', immediateRender: false}}, {b - 0.24});
K.fromTo('#slab2', {{xPercent: -110}}, {{xPercent: 110, duration: 0.22, ease: 'power2.inOut', immediateRender: false}}, {b - 0.16});
''')
F.sfx(a, 'whoosh.mp3', -11); F.sfx(a + 0.3, 'swish_1.wav', -19); F.sfx(t(67, -0.36), 'whoosh.mp3', -13)
F.sfx(t(67, 0.02), 'swish_1.wav', -18); F.sfx(b - 0.24, 'whoosh.mp3', -12)

# ================================================================================================================
# S11 MARCH 2023 — black; streetwear label card; the PHONE (real launch post on screen) slides in on a tilted clay square,
# then a SNAP ZOOM into the screen lands on the highlighted date (REF-D laptop 22-25.7 s)
IP = 'assets/img/page_introducing.json'
ibs = json.load(open(ROOT / IP))['boxes']
ib_date = [x for x in ibs if x['text'] == 'Mar 14, 2023'][0]
ib_title = [x for x in ibs if x['text'] == 'Introducing Claude'][0]
isc = 0.5
PW, PH = 480, 980
pg_left = 34 - ib_date['x'] * isc
pg_top = 150 - ib_title['y'] * isc
scr = (f'<div class="abs" style="left:{pg_left:.0f}px;top:{pg_top:.0f}px;width:{2200*isc:.0f}px">'
       f'<img src="assets/img/page_introducing.jpg" style="width:100%;display:block" alt="">'
       f'<div class="hl s11-hl" style="left:{ib_date["x"]*isc-6:.0f}px;top:{ib_date["y"]*isc-3:.0f}px;width:{ib_date["w"]*isc+12:.0f}px;height:{ib_date["h"]*isc+6:.0f}px"></div></div>')
# where the date lands on screen (phone at 300,760 + 22 px bezel), then the translate that brings it to (540, 880)
dx_, dy_ = 300 + 22 + pg_left + (ib_date['x'] + ib_date['w'] / 2) * isc, 760 + 22 + pg_top + (ib_date['y'] + ib_date['h'] / 2) * isc
sx11, sy11 = 540 - (540 + (dx_ - 540) * 1.75), 880 - (1240 + (dy_ - 1240) * 1.75)
a, b = SB(10)
F.scene('s11', a, b, 'w-black', f'''
  <div class="cam" id="s11-cam">
    <div class="label" id="s11-top" style="left:90px;top:250px;width:900px;height:330px">
      <div class="abs" style="left:34px;top:26px;font:900 128px/1 'V3 Sans';letter-spacing:-.05em">CLAUDE</div>
      <div class="abs" style="left:560px;top:30px;font:italic 500 54px 'V3 Serif'">001</div>
      <img class="abs" src="assets/img/Claude_AI_symbol.svg" style="left:572px;top:104px;width:58px;height:58px" alt="">
      <div class="abs t-mono" style="left:38px;top:182px;font-size:21px;line-height:1.55">MODEL · CLAUDE + CLAUDE INSTANT<br>RELEASED · 03.14.2023<br>MAKER · ANTHROPIC, PBC</div>
      <div class="abs" style="right:30px;top:34px">{qr(9, 21, 6)}</div>
      <div class="abs hatch" style="right:30px;top:180px;width:126px;height:58px"></div>
      <div class="abs" style="right:30px;bottom:24px">{barcode(21, 230, 40)}</div>
    </div>
    <div class="abs center-x t-track light" style="top:650px;font-size:36px">{W(72,'In ')}{W(73,'March ')}{W(74,'2023')}</div>
    <div class="abs" id="s11-dev" style="left:0;top:0;width:1080px;height:1920px;transform-origin:540px 1240px">
      <div class="abs" id="s11-sq" style="left:200px;top:780px;width:700px;height:860px;background:{ACC};transform:rotate(-12deg);box-shadow:0 40px 80px rgba(0,0,0,.4)"></div>
      <div class="abs" id="s11-ph" style="left:300px;top:760px;width:{PW}px;height:{PH}px">
        {phone(0, 0, PW, PH, scr, 's11-phone')}
      </div>
    </div>
    <div class="abs center-x t-track light" style="top:712px;font-size:36px;z-index:5">{W(75,'they ')}{W(76,'released ')}{W(77,'it', cls='acc')}</div>
  </div>''', f'''
K.sliver('#s11-top', {a + 0.04}, 0.36);
K.words('#s11');
K.show('#s11-sq, #s11-ph', {t(73, -0.05)});
K.fromTo('#s11-sq', {{x: -1000, rotation: -40}}, {{x: 0, rotation: -12, duration: 0.5, ease: 'expo.out'}}, {t(73, -0.05)});
K.fromTo('#s11-ph', {{x: -1100, rotation: -32}}, {{x: 0, rotation: -5, duration: 0.55, ease: 'expo.out'}}, {t(73, 0.05)});
K.cam('#s11-ph', {t(73, 0.6)}, {b}, {{rotation: -5}}, {{rotation: -1}}, 'none', false);
K.snap('#s11-dev', {t(76, 0.05)}, 1, 1.75, {{x1: {sx11:.0f}, y1: {sy11:.0f}, dur: 0.32, blur: 9}});
K.hl('#s11 .s11-hl', {t(77, -0.06)}, 0.3);
K.cam('#s11-cam', {a}, {b}, {{x: 30, y: 0}}, {{x: -30, y: -30}});
K.bloom('#flash', {b - 0.25}, 0.18, 0.28);
''')
F.sfx(a + 0.04, 'swish_1.wav', -15); F.sfx(t(73, 0.05), 'whoosh.mp3', -10); F.sfx(t(76, 0.05), 'impact_2.wav', -12)
F.sfx(t(77, 0.22), 'swish_1.wav', -19)

# ================================================================================================================
# S12 CLAUDE — sky world (real clouds drifting); "Claude." opens from a sliver inside a gold selection box with handles
# (REF-D "RECIPROCITY" 15.3 s); the mark spins in above it
a, b = SB(11)
F.scene('s12', a, b, '', f'''
  <div class="cam" id="s12-cam">
    <img class="abs" id="s12-sky" src="assets/img/sky.jpg" style="left:-1400px;top:0;height:1920px" alt="">
    <div class="glow" style="left:-200px;top:-300px;width:1100px;height:1100px;opacity:.8"></div>
    <div class="abs center-x" style="top:470px"><span class="t-thin" style="font-size:60px;color:#fff;text-shadow:0 4px 18px rgba(0,40,90,.45)">{W(78,'And ')}{W(79,'they ')}{W(80,'called ')}{W(81,'it')}</span></div>
    <img id="s12-spark" class="abs" src="assets/img/Claude_AI_symbol.svg" style="left:440px;top:600px;width:200px;height:200px;filter:drop-shadow(0 16px 24px rgba(0,30,80,.35))" alt="">
    {selbox(150, 860, 780, 270, f'<div class="abs" id="s12-word" style="left:0;right:0;top:50px;text-align:center;font-size:160px;line-height:1;white-space:nowrap;{HEAVY_IV}">Claude.</div>', 's12-sel')}
  </div>
  <div class="w" data-w="82" data-mode="cut" style="{CUT}"></div>''', f'''
K.blurIn('#s12-cam', {a}, 0.2, 16);
K.cam('#s12-sky', {a}, {b}, {{x: 0, y: 0}}, {{x: 200, y: -30}});
K.words('#s12');
K.fly('#s12-spark', {t(80)}, {{y: -700, rot: 300, s0: 0.3, dur: 0.55, until: {b}, spin: 60}});
K.fromTo('#s12 .s12-sel', {{scaleX: 0.02, opacity: 0}}, {{scaleX: 1, opacity: 1, duration: 0.36, ease: 'expo.out'}}, {t(82, -0.08)});
K.fromTo('#s12-word', {{scaleX: 0.3, filter: 'blur(10px)'}}, {{scaleX: 1, filter: 'blur(0px)', duration: 0.4, ease: 'expo.out'}}, {t(82, -0.04)});
K.cam('#s12-cam', {a}, {b}, {{scale: 1.0}}, {{scale: 1.06}});
K.fromTo('#s12-cam', {{rotation: 0, filter: 'blur(0px)', opacity: 1}}, {{rotation: 22, filter: 'blur(18px)', opacity: 0, duration: 0.2, ease: 'power3.in', immediateRender: false}}, {b - 0.2});
''')
F.sfx(a, 'whoosh.mp3', -13); F.sfx(t(80, 0.1), 'swish_1.wav', -15); F.sfx(t(82), 'sparkle.mp3', -13)
F.sfx(b - 0.2, 'whoosh.mp3', -12)

# ================================================================================================================
# S13 SHANNON — name lock-up (portrait in a disc, his name BEHIND his jacket, sheen) then a taped frame where his photos
# wipe up faster and faster (REF-C lock-up, REF-B photo stack); camera never stops
a, b = SB(12)
stack_t = [t(90, -0.05), t(91, 0.05), t(93, -0.05), t(93, 0.3), t(94, -0.02)]
shots = ['shannon_1958_rect.jpg', 'shannon_theseus.jpg', 'shannon_1930_rect.jpg', 'shannon_mfo.jpg', 'shannon_tek_rect.jpg']
stack = ''.join(f'<div class="mask s13-ph{k}" style="left:0;top:0;width:800px;height:820px"><img src="assets/img/{f}" style="width:100%;height:100%;object-fit:cover;display:block" alt=""></div>' for k, f in enumerate(shots))
F.scene('s13', a, b, 'w-ivory', f'''
  <div class="cam" id="s13a">
    <div class="grid"></div>
    <div class="abs center-x t-thin dark" style="top:300px;font-size:54px">{W(83,'Many ')}{W(84,'believe ')}{W(85,"it's ")}{W(86,'named ')}{W(87,'after')}</div>
    <div class="abs" id="s13-disc" style="left:200px;top:470px;width:680px;height:680px;border-radius:50%;overflow:hidden;background:radial-gradient(circle at 40% 35%, #E4C3AE, {ACC})">
      <div class="abs s13-sheen" style="left:0;top:-30%;width:35%;height:160%;background:linear-gradient(90deg, rgba(255,255,255,0), rgba(255,255,255,.55), rgba(255,255,255,0));transform:rotate(20deg);z-index:3"></div>
    </div>
    <div class="abs center-x" style="top:1060px;z-index:2"><span style="font-size:190px;line-height:1;{HEAVY_INK}">{W(88,'Claude', mode='letters')}</span></div>
    <div class="abs center-x" style="top:1230px;z-index:4"><span style="font:italic 600 150px/1 'V3 Serif';letter-spacing:-.01em;color:#141414">{W(89,'Shannon', mode='letters')}</span></div>
    <div class="mask" style="left:200px;top:300px;width:680px;height:850px;z-index:3;-webkit-mask-image:radial-gradient(circle 340px at 340px 510px, #000 99%, transparent 100%), linear-gradient(#000,#000);-webkit-mask-size:100% 100%, 100% 52%;-webkit-mask-repeat:no-repeat;mask-image:radial-gradient(circle 340px at 340px 510px, #000 99%, transparent 100%), linear-gradient(#000,#000);mask-size:100% 100%, 100% 52%;mask-repeat:no-repeat">
      <img class="cut" id="s13-shan" src="assets/img/shannon_tek.png" style="left:70px;top:120px;width:560px" alt="">
    </div>
  </div>
  <div class="fill w-grey" id="s13b" style="opacity:0">
    <div class="abs" id="s13-frame" style="left:140px;top:430px;width:800px;height:820px;box-shadow:0 50px 90px rgba(0,0,0,.35);background:#333;overflow:hidden">{stack}</div>
    <div class="tape" style="left:90px;top:410px;transform:rotate(-38deg)"></div>
    <div class="tape" style="left:800px;top:410px;transform:rotate(38deg)"></div>
    <div class="abs t-thin light" style="left:190px;top:1000px;font-size:60px;z-index:3;text-shadow:0 3px 16px rgba(0,0,0,.6)">{W(90,'the ')}{W(91,'father ')}{W(92,'of')}</div>
    <div class="abs" style="left:170px;top:1075px;z-index:3;font-size:92px;line-height:1;white-space:nowrap;{HEAVY_IV}">{W(93,'information', mode='pop')}<br>{W(94,'theory.', mode='pop')}</div>
  </div>''', f'''
K.blurIn('#s13a', {a}, 0.22, 16);
K.words('#s13');
K.in('#s13-disc', {a + 0.12}, {{blur: 10, scale: 0.7, dur: 0.4, ease: 'expo.out'}});
K.rise('#s13-shan', {a + 0.25}, 520, 0.6);
K.sheen('#s13 .s13-sheen', {t(89, 0.3)}, 0.8);
K.cam('#s13a', {a + 0.25}, {t(90, -0.1)}, {{scale: 1.0, x: 30}}, {{scale: 1.08, x: -40}}, 'none', false);
K.fromTo('#s13b', {{opacity: 0}}, {{opacity: 1, duration: 0.16}}, {stack_t[0] - 0.1:.3f});
K.set('#s13a', {{opacity: 0}}, {stack_t[0] + 0.08:.3f});
K.cam('#s13b', {stack_t[0] - 0.1:.3f}, {b}, {{scale: 1.0, rotation: -1}}, {{scale: 1.08, rotation: 1}}, 'none', false);
''' + '\n'.join(f"K.fromTo('#s13 .s13-ph{k}', {{yPercent: 100}}, {{yPercent: 0, duration: {0.3 if k < 2 else 0.2}, ease: 'expo.out'}}, {ts:.3f});" for k, ts in enumerate(stack_t)) + f'''
K.blurOut('#s13b', {b - 0.17}, 0.17, 16);
''')
F.sfx(a, 'whoosh.mp3', -14); F.sfx(a + 0.25, 'subboom_1.wav', -16); F.sfx(t(89, 0.3), 'sparkle.mp3', -19)
for k, ts in enumerate(stack_t):
    F.sfx(ts, 'swish_1.wav', -15 - (k % 2))

# ================================================================================================================
# S14 $965 BILLION — slate + the HQ dimmed; condensed stacked type; a clay CHART LINE draws up through the real
# valuation history and out of the top with an arrow (REF-D 2000 %); the number rolls; banknotes spin in under BILLION
a, b = SB(13)
pts = [(140, 1150, '$61.5B', 'MAR 2025'), (420, 1110, '$183B', 'SEP 2025'), (700, 1046, '$380B', 'FEB 2026'), (920, 820, '$965B', 'MAY 2026')]
path_d = 'M 60 1170 ' + ' '.join(f'L {x} {y}' for x, y, *_ in pts) + ' L 1000 610'
dots = ''.join(f'<circle class="s14-dot" cx="{x}" cy="{y}" r="13" fill="{IV}" stroke="{ACC}" stroke-width="6" style="opacity:0"/>' for x, y, *_ in pts)
labs = ''.join(f'<div class="abs t-mono s14-lab" style="left:{x - 75}px;top:{y + 26}px;width:150px;text-align:center;color:{IV};font-size:18px;opacity:0">{v}<br><span style="opacity:.6">{d}</span></div>' for x, y, v, d in pts)
F.scene('s14', a, b, 'w-slate', f'''
  <div class="cam" id="s14-cam">
    <img class="abs" id="s14-hq" src="assets/img/hq.jpg" style="left:-380px;top:-20px;width:1900px;opacity:.38" alt="">
    <div class="fill" style="background:linear-gradient(180deg, rgba(20,20,19,.2), rgba(20,20,19,.75) 55%, rgba(20,20,19,.95))"></div>
    {svg(1080, 1920, f'<path class="pen s14-line" d="{path_d}" pathLength="1" stroke="{ACC}" stroke-width="14" style="stroke-dasharray:1;stroke-dashoffset:1;filter:drop-shadow(0 0 14px rgba(217,119,87,.7))"/>' + f'<path class="pen s14-arrow" d="M 962 640 L 1000 610 L 990 660" pathLength="1" stroke="{ACC}" stroke-width="14" style="stroke-dasharray:1;stroke-dashoffset:1"/>' + dots, style='left:0;top:0;z-index:2')}
    {labs}
  </div>
  <div class="abs t-thin light" style="left:80px;top:200px;font-size:58px">{W(95,'Today,')}</div>
  <div class="abs t-cond light" style="left:74px;top:270px;font-size:200px">{W(96,'ANTHROPIC', mode='slideL')}</div>
  <div class="abs t-cond light" style="left:78px;top:470px;font-size:108px;opacity:.92">{W(97,'IS ')}{W(98,'VALUED ')}{W(99,'AT')}</div>
  <div class="abs" style="left:60px;top:640px;z-index:5"><span class="w" data-w="100" data-mode="blur" style="font:400 340px/1 'V3 Cond';color:{IV};{ext(12, CLAYD)}">${odo('000', '965', '', 340, spins=[0, 1, 2], style="font-family:'V3 Cond'")}</span></div>
  <div class="abs" id="s14-bills" style="left:0;top:0;width:1080px;height:1920px;z-index:4">
    <div class="bill s14-b" style="left:160px;top:1060px;transform:rotate(-14deg)"></div>
    <div class="bill s14-b" style="left:330px;top:1010px;transform:rotate(9deg)"></div>
    <div class="bill s14-b" style="left:250px;top:1120px;transform:rotate(-3deg)"></div>
  </div>
  <div class="abs t-cond" style="left:70px;top:1000px;font-size:250px;z-index:6;color:{IV};{ext(12, CLAYD)}">{W(101,'BILLION', mode='pop')}</div>
  <div class="abs t-thin light" style="left:84px;top:1290px;font-size:58px;z-index:7;text-shadow:0 2px 14px rgba(0,0,0,.95),0 0 4px rgba(0,0,0,.9)">{W(102,'dollars.')}</div>
  <div class="abs" id="s14-rcpt" style="left:440px;top:1420px;width:580px;height:200px;z-index:6">
   <div class="abs" style="inset:0;background:#FBFAF7;overflow:hidden;transform:rotate(-4deg);box-shadow:0 30px 60px rgba(0,0,0,.5)">
    <img src="assets/img/page_valuation.jpg" style="position:absolute;left:{290 - 1159*0.42:.0f}px;top:{70 - 982*0.42:.0f}px;width:{2200*0.42:.0f}px" alt="">
    <div class="hl s14-hl" style="left:{290 - 1159*0.42 + 818*0.42 - 4:.0f}px;top:{70 - 2:.0f}px;width:{342*0.42 + 8:.0f}px;height:{94*0.42 + 4:.0f}px"></div>
    <div class="abs t-mono" style="left:0;right:0;bottom:0;padding:6px 12px;background:#1C1B1E;color:#F2EEE4;font-size:15px">BLOOMBERG LAW · MAY 28, 2026</div>
   </div>
  </div>
  <div class="fill" id="s14-glitch" style="opacity:0;z-index:20;background:repeating-linear-gradient(90deg, rgba(255,255,255,.95) 0 6px, transparent 6px 22px, rgba(255,255,255,.6) 22px 40px, transparent 40px 70px)"></div>''', f'''
K.blurIn('#s14-cam', {a}, 0.25, 20);
K.cam('#s14-hq', {a}, {b}, {{scale: 1.0, x: 0}}, {{scale: 1.14, x: -120}});
K.words('#s14');
K.draw('#s14 .s14-line', {t(97, -0.1)}, {t(100) - t(97, -0.1) + 0.35:.2f}, 'power1.in');
K.fromTo('#s14 .s14-dot', {{opacity: 0, scale: 0}}, {{opacity: 1, scale: 1, duration: 0.16, ease: 'back.out(3)', stagger: {(t(100) - t(97)) / 4:.2f}, transformOrigin: '50% 50%'}}, {t(97, 0.1)});
K.fromTo('#s14 .s14-lab', {{opacity: 0, y: 12}}, {{opacity: 1, y: 0, duration: 0.18, stagger: {(t(100) - t(97)) / 4:.2f}}}, {t(97, 0.15)});
K.draw('#s14 .s14-arrow', {t(100, 0.2)}, 0.18);
K.odo('#s14 .odo', {t(100, 0.02)}, 1.1, {{ease: 'power2.out'}});
K.fly('#s14 .s14-b', {t(101, -0.22)}, {{y: 1100, x: -200, rot: 420, s0: 0.6, dur: 0.5, stagger: 0.08}});
K.cam('#s14-bills', {t(101, 0.4)}, {b}, {{rotation: 0, y: 0}}, {{rotation: 3, y: -20}}, 'none', false);
K.in('#s14-rcpt', {t(102, 0.1)}, {{blur: 10, y: 120, dur: 0.35, ease: 'expo.out'}});
K.hl('#s14 .s14-hl', {t(102, 0.4)}, 0.3);
K.fromTo('#s14-glitch', {{opacity: 0, x: -60}}, {{opacity: 1, x: 40, duration: 0.06}}, {b - 0.16});
K.fromTo('#s14-glitch', {{opacity: 1}}, {{opacity: 0, duration: 0.1, immediateRender: false}}, {b - 0.08});
''')
F.sfx(a, 'whoosh.mp3', -12); F.sfx(t(96), 'impact_2.wav', -14); F.sfx(t(97, -0.1), 'riser_2.wav', -16)
F.sfx(t(100), 'subboom_1.wav', -11); F.sfx(t(101, -0.1), 'swish_1.wav', -14); F.sfx(t(101), 'impact-bass-1.mp3', -12)
F.sfx(t(102, 0.1), 'swish_1.wav', -17)

# ================================================================================================================
# S15 THESIS — black; a small window of the real co-founders' film; staircase caption with script words underlined;
# highlights bloom to white (REF-A ending)
a, b = SB(14)
F.scene('s15', a, b, 'w-black', f'''
  <div class="abs t-thin light" style="left:110px;top:930px;font-size:58px">{W(103,'Sometimes,')}</div>
  <div class="abs light" style="left:230px;top:1005px"><span class="t-script" style="font-size:150px">{W(104,'walking ')}{W(105,'away')}</span></div>
  {svg(1080, 1920, pen_path('M240 1200 C 420 1190, 640 1192, 800 1182', ACC, 5, 's15-u1') + pen_path('M560 1440 C 700 1432, 820 1434, 930 1426', ACC, 5, 's15-u2'), style='left:0;top:0')}
  <div class="abs t-thin light" style="left:430px;top:1215px;font-size:58px">{W(106,'is ')}{W(107,'the')}</div>
  <div class="abs light" style="left:560px;top:1260px"><span class="t-script" style="font-size:160px">{W(108,'start.')}</span></div>''', f'''
K.words('#s15');
K.draw('#s15 .s15-u1', {t(105, 0.15)}, 0.3);
K.draw('#s15 .s15-u2', {t(108, 0.12)}, 0.3);
K.bloom('#flash', {b - 0.3}, 0.26, 0.3);
''')
F.add_media(f'<video id="s15-clip" class="clip" src="assets/img/table_wide.mp4" muted playsinline data-start="{a}" data-duration="{round(b - a, 3)}" data-track-index="2" style="position:absolute;left:110px;top:380px;width:860px;height:484px;object-fit:cover;z-index:40;box-shadow:0 30px 70px rgba(0,0,0,.6)"></video>')
F.sfx(t(104), 'swish_1.wav', -20); F.sfx(b - 0.3, 'riser_1.wav', -15)

# ================================================================================================================
# S16 CTA — ivory; tracked FOLLOW; the mark spinning; dip to black
a, b = SB(15)
F.scene('s16', a, END, 'w-ivory', f'''
  <div class="cam" id="s16-cam">
    <div class="grid"></div>
    <img id="s16-spark" class="abs" src="assets/img/Claude_AI_symbol.svg" style="left:460px;top:500px;width:160px;height:160px" alt="">
    <div class="abs center-x t-track dark" style="top:740px;font-size:44px">{W(109,'Follow')}</div>
    <div class="abs center-x t-thin dark" style="top:820px;font-size:60px">{W(110,'for ')}{W(111,'the ')}{W(112,'next')}</div>
    <div class="abs center-x" style="top:880px"><span style="font-size:190px;line-height:1.1;color:{ACC};font-family:'V3 Heavy';text-transform:uppercase;{ext(10, CLAYD)}">{W(113,'story.', mode='pop')}</span></div>
    <div class="abs t-mono dark" style="left:70px;top:1500px;opacity:.55;font-size:18px;line-height:1.5">SOURCES: WIKIPEDIA · ANTHROPIC.COM · ARXIV · BLOOMBERG LAW<br>PHOTOS: TECHCRUNCH (CC BY 2.0) · WIKIMEDIA COMMONS · ANTHROPIC (YOUTUBE)</div>
  </div>
  <div class="fill" id="s16-dip" style="background:#000;opacity:0"></div>''', f'''
K.blurIn('#s16-cam', {a}, 0.3, 14);
K.words('#s16');
K.fly('#s16-spark', {a + 0.05}, {{y: -600, rot: 300, s0: 0.3, dur: 0.5, until: {END}, spin: 45}});
K.cam('#s16-cam', {a}, {END}, {{scale: 1.0, y: 0}}, {{scale: 1.06, y: -30}});
K.fromTo('#s16-dip', {{opacity: 0}}, {{opacity: 1, duration: 0.35}}, {END - 0.4});
''')
F.sfx(a + 0.05, 'whoosh.mp3', -14); F.sfx(t(113), 'impact_2.wav', -16)

# ================================================================================================================
F.overlay(f'''<div class="abs" style="inset:0;z-index:90;pointer-events:none" data-layout-ignore>
  <div class="leak" id="leak"></div>
  <div class="abs" id="slab1" style="left:-10%;top:-10%;width:120%;height:120%;background:{ACC}"></div>
  <div class="abs" id="slab2" style="left:-10%;top:-10%;width:120%;height:120%;background:{IV}"></div>
  {blots('blots', 9, 4, '#0B0B0C')}
  <div class="streak" id="streak"></div>
  <div class="flash" id="flash"></div>
  <div class="grain"></div>
</div>''', '''
K.set('#slab1, #slab2', {skewX: -14, xPercent: -110}, 0);
K.flash('#flash', '#streak', 0.1);
''')
F.add_media('<audio id="vo" class="clip" src="assets/audio/vo_norm.wav" data-start="0" data-duration="%s" data-track-index="10" data-volume="1"></audio>' % round(LINES[-1]['end'] + 0.3, 2))
F.add_media(f'<audio id="bed" class="clip" src="assets/audio/bed.wav" data-start="0" data-duration="{END}" data-track-index="11" data-volume="1"></audio>')
F.add_media(f'<audio id="sfx" class="clip" src="assets/audio/sfx.wav" data-start="0" data-duration="{END}" data-track-index="12" data-volume="1"></audio>')

print(F.build(duration=END), 'END', END, len(F.cues), 'cues')
