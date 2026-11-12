#!/bin/bash
# New MG V3 film project.  usage: new_film.sh <dir> [9x16|16x9]
set -e
D="$1"; F="${2:-9x16}"; SK="${MGV3:-$HOME/.claude/skills/motion-graphics-v3}"
mkdir -p "$D"/{assets/v3,assets/fonts,assets/img,assets/video,assets/audio,assets/sfx,assets/vendor,work,renders}
cp "$SK/kit/kit.js" "$D/assets/v3/"; cp "$SK"/kit/fonts/*.woff2 "$D/assets/fonts/"; cp "$SK"/kit/img/* "$D/assets/img/"
cp "$SK"/kit/sfx/* "$D/assets/sfx/"; cp "$SK/kit/vendor/gsap.min.js" "$D/assets/vendor/"
V=$(npx --yes hyperframes --version 2>/dev/null | tail -1)
cat > "$D/package.json" <<J
{ "name": "$(basename "$D")", "private": true, "type": "module",
  "scripts": { "dev": "npx --yes hyperframes@$V preview", "check": "npx --yes hyperframes@$V check", "render": "npx --yes hyperframes@$V render" } }
J
echo '{ "paths": { "blocks": "compositions", "components": "compositions/components", "assets": "assets" }, "media": { "autoProxy": true } }' > "$D/hyperframes.json"
cat > "$D/work/script.json" <<'J'
{ "voice": "am_michael", "speed": 1.08, "gap": 0.18, "lead": 0.12,
  "lines": [ ["Shown line one.", "Spoken line one."] ] }
J
cp "$SK/example/sound.json" "$D/work/sound.json"
sed "s/F = Film(ROOT, title='How Claude Was Born')/F = Film(ROOT, title='$(basename "$D")'$( [ "$F" = 16x9 ] && echo ', w=1920, h=1080'))/" "$SK/example/build.py" > "$D/build.example.py"
echo "created $D ($F). Next: write work/script.json, then tools/vo.py + tools/align.py, then build.py (start from build.example.py)."
