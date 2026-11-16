### Task 4 — Stop every plugin guard from vouching for `git commit --amend`, or for a commit compounded with a ref move

**Goal:** Make sure no harness guard emits `allow` for a command in which **any** piece rewrites a commit or moves a branch ref: an amend in any commit piece, not only the first, and a `reset`, `rebase`, `update-ref` or other git call riding beside a commit. A hook `allow` short-circuits the permission system and covers the **whole command** (`docs/guard-verification.md` row WK30), so without this the profile's new `Bash(git commit --amend:*)` deny and its `ask` entries for `git reset` and `git rebase`, which Task 2 relies on, would be bypassed by `git-commit-branch-guard.sh`'s own `allow` on an ordinary branch.

**Depends on:** Task 2. That task removes `Bash(git commit:*)` from the profile's `allow` and adds `Bash(git commit --amend:*)` to its `deny`. With this guard silent, an unattended run's amend, or a commit compounded with a ref move, then matches nothing in `allow`, and `dontAsk` refuses it. Interactively, silence costs one ordinary permission prompt.

**The one rule this task keeps intact: the shared refusal withholds `allow`, and nothing else.** `git-commit-branch-guard.sh` is not an allow-only guard: it emits `allow`, `ask` or silence. Its header's **FAIL-CLOSED TABLE** and `plugin/hooks/README.md` → `## Fail closed — and what that means for an allow-only guard` give it `ask` on a protected branch, on a detached HEAD and on an unresolvable configuration within jurisdiction, and silence out of jurisdiction. Every one of those outcomes stays exactly as it is, for an amend as for any other commit. The new test runs only in the branch-is-not-protected arm (`hc_branch_is_protected` returning `1`), where it turns `emit allow` into silence.

**Where this layer stops.** Only the guard, its shared library and the hooks README change. Recording the guard's decisions in `docs/guard-verification.md` is **Task 6's**. Task 6 drives the decisions below and records them, so this file states them as the contract. `allow-safe-compounds.sh`'s prefix set (`hc_safe_prefixes`) is not changed: it carries no `commit`, `reset`, `rebase` or `update-ref` prefix, so it admits none of those.

| # | payload command | branch state of `<dir>` | `git-commit-branch-guard.sh` |
|---|---|---|---|
| 1 | `git -C <dir> commit -m x` | ordinary | `allow` (unchanged) |
| 2 | `git -C <dir> add f && git -C <dir> commit -m x` | ordinary | `allow` |
| 3 | `cd <dir> && git commit -m x` | ordinary | `allow` |
| 4 | `git -C <dir> commit --fixup=HEAD` | ordinary | `allow`: makes a new commit and rewrites nothing |
| 5 | `git -C <dir> commit --amend -m x` | ordinary | SILENT |
| 6 | `git -C <dir> commit --amen --no-edit` | ordinary | SILENT |
| 7 | `git -C <dir> commit "--amend" -m x` | ordinary | SILENT |
| 8 | `git -C <dir> commit $F -m x` | ordinary | SILENT |
| 9 | `git -C <dir> commit -m x && git -C <dir> commit --amend -m y` | ordinary | SILENT |
| 10 | `git -C <dir> commit -m x && git -C <dir> reset --hard HEAD~1` | ordinary | SILENT |
| 11 | `git -C <dir> commit -m x && git -C <dir> update-ref refs/heads/<b> HEAD~1` | ordinary | SILENT |
| 12 | `git -C <dir> commit -m x && git -C <dir> rebase HEAD~1` | ordinary | SILENT |
| 13 | `git -C <dir> commit -m x && bash ./x.sh` | ordinary | SILENT |
| 14 | `git -C <dir> commit -m x \| cat` | ordinary | SILENT |
| 15 | `git -C <dir> commit --amend -m x` | protected | `ask` (unchanged) |
| 16 | `git -C <dir> commit --amend -m x` | detached HEAD | `ask` (unchanged) |

### Targets

- `plugin/hooks/lib/harness-config-lib.sh` — `hc_piece_is_never_safe` and its header comment.
- `plugin/hooks/git-commit-branch-guard.sh` — its piece walk, its `allow` arm, its header, its **FAIL-CLOSED TABLE** and its REPRO block.
- `plugin/hooks/README.md` — the outcome-table row for `git-commit-branch-guard.sh`.

**Work:**

- [ ] `hc_piece_is_never_safe`: add a `commit` arm beside the `branch` one. For a piece whose `hc_git_piece_parts` subcommand is `commit`, return `0` (never safe) when:
  - the rest of the piece carries a `$` or a backtick anywhere, since an unexpanded token says nothing about the flag it will run; or
  - any token, with every quote character deleted as the `branch` arm deletes them, is a long option whose body is a non-empty prefix of `amend`. Git accepts any unambiguous abbreviation, so `--am`, `--ame`, `--amen` and `--amend` all rewrite. A stub ambiguous to git, such as `--a`, is refused too, and costs nothing because git rejects it without running.

  Return `1` for every other `commit` piece, `--fixup` and `--squash` included, since each makes a new commit. A `-m` message token that happens to read `--amend` is over-refused, which costs one prompt and is accepted. Keep the function free of shell options: the library sets none. The four allow-only guards already call it on every piece; none of them grants a `git commit` piece (it is not in `hc_safe_prefixes`), so the new arm changes none of their decisions.
- [ ] Library header above `hc_piece_is_never_safe`: extend **WHY IT EXISTS** and **IT JUDGES THE OPERATION** with the commit arm. An amend overwrites the branch tip with a rewritten commit, so in a run copy, outside the wrappers, it moves that copy's ref alone. The **KEEP THIS AND THE PROFILE'S `deny` ENTRIES IN STEP** note gains the profile's `Bash(git commit --amend:*)`. Change *"All four allow-only guards call it"* to say that `git-commit-branch-guard.sh` also calls it, on **every** piece, and that there it withholds only that guard's `allow` — the guard's own `ask` decisions come first and are not overridden.
- [ ] `git-commit-branch-guard.sh`, the piece walk and the `allow` arm:
  - The loop no longer `break`s at the first commit piece. It still records the **first** commit piece and its `-C` as `commit_piece` / `commit_dir`, so jurisdiction and the repository judged are resolved exactly as today, and it now judges **every** piece of `hc_split_command`'s output into one flag, `vouchable` (start `1`).
  - A piece clears `vouchable` when any of these holds: it carries a `|`, `<`, `>`, `$` or backtick (the splitter does not split on a pipe, so a second command can ride inside a piece); it is a git piece (`hc_git_piece_parts` succeeds) for which `hc_piece_is_never_safe` returns `0`; it is a git piece whose subcommand is outside this guard's remit — the remit is exactly `commit`, `add`, `status`, `diff`, `log`, `show`, `rev-parse` and `ls-files`, none of which moves a ref, so `reset`, `rebase`, `update-ref`, `symbolic-ref`, `checkout`, `switch`, `merge`, `pull`, `cherry-pick`, `revert`, `stash`, `branch`, `fetch`, `worktree`, `tag` and `push` all fall outside; or it is not a git piece and is not a leading `cd <dir>` (any other command, a script included, could move a ref).
  - In the `case $?` of `hc_branch_is_protected`, arm `1` only: when `vouchable` is `0`, exit `0` with no output **instead of** `emit allow`. Arms `0` and `*`, and the detached-HEAD branch above them, are untouched and still `ask` whatever the pieces are. Keep `set -u`, never `set -e`, and the at-most-one-JSON-object output.
  - Name the remit set once, in one place in the file, with a comment saying why it is a closed allowlist rather than a list of refused subcommands: a refused list is wrong again at the next ref-moving spelling.
- [ ] `git-commit-branch-guard.sh` header:
  - The opening paragraph: the guard auto-allows a commit on an ordinary branch only when **every** piece of the command is within its remit and none rewrites a commit; otherwise it stays silent there. Add one paragraph explaining why — its `allow` covers the whole compound and short-circuits the profile's `deny` and `ask` entries (WK30).
  - **FAIL-CLOSED TABLE**: keep the detached / protected / unresolvable `ask` rows and the two SILENT rows exactly. Replace *"anything else -> allow"* with two rows: *"ordinary branch, and any piece rewrites a commit (`--amend` in any abbreviation, or an unexpanded token), is a git call outside the remit, is a non-git command other than a leading `cd`, or carries a pipe, redirection or substitution -> SILENT"*, then *"anything else (ordinary branch) -> allow"*.
  - REPRO: add rows 5, 9 and 10 of the contract table as `printf '{"tool_input":{"command":"…"},"cwd":"<dir>"}' | bash plugin/hooks/git-commit-branch-guard.sh` lines, each with its expectation worded *on an ordinary branch: no output, exit 0; on a protected branch or a detached HEAD: `ask`, unchanged*.
- [ ] `plugin/hooks/README.md`, the outcome-table row for `git-commit-branch-guard.sh`: say that on an ordinary branch it allows only when every piece of the command is within its remit and none rewrites a commit (`--amend`), and is otherwise silent there; and that on a protected branch, a detached HEAD or an unresolvable configuration it still asks, amend or not. Leave the row's `allow`, `ask` or silence column, the `## Fail closed` table row (*`ask`, with a reason naming the unresolvable configuration*) and the jq paragraph's *"`git-commit-branch-guard.sh` asks on every commit"* unchanged, since this task changes none of them. If the README names the callers of `hc_piece_is_never_safe` anywhere, add this guard to that list with the same *withholds only its `allow`* qualifier.

**Verification:**

- Run the guard's REPRO block, the new lines included, against a throwaway `git init` fixture under the system temp directory that carries a `devscene.config.json` and two branches (one ordinary, one in the protected set), per `.claude/context/plugin.md` → `## Verifying a change in this layer`. Every row of the contract table above answers as stated: `allow` for rows 1–4, no output for rows 5–14, and `ask` for rows 15 and 16.
- The unresolvable-configuration case (invalid JSON in the fixture's config) still answers `ask` for `git -C <dir> commit --amend -m x`, and a fixture with no `devscene.config.json` still answers nothing.
- `hc_piece_is_never_safe` still refuses `git branch -D x` and still permits `git branch --show-current` on the same fixture. The `branch` arm is unchanged.
- `bash scripts/typecheck.sh` exits 0.
