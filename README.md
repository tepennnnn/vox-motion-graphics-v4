# vox-motion-graphics-v4

## What it is

OpenCode plugin packaging the "motion graphics V3" editorial story pipeline (voice, alignment, kit, render) used for the Rolls-Royce / Somerton / Wright-flight shorts.

## Install

```
opencode plugin add 'vox-motion-graphics-v4@git+https://github.com/tepennnnn/vox-motion-graphics-v4.git#main'
```

## Upgrade

Bump `package.json` version → push → `opencode plugin update vox-motion-graphics-v4` (startup auto-checks too).

## Layout

`skills/motion-graphics-v3/` is the pipeline (SKILL.md, NOTES.md, reference/, kit/, tools/, example/); `index.js` registers it.

## Machine note

Python envs/fonts are found via `tools/env.sh` (self-resolving), not by path.
