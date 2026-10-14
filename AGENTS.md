# VIBE-OS repository maintenance guidance

- This is a portable skill and Python standard-library CLI. Maintain Python 3.10+ compatibility.
- Prefer tests under `tests/` for behavioral changes. Run `python -m unittest discover -s tests -v`.
- Keep the root `vibeos/bundle/vibe-os/SKILL.md` concise and other details in `references/`.
- Don't introduce nonstandard runtime packages without a documented reason.
- Don't claim benchmark superiority until controlled, replicated results exist.
- Do not run `verify` commands against unknown repos without inspecting their side effects.
- Preserve user data and project files by default; `--force` should be explicit.
