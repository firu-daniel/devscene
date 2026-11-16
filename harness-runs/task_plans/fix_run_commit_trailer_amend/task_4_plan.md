### Task 4 — Stop every plugin guard from vouching for `git commit --amend`

**Goal:** Make sure no harness guard emits `allow` for a `git commit` that rewrites the branch tip. A hook `allow` short-circuits the permission system (`docs/guard-verification.md` row WK30), so without this the profile's new `Bash(git commit --amend:*)` deny, which comes from Task 1, would be bypassed by `git-commit-branch-guard.sh`'s own `allow` on an ordinary branch.

**Depends on:** Task 1. That task removes `Bash(git commit:*)` from the profile's `allow` and adds `Bash(git commit --amend:*)` to its `deny`. With this guard silent, an unattended run's amend then matches only that deny and nothing in `allow`, and `dontAsk` refuses it. Interactively, silence costs one ordinary permission prompt.

**Where this layer stops.** Only the guard and its shared library change. Recording the guard's decisions in `docs/guard-verification.md` is **Task 7's**. Task 7 drives the decisions below and records them, so this file states them as the contract:

| payload command (`<dir>` on an ordinary branch) | `git-commit-branch-guard.sh` |
|---|---|
| `git -C <dir> commit -m x` | `allow` (unchanged) |
| `git -C <dir> commit --amend -m x` | SILENT |
| `git -C <dir> commit --amen --no-edit` | SILENT |
| `git -C <dir> commit "--amend" -m x` | SILENT |
| `git -C <dir> commit $F -m x` | SILENT |
| `git -C <dir> commit --fixup=HEAD` | `allow`: makes a new commit and rewrites nothing |

### Targets

- `plugin/hooks/lib/harness-config-lib.sh` — `hc_piece_is_never_safe` and its header comment.
- `plugin/hooks/git-commit-branch-guard.sh` — its decision, its header's FAIL-CLOSED table and its REPRO block.
- `plugin/hooks/README.md` — the outcome-table row for `git-commit-branch-guard.sh`.

**Work:**

- [ ] `hc_piece_is_never_safe`: add a `commit` arm beside the `branch` one. For a piece whose `hc_git_piece_parts` subcommand is `commit`, return `0` (never safe) when:
  - the rest of the piece carries a `$` or a backtick anywhere, since an unexpanded token says nothing about the flag it will run; or
  - any token, with every quote character deleted as the `branch` arm deletes them, is a long option whose body is a non-empty prefix of `amend`. Git accepts any unambiguous abbreviation, so `--am`, `--ame`, `--amen` and `--amend` all rewrite. A stub ambiguous to git, such as `--a`, is refused too, and costs nothing because git rejects it without running.

  Return `1` for every other `commit` piece, `--fixup` and `--squash` included, since each makes a new commit. A `-m` message token that happens to read `--amend` is over-refused, which costs one prompt and is accepted. Keep the function free of shell options: the library sets none.
- [ ] Library header above `hc_piece_is_never_safe`: extend **WHY IT EXISTS** and **IT JUDGES THE OPERATION** with the commit arm. An amend overwrites the branch tip with a rewritten commit, so in a run copy, outside the wrappers, it moves that copy's ref alone. The **KEEP THIS AND THE PROFILE'S `deny` ENTRIES IN STEP** note gains the profile's `Bash(git commit --amend:*)`. Also state that `git-commit-branch-guard.sh` now calls the function on its commit piece, alongside the four allow-only guards.
- [ ] `git-commit-branch-guard.sh`: after the loop finds `commit_piece`, and before jurisdiction is resolved, run `hc_piece_is_never_safe "$commit_piece"`. On `0`, exit `0` with no output. Add a row to the header's **FAIL-CLOSED TABLE**, *"a commit piece that rewrites the tip (`--amend`, any abbreviation) or carries an unexpanded token -> SILENT"*. Add a REPRO line, `printf '{"tool_input":{"command":"git -C <dir> commit --amend -m x"},"cwd":"<dir>"}' | bash plugin/hooks/git-commit-branch-guard.sh`, with the expected outcome *no output, exit 0, on any branch*. Keep `set -u`, never `set -e`, and the at-most-one-JSON-object output.
- [ ] `plugin/hooks/README.md`: in the outcome table, extend the `git-commit-branch-guard.sh` row to say it stays silent on a commit that rewrites the tip (`--amend`), whatever the branch. If the README names the callers of `hc_piece_is_never_safe` anywhere, add this guard to that list.

**Verification:**

- Run the guard's REPRO block, the new amend line included, against a throwaway `git init` fixture under the system temp directory that carries a `devscene.config.json` and two branches, per `.claude/context/plugin.md` → `## Verifying a change in this layer`. Each row of the contract table above answers as stated: `allow` for the plain commit and for `--fixup`, and no output for the four rewrite or unexpanded rows.
- `hc_piece_is_never_safe` still refuses `git branch -D x` and still permits `git branch --show-current` on the same fixture. The `branch` arm is unchanged.
- `bash scripts/typecheck.sh` exits 0.
