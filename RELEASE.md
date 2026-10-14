# VIBE-OS 1.0.0 release record

**Release date:** 2026-10-14  
**Release type:** first usable portable workflow + local helper CLI.

## Verified in this release

- 19 standard-library automated tests passing (`python -m unittest discover -s tests -v`).
- Built Python package wheel and installed in isolated target directory; version and risk selector resolved from bundled distribution.
- Fresh-project end-to-end smoke flow: `init` → `task` → explicit `verify` → `report` succeeded.
- Portable skill includes YAML frontmatter and targeted reference files. External official Agent Skills validator was **not** run; only project-local manifest checks were performed.

## Not yet verified

- Actual coding productivity gains over no-skill, Spec Kit, Superpowers or other coding frameworks.
- Live end-to-end activation across Codex, Claude Code and Cursor accounts/builds.
- Isolation against malicious/untrusted executable verification commands.
- Performance on production-scale repositories.

The release must not be marketed as a proven superior or autonomous coding system until future independent trials establish these claims.
