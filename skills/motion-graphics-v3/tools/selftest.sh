#!/bin/bash
# Proves the install works: a 4-second MG V3 film made end to end on this computer (Kokoro voice → word timings →
# a paper world with words landing on the voice → soft effects → render → mux).  ~/motion-graphics-v3/_selftest  (~2 min)
set -e
export MGV3="${MGV3:-$(cd "$(dirname "$0")/.." && pwd)}"
source "$MGV3/tools/env.sh" >/dev/null
D="$HOME/motion-graphics-v3/_selftest"; [ -d "$D" ] && rm -rf "${D:?}"
bash "$MGV3/tools/new_film.sh" "$D" 9x16 >/dev/null
cat > "$D/work/script.json" <<'J'
{ "voice": "am_michael", "speed": 1.08, "gap": 0.18, "lead": 0.12,
  "lines": [ ["Every word lands on the voice.", "Every word lands on the voice."] ] }
J
"$MGV3_TTS" "$MGV3/tools/vo.py" "$D"
"$MGV3_ALIGN" "$MGV3/tools/align.py" "$D"
cat > "$D/build.py" <<'P'
import sys, json, os
from pathlib import Path
sys.path.insert(0, str(Path(os.environ['MGV3']) / 'kit'))
from v3lib import Film, W, ext
ROOT = Path(__file__).resolve().parent
F = Film(ROOT, title='selftest')
END = round(json.load(open(ROOT / 'work/vo_lines.json'))[-1]['end'] + 0.9, 2)
F.scene('s1', 0, END, 'w-ivory', f'''<div class="cam" id="s1-cam">
  <div class="abs center-x" style="top:640px;font:800 104px 'V3 Serif';line-height:1.05;text-align:center;width:960px;color:#141413">{W(0,'Every ')}{W(1,'word ')}{W(2,'lands', mode='pop')}<br>{W(3,'on ')}{W(4,'the ')}{W(5,'voice.', mode='rise')}</div>
</div>''', js="K.words('#s1');")
print(F.build(duration=END))
P
(cd "$D" && python3 build.py)
END=$(python3 -c "import json;print(round(json.load(open('$D/work/vo_lines.json'))[-1]['end']+0.9,2))")
echo "{\"duration\": $END, \"bed\": {\"src\": \"assets/audio/music.mp3\"}, \"sfx_dir\": \"$D/assets/sfx\", \"cues\": []}" > "$D/work/sound.json"
"$MGV3_TTS" "$MGV3/tools/mix.py" "$D"
cd "$D" && npx --yes hyperframes check >/dev/null && npx --yes hyperframes render . -o renders/silent.mp4 >/dev/null
ffmpeg -loglevel error -y -i renders/silent.mp4 -i assets/audio/vo.wav -i assets/audio/sfx.wav -filter_complex "[1][2]amix=inputs=2:normalize=0,loudnorm=I=-15:TP=-1.2[a]" -map 0:v -map "[a]" -c:v copy -c:a aac -shortest renders/selftest.mp4
ffmpeg -loglevel error -y -i renders/selftest.mp4 -vf "fps=2,scale=216:-1,tile=8x1" -frames:v 1 work/selftest_sheet.jpg
echo "SELFTEST PASSED: $D/renders/selftest.mp4 · sheet $D/work/selftest_sheet.jpg"
