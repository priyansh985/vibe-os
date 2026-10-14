# VIBE-OS repository maintenance guidance

- This is a portable skill, Python standard-library CLI, and native Node.js skill installer. Maintain Python 3.10+ compatibility.
- For Node installer changes, add tests under `tests-node/` and run `npm test` plus `npm pack --dry-run`. The Node entry point is `bin/vibe-os.cjs`.
- Prefer tests under `tests/` for behavioral changes. Run `python -m unittest discover -s tests -v`.
- Keep the root `vibeos/bundle/vibe-os/SKILL.md` concise and other details in `references/`.
- Don't introduce nonstandard runtime packages without a documented reason.
- Don't claim benchmark superiority until controlled, replicated results exist.
- Do not run `verify` commands against unknown repos without inspecting their side effects.
- Preserve user data and project files by default; `--force` should be explicit.
