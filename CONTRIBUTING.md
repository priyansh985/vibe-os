# Contributing to VIBE-OS

Thank you for improving VIBE-OS. This repository is an experimental, evidence-oriented engineering workflow. Proposals should demonstrate a tangible benefit without imposing unnecessary ceremony.

## Development setup

Prerequisites: Python 3.10 or newer; Git. No account or API key is required for local development.

```bash
git clone https://github.com/priyansh985/vibe-os.git
cd vibe-os
python -m pip install -e .
python -m unittest discover -s tests -v
```

The public repository URL above will work once the initial repository is published. Until then, use the prepared source bundle.

## Contribution flow

1. Open an issue for substantial feature or behavior changes; small fixes can go directly to a pull request.
2. Create a branch and make one well-scoped change. Read `AGENTS.md` and `docs/SECURITY.md`.
3. Add or update tests for changes to the CLI, mode selector, or bundled skill structure.
4. Run `python -m unittest discover -s tests -v` and record results.
5. Update docs and changelog when user-visible behavior changes.
6. Open a pull request describing the motivation, verification evidence, and any gaps.

Use a normal discussion or issue instead of disclosing security-sensitive exploits publicly; see [Security policy](SECURITY.md).

## Scope and philosophy

- Prefer a small, working, testable behavior over a large conceptual layer.
- Do not make unsupported claims about productivity gains.
- Preserve compatibility with documented Agent Skills structure where possible.
- Avoid agent-specific lock-in; keep integrations lightweight.
- Do not commit secrets, account data, benchmark outputs containing confidential code, or generated `.vibeos/` project-state directories from other users.

## Code standards

Use the Python standard library unless a dependency has clear benefit. Keep source readable, prefer explicit exceptions and defensive file handling, and validate all changes with automated tests. Documentation examples should be executable or clearly marked as illustrative.

## License

By contributing, you agree your contributions are made available under the project's [MIT License](LICENSE).
