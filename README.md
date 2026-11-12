# vox-motion-graphics-v4

## What it is

OpenCode plugin packaging the "motion graphics V3" editorial story pipeline (voice, alignment, kit, render) used for the Rolls-Royce / Somerton / Wright-flight shorts.

## Install

```
opencode plugin add 'vox-motion-graphics-v4@git+https://github.com/tepennnnn/vox-motion-graphics-v4.git#main'
```

## Upgrade

On OpenCode 1.19.5 (verified live):

1. Bump `package.json` version, commit, push (tag optional).
2. Delete the installed package dir: `rm -rf ~/.cache/opencode/packages/vox-motion-graphics-v4@git+https:`
3. Reinstall: `opencode plugin 'vox-motion-graphics-v4@git+https://github.com/tepennnnn/vox-motion-graphics-v4.git#main' --global`
4. Verify: package-lock.json `resolved` now points at the new commit, and the installed package.json shows the new version.

Newer OpenCode versions auto-check unpinned git plugins at startup and support `opencode plugin update`. Caveat: `--force` alone does not refresh content — npm's lockfile pins the resolved commit.

## Layout

`skills/motion-graphics-v3/` is the pipeline (SKILL.md, NOTES.md, reference/, kit/, tools/, example/); `index.js` registers it.

## Machine note

Python envs/fonts are found via `tools/env.sh` (self-resolving), not by path.
