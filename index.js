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
