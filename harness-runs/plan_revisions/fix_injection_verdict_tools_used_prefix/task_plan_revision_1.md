# Revision note — round 1
- task-plan 1 (harness-runs/task_plan_reviews/fix_injection_verdict_tools_used_prefix/review_0.md) — files: task_plans/fix_injection_verdict_tools_used_prefix/task_3_plan.md, story_plans/fix_injection_verdict_tools_used_prefix_story_plan.md — resolved
Unrequested changes: none

How it was resolved:

- **task-plan 1.** Task 3's single `git diff --no-index --exit-code` check is now two checks. `git diff --no-index --numstat` must report `0` added and `0` deleted lines, and the bullet says its exit status of 1 is expected because the modes differ by design. `git diff --summary HEAD --` on the adopted copy must print nothing while the edit is uncommitted. Both were run on this tree and in a scratch repository: differing content reports non-zero counts, and a changed mode prints a `mode change` line. The story index's second `Top risks:` entry, which the finding names as relying on the old check, now describes the two checks. The target set is unchanged, so the scope register was not re-derived.
