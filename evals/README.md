# VIBE-OS evaluation protocol v1

## Research question

Does VIBE-OS improve *verified task completion* and *rework-adjusted effort* compared to a baseline AI coding agent using the same model, tooling and repository snapshot? Null: no improvement.

## Conditions

- Baseline: the host coding agent with its usual repository instructions, no VIBE-OS.
- VIBE-OS v1: same agent and prompts, plus VIBE-OS skill and CLI where applicable.
- Optional comparisons: separately configured Spec Kit / OpenSpec / Superpowers workflows, with clear versions and fair setup.

Never compare different model tiers or different tool permissions as if workflow were the only change. Randomize condition order and use fresh clean worktrees for every run. Do not let one condition observe patches or feedback from the other. Freeze dependencies, seeds and task descriptions when possible. Human judges should be blind to condition labels for subjective quality ratings.

## Task matrix

`tasks.jsonl` contains *proposed scenario definitions*, not runnable fixtures. Build or identify real, reproducible repositories and install independent acceptance tests before executing a credible benchmark. Begin with at least 12 unique tasks across new features, bug fixes and maintenance. Include at least three repetitions per task/condition and multiple real repositories if possible. Predetermine time/token budgets and stop conditions.

## Metrics

Primary: success on held-out behavioral acceptance tests, including regressions. Secondary: human intervention count, wall-clock duration, API/tool token consumption, test failures/regressions, unapproved unsafe actions and reviewer-rated maintainability. Record retries, setup overhead and review cost. A test that merely checks whether code parses is insufficient for functional success.

## Raw JSONL schema

One independent **agent run** per line (not one command check). Required fields:

```json
{"variant":"baseline","task_id":"T01","passed":true,"duration_seconds":140.0,"tokens":12345,"interventions":1}
```

These numbers illustrate the **format only** and do not represent an actual test. More fields may be added, such as `model`, `repository_commit`, `run_id`, `regressions`, `security_violations`, `review_score`, `condition_order`, `test_report_path` and `notes`.

Summarize your **own measured** data with:

```bash
python -m vibeos score /path/to/results.jsonl
```

The score command emits descriptive averages and pass rates only. It does **not** launch agents, validate provenance, calculate significance or demonstrate causality. For a publishable comparison, use paired per-task analyses, confidence intervals, judge blinding where possible, and a pre-registered protocol. Account for repeated runs and non-independence. Document exclusions and incomplete runs.

## Failure criteria

A condition fails a task if required acceptance tests fail or if the patch introduces a critical security regression, even if basic check commands returned zero. Track missing evidence separately from failed evidence. If VIBE-OS costs more without measurable benefit, remove or narrow its ceremony rather than redefining success.
