# vox motion graphic v4 — plugin design (short)

Date: 2026-11-12 · Status: awaiting approval

## Intent

Package the motion-graphics-v3 pipeline (the one that made the Rolls-Royce,
Somerton and Wright-flight videos) as an **upgradable OpenCode plugin** named
"vox motion graphic v4", hosted on GitHub and installed with
`opencode plugin add`. Upgrades ship as normal git pushes and land with
`opencode plugin update` (OpenCode also auto-checks unpinned git plugins at
startup). The user picked this (A) over a local-only repo (B) and an npm
package (C — needs an npm account and is awkward for the 2.9 MB of fonts/SFX).

## Where the pipeline is today

- `~/.config/opencode/skills/motion-graphics-v3/` — the pipeline (SKILL.md,
  NOTES.md, reference/, kit/ 2.3 MB, tools/, example/), not under git.
- `~/.claude/skills/motion-graphics-v3` — a symlink to the above.
- `~/.claude/skills/arcade-motiongraphics/` — separate skill, NOT in scope.
- Video projects live in `~/motion-graphics-v3/` (rolls_royce, somerton,
  wright-flight, _selftest) — untouched by this change.

## Repo layout (built locally at `~/vox-motion-graphics-v4/`)

```
vox-motion-graphics-v4/
  package.json        name "vox-motion-graphics-v4", version 0.1.0, type module,
                      main index.js
  index.js            default export { id, setup } — setup() registers the skill
                      via ctx.skill.transform (same contract superpowers uses on
                      OpenCode 1.19.5)
  skills/
    motion-graphics-v3/   the full pipeline, verbatim content:
                          SKILL.md NOTES.md reference/ kit/ tools/ example/
  DESIGN.md (this file) · .gitignore · README.md (install + upgrade one-pager)
```

Naming call: package/repo id is lowercase `vox-motion-graphics-v4` (npm-safe).
The skill inside stays `motion-graphics-v3` — all of its internal language,
docs and tool names are V3; the plugin name is only the delivery wrapper.
(Correct me if you want the skill renamed v4 too.)

## The one code change: self-resolving paths

The pipeline hardcodes `~/.claude/skills/motion-graphics-v3`, which breaks
inside the plugin cache. Fix is minimal and makes the skill location-agnostic:

- `tools/env.sh`: derive `MGV3` from the script's own location (BASH_SOURCE)
  instead of a hardcoded path; still respect a pre-set `$MGV3`.
- `tools/new_film.sh`: `SK="${MGV3:-<derived>}"`
- `SKILL.md`: instructions say `SK=<this skill's directory>` / "source
  tools/env.sh, then use $MGV3".
- `example/build.py`: keeps the `$MGV3` env override (already does).

Everything downstream already keys off `$MGV3`/`$SK`, so video projects and
the workflow are unchanged.

## Install + cutover

1. Add `"vox-motion-graphics-v4"` to the `plugin` array in
   `~/.config/opencode/opencode.jsonc` (alongside superpowers).
2. `opencode plugin add github:YOU/vox-motion-graphics-v4#main`
   (needs a GitHub username + HTTPS personal-access-token to push).
3. Retire the loose copies so there is one source of truth:
   delete `~/.config/opencode/skills/motion-graphics-v3/` and re-point the
   `~/.claude/skills/motion-graphics-v3` symlink into the installed plugin's
   skill dir — old scripts and notes keep working.
4. Verify: `opencode plugin list` shows it; a fresh session's skill tool lists
   motion-graphics-v3; `tools/new_film.sh` + a tiny HyperFrames check render
   run from the plugin cache location.

## Upgrade flow (after it ships)

Edit in the repo → bump `package.json` version → commit/push →
`opencode plugin update vox-motion-graphics-v4`. Pinned commit installs stay
frozen; `#main` installs stay upgradable.

## Goals / non-goals

- Goals: one command to install, one command to upgrade; identical V3 skill
  behavior; existing projects unaffected.
- Non-goals: no style/content changes to V3; not packaging arcade-motiongraphics;
  not publishing to npm; no CI.
- Anti-goal: two live copies of the pipeline (that is how upgrades silently
  break).

## Open item (yours)

GitHub username, and an HTTPS PAT (repo + content scopes) to create/push the
remote — or a repo you create yourself and hand me as a URL.
