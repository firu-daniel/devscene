### 3. The hooks README's commit-guard row hides that a commit message's own prose now costs the `allow`

**Site:** `plugin/hooks/README.md`, the outcome-table row for `git-commit-branch-guard.sh` (*"Allows a `git commit` when the repository it names is on an ordinary branch, only when every piece of the command is within its remit and none rewrites a commit (`--amend`), and is otherwise silent there; …"*).

**The problem.** `hc_commit_piece_may_ride_along` refuses any raw piece carrying `|`, `<`, `>`, `$` or a backtick. The commit piece itself is one of those pieces, so the bytes of its **message** count. On an ordinary branch the guard used to allow the following, and is now silent on them. Measured 2026-11-16 by this review on a throwaway fixture, before = `origin/dev`, after = `HEAD`:

| Payload command | before | after |
|---|---|---|
| `git commit -m "$(cat <<'EOF'` … `EOF` `)"` (Claude Code's default commit spelling) | allow | silent |
| ``git commit -m "fix: use `foo` here"`` | allow | silent |
| `git commit -m "fix: handle <branch> names"` | allow | silent |

The `$` and backtick cases really are substitutions. The `<`/`>` case is prose. Either way, in an interactive session every such commit is now a prompt. The supervised flow makes exactly this kind of raw commit (`plugin/instructions/plan_orchestration_instructions.md`, step 6, *"create a dedicated git commit"*). The README states its reader as *"an adopter deciding whether to enable this plugin"*. Reading the row, that adopter concludes that a plain commit on an ordinary branch is still auto-allowed, and then meets a prompt the row never mentioned. The same table's `autonomous-script-allowlist-guard.sh` row discloses its own prose cost (*"class (ii) … fire on **prose in a wrapper's own arguments**"*). This row discloses none.

**Fix.** In that README row, after *"and is otherwise silent there;"*, insert:

> silent there too when any piece — the commit's own message included — carries a `$`, a backtick, `|`, `<` or `>`, so Claude Code's default `git commit -m "$(cat <<'EOF' … EOF)"` spelling and a subject naming a placeholder in angle brackets each cost one prompt, never a permit;

Leave the rest of the row, the `## Fail closed` table and the jq paragraph unchanged.
