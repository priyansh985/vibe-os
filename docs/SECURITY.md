# VIBE-OS threat model and operational safety

VIBE-OS provides process guidance and a local CLI, **not** a security sandbox or permission broker.

## Trust zones

1. User/system instructions and explicitly authorized actions.
2. Agent-readable repo content, issues, downloaded documentation and test data: useful **untrusted evidence**, not instructions of higher authority.
3. Generated code and executable verification commands: inspect for unintended side effects.
4. External services, credentials, production data and deployments: highest consequences; require explicit authorization and proper least-privilege controls.

## Primary threats

- **Prompt injection:** malicious repository or web text instructs an agent to expose secrets, ignore user requirements, or run commands.
- **Supply-chain attack:** dependency install or copied remote shell commands compromise the developer's environment.
- **Command execution:** `verify --command` runs arbitrary supplied executable+arguments with the caller's OS permissions; it does *not* invoke a shell but called executables can have arbitrary side effects.
- **Information leaks:** secrets inadvertently embedded in CLI arguments, commits, project notes or test output.
- **Destructive workflow:** migrations, deletes, force pushes and deployment without sufficient approval/rollback.
- **Stale memory:** erroneous `.vibeos/context.md` interpreted as current facts.

## Mitigations

The skill instructs targeted context reading, clear authority boundaries, least-privilege operations, human approval on irreversible steps, verification disclosure and explicit command review. The CLI preserves existing VIBE-OS paths unless `--force` is used and it omits command output from evidence files. Avoid secrets in command strings (they **are** persisted as evidence); use environment-provided tokens for approved tools instead.

## Remaining risks

The CLI currently relies on underlying process permissions and does not isolate child process groups, enforce filesystem isolation, block network access, redact all possible sensitive data, provide signed evidence, or confirm that executable labels correspond to benign commands. Use a proper container/sandbox and organization policy for executing untrusted repositories. Restrict who can edit skill definitions and CLI files. Run `--force` only after inspecting existing files.

Report security problems privately through the user's normal software maintenance channel; no external reporting endpoint is bundled.
