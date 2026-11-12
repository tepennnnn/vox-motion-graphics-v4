"""Screenshot real pages for the edit (local Playwright/Chromium). Also records where each highlight word sits.
usage: python capture.py <out_dir> <name> <url> [--w 1280] [--h 1600] [--scroll SELECTOR_OR_TEXT] [--find "word|word"]
Writes <out_dir>/<name>.png (viewport at device scale 2) and <name>.json with the boxes (in png pixels) of every
--find text, so a highlighter can sweep exactly over the real words.
"""
import sys, json, argparse, time
from playwright.sync_api import sync_playwright

ap = argparse.ArgumentParser()
ap.add_argument('out'); ap.add_argument('name'); ap.add_argument('url')
ap.add_argument('--w', type=int, default=1280); ap.add_argument('--h', type=int, default=1600)
ap.add_argument('--scroll', default=''); ap.add_argument('--find', default='')
ap.add_argument('--settle', type=float, default=3.5)
a = ap.parse_args()

JS = """(needles) => {
  const out = [];
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let n;
  while ((n = walker.nextNode())) {
    for (const nd of needles) {
      let i = n.textContent.indexOf(nd);
      while (i >= 0) {
        const r = document.createRange(); r.setStart(n, i); r.setEnd(n, i + nd.length);
        for (const b of r.getClientRects()) if (b.width > 2 && b.top > -5 && b.top < innerHeight)
          out.push({text: nd, x: b.left, y: b.top, w: b.width, h: b.height});
        i = n.textContent.indexOf(nd, i + nd.length);
      }
    }
  }
  return out;
}"""

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': a.w, 'height': a.h}, device_scale_factor=2,
                    user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36')
    pg.goto(a.url, wait_until='domcontentloaded', timeout=60000)
    time.sleep(a.settle)
    # kill cookie banners / sticky headers that would cover the text
    pg.add_style_tag(content='[class*=cookie],[id*=cookie],[class*=Cookie],[id*=onetrust],[class*=consent],[id*=consent]{display:none!important}')
    if a.scroll:
        try:
            pg.get_by_text(a.scroll, exact=False).first.scroll_into_view_if_needed(timeout=5000)
            pg.evaluate('window.scrollBy(0, -innerHeight * 0.3)')
        except Exception as e:
            print('scroll miss', e)
    time.sleep(0.8)
    pg.screenshot(path=f'{a.out}/{a.name}.png')
    boxes = pg.evaluate(JS, [s for s in a.find.split('|') if s]) if a.find else []
    for bx in boxes:
        for k in ('x', 'y', 'w', 'h'): bx[k] = round(bx[k] * 2, 1)
    json.dump({'url': a.url, 'w': a.w * 2, 'h': a.h * 2, 'boxes': boxes}, open(f'{a.out}/{a.name}.json', 'w'), indent=1)
    print(a.name, len(boxes), 'boxes', pg.title()[:80])
    b.close()
