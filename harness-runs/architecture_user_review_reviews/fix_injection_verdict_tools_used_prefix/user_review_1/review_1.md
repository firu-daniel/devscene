# Architecture review — round 1

verdict: PASS
review_mode: full

## Should Fix

1. **`finding_1.md`, `finding_2.md` and `finding_3.md` still prescribe a tool that no harness contract requires.** Each says "Apply the same edits to `scripts/prompt-injection-screen.sh` with the file-edit tool, keeping its mode." A search of `plugin/`, `docs/`, `.claude/`, `cli/templates/` and `scripts/` finds no contract stating "file-edit tool"; the only precedent is this branch's `task_3_plan.md`, which is not a harness contract (`${CLAUDE_PLUGIN_ROOT}/instructions/untrusted_input.md` → `## The laundering check`). No guard or sandbox rule makes the clause fail: `plugin/hooks/git-trust-file-guard.sh` refuses only three `.git` paths. Following it therefore gives no wrong result, no failure sentence can be completed, and it stays a Should Fix (`${CLAUDE_PLUGIN_ROOT}/instructions/finding_grades.md` → `### Checklist triggers`). This is round 0's Should Fix 3, which the user's live answer did not select.
   **Fix:** state only the required result: the same edits, byte-identical content and the file's mode unchanged.
