# Prior art and design lineage

VIBE-OS composes established coding-agent practices. Its name and packaging should not be confused with a proven novel algorithm.

| Reference | Relevant design idea | VIBE-OS decision |
|---|---|---|
| [Agent Skills specification](https://agentskills.io/specification) | SKILL.md frontmatter, progressive disclosure, references/scripts/assets | Portable root skill with on-demand references |
| [OpenAI Skills guide](https://developers.openai.com/api/docs/guides/tools-skills) | Skill metadata and context-conscious structure | Short activation description; detailed references split out |
| [Cursor Rules](https://docs.cursor.com/context/rules) | Scoped .mdc project rules | Concise Cursor adapter |
| [Claude Code Skills](https://code.claude.com/docs/en/skills) | .claude/skills skill discovery | Native installed skill folder |
| [GitHub Spec Kit](https://github.com/github/spec-kit) | Spec/plan/task workflow | Use measurable acceptance criteria for substantial changes |
| [OpenSpec](https://github.com/Fission-AI/OpenSpec) | Lightweight change artifacts | Avoid oversized plans for local edits |
| [BMad Method](https://github.com/bmad-code-org/BMAD-METHOD) | Adaptive engineering workflow | Workflow depth varies by task risk |
| [Superpowers](https://github.com/obra/superpowers) | Verification discipline, code review | Evidence-based completion and disciplined tests |
| [Aider](https://github.com/Aider-AI/aider) | Repository-aware editing | Targeted context retrieval |
| [AGENTS.md](https://agents.md/) | Portable repo instructions | Read guidance without overwriting existing policy |

These are design references, not benchmarking wins. Consult upstream docs to confirm behavior against product versions at installation time.
