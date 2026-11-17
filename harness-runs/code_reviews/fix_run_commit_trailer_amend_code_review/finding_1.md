### 1. The commit guard lets a commit into a different repository ride along on its `allow`

**Site:** `plugin/hooks/lib/harness-config-lib.sh` → `hc_commit_piece_may_ride_along`, the git-piece path after `hc_git_piece_parts "$p"` succeeds (`case " commit add status diff log show rev-parse ls-files " in` … `hc_piece_is_never_safe "$p" && return 1`). The caller is `plugin/hooks/git-commit-branch-guard.sh`, in the `1)` arm of `case $?` after `hc_branch_is_protected` (`hc_commit_piece_may_ride_along "$root" "$piece" "$idx" || vouchable=0`).

**The problem.** The guard resolves `root` from the **first** `commit` piece only, then asks the library whether every piece may ride along on its `allow`. For a git piece, the library checks only the subcommand (against the closed remit set) and `hc_piece_is_never_safe`. It never checks **which repository that piece runs in**. So a second `git -C <other> commit`, or a `git -C <other> add`, rides along on an `allow` that judged a different repository. That holds even when `<other>` is on a protected branch, where this guard's own contract is to `ask`.

Driven on 2026-11-16 by this review, using `/bin/bash` and a throwaway fixture under the system temp directory. The fixture held two repositories, both configured from `examples/devscene.config.json`: `<O>` on the ordinary branch `feat_probe`, and `<P>` on `main`, which is protected. The payload `cwd` was `<O>`. "before" is `origin/dev`'s `plugin/hooks` and "after" is `HEAD`'s.

| Payload command | before | after |
|---|---|---|
| `git -C <O> commit -m x && git -C <P> commit -m y` | allow | **allow** |
| `git -C <O> commit -m x && git -C <P> add f` | allow | **allow** |
| `git -C <P> commit -m y` (alone) | ask | ask |
| `git -C <O> commit -m x && cd <P> && git commit -m y` | allow | silent |

The first row grants a commit onto protected `main` in `<P>` with no prompt. That is exactly what the guard header says it asks on (*"ask for confirmation when that branch is one the repository's own `devscene.config.json` protects"*). The hole is older than this branch. But this branch rewrote the guard to judge **every** piece, and its header, FAIL-CLOSED table and README row now claim that every piece is within the guard's remit before it allows. A piece in another repository is not within that remit. The precedent for closing this already exists: `plugin/hooks/git-rewrite-branch-guard.sh` grants a `git mv`/`git rm` piece only when the piece rebuilds from its parts and its own `-C` is absolute and resolves to the repository the guard judged (the `"git -C $HC_GIT_DIR $HC_GIT_REST"` case, then `hc_repo_root "$HC_GIT_DIR"` = `$top`). Rebuilding the piece also refuses `--git-dir=`, `--work-tree=` and `-c core.worktree=`, which `hc_git_piece_parts` steps over without reporting.

**Fix.**

1. In `plugin/hooks/lib/harness-config-lib.sh`, give `hc_commit_piece_may_ride_along` a fourth parameter, `<bare_root>`: the repository a git piece with no `-C` runs in. Change its first line to:
   ```sh
   local root="${1-}" piece="${2-}" position="${3-}" bare_root="${4-}" p patterns
   ```
   Then replace the last line, `return 0`, with:
   ```sh
   # The piece must run in the repository the guard judged: rebuilt from its two
   # parts (so `--git-dir=`, `--work-tree=` and `-c core.worktree=` spellings
   # are refused by construction, as in git-rewrite-branch-guard.sh), with an
   # absolute `-C` resolving to <root>, or no `-C` and <bare_root> equal to <root>.
   case "$p" in
     "git $HC_GIT_REST")
       [ -n "$bare_root" ] && [ "$bare_root" = "$root" ] || return 1
       ;;
     "git -C $HC_GIT_DIR $HC_GIT_REST"|"git -C \"$HC_GIT_DIR\" $HC_GIT_REST"|"git -C '$HC_GIT_DIR' $HC_GIT_REST")
       case "$HC_GIT_DIR" in
         /*) ;;
         *) return 1 ;;
       esac
       [ "$(hc_repo_root "$HC_GIT_DIR" 2>/dev/null)" = "$root" ] || return 1
       ;;
     *) return 1 ;;
   esac
   return 0
   ```
   Extend the function's header comment with one paragraph: a git piece rides along only when it runs in `<root>`, meaning an absolute `-C` resolving there, or no `-C` with `<bare_root>` equal to `<root>`, where `<bare_root>` is the repository of the leading `cd` or else the payload cwd. Any other global option, and a relative `-C`, is refused at one prompt, as `git-rewrite-branch-guard.sh` refuses them.
2. In `plugin/hooks/git-commit-branch-guard.sh`, inside the `1)` arm and before the `vouchable=1` line, compute `bare_root` from piece 1:
   ```sh
       first_piece=""
       while IFS= read -r piece; do first_piece="$piece"; break; done <<EOF
   $pieces
   EOF
       case "$(hc_clean_piece "$first_piece")" in
         cd\ *) bare_root=$(hc_resolve_repo_root "$first_piece" "$cwd") || bare_root="" ;;
         *) bare_root=$(hc_resolve_repo_root "" "$cwd") || bare_root="" ;;
       esac
   ```
   Then change the loop's call to `hc_commit_piece_may_ride_along "$root" "$piece" "$idx" "$bare_root" || vouchable=0`. Leave every `ask` arm unchanged.
3. In the guard's header **FAIL-CLOSED TABLE**, add to the SILENT row's list of `hc_commit_piece_may_ride_along` conditions: *"runs in a repository other than the one judged (its own absolute `-C`, else the leading `cd` or the payload cwd), or carries a git global option other than `-C`"*. In the **REPRO** block, add this line with the expectation *on an ordinary `<dir>` and a protected `<other>`: no output, exit 0*:
   ```
   printf '{"tool_input":{"command":"git -C <dir> commit -m x && git -C <other> commit -m y"},"cwd":"<dir>"}' \
     | bash plugin/hooks/git-commit-branch-guard.sh
   ```
4. In `plugin/hooks/README.md` → `## The shared library`, the paragraph beginning *"It owns the commit guard's **ride-along answer** as well"*: add *"a git piece rides along only when it runs in the repository the guard judged"* to the list of what `hc_commit_piece_may_ride_along` owns.
5. Verify by running the guard's REPRO block on a throwaway `git init` fixture under the system temp directory (`.claude/context/plugin.md` → `## Verifying a change in this layer`). The fixture needs a second repository on a protected branch for the new line. CG1–CG4 of `docs/guard-verification.md` → `#### The commit guard's amend and remit rows (fix_run_commit_trailer_amend)` must still answer `allow`. Recording the re-drive in that document is Finding 2.
