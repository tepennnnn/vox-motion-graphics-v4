# vox motion graphic v4 (OpenCode plugin) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Package the motion-graphics-v3 pipeline as the upgradable OpenCode plugin `vox-motion-graphics-v4`, hosted on GitHub, installed via `opencode plugin add`, with the loose local copies retired.

**Architecture:** A minimal OpenCode plugin package (`package.json` + `index.js`) that registers the existing pipeline unchanged as a skill. The pipeline moves verbatim into `skills/motion-graphics-v3/`; its five hardcoded-path references are made self-resolving so the skill works from any install location. `index.js` mirrors the proven superpowers dual contract (V1 named export + config hook; V2 `{id, setup}` + `ctx.skill.transform`).

**Tech Stack:** Node ≥ 18 (ESM, no dependencies), git/GitHub (HTTPS + PAT), OpenCode 1.19.5 on this machine.

**Spec:** `docs/superpowers/specs/2026-11-12-vox-motion-graphics-v4-design.md`

## Global Constraints

- OpenCode on this machine is **1.19.5** (a "V1" host); the plugin must also work on V2 hosts — dual export, same as superpowers.
- Pipeline content is copied **byte-identical** except the five portability edits listed in Task 2. No style/content changes.
- Plugin id/package name: `vox-motion-graphics-v4` (lowercase, npm-safe). Skill id stays `motion-graphics-v3`.
- Install spec pinned to a **branch** (`#main`), never a commit hash, so `opencode plugin update` can upgrade it.
- PATs/secrets are never written to disk, to config, or committed; pushes are done by the user or via a transient credential helper.
- `opencode plugin list` does not exist on 1.19.5 (it mis-parses as a package name) — verify plugins via the cache dir and config files instead.
- Repo: `~/vox-motion-graphics-v4`, branch `main`, remote `https://github.com/tepennnnn/vox-motion-graphics-v4.git`.

## Review Focus

1. **Symlinked invocation** (`~/.claude/skills/motion-graphics-v3/...`) must resolve `MGV3` to the *real* directory, not the symlink path. Test: Task 2 Step 3 (temp symlink, expect `pwd -P`-resolved output).
2. **V1 host calling `default.setup`** with a V1-shaped ctx must return quietly, never throw. Test: Task 2 Step 8 (`node -e`, expect no output/throw).
3. **Local-scope config hiding**: `opencode plugin add` writes `~/.opencode/opencode.json` (local scope) — the plugin would not load in projects started elsewhere. Task 4 migrates the entry into the global `~/.config/opencode/opencode.jsonc` and asserts no local-scope entry remains.
4. **Two live copies** after a failed cutover silently serve stale code. Task 5 asserts the old `~/.config/opencode/skills/motion-graphics-v3` is gone and the `~/.claude` symlink resolves into the plugin cache.
5. **Upgrade silently broken** (pinned commit, wrong spec, or version not bumped). Task 6 drills the full bump → push → `opencode plugin update` → verify-version loop.

---

### Task 1: Repo skeleton + pipeline import

**Files:**
- Create: `package.json`, `index.js`, `.gitignore`, `README.md`
- Create (copy): `skills/motion-graphics-v3/**` from `~/.config/opencode/skills/motion-graphics-v3/`

**Interfaces:**
- Consumes: pipeline source dir `~/.config/opencode/skills/motion-graphics-v3/` (read-only).
- Produces: `skills/motion-graphics-v3/` (byte-identical copy) and `index.js` exporting `VoxMotionGraphicsV4Plugin` (named) and `default: {id, server, setup}` — later tasks import/verify these.

- [ ] **Step 1: Init the repo**

```bash
cd ~/vox-motion-graphics-v4 && git init -b main
```

- [ ] **Step 2: Write `package.json`, `.gitignore`, `README.md`** (exact contents below)

```json
{
  "name": "vox-motion-graphics-v4",
  "version": "0.1.0",
  "description": "Vox motion graphic v4 - the MG V3 editorial story motion-graphics pipeline (Kokoro voice, wav2vec2 alignment, HyperFrames render) as an upgradable OpenCode plugin",
  "type": "module",
  "main": "index.js",
  "files": ["index.js", "skills", "README.md", "docs"],
  "keywords": ["opencode", "opencode-plugin", "skills", "motion-graphics", "video"]
}
```

`.gitignore`:
```
node_modules/
.DS_Store
```

`README.md` — five short sections, no fluff:
1. What it is: OpenCode plugin packaging the "motion graphics V3" editorial story pipeline (voice, alignment, kit, render) used for the Rolls-Royce / Somerton / Wright-flight shorts.
2. Install: `opencode plugin add 'vox-motion-graphics-v4@git+https://github.com/tepennnnn/vox-motion-graphics-v4.git#main'`
3. Upgrade: bump `package.json` version → push → `opencode plugin update vox-motion-graphics-v4` (startup auto-checks too).
4. Layout: `skills/motion-graphics-v3/` is the pipeline (SKILL.md, NOTES.md, reference/, kit/, tools/, example/); `index.js` registers it.
5. Machine note: Python envs/fonts are found via `tools/env.sh` (self-resolving), not by path.

- [ ] **Step 3: Copy the pipeline verbatim**

```bash
mkdir -p ~/vox-motion-graphics-v4/skills
cp -a ~/.config/opencode/skills/motion-graphics-v3 ~/vox-motion-graphics-v4/skills/
diff -r ~/.config/opencode/skills/motion-graphics-v3 ~/vox-motion-graphics-v4/skills/motion-graphics-v3
```
Expected: `diff` prints nothing (byte-identical).

- [ ] **Step 4: Write `index.js`** (full content below — V1 + V2 dual contract)

```js
// vox motion graphic v4 — packages the motion-graphics-v3 pipeline as an OpenCode plugin.
// Contract mirrors the proven superpowers plugin: V1 hosts scan named exports and read the
// config hook; V2 hosts call default.setup() which registers skills via ctx.skill.transform.
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const skillsDir = path.resolve(__dirname, 'skills')

// Minimal frontmatter reader for our own SKILL.md files: top-level `key: value`
// plus folded (`>-`) or literal (`|`) indented blocks. Not a YAML parser.
function readFrontmatter(raw) {
  const m = raw.match(/^---\n([\s\S]*?)\n---\n?/)
  if (!m) return { frontmatter: {}, content: raw }
  const meta = {}
  const lines = m[1].split('\n')
  for (let i = 0; i < lines.length; i++) {
    const kv = lines[i].match(/^(\w[\w-]*):\s*(.*)$/)
    if (!kv) continue
    let [, key, val] = kv
    if (val === '>-' || val === '>' || val === '|') {
      const block = []
      while (i + 1 < lines.length && /^(\s{2,}|\t)/.test(lines[i + 1])) block.push(lines[++i].trim())
      val = block.join(' ')
    }
    meta[key] = val.replace(/^["']|["']$/g, '')
  }
  return { frontmatter: meta, content: raw.slice(m[0].length) }
}

function collectSkills() {
  const out = []
  if (!fs.existsSync(skillsDir)) return out
  for (const entry of fs.readdirSync(skillsDir, { withFileTypes: true })) {
    if (!entry.isDirectory() || entry.name.startsWith('.')) continue
    const file = path.join(skillsDir, entry.name, 'SKILL.md')
    if (!fs.existsSync(file)) continue
    const { frontmatter, content } = readFrontmatter(fs.readFileSync(file, 'utf8'))
    out.push({
      id: entry.name,
      name: frontmatter.name || entry.name,
      ...(frontmatter.description ? { description: frontmatter.description } : {}),
      path: file,
      content,
    })
  }
  return out
}

// V1 plugin (OpenCode 1.x): named export + default.server. The config hook adds our
// skills directory so OpenCode scans it for <name>/SKILL.md natively.
export const VoxMotionGraphicsV4Plugin = async () => ({
  config: async (config) => {
    if (Array.isArray(config.skills)) return // V2 host: setup() registers skills instead
    config.skills = config.skills || {}
    config.skills.paths = config.skills.paths || []
    if (!config.skills.paths.includes(skillsDir)) config.skills.paths.push(skillsDir)
  },
})

// V2 setup (OpenCode 2.x): register each skill with ctx.skill.transform; guard against
// V1-shaped ctx, and never let one failure disable the plugin.
async function setup(ctx) {
  if (!ctx || !ctx.skill || typeof ctx.skill.transform !== 'function') return
  try {
    const skills = collectSkills()
    await ctx.skill.transform((draft) => {
      for (const skill of skills) {
        try { draft.add(skill) } catch (err) {
          console.error(`[vox-motion-graphics-v4] skill "${skill.id}" rejected by host, skipping:`, err)
        }
      }
    })
  } catch (err) {
    console.error('[vox-motion-graphics-v4] skill registration failed:', err)
  }
}

export default {
  id: 'vox-motion-graphics-v4',
  server: VoxMotionGraphicsV4Plugin,
  setup,
}
```

- [ ] **Step 5: Smoke-test the module exports**

```bash
node -e "import('file:///data/data/com.termux/files/home/vox-motion-graphics-v4/index.js').then(m => console.log(typeof m.VoxMotionGraphicsV4Plugin, m.default.id))"
```
Expected: `function vox-motion-graphics-v4`

- [ ] **Step 6: Commit**

```bash
cd ~/vox-motion-graphics-v4 && git add -A && git commit -m "feat: package MG V3 pipeline as vox-motion-graphics-v4 OpenCode plugin"
```

---

### Task 2: Self-resolving paths (the five portability edits)

**Files:**
- Modify: `skills/motion-graphics-v3/tools/env.sh:1-2`
- Modify: `skills/motion-graphics-v3/tools/new_film.sh:4`
- Modify: `skills/motion-graphics-v3/SKILL.md:77-78`
- Modify: `skills/motion-graphics-v3/example/build.py:11`
- Modify: `skills/motion-graphics-v3/NOTES.md:6-7`

**Interfaces:**
- Consumes: the repo copy from Task 1.
- Produces: `MGV3` env var = the real (physical) skill directory wherever the skill lives; `SK` in `new_film.sh` self-derives the same way. Downstream tools/tests all key off `$MGV3`/`$SK` (unchanged names).

- [ ] **Step 1: Rewrite `env.sh` lines 1–2** — replace

```bash
# MG V3 environment: source this first.  `source ~/.claude/skills/motion-graphics-v3/tools/env.sh`
export MGV3="${MGV3:-$HOME/.claude/skills/motion-graphics-v3}"
```
with
```bash
# MG V3 environment: source this first, e.g.  source "$MGV3/tools/env.sh"
# (resolves its own location; works from a checkout, the plugin cache, or the ~/.claude symlink)
_MGV3_SELF="${BASH_SOURCE[0]:-$0}"
_MGV3_DIR="$(cd -- "$(dirname -- "$_MGV3_SELF")/.." && pwd -P)"
export MGV3="${MGV3:-$_MGV3_DIR}"
unset _MGV3_SELF _MGV3_DIR
```
Everything below (the `pick()` function, `MGV3_TTS/ALIGN/IMG/AUDIO` exports, final echo) stays byte-identical.

- [ ] **Step 2: `new_film.sh:4`** — replace
`D="$1"; F="${2:-9x16}"; SK="${MGV3:-$HOME/.claude/skills/motion-graphics-v3}"`
with
`D="$1"; F="${2:-9x16}"; SK="${MGV3:-$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)}"`

- [ ] **Step 3: SKILL.md:77–78** — replace
```
Every step: `source ~/.claude/skills/motion-graphics-v3/tools/env.sh` (picks the local Python envs; on a fresh machine run
`tools/setup.sh` once). `SK=~/.claude/skills/motion-graphics-v3`.
```
with
```
Every step: `source "<this skill's directory>/tools/env.sh"` (picks the local Python envs; on a fresh machine run
`tools/setup.sh` once). env.sh resolves its own location and sets `MGV3`; use `SK="$MGV3"`.
```

- [ ] **Step 4: example/build.py:11** — replace
`sys.path.insert(0, str(Path(os.environ.get('MGV3', Path.home() / '.claude/skills/motion-graphics-v3')) / 'kit'))`
with
`sys.path.insert(0, str(Path(os.environ.get('MGV3', Path(__file__).resolve().parents[1])) / 'kit'))`

- [ ] **Step 5: NOTES.md:6–7** — replace the two install-location lines with
```
The skill ships as the OpenCode plugin `vox-motion-graphics-v4` (after `opencode plugin add` it lives under
`~/.cache/opencode/packages/`; `~/.claude/skills/motion-graphics-v3` is a symlink into it; `tools/env.sh` resolves
its own location, so everything works from anywhere). Machine specifics a build must respect:
```

- [ ] **Step 6: Test — derivation from the repo copy**

```bash
bash ~/vox-motion-graphics-v4/skills/motion-graphics-v3/tools/env.sh | head -1
```
Expected: `MGV3=/data/data/com.termux/files/home/vox-motion-graphics-v4/skills/motion-graphics-v3`

- [ ] **Step 7: Test — derivation through a symlink (Review Focus 1)**

```bash
ln -sfn ~/vox-motion-graphics-v4/skills/motion-graphics-v3 /tmp/mgv3-link
env -u MGV3 bash -c 'source /tmp/mgv3-link/tools/env.sh; echo "$MGV3"'; rm /tmp/mgv3-link
```
Expected: the real repo path printed (`pwd -P` resolves through the symlink), not `/tmp/mgv3-link`.

- [ ] **Step 8: Test — V1-shaped ctx must no-op (Review Focus 2)**

```bash
node -e "import('file:///data/data/com.termux/files/home/vox-motion-graphics-v4/index.js').then(m => m.default.setup({})).then(() => console.log('setup ok'))"
```
Expected: `setup ok`, no throw.

- [ ] **Step 9: Test — `new_film.sh` scaffolds without `MGV3` preset**

```bash
env -u MGV3 bash ~/vox-motion-graphics-v4/skills/motion-graphics-v3/tools/new_film.sh /tmp/mgv4-demo 9x16 && ls /tmp/mgv4-demo && rm -rf /tmp/mgv4-demo
```
Expected: `created /tmp/mgv4-demo (9x16)` and the scaffold dirs exist (assets/v3, assets/fonts, work, renders).

- [ ] **Step 10: Commit**

```bash
cd ~/vox-motion-graphics-v4 && git add -A && git commit -m "fix: derive skill paths from script location; drop hardcoded ~/.claude paths"
```

---

### Task 3: Local registration smoke test (before pushing)

**Files:**
- Modify (temporarily): `~/.config/opencode/opencode.jsonc`; restore from backup afterwards.

**Interfaces:**
- Consumes: repo from Task 2 (its `index.js` + skills dir).
- Produces: confidence that OpenCode 1.19.5 registers the skill from a directory entry; no lasting config change.

- [ ] **Step 1: Back up the config**

```bash
cp ~/.config/opencode/opencode.jsonc /tmp/opencode.jsonc.bak
```

- [ ] **Step 2: Add a temporary local-path plugin entry** — in `~/.config/opencode/opencode.jsonc`, append `"/data/data/com.termux/files/home/vox-motion-graphics-v4"` to the existing `"plugin"` array (the entry stays a directory path with `index.js`, which both V1 and V2 accept).

- [ ] **Step 3: Verify registration with a non-interactive run**

```bash
opencode run 'Use the skill tool and tell me: is a skill with id motion-graphics-v3 available? Answer yes or no and its id.'
```
Expected: answer contains `motion-graphics-v3`. If the skill is missing, check `opencode run --print-logs` output for plugin load errors and fix `index.js` before proceeding.

- [ ] **Step 4: Revert the config**

```bash
cp /tmp/opencode.jsonc.bak ~/.config/opencode/opencode.jsonc && rm /tmp/opencode.jsonc.bak
```
Expected: `diff` with the pre-test file is empty.

---

### Task 4: GitHub push + real install

**Files:**
- Modify: `~/.config/opencode/opencode.jsonc` (final `plugin` entry), `~/.opencode/opencode.json` (deleted).

**Interfaces:**
- Consumes: repo from Task 2, GitHub account `tepennnnn`.
- Produces: installed package at `~/.cache/opencode/packages/vox-motion-graphics-v4@git+https:/github.com/tepennnnn/vox-motion-graphics-v4.git/node_modules/vox-motion-graphics-v4` (verify exact dir name with `ls`), tag `v0.1.0`.

- [ ] **Step 1: Confirm the GitHub repo exists (user creates it if not — empty repo, no README/license)**

```bash
git ls-remote https://github.com/tepennnnn/vox-motion-graphics-v4.git HEAD
```
Expected: no `Repository not found` error (empty output is fine). If missing: stop and ask the user to create it, then re-run.

- [ ] **Step 2: Add the remote**

```bash
cd ~/vox-motion-graphics-v4 && git remote add origin https://github.com/tepennnnn/vox-motion-graphics-v4.git
```

- [ ] **Step 3: Push — by the user, so the PAT never touches chat or disk.** Give them this command to run in their own terminal:

```bash
cd ~/vox-motion-graphics-v4 && git push -u origin main && git tag v0.1.0 && git push origin v0.1.0
```
(Their stored GitHub credentials or `git credential` prompt handles auth.) I verify afterwards:
```bash
git ls-remote origin refs/heads/main refs/tags/v0.1.0
```
Expected: both refs listed.

- [ ] **Step 4: Install from GitHub**

```bash
opencode plugin add 'vox-motion-graphics-v4@git+https://github.com/tepennnnn/vox-motion-graphics-v4.git#main'
```
Expected: install spinner completes; it reports the config file it updated (`~/.opencode/opencode.json`, local scope — see Step 5).

- [ ] **Step 5: Migrate the entry to the global config (Review Focus 3)** — append the exact spec string `'vox-motion-graphics-v4@git+https://github.com/tepennnnn/vox-motion-graphics-v4.git#main'` to the `plugin` array in `~/.config/opencode/opencode.jsonc` (next to superpowers), then delete the local-scope file:

```bash
rm -f ~/.opencode/opencode.json
```

- [ ] **Step 6: Verify the installed package**

```bash
ls ~/.cache/opencode/packages/ | grep vox
```
Expected: a `vox-motion-graphics-v4@git+https:/github.com/tepennnnn/vox-motion-graphics-v4.git` directory containing `node_modules/vox-motion-graphics-v4/skills/motion-graphics-v3/SKILL.md` and `package.json` version `0.1.0` (`node -p` on it).

---

### Task 5: Cutover — one source of truth

**Files:**
- Delete: `~/.config/opencode/skills/motion-graphics-v3/` (the loose copy)
- Modify: `~/.claude/skills/motion-graphics-v3` symlink → into the installed plugin cache

**Interfaces:**
- Consumes: the verified install from Task 4.
- Produces: single live pipeline (the plugin cache); `~/.claude/.../env.sh` invocations keep working through the re-pointed symlink.

- [ ] **Step 1: Remove the loose copy**

```bash
rm -rf ~/.config/opencode/skills/motion-graphics-v3
```

- [ ] **Step 2: Re-point the symlink into the cache** (use the exact dir name found in Task 4 Step 6)

```bash
ln -sfn ~/.cache/opencode/packages/vox-motion-graphics-v4@git+https:/github.com/tepennnnn/vox-motion-graphics-v4.git/node_modules/vox-motion-graphics-v4/skills/motion-graphics-v3 ~/.claude/skills/motion-graphics-v3
readlink -f ~/.claude/skills/motion-graphics-v3
```
Expected: prints the physical plugin-cache path.

- [ ] **Step 3: Verify the old entry point still works (Review Focus 4, part 1)**

```bash
bash ~/.claude/skills/motion-graphics-v3/tools/env.sh | head -1
```
Expected: `MGV3=<plugin cache skill dir>`.

- [ ] **Step 4: Verify the old copy is gone (Review Focus 4, part 2)**

```bash
ls ~/.config/opencode/skills/
```
Expected: the directory is empty or absent — no `motion-graphics-v3`.

- [ ] **Step 5: Verify an existing project still builds through the new location** — run the `_selftest` film:

```bash
cd ~/motion-graphics-v3/_selftest && python3 build.py && npx hyperframes check --json
```
Expected: build completes and check reports `0` errors (the `_selftest` project exists for exactly this).

- [ ] **Step 6: Verify the skill is available from the installed plugin in a fresh session**

```bash
opencode run 'Use the skill tool and tell me: is a skill with id motion-graphics-v3 available? Answer yes or no and its id.'
```
Expected: answer contains `motion-graphics-v3`.

- [ ] **Step 7: Record the cutover in the repo's `skills/motion-graphics-v3/NOTES.md`** — append a dated line: "2026-11-12 — shipped as plugin `vox-motion-graphics-v4` v0.1.0; loose copies retired; `~/.claude/skills/motion-graphics-v3` now points into the plugin cache." Commit:

```bash
cd ~/vox-motion-graphics-v4 && git add -A && git commit -m "docs: record v0.1.0 cutover in NOTES.md"
```
(Push happens in Task 6 together with the version bump.)

---

### Task 6: Upgrade drill (prove "upgradable")

**Files:**
- Modify: `package.json` (0.1.0 → 0.1.1)

**Interfaces:**
- Consumes: remote + tag flow from Task 4, installed plugin from Task 5.
- Produces: demonstrated end-to-end upgrade: version `0.1.1` live in the cache.

- [ ] **Step 1: Bump and commit**

```bash
cd ~/vox-motion-graphics-v4 && sed -i 's/"version": "0.1.0"/"version": "0.1.1"/' package.json && git add package.json && git commit -m "chore: release 0.1.1"
```

- [ ] **Step 2: User pushes (same terminal, same credential flow as Task 4 Step 3):**

```bash
cd ~/vox-motion-graphics-v4 && git tag v0.1.1 && git push origin main v0.1.1
```

- [ ] **Step 3: Update the installed plugin**

```bash
opencode plugin update vox-motion-graphics-v4
```
Expected: it reports an update/install; no error.

- [ ] **Step 4: Verify the new version is live**

```bash
node -p "require('/data/data/com.termux/files/home/.cache/opencode/packages/vox-motion-graphics-v4@git+https:/github.com/tepennnnn/vox-motion-graphics-v4.git/node_modules/vox-motion-graphics-v4/package.json').version"
```
Expected: `0.1.1` (if the cache dir name changed after update, re-locate it with `ls ~/.cache/opencode/packages/ | grep vox` first).

- [ ] **Step 5: Report to the user:** plugin name, id, install + upgrade commands, where the skill lives, and that the drill proved `opencode plugin update` works.
