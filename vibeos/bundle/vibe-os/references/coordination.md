# Optional parallel-agent coordination

Default to one agent. Parallel agents can help only where independent work can be assigned with explicit interfaces, separate file ownership or worktrees, and clear merging/verification responsibilities.

Before delegation specify: deliverable, files to own/avoid, tests to run, dependencies, acceptance conditions, output format and merge reviewer. Avoid delegating changes to shared central modules in parallel without isolation.

A coordinating agent integrates code, reconciles conflicts, runs the combined test suite and reports which claims are independently verified. Never treat subagent self-reports as sufficient proof. For tightly coupled small tasks, use a single agent to reduce cost and collisions.
