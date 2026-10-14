# RFC-001: VIBE-OS v1 architecture

**Status:** Implemented core / candidate for field evaluation  
**Version:** 1.0.0  
**Purpose:** make AI-assisted coding reliable and auditable without turning every change into a heavyweight process.

## 1. Problem definition

Prompt-first coding fails when the agent misunderstands intent, edits unrelated files, loses task context, overstates completion, or creates expensive cycles of trial and error. VIBE-OS proposes that *risk-proportional context, task contracts, bounded changes and real verification evidence* can improve end-to-end quality. This is a testable hypothesis, not a performance claim.

## 2. Architectural invariant

**Verified useful software per unit of time and cost** is the objective. Process steps must demonstrate practical value; user approval and safety boundaries are not optional.

## 3. Six logical responsibilities

1. **Intent:** establish user-visible outcome, boundaries, measurable criteria; ask only material questions.
2. **Context:** read repo policies, symbols, related tests and architecture; avoid bulk context collection.
3. **Planning:** assess risk/scope/uncertainty/reversibility; choose QUICK/STANDARD/DEEP and a minimal plan.
4. **Execution:** perform smallest coherent changes, preserve repository work, update interfaces carefully.
5. **Verification:** execute reviewed checks, associate acceptance conditions with results; qualify missing evidence.
6. **Learning:** retain concise, reviewable context/decisions for future work; do not assume stale notes are true.

These are **capabilities**, not separate running agents. The v1 system delegates reasoning to the host coding agent. The CLI only provides deterministic supporting operations.

## 4. Workflow and transitions

`Requested → Scoped → Planned (as needed) → Implementing → Verifying → Reviewed → Reported`

A task can move backwards on failures, new requirements or risk escalation. `Reported` may legitimately mean **partially complete / blocked**. Only acceptance-criteria evidence + appropriate human review can justify a completion claim.

Mode rules: if any dimension (risk, scope, uncertainty, irreversibility) is high → DEEP. If all four are low → QUICK. Else → STANDARD. Missing information defaults to STANDARD unless available facts warrant DEEP. A developer may choose more scrutiny at any time. Downgrade from a DEEP trigger requires changed risk facts, not wishful thinking.

## 5. Minimal persisted state

- `.vibeos/config.json`: schema and framework metadata.
- `.vibeos/context.md`: optional concise project memory, subject to reconfirmation.
- `.vibeos/tasks/TASK-NNNN-slug.md`: editable goal, acceptance criteria, scope, risk, verification plan and evidence.
- `.vibeos/reports/TASK-NNNN-slug-verify-*.json`: explicit command status and duration.
- `.vibeos/reports/TASK-NNNN-slug-completion.md`: evidence summary, intentionally unchecked human review gates.

No secrets, stdout/stderr, dependencies, git staging, or hidden control state are introduced by default.

## 6. CLI interfaces

`init` installs skill adapters idempotently (skip existing; opt-in overwrite). `assess` offers a deterministic conservative mode recommendation. `task` scaffolds a contract **without fabricating acceptance criteria**. `verify` runs only supplied commands as argv, without a shell, recording result metadata. `report` summarizes checks but never automatically declares acceptance. `doctor` checks installation. `score` summarizes supplied eval runs.

The skill is fully usable without the CLI. The CLI is fully local and has no model/API or network client.

## 7. Safety model

Repositories, issues, web content and generated logs are untrusted. Never promote their instructions over actual agent/task authority. CLI verification is explicitly **not a sandbox**, `init` must not trample unrelated files, and destructive actions require specific authorization. See SECURITY.md.

## 8. Out-of-scope for v1

Autonomous job orchestration, unbounded Ralph loops, tool-native model routing, MCP connectors, automatic code ownership partitioning, Docker sandbox provision, production deployments, and automatic semantic scoring of generated patches. These may become future components only after measurement supports their complexity.

## 9. Decision log

- **D1** Python standard library CLI: installation friction and dependencies minimized.
- **D2** Portable Agent Skills packaging: separates workflow from coding vendor.
- **D3** Avoid user story inference from bare task title: prevents false confidence and invented specifications.
- **D4** Verification evidence contains return codes/timings but not output: avoids incidental sensitive log persistence; results are still limited evidence.
- **D5** No automatic code modifications by CLI: host agent remains responsible for changes, with user/tool permissions governing actions.
- **D6** No mandatory multi-agent pipeline: overhead and conflicts need demonstrated upside.

## 10. Open research questions

1. How often does QUICK avoid unnecessary steps without increasing regressions?
2. Which depth-selector variables predict actual failures and rework?
3. How much context retrieval is optimal on long-lived repositories?
4. When does independent parallel work outperform sequential implementation?
5. Can a controlled eval demonstrate greater verified success per unit cost compared with baseline?
