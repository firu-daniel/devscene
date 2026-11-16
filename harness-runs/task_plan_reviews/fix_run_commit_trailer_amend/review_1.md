# Task plan review — round 1

verdict: PASS
review_mode: full

## Should Fix

- **`task_4_plan.md`, and the story index `## Scope register` row 16: the shared-library paragraph of `plugin/hooks/README.md` goes stale.** `plugin/hooks/README.md` → the `hc_piece_is_never_safe` paragraph says *"It owns one **refusal** on the same terms"* and *"all four of those guards call it before every other test"*. After Task 4, the function owns a second refusal (the `commit` arm). It also has a fifth caller, `git-commit-branch-guard.sh`, which is not an allow-only guard. Task 4's `### Targets` and register row 16 name only the outcome-table row. Its last Work bullet reaches the callers list only conditionally (*"If the README names the callers … anywhere"*), and nothing reaches *"one refusal"*. Name that paragraph in Task 4's targets and in row 16 as `change`.
- **`task_4_plan.md` / `task_6_plan.md`, and the story index `## Scope register` row 21: recorded commit-guard decisions that Task 4 silences are neither superseded nor named.** `docs/guard-verification.md` → `### 3.1 Narrowed — \`allow\` → SILENT` records several commit-guard shapes as `allow`:
  - **WK2:** `git commit -m "a & b"`. Its split fragment `b"` is a non-git piece, which Task 4's remit test refuses.
  - **WK4:** `git commit -m x 2>&1`. It carries a `>`.
  - **W10–W12, WK5 and WK6:** `rm -r-f <dir> & git commit -m x`, `ls & git commit -m x`, `bash /tmp/<script>.sh && git commit -m x`.

  Under Task 4's rules every one of these becomes SILENT on an ordinary branch. Row 21's reason tests only whether a row *"carries `--amend`"*, which is the wrong test for a change that also narrows on pipes, redirections and non-git pieces. Task 4's contract table and Task 6's sixteen recorded payloads cover `| cat` but not a descriptor duplication or a quoted separator. Two fixes:
  - Add at least the `2>&1` and the quoted-`&` shapes to Task 4's table and to Task 6's recorded rows, or state that the descriptor-duplication cost is accepted.
  - Have Task 6's new subsection name the earlier `allow` rows it supersedes.
- **`task_6_plan.md`: the guard change's per-call cost is left unrecorded.** `.claude/context/plugin.md` → *"A change to any guard or to the library re-measures itself in `docs/guard-verification.md`, which is where the per-Bash-call cost and the cross-guard matrices live"*. Task 4 makes the commit guard walk and judge **every** piece of every payload carrying `commit`, where it used to stop at the first commit piece. Task 6 is right not to retake §1.2 in-run (`harness-runs/lessons.md` → *Evidence and measurement*, the wall-clock rule). It should still record that §1.2 is `owed` for this change, so the latency table is not read as covering the new walk. This is carried from round 0.
- **`task_1_plan.md`: `.git/packed-refs` is given `bubblewrapDenyWrite: true` while its presence rests on a derivation.** `docs/cli.md` → **Everything that runs outside the sandbox is write-protected on both sides** records that an exact entry for an absent path mounts a placeholder that *"reads as `/dev/null`"*, and that this made git in the run copy exit 128 for `commondir` (F9). That is the reason the trio is `omit`. Task 1 keeps `packed-refs` at `deny` on the claim that *"`packed-refs` exists in every clone `git clone` wrote refs into"*. The run copy is made by `hr_clone_create_var` (`git clone --shared --no-checkout --template= --no-tags`), which also prunes remote refs (*WHY ONLY THOSE REMOTE REFS*). State in Task 1 why `packed-refs` survives that pruning, or make CS16 (Linux) a stated precondition before the row's rendered claim is relied on. The story index's `Top risks:` already names the risk; the task file should carry the derivation it rests on.

## Nice to Have

- `task_6_plan.md` → `**Verification:**`: the last two bullets have run together on one line (*"…none claims a decision that was not driven.- No citation added…"*).
- Story index `## Context`: the **What this branch does not change.** paragraph and the `**Top risks:**` heading have no blank line between them, so they render as one paragraph.
