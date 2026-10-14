"""Unit and local integration tests; no network or external dependencies."""
import contextlib
from io import StringIO
import json
from pathlib import Path
import sys
import tempfile
import unittest

from vibeos.cli import main, SKILL
from vibeos.core import assess


class ModeTests(unittest.TestCase):
    def test_quick(self):
        self.assertEqual(assess("low", "small", "low", "easy").mode, "QUICK")

    def test_default(self):
        self.assertEqual(assess().mode, "STANDARD")

    def test_deep_risk(self):
        self.assertEqual(assess("high", "small", "low", "easy").mode, "DEEP")

    def test_deep_irreversibility(self):
        self.assertEqual(assess("low", "small", "low", "hard").mode, "DEEP")

    def test_deep_uncertainty(self):
        self.assertEqual(assess("low", "small", "high", "easy").mode, "DEEP")

    def test_invalid(self):
        with self.assertRaises(ValueError):
            assess(risk="unknown")


class CLITests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.project = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def call(self, *args):
        out, err = StringIO(), StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            result = main(list(args))
        return result, out.getvalue(), err.getvalue()

    def init(self, agent="all"):
        return self.call("init", "--project", str(self.project), "--agent", agent)

    def task(self, **kwargs):
        extra = []
        for name, value in kwargs.items():
            extra.extend(["--" + name.replace("_", "-"), value])
        return self.call("task", "Change greeting", "--project", str(self.project), *extra)

    def test_full_init(self):
        ret, _, _ = self.init()
        self.assertEqual(ret, 0)
        self.assertTrue((self.project / ".agents/skills/vibe-os/SKILL.md").exists())
        self.assertTrue((self.project / ".claude/skills/vibe-os/SKILL.md").exists())
        self.assertTrue((self.project / ".cursor/rules/vibe-os.mdc").exists())
        self.assertTrue((self.project / ".vibeos/context.md").exists())
        ret, _, _ = self.call("doctor", "--project", str(self.project))
        self.assertEqual(ret, 0)

    def test_init_preserves_content(self):
        self.init()
        p = self.project / ".vibeos/context.md"
        p.write_text("Keep my notes", encoding="utf-8")
        self.init()
        self.assertEqual(p.read_text(encoding="utf-8"), "Keep my notes")

    def test_single_adapter(self):
        self.init("codex")
        self.assertTrue((self.project / ".agents/skills/vibe-os/SKILL.md").exists())
        self.assertFalse((self.project / ".claude/skills/vibe-os/SKILL.md").exists())

    def test_contract_and_sequence(self):
        self.init()
        self.assertEqual(self.task(risk="low", scope="small", uncertainty="low", reversibility="easy")[0], 0)
        self.assertEqual(self.task()[0], 0)
        tasks = sorted((self.project / ".vibeos/tasks").glob("*.md"))
        self.assertEqual(len(tasks), 2)
        self.assertIn("QUICK", tasks[0].read_text(encoding="utf-8"))
        self.assertIn("STANDARD", tasks[1].read_text(encoding="utf-8"))
        self.assertIn("Observable behavior", tasks[0].read_text(encoding="utf-8"))

    def test_standard_cannot_be_downgraded(self):
        self.init()
        rc, _, err = self.task(mode="quick")
        self.assertEqual(rc, 2)
        self.assertIn("STANDARD required", err)

    def test_deep_cannot_be_downgraded(self):
        self.init()
        rc, _, err = self.task(risk="high", mode="quick")
        self.assertEqual(rc, 2)
        self.assertIn("DEEP required", err)

    def test_invalid_task_reference(self):
        self.init()
        rc, _, err = self.call("report", "--project", str(self.project), "--task", "../secret")
        self.assertEqual(rc, 2)
        self.assertIn("inside .vibeos/tasks", err)

    def test_verify_pass_and_report(self):
        self.init()
        self.task()
        cmd = f'{sys.executable} -c "print(chr(49)+chr(50)+chr(51))"'
        rc, output, _ = self.call("verify", "--project", str(self.project), "--task", "TASK-0001", "--command", cmd)
        self.assertEqual(rc, 0)
        evidence = list((self.project / ".vibeos/reports").glob("*.json"))
        self.assertEqual(len(evidence), 1)
        data = json.loads(evidence[0].read_text(encoding="utf-8"))
        self.assertTrue(data["all_checks_passed"])
        self.assertNotIn("123", json.dumps(data))  # printed output not stored
        rc, _, _ = self.call("report", "--project", str(self.project), "--task", "TASK-0001")
        self.assertEqual(rc, 0)
        report = list((self.project / ".vibeos/reports").glob("*completion.md"))[0]
        self.assertIn("[ ] Acceptance criteria", report.read_text(encoding="utf-8"))

    def test_verify_failure(self):
        self.init()
        self.task()
        cmd = f'{sys.executable} -c "import sys; sys.exit(4)"'
        rc, _, _ = self.call("verify", "--project", str(self.project), "--task", "TASK-0001", "--command", cmd)
        self.assertEqual(rc, 1)
        evidence = list((self.project / ".vibeos/reports").glob("*.json"))[0]
        self.assertFalse(json.loads(evidence.read_text(encoding="utf-8"))["all_checks_passed"])

    def test_verify_missing_command(self):
        self.init()
        self.task()
        rc, _, err = self.call("verify", "--project", str(self.project), "--task", "TASK-0001")
        self.assertEqual(rc, 2)
        self.assertIn("explicit", err)

    def test_score(self):
        records = self.project / "records.jsonl"
        entries = [
            {"variant": "baseline", "task_id": "T1", "passed": False, "duration_seconds": 12, "tokens": 1000, "interventions": 2},
            {"variant": "vibe-os", "task_id": "T1", "passed": True, "duration_seconds": 15, "tokens": 1100, "interventions": 1},
        ]
        records.write_text("\n".join(json.dumps(x) for x in entries), encoding="utf-8")
        rc, out, _ = self.call("score", str(records))
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(out)["variants"]["vibe-os"]["pass_rate"], 1)

    def test_invalid_score_input(self):
        records = self.project / "records.jsonl"
        records.write_text('{"variant":"a","task_id":"x","passed":1,"duration_seconds":1,"tokens":1,"interventions":0}', encoding="utf-8")
        self.assertEqual(self.call("score", str(records))[0], 2)


class SkillTests(unittest.TestCase):
    def test_manifest_and_references(self):
        content = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(content.startswith("---\nname: vibe-os\n"))
        self.assertIn("description:", content)
        self.assertLess(len(content.splitlines()), 500)
        for folder in ("assets", "references"):
            self.assertTrue(list((SKILL / folder).glob("*.md")))


if __name__ == "__main__":
    unittest.main()
