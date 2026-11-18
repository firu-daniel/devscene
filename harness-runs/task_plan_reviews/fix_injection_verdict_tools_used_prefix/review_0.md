# Task plan review — round 0

verdict: FAIL
review_mode: full

## Must Fix
1. **`task_3_plan.md` — the byte-comparison verification fails even when the two files are byte-identical**
   The template is tracked as mode `100644` and `scripts/prompt-injection-screen.sh` as `100755` (`git ls-files -s`; `cli/src/generators/outerLoopScripts.ts` gives the written script mode `0o755`). `git diff --no-index` compares modes as well as content. Run on the tree as it stands, where both files have the same blob `1f4ab7c447bef91f6f2c6f3b9fe20e6bc707e0d9`, the command prints `old mode 100644` / `new mode 100755` and exits 1. So the bullet can never hold, and Task 3 must not restore it by changing a mode: the template has to stay `100644` and the adopted copy `100755`. The bullet's closing claim is also backwards, since the command reports the mode difference rather than confirming the mode is unchanged. The story index's second `Top risks:` entry relies on this check ("Task 3 guards it with a byte comparison").
   **Raised against:** `git diff --no-index --exit-code cli/templates/scripts/prompt-injection-screen.sh scripts/prompt-injection-screen.sh` prints nothing and exits 0, which also confirms the file mode is unchanged.
   **Must hold:** Task 3's verification passes exactly when the two files' contents are identical, whatever their differing modes, and it checks separately that `scripts/prompt-injection-screen.sh` keeps its committed mode. Every command it names can run under the unattended profile.
   **Class:** Wrong action from operative text
   **Failure:** If the `general` layer implementer runs Task 3's first `**Verification:**` command after a correct edit, then it prints a mode change and exits 1, so the task's check fails on correct work.
   **Fix:** In `task_3_plan.md`, replace the bullet with two checks. (a) `git diff --no-index --numstat cli/templates/scripts/prompt-injection-screen.sh scripts/prompt-injection-screen.sh` reports `0` added and `0` deleted lines; state that its exit status is 1 because the modes differ by design. (b) `git diff --summary HEAD -- scripts/prompt-injection-screen.sh` prints nothing, which shows no mode change. Both are `git diff` calls, which the unattended profile allows; `cmp` is not in `cli/templates/claude/settings.autonomous.json` → `permissions.allow`. Both were run on this tree: (a) printed `0	0` and (b) printed nothing.

## Nice to Have
- `task_1_plan.md`, **The contract Tasks 2, 3 and 4 rely on.**: "A tools-used line anywhere after the frame leaves the result wrapped" is not true of an indented line inside the reply, which is unwrapped and then refused by the parse, as the task's own fourth Work bullet says. The outcome, `malformed-verdict`, is the same either way.
