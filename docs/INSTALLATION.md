# Installation guide

VIBE-OS has three installation approaches: the native Node.js skill installer, the full Python CLI + skill installer, or skill-only copy. **Python 3.10+** is required for the CLI. The skill itself is Markdown and does not require Python.

## Option A — Node.js installer (npm / npx)

Node.js 18+ is sufficient to install the skill with no Python. From your target application repository:

```sh
npx --yes github:priyansh985/vibe-os init --agent all
```

Or install the bootstrapper globally from GitHub:

```sh
npm install --global github:priyansh985/vibe-os
vibe-os init --project . --agent all
vibe-os doctor --project .
```

**Important:** `npx vibe-os init` and `npm install -g vibe-os` by the bare package name require an npm registry publication that has **not been performed**. The Node bootstrapper supports `init` and `doctor`; use Python for additional CLI commands. See [Node.js installation](NODE_INSTALLATION.md).

## Option B — Python CLI (complete toolkit)

### Install from GitHub (once published)

```bash
python -m pip install "git+https://github.com/priyansh985/vibe-os.git"
python -m vibeos --version
```

If you prefer not to install into your global Python environment, use a virtual environment:

```bash
python -m venv .venv
# Linux/macOS:
. .venv/bin/activate
# Windows PowerShell instead: .venv\Scripts\Activate.ps1
python -m pip install "git+https://github.com/priyansh985/vibe-os.git"
```

VIBE-OS is **not** represented as published on PyPI; do not assume `pip install vibe-os` resolves to this project. `git+...` installs directly from this repository once it exists.

### Install from a local checkout or ZIP

```bash
# In the extracted source directory:
python -m pip install .
python -m vibeos --version
```

Alternatively, without installing the package, use `python -m vibeos ...` from the source directory.

### Set up a target project

```bash
python -m vibeos init --project /path/to/your-app --agent all
python -m vibeos doctor --project /path/to/your-app
```

`--agent` can be `codex`, `claude`, `cursor`, or `all`. The installer creates:

```text
/path/to/your-app/
├── .agents/skills/vibe-os/     # Codex native skill
├── .claude/skills/vibe-os/     # Claude Code native skill
├── .cursor/rules/vibe-os.mdc  # Cursor rule adapter
└── .vibeos/
    ├── config.json
    ├── context.md
    ├── tasks/
    └── reports/
```

Existing files are preserved by default. `--force` overwrites VIBE-OS-managed paths; back up customized skill content before using it. The CLI does not change root `AGENTS.md` or global coding-agent settings.

### Use your first task

```bash
python -m vibeos assess --risk low --scope small --uncertainty low --reversibility easy
python -m vibeos task "Add a health endpoint" --project /path/to/your-app \
  --risk low --scope small --uncertainty low --reversibility easy
```

Fill `.vibeos/tasks/TASK-0001-*.md` with actual acceptance criteria. Then ask your coding agent to use VIBE-OS to implement them. After inspecting verification commands:

```bash
python -m vibeos verify --project /path/to/your-app --task TASK-0001 \
  --command "python -m unittest discover -s tests"
python -m vibeos report --project /path/to/your-app --task TASK-0001
```

On Windows PowerShell, enter commands on one line instead of using the Unix continuation backslash.

The verification command runs without a shell but has the current user's permissions; it is **not sandboxed**. Do not pass tokens/passwords into command arguments.

## Option C — skill only (no Node or Python)

Copy the entire [`vibeos/bundle/vibe-os/`](../vibeos/bundle/vibe-os/) directory into your repository's `.agents/skills/vibe-os/` (Codex) or `.claude/skills/vibe-os/` (Claude Code). Keep all `references/` and `assets/` alongside `SKILL.md`.

For Cursor, copy [`vibeos/bundle/cursor-rule.mdc`](../vibeos/bundle/cursor-rule.mdc) into `.cursor/rules/vibe-os.mdc` in the target repository. Agent activation behavior and supported paths depend on individual product versions. You can also explicitly request the agent to follow the VIBE-OS skill.

## Update or remove

Update the source package via a fresh Git checkout and `python -m pip install --upgrade .`. To refresh installed project adapters, run `python -m vibeos init --project /path/to/your-app --agent all --force` **after reviewing local customizations**.

To uninstall the Python package, run `python -m pip uninstall vibe-os`. The project-local `.agents/skills/vibe-os`, `.claude/skills/vibe-os`, `.cursor/rules/vibe-os.mdc`, and `.vibeos/` files are not removed automatically; inspect before deleting them.

## Next steps

- [Examples](../examples/walkthrough.md)
- [Troubleshooting](TROUBLESHOOTING.md)
- [Architecture](RFC-001-architecture.md)
- [Security boundaries](SECURITY.md)
