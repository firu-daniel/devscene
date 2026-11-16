### 1. The commit guard re-derives the ride-along answer the shared library owns

**Site:** `plugin/hooks/git-commit-branch-guard.sh`, in the piece walk: the new `remit=" commit add status diff log show rev-parse ls-files "` set, the per-piece `case "$piece" in *'|'*|*'<'*|*'>'*|*'$'*|*'`'*) vouchable=0` scan, and the `cd\ *)` arm (`d=${p#cd }` … `[ "$idx" -eq 1 ] && [ -n "$d" ] && [ "${d#* }" = "$d" ] || vouchable=0`) that together compute `vouchable`.

**Rule violated.**

- `.claude/context/conventions.md` → `### Where a new responsibility goes`: *"`plugin/hooks/lib/harness-config-lib.sh` is the only place **any** shell asset in `plugin/` resolves the repository it is judging, … or builds its safe-prefix set (`hc_safe_prefixes`)"*, and *"A responsibility that already has a home does not get a second one."*
- `.claude/context/plugin.md` → `## Guards, the shared library and the helper scripts`: *"A guard never re-derives a shared answer. … No two guards may apply a different definition of the workspace, and a guard that needs a second copy of one needs the library to grow instead."*

**The problem.** Before this branch the commit guard judged only the commit piece. It now also decides whether every *other* piece of the compound may ride along on its `allow`. That is the same question the four allow-only guards answer, and each of them answers it only through the library: `hc_safe_prefixes`, `hc_path_anchored_patterns` / `hc_matches_any_pattern` (the `cd <dir>` arm with its veto globs) and `hc_piece_is_never_safe`. You can see this in `allow-safe-compounds.sh`, `git-rewrite-branch-guard.sh`, `autonomous-script-allowlist-guard.sh` and `allow-qa-credentials-read.sh`, the `safe_prefixes=$(hc_safe_prefixes "$top")` / `hc_matches_any_pattern "$piece" "$path_anchored_patterns"` call sites. The commit guard calls only the last of those three, and it builds its own versions of the other two in its own body:

- **A second safe set.** The guard defines a private closed list of git subcommands that may ride along, which is a second safe-prefix set that the library does not know about.
- **A second `cd` acceptance.** The guard accepts a leading `cd` of any single-word directory. It applies no workspace test and none of the library's veto globs (`/../`, a trailing `/..`, characters outside `[A-Za-z0-9._/-]`). So the commit guard and the other guards now define a vouchable leading `cd` differently.
- **A third copy of the composition scan.** The guard carries its own composition-grammar scan, alongside the one `autonomous-script-allowlist-guard.sh` already carries.

A closed allowlist narrower than `hc_safe_prefixes` is a legitimate choice for this guard. Making it in the guard's body leaves it outside the library, though, where `KEEP THIS AND THE PROFILE'S deny ENTRIES IN STEP` and the README's `## The shared library` contract cannot see it. The next change to the shared answer would then drift from it silently.

**Fix.**

1. In `plugin/hooks/lib/harness-config-lib.sh`, add one function next to `hc_piece_is_never_safe`, for example `hc_commit_piece_may_ride_along <piece> <position>`. It owns:
   - the closed commit-remit subcommand set (`commit add status diff log show rev-parse ls-files`), parsed through `hc_git_piece_parts`;
   - the pipe / redirection / substitution scan;
   - the leading-`cd` acceptance, decided through `hc_path_anchored_patterns` and `hc_matches_any_pattern` rather than through a bare single-word test, so that the `cd` arm and its vetoes are the library's;
   - the `hc_piece_is_never_safe` call.
   
   Its header comment should state why the set is a closed allowlist ("none of these moves a ref") and why it is narrower than `hc_safe_prefixes`.
2. In `plugin/hooks/git-commit-branch-guard.sh`, replace the `remit` variable, the inline `case "$piece"` scan and the `cd\ *)` arm with one call per piece to that function, which sets `vouchable=0` when it returns non-zero. Keep the `[ "$vouchable" -eq 1 ] || exit 0` gate on the ordinary-branch arm only, so every `ask` decision is unchanged.
3. Update the guard's header FAIL-CLOSED row and `plugin/hooks/README.md` → `## The shared library` so they name the new library function as the owner of the commit guard's ride-along answer.
4. Because this is a change to a guard and to the library, re-drive the existing CG1–CG16 rows in `docs/guard-verification.md` → `#### The commit guard's amend and remit rows (fix_run_commit_trailer_amend)` against the moved code (`.claude/context/plugin.md` → *"A change to any guard or to the library re-measures itself in `docs/guard-verification.md`"*). Add a row for a leading `cd` whose operand the library's vetoes withdraw.
