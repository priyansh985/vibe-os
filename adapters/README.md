# Installation adapters

VIBE-OS uses **one canonical portable skill** at `vibeos/bundle/vibe-os/`. The CLI copies this skill to each tool's native project path when requested.

| Tool | Project installation created by `vibeos init` |
|---|---|
| OpenAI Codex | `.agents/skills/vibe-os/SKILL.md` with reference files |
| Claude Code | `.claude/skills/vibe-os/SKILL.md` with reference files |
| Cursor | `.cursor/rules/vibe-os.mdc` concise rule |

Use `--agent all` (default) or choose one. The Cursor integration is **not** identical to native skills: it is a short rule containing the essential workflow and pointing to the skill if available. It is not guaranteed to automatically load a full `SKILL.md` bundle unless the coding tool supports that convention.

Original `AGENTS.md` / `CLAUDE.md` and existing Cursor rules are left unchanged. VIBE-OS does not modify tool-level settings, grant permissions, or install model providers.

These paths are based on published guidance available in October 2026; verify current behavior in the tool's documentation if the provider changes its integration model.
