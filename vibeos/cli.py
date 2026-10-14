"""VIBE-OS local CLI. Uses Python standard library only."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
import time
from collections import defaultdict

from . import __version__
from .core import assess

PACKAGE = Path(__file__).resolve().parent
SKILL = PACKAGE / "bundle" / "vibe-os"
MODES = ("auto", "quick", "standard", "deep")


def utc_now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def save_text(path: Path, content: str, *, force: bool = False) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.is_symlink():
        raise ValueError(f"Refusing to write through symlink: {path}")
    if path.exists() and not force:
        return False
    path.write_text(content, encoding="utf-8")
    return True


def dump_json(path: Path, data: dict, *, force: bool = False) -> bool:
    return save_text(path, json.dumps(data, indent=2) + "\n", force=force)


def project_dir(path: str) -> Path:
    project = Path(path).expanduser().resolve()
    if not project.is_dir():
        raise ValueError(f"Project directory does not exist: {project}")
    return project


def install_skill(target: Path, *, force: bool) -> bool:
    if target.exists() and not force:
        return False
    if target.is_symlink():
        raise ValueError(f"Refusing to overwrite a symlink at {target}")
    # Avoid silently replacing existing directories unless force was specified.
    if target.exists():
        shutil.rmtree(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(SKILL, target)
    return True


def install_cursor_rule(project: Path, *, force: bool) -> bool:
    source = PACKAGE / "bundle" / "cursor-rule.mdc"
    return save_text(project / ".cursor" / "rules" / "vibe-os.mdc",
                     source.read_text(encoding="utf-8"), force=force)


def cmd_init(args):
    p = project_dir(args.project)
    if not (SKILL / "SKILL.md").exists():
        raise ValueError("Bundled skill missing. Reinstall the VIBE-OS package.")
    state = p / ".vibeos"
    state.mkdir(exist_ok=True)
    (state / "tasks").mkdir(exist_ok=True)
    (state / "reports").mkdir(exist_ok=True)
    files = [
        (state / "config.json", json.dumps({
            "schema_version": 1, "framework_version": __version__,
            "default_mode": "auto", "verification_is_explicit": True
        }, indent=2) + "\n"),
        (state / "context.md", "# Project context\n\n## Purpose\n(TODO)\n\n## Stack and conventions\n(TODO)\n\n## Commands and environments\n(TODO)\n\n## Important constraints\n(TODO)\n\n## Decisions\n(Keep concise; use ADRs for major decisions.)\n"),
    ]
    for path, content in files:
        changed = save_text(path, content, force=args.force)
        print(f"{'CREATED' if changed else 'SKIPPED'} {path.relative_to(p)}")
    agents = ("codex", "claude", "cursor") if args.agent == "all" else (args.agent,)
    for agent in agents:
        if agent == "codex":
            target = p / ".agents" / "skills" / "vibe-os"
            changed = install_skill(target, force=args.force)
        elif agent == "claude":
            target = p / ".claude" / "skills" / "vibe-os"
            changed = install_skill(target, force=args.force)
        else:
            target = p / ".cursor" / "rules" / "vibe-os.mdc"
            changed = install_cursor_rule(p, force=args.force)
        print(f"{'INSTALLED' if changed else 'SKIPPED'} {target.relative_to(p)}")
    print("Next: fill .vibeos/context.md; create a task with `python -m vibeos task ...`.")
    print("Existing files were preserved unless --force was specified.")
    return 0


def assessment_from_args(args):
    return assess(args.risk, args.scope, args.uncertainty, args.reversibility)


def cmd_assess(args):
    a = assessment_from_args(args)
    print(json.dumps({"recommended_mode": a.mode, "reasons": list(a.reasons)}, indent=2))
    return 0


def cmd_task(args):
    p = project_dir(args.project)
    tasks = p / ".vibeos" / "tasks"
    if not tasks.is_dir():
        raise ValueError("Project not initialized. Run `python -m vibeos init` first.")
    recommended = assessment_from_args(args)
    chosen = recommended.mode if args.mode == "auto" else args.mode.upper()
    ranks = {"QUICK": 0, "STANDARD": 1, "DEEP": 2}
    if ranks[chosen] < ranks[recommended.mode]:
        raise ValueError(f"{recommended.mode} required by assessed factors. Resolve risks before downgrading.")
    previous = [int(m.group(1)) for f in tasks.glob("TASK-*.md")
                if (m := re.match(r"TASK-(\d{4})-", f.name))]
    number = max(previous, default=0) + 1
    short = re.sub(r"[^a-z0-9]+", "-", args.goal.lower()).strip("-")[:45].strip("-") or "task"
    task_id = f"TASK-{number:04d}"
    template = (SKILL / "assets" / "task-contract.md").read_text(encoding="utf-8")
    replacements = {
        "__ID__": task_id, "__GOAL__": " ".join(args.goal.split()),
        "__MODE__": chosen, "__DATE__": utc_now(),
        "__REASON__": "; ".join(recommended.reasons),
        "__RISK__": args.risk, "__SCOPE__": args.scope,
        "__UNCERTAINTY__": args.uncertainty, "__REVERSIBILITY__": args.reversibility,
    }
    for old, new in replacements.items():
        template = template.replace(old, new)
    target = tasks / f"{task_id}-{short}.md"
    save_text(target, template)
    print(f"Created {target.relative_to(p)} ({chosen})")
    if chosen != recommended.mode:
        print(f"Note: manual mode differs from conservative recommendation ({recommended.mode}).")
    print("Fill measurable acceptance criteria and verification plan before implementation.")
    return 0


def resolve_task(project: Path, value: str) -> Path:
    tasks = (project / ".vibeos" / "tasks").resolve()
    if re.fullmatch(r"TASK-\d{4}", value):
        found = list(tasks.glob(f"{value}-*.md"))
        if len(found) != 1:
            raise ValueError(f"Expected one task matching {value}, found {len(found)}")
        result = found[0].resolve()
    else:
        result = (project / value).resolve()
    if not result.is_relative_to(tasks) or not result.is_file():
        raise ValueError("Task must be an existing file inside .vibeos/tasks")
    return result


def cmd_verify(args):
    p = project_dir(args.project)
    task = resolve_task(p, args.task)
    if not args.command:
        raise ValueError("At least one explicit --command must be supplied.")
    if not 1 <= args.timeout <= 1800:
        raise ValueError("--timeout must be between 1 and 1800 seconds")
    checks = []
    for command in args.command:
        argv = shlex.split(command, posix=os.name != "nt")
        if not argv:
            raise ValueError("Empty verification command")
        print(f"CHECK {len(checks) + 1}: {command}", flush=True)
        started = time.monotonic()
        try:
            run = subprocess.run(argv, cwd=p, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, text=True,
                                 encoding="utf-8", errors="replace", timeout=args.timeout,
                                 check=False)
            code = run.returncode
            outcome = "passed" if code == 0 else "failed"
            output = (run.stdout or "") + (run.stderr or "")
        except subprocess.TimeoutExpired:
            code, outcome, output = None, "timeout", "Command exceeded timeout."
        except OSError as e:
            code, outcome, output = None, "error", str(e)
        seconds = round(time.monotonic() - started, 3)
        checks.append({"command": command, "outcome": outcome,
                       "exit_code": code, "duration_seconds": seconds})
        print(f"  {outcome.upper()} ({seconds:.3f}s)")
        if args.show_output and output:
            print(output[-6000:])
        if outcome != "passed" and not args.keep_going:
            break
    report = {
        "task": task.name, "created_at": utc_now(),
        "checks": checks,
        "all_checks_passed": all(c["outcome"] == "passed" for c in checks),
        "note": "Passing commands is not proof of complete behavior, safety, or acceptance criteria.",
        "output_saved": False,
    }
    fname = f"{task.stem}-verify-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')}.json"
    destination = p / ".vibeos" / "reports" / fname
    dump_json(destination, report)
    print(f"Evidence: {destination.relative_to(p)} (output intentionally not persisted)")
    return 0 if report["all_checks_passed"] else 1


def cmd_report(args):
    p = project_dir(args.project)
    task = resolve_task(p, args.task)
    evidence_files = sorted((p / ".vibeos" / "reports").glob(f"{task.stem}-verify-*.json"))
    records = []
    for entry in evidence_files:
        data = json.loads(entry.read_text(encoding="utf-8"))
        records.append((entry, data))
    lines = [f"# Completion evidence — {task.name}", "", f"Generated: {utc_now()}", "",
             "## Verification executions", ""]
    if not records:
        lines.append("No checks recorded. **Verification evidence: missing.**")
    else:
        for filepath, data in records:
            status = "PASS" if data.get("all_checks_passed") else "FAIL"
            lines.append(f"### {filepath.name} — {status}")
            for c in data.get("checks", []):
                lines.append(f"- `{c['command']}`: {c['outcome']} (exit={c['exit_code']}, {c['duration_seconds']}s)")
            lines.append("")
    lines += ["", "## Human/agent review — not automated", "",
              "- [ ] Acceptance criteria individually demonstrated", "- [ ] Scope and regression review completed",
              "- [ ] Security/privacy implications reviewed", "- [ ] Limitations, skipped tests, and follow-up work recorded",
              "", "**Important:** command exit codes alone never establish task completion.", ""]
    output = p / ".vibeos" / "reports" / f"{task.stem}-completion.md"
    save_text(output, "\n".join(lines), force=True)
    print(f"Wrote {output.relative_to(p)}; human completion gates remain unchecked.")
    return 0


def cmd_doctor(args):
    p = project_dir(args.project)
    checks = {
        "bundled skill": (SKILL / "SKILL.md").is_file(),
        "project state": (p / ".vibeos" / "config.json").is_file(),
        "project context": (p / ".vibeos" / "context.md").is_file(),
        "tasks folder": (p / ".vibeos" / "tasks").is_dir(),
        "Codex skill": (p / ".agents" / "skills" / "vibe-os" / "SKILL.md").is_file(),
        "Claude skill": (p / ".claude" / "skills" / "vibe-os" / "SKILL.md").is_file(),
        "Cursor rule": (p / ".cursor" / "rules" / "vibe-os.mdc").is_file(),
    }
    for item, ok in checks.items():
        print(f"{'OK' if ok else '--'}  {item}")
    print("One supported agent integration is sufficient; all three are optional.")
    return 0 if checks["project state"] and checks["bundled skill"] and any(
        checks[name] for name in ("Codex skill", "Claude skill", "Cursor rule")) else 1


def cmd_score(args):
    data = defaultdict(list)
    input_path = Path(args.results).expanduser().resolve()
    for i, raw in enumerate(input_path.read_text(encoding="utf-8").splitlines(), start=1):
        if not raw.strip():
            continue
        item = json.loads(raw)
        required = ("variant", "task_id", "passed", "duration_seconds", "tokens", "interventions")
        if any(k not in item for k in required) or type(item["passed"]) is not bool:
            raise ValueError(f"Line {i}: missing/invalid required fields")
        if any(not isinstance(item[k], (int, float)) or item[k] < 0
               for k in ("duration_seconds", "tokens", "interventions")):
            raise ValueError(f"Line {i}: numeric metrics must be nonnegative")
        data[str(item["variant"])].append(item)
    if not data:
        raise ValueError("Empty results file")
    out = {}
    for variant, items in sorted(data.items()):
        n = len(items)
        out[variant] = {
            "runs": n,
            "pass_rate": round(sum(x["passed"] for x in items) / n, 4),
            "mean_duration_seconds": round(sum(x["duration_seconds"] for x in items) / n, 2),
            "mean_tokens": round(sum(x["tokens"] for x in items) / n, 1),
            "mean_interventions": round(sum(x["interventions"] for x in items) / n, 2),
            "tasks": sorted(set(str(x["task_id"]) for x in items)),
        }
    task_sets = [set(v["tasks"]) for v in out.values()]
    print(json.dumps({"descriptive_statistics_only": True,
                      "balanced_task_coverage": all(t == task_sets[0] for t in task_sets),
                      "variants": out}, indent=2))
    return 0


def add_factors(parser):
    parser.add_argument("--risk", choices=("low", "medium", "high"), default="medium")
    parser.add_argument("--scope", choices=("small", "medium", "large"), default="medium")
    parser.add_argument("--uncertainty", choices=("low", "medium", "high"), default="medium")
    parser.add_argument("--reversibility", choices=("easy", "moderate", "hard"), default="moderate")


def build_parser():
    parser = argparse.ArgumentParser(prog="vibeos", description="VIBE-OS v1 coding workflow toolkit")
    parser.add_argument("--version", action="version", version=__version__)
    sub = parser.add_subparsers(dest="action", required=True)
    init = sub.add_parser("init", help="install skills/rules and create project state")
    init.add_argument("--project", default=".")
    init.add_argument("--agent", choices=("codex", "claude", "cursor", "all"), default="all")
    init.add_argument("--force", action="store_true", help="overwrite existing VIBE-OS-managed files")
    init.set_defaults(func=cmd_init)
    mode = sub.add_parser("assess", help="recommend task workflow depth")
    add_factors(mode)
    mode.set_defaults(func=cmd_assess)
    task = sub.add_parser("task", help="create an editable task contract")
    task.add_argument("goal")
    task.add_argument("--project", default=".")
    task.add_argument("--mode", choices=MODES, default="auto")
    add_factors(task)
    task.set_defaults(func=cmd_task)
    verify = sub.add_parser("verify", help="run explicit checks without a shell and record evidence")
    verify.add_argument("--task", required=True, help="TASK-0001 or .vibeos/tasks/TASK-0001-*.md")
    verify.add_argument("--project", default=".")
    verify.add_argument("--command", action="append", help="repeatable explicit check command")
    verify.add_argument("--timeout", type=int, default=180)
    verify.add_argument("--keep-going", action="store_true")
    verify.add_argument("--show-output", action="store_true", help="print tool output; never persisted")
    verify.set_defaults(func=cmd_verify)
    report = sub.add_parser("report", help="write summary of recorded checks and remaining review")
    report.add_argument("--task", required=True)
    report.add_argument("--project", default=".")
    report.set_defaults(func=cmd_report)
    doctor = sub.add_parser("doctor", help="check local setup")
    doctor.add_argument("--project", default=".")
    doctor.set_defaults(func=cmd_doctor)
    score = sub.add_parser("score", help="summarize a JSONL benchmark results file")
    score.add_argument("results")
    score.set_defaults(func=cmd_score)
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except (OSError, ValueError, json.JSONDecodeError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
