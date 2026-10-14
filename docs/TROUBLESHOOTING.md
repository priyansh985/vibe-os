# Troubleshooting

**`No module named vibeos`** — Execute from the source checkout or install into the active Python environment with `python -m pip install .`. Confirm with `python -m vibeos --version`.

**`Project directory does not exist`** — Create the application project first; `init` requires an existing folder. Use an absolute path if uncertain.

**`Project not initialized`** — Run `python -m vibeos init --project /path/to/app --agent all` before `task`.

**`SKIPPED` instead of `INSTALLED`** — Existing paths are preserved by design. Back up modifications and use `--force` only when replacement is appropriate.

**`doctor` indicates a missing adapter** — Only one integration is needed. A `doctor` exit code 0 means the state and at least one supported adapter are present.

**`DEEP required by assessed factors`** — Increase your requested mode or correct incorrectly classified risk inputs. The tool won't downgrade a DEEP risk assessment to QUICK.

**Verification fails or hangs** — Commands use the current OS user's privileges and execute without a shell. Inspect executable arguments, environment, dependencies, test runner, and timeout. Use `--show-output` to print captured output (not persisted). Avoid dangerous or secret-bearing commands.

**Coding agent doesn't automatically use the skill** — Confirm its native skill/rule path, reload or restart its project session if needed, and ask explicitly for VIBE-OS. VIBE-OS cannot control agent tool permissions or guarantee automatic activation.

**Windows command copied with `\` continuation fails** — Put options on a single line in PowerShell; `\` line continuation in examples is for Unix shells.

**`pip install vibe-os` retrieves an unexpected project** — This release is not claimed to be on PyPI. Install from the GitHub source or the downloaded project archive instead.
