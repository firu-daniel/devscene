### 1. Planning-record library re-declares the artifact table's subjects and path sets

**Severity:** Should Fix (non-gating)

**Sites:**
- `cli/templates/scripts/lib/planning-record-lib.sh`:
  - `prl_round_commit`: `prl_commit "chore: Plan round $1 for $PRL_BRANCH"`
  - `prl_partial_commit`: `prl_commit "chore: Plan round $1 partial for $PRL_BRANCH"`
  - `prl_convergence_commits`: `prl_commit "chore: Add UI-test plan for $b"` and `prl_commit "chore: Add task plan for $b" …`, with their path lists
  - `prl_ledger_flip`: `prl_commit "chore: Flow progress $id for $PRL_BRANCH" "$rel"`
  - The `chore: Log improvement observations for $PRL_BRANCH` commit
- The self-adopted copy at `scripts/lib/planning-record-lib.sh`, which is byte-identical.
- The other declaration of the same strings: `cli/templates/scripts/lib/unit-commit-lib.sh` → `ucl_artifact`. Its own comment calls it *"The single declaration of every artifact kind's subject and path set."*

**Problem.** This branch adds `ucl_artifact` as the table that declares each artifact kind's commit subject and path set: `task-plan`, `plan-round`, `plan-round-partial`, `ui-test-plan`, `ledger-flip`, `improvement-observations`, and the rest. The planning driver's library already held six of those subjects, plus the matching path sets, as hardcoded literals, and it keeps them. So the repository now declares one responsibility, the fixed artifact subjects and their staged path sets, in two places. Two documents disagree with that:

- The new library's header says `ucl_artifact` is "the single declaration". The same header also admits that `prl_round_commit`, `prl_partial_commit` and `prl_convergence_commits` "hardcode the same strings", so the header contradicts itself.
- `planning-record-lib.sh`'s rewritten header says its subjects are "held equal" to the table by a drift test. That means it knows it is a second copy.

The rule this conflicts with is `.claude/context/conventions.md` → `### Where a new responsibility goes`: *"A responsibility that already has a home does not get a second one"* and *"Before adding a copy of anything, grep for it"*. That section points to `cli/src/core/repoPaths.ts` as the cost of drifted copies. `.claude/context/cli.md` → `## How a module in this layer is written` → **One string, one producer** says the same for this layer: a shipped table is "read rather than copied".

`cli/test/planning-subjects-drift.test.mjs` detects drift between the copies, but it does not remove the second owner. A path added to one kind's set in `ucl_artifact`, such as the `task-plan` set's `ui_test_plan_reviews/<branch>/`, has to be copied by hand into `prl_convergence_commits`, or the test fails.

This is graded Should Fix rather than Must Fix for two reasons. The conventions documents' list of stated monopolies does not name the artifact table. And the drift test closes the silent-drift risk.

**Fix.** Make `planning-record-lib.sh` read the subjects and path sets from `ucl_artifact`, and stop spelling them itself. It still commits through `prl_commit`'s plain form and its own `push-branch.sh` call; only the subjects and paths move.

1. In `cli/templates/scripts/lib/planning-record-lib.sh`, state in the header that the caller sources `lib/unit-commit-lib.sh` beside `lib/harness-run-lib.sh`. Then make the planning driver (`cli/templates/scripts/lib/planning-driver-lib.sh`, or whichever file sources `planning-record-lib.sh`) source `unit-commit-lib.sh` from the same `${BASH_SOURCE[0]}`-derived `lib/` directory. The `unit-commit-lib.sh` header already names "the script-driven driver" as a future caller.
2. Rewrite the five call sites to get each subject and path set from the table, then pass them to `prl_commit`:
   - `prl_round_commit`: `ucl_artifact plan-round "$PRL_STATE_DIR" "$PRL_BRANCH" "$1" '' ''`, then `prl_commit "$UCL_SUBJECT" "${UCL_PATHS[@]}"`.
   - `prl_partial_commit`: the same with `plan-round-partial`.
   - `prl_convergence_commits`: `ui-test-plan`, then `task-plan`.
   - `prl_ledger_flip`: `ledger-flip`, with `<entry>` set to the id.
   - The improvement-observations commit: its kind.

   Delete the hardcoded strings and path lists, and `prl_round_paths` if nothing else uses it. A non-zero return from `ucl_artifact` is a `prl_fail` with return 2.
3. Update both headers. `unit-commit-lib.sh`'s artifact-table paragraph should no longer say that `planning-record-lib.sh` hardcodes the same strings. `planning-record-lib.sh` should say it reads the table rather than holding values equal to it.
4. Repoint `cli/test/planning-subjects-drift.test.mjs`. Its header's rule should become that the planning driver's commits carry `ucl_artifact`'s subject and path set. Alternatively, delete the suite if the behavioural planning-driver suites already cover these commits; if you delete it, also remove any `treeGuards` entry that names it.
5. Re-render the self-adopted copies so that `scripts/lib/planning-record-lib.sh` and `scripts/lib/unit-commit-lib.sh` stay byte-identical to their templates, as Task 24 did.
