# Example: bug fix in a Python web app

This is an illustrative workflow, not a test run on a real project.

User request: "Fix a login response that incorrectly returns HTTP 500 when credentials are invalid."

1. Inspect repository policies, authentication implementation, error handling and login tests.
2. Mode choice: **DEEP**, because authentication behavior is security-sensitive; document the impact and test authorization boundaries.
3. Create a contract: AC1 incorrect credentials return the documented status; AC2 no secrets leak in errors; AC3 valid login remains functional; AC4 existing auth tests pass.
4. Choose the smallest code change consistent with framework conventions. Make a failing regression test first if feasible.
5. Run vetted targeted auth tests and project test suite. Explicitly note which checks couldn't run.
6. Report observed behavior, patch summary, tested commands and any blocked security scenarios.

Example commands from the VIBE-OS distribution root (adapt to your repository):

```bash
python -m vibeos init --project /path/to/app --agent codex
python -m vibeos task "Fix invalid login response" --project /path/to/app --risk high --scope small --uncertainty medium --reversibility easy
# Edit the generated task contract, then have your coding agent implement the fix.
python -m vibeos verify --project /path/to/app --task TASK-0001 --command "python -m unittest discover -s tests"
python -m vibeos report --project /path/to/app --task TASK-0001
```

The example assumes the app actually uses `unittest` and its tests are safe. Inspect the project first; different test commands may be appropriate.
