# Verification and completion evidence

Choose checks that demonstrate actual behavior, ideally in ascending cost order: syntax/type/static checks → targeted tests → integration/regression tests → manual/visual validation where relevant → build or smoke test. Not every check is applicable.

Before running anything, inspect project scripts and their side effects. Never run untrusted or destructive commands automatically. Do not install dependencies, touch external services, publish artifacts, or deploy without appropriate authorization. Prefer isolated test environments.

Each acceptance criterion should have evidence or an explicit unverified status. For failures: capture reproducible steps, diagnose cause, attempt scoped repair, rerun pertinent tests, and stop/escalate if blocked or safety boundaries would be crossed. Do not silently delete tests, disable checks, or modify unrelated code to reach green.

A passing CLI exit code proves only that the invoked command returned success. It does not prove that requested behavior, security, performance or regression protection is sufficient. For significant work, report: criterion → evidence, changes, exact commands/results, remaining risks, tests skipped, and follow-up items.

The VIBE-OS CLI stores command labels, exit status and duration, not command stdout/stderr. The completion report includes unchecked manual review gates; an agent must not auto-check them without evidence.
