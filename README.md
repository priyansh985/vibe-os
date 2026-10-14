# VIBE-OS v1.0.0

[Installation](docs/INSTALLATION.md) · [Node.js / npm / npx](docs/NODE_INSTALLATION.md) · [Examples](examples/walkthrough.md) · [Architecture](docs/RFC-001-architecture.md) · [Contributing](CONTRIBUTING.md) · [Security](SECURITY.md) · [Changelog](CHANGELOG.md) · [Publishing](docs/PUBLISHING.md)

**Adaptive Vibe Engineering System** — an open, portable workflow for AI-assisted software development that prioritizes *verified behavior* over prompt volume, ceremony, or agent count.

**Status:** usable v1 reference implementation and skill. **Not** an autonomous coding model, orchestration server, sandbox, or scientifically validated productivity improvement. Initial claims about benefits are hypotheses until independently benchmarked.

## What's included

- Portable `vibe-os` skill using the Agent Skills `SKILL.md` format; focused supporting references and templates.
- Adapters for Codex (`.agents/skills/vibe-os`), Claude Code (`.claude/skills/vibe-os`), Cursor (`.cursor/rules/vibe-os.mdc`).
- Dependency-free Python CLI to install adapters, assess workflow risk, scaffold task contracts, run *explicitly chosen* verification checks, preserve evidence and summarize eval results.
- Native Node.js 18+ skill installer (`vibe-os init` / `vibe-os doctor`) for GitHub-backed npm/npx installs; no Python needed for skill setup.
- Task/risk protocol, engineering safety guidance, reproducible evaluation instructions and standard-library tests.

## Quick start

### Node.js — npx / npm

To install the VIBE-OS coding skill into your **current application project** without Python, use the GitHub-backed package:

```sh
npx --yes github:priyansh985/vibe-os init --agent all
```

Or install the Node installer globally from GitHub:

```sh
npm install --global github:priyansh985/vibe-os
vibe-os init --project . --agent all
vibe-os doctor --project .
```

The Node installer works with Codex, Claude Code, and Cursor, and does **not** implement all of the Python CLI's task/verification commands. The shorter `npx vibe-os init` command will only work **after the project is published on npm under that exact name**. See [Node.js install / npm publication guide](docs/NODE_INSTALLATION.md).

### Python full toolkit

Install from this GitHub repository (after publication):

```bash
python -m pip install "git+https://github.com/priyansh985/vibe-os.git"
python -m vibeos --version
```

Or use the local source files as described below. For native skill-only setup, Windows instructions, project layout, updates and removal, see the [complete installation guide](docs/INSTALLATION.md).


Requirements: **Python 3.10+**. No API key, paid service or extra package required.

From the extracted `vibe-os-v1` folder:

```bash
# Install VIBE-OS into your existing application repository; safe by default.
python -m vibeos init --project /path/to/your-project --agent all

# Review the state file: /path/to/your-project/.vibeos/context.md
python -m vibeos assess --risk low --scope small --uncertainty low --reversibility easy

# Create a task agreement. The CLI does not guess acceptance criteria.
python -m vibeos task "Add a health endpoint" --project /path/to/your-project \
  --risk low --scope small --uncertainty low --reversibility easy

# Fill .vibeos/tasks/TASK-0001-*.md with concrete behavior and verification.
# Run ONLY checks you have inspected and approved in the target repo.
python -m vibeos verify --project /path/to/your-project --task TASK-0001 \
  --command "python -m unittest discover -s tests"

python -m vibeos report --project /path/to/your-project --task TASK-0001
python -m vibeos doctor --project /path/to/your-project
```

On Windows, run `py -m vibeos ...` or `python -m vibeos ...`; command-line continuation syntax differs (prefer each command on one line in PowerShell). If working outside the extracted directory, either launch with that directory as your working directory, set `PYTHONPATH` to it, or install locally with `python -m pip install -e /path/to/vibe-os-v1`.

### Use directly as a skill (no CLI required)

You can copy **`vibeos/bundle/vibe-os/`** into `.agents/skills/vibe-os/` for Codex, or `.claude/skills/vibe-os/` for Claude Code. Alternatively use the separate ZIP containing only `vibe-os/`. In Cursor, use the provided `.cursor/rules/vibe-os.mdc` adapter. Models may select the skill when applicable; you can explicitly ask the agent to use VIBE-OS for a coding task.

The CLI installs files only in the target project. It **does not** configure accounts, start agents, execute model calls, or modify root AGENTS.md. Existing VIBE-OS paths are skipped by default; `--force` explicitly overwrites them.

## Design: small core, specialized references

| Dimension | QUICK | STANDARD | DEEP |
|---|---|---|---|
| Trigger | All low-risk/small/clear/reversible | Partial complexity, default unknowns | Any high-risk/uncertainty, large scope or hard rollback |
| Planning | In-chat/implicit | Short task contract | Alternatives, decisions, risk gates, slice plan |
| Tests | Targeted | Targeted + regression | Layered validation + rollback and approval |
| Handoff | Brief summary | Evidence + unresolved issues | Traceable verification and formal gates |

Six logical responsibilities (not necessarily six agents): intent, context, planning, execution, verification and learning. Each has narrow boundaries. The model makes coding decisions; the CLI gives it a stable work product and measurable evidence.

## Supported CLI

```text
python -m vibeos --help
python -m vibeos init --project . --agent all|codex|claude|cursor [--force]
python -m vibeos assess --risk low|medium|high --scope small|medium|large \
  --uncertainty low|medium|high --reversibility easy|moderate|hard
python -m vibeos task "goal" [--project .] [--mode auto|quick|standard|deep] [factor flags]
python -m vibeos verify --task TASK-0001 [--project .] \
  --command "your approved command" [--command "second command"] [--timeout 180]
python -m vibeos report --task TASK-0001 [--project .]
python -m vibeos doctor [--project .]
python -m vibeos score evals/results.jsonl
```

If factors are omitted, their defaults are medium/moderate, resulting in STANDARD. `task --mode` can increase scrutiny but cannot downgrade the risk-based mode; reassess the inputs if the facts change. `verify` runs commands **without a shell** using the user's privileges and is **not a sandbox**. Output is not persisted (command string, exit code and timing are). Do not supply commands with tokens/passwords or run potentially destructive scripts without review.

## Evaluation

See [evals/README.md](evals/README.md) for the task matrix, experimental design and JSONL score format. The `score` command computes *descriptive* aggregate statistics from supplied runs; it neither launches coding agents nor makes causal claims. Run the same pre-registered tasks from clean, identical repository snapshots for baseline and VIBE-OS conditions. Do not use the sample data as claimed results.

## Reference documentation

- [Core architecture / RFC-001](docs/RFC-001-architecture.md)
- [Threat model and boundaries](docs/SECURITY.md)
- [Design rationale and prior art](docs/RESEARCH.md)
- [Example usage](examples/walkthrough.md)

## Test locally

```bash
python -m unittest discover -s tests -v
npm test
npm pack --dry-run
```

## Limitations

- The skill depends on an external coding agent; this package is not a model or autonomous agent runner.
- Repository context selection and acceptance-criteria evaluation are performed by the agent/human, not automated by the CLI.
- The CLI's commands run with your user permissions and could have side effects. The caller must check them first.
- Cursor gets a concise project rule adapter rather than the full skill auto-activation; exact product behavior can change.
- The Node command is a **bootstrapper** (`init` / `doctor`), not a replacement for the seven-command Python toolkit.
- Parallel coding, deployment automation, audit guarantees, and hosted persistence are intentionally out of scope for v1.

## Community and maintenance

See [CONTRIBUTING.md](CONTRIBUTING.md) for development and pull requests, [SECURITY.md](SECURITY.md) for vulnerability reporting, and [GitHub Actions CI](.github/workflows/ci.yml) for the automated test/build workflow. The initial v1 suite includes 19 local tests; CI results become available only after repository publication and a workflow run.

## License

MIT, see [LICENSE](LICENSE). Not affiliated with Codex, Cursor, Anthropic, or any other coding tool provider.
