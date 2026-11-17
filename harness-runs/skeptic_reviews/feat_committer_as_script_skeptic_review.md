# Skeptic review — feat_committer_as_script

## Context

Branch `feat_committer_as_script`, reviewed 2026-11-16. The base was the merge base with `origin/dev`, because the run copy has no local `dev` branch.

**What was reviewed.** The whole-branch diff, read adversarially. 42 run-artifact files were excluded from the reviewed diff. The review covered:

- the new `cli/templates/scripts/lib/unit-commit-lib.sh`;
- the `--unit` / `--artifact` / `--push` front end of `commit-on-branch.sh`, read end to end from argument parse to `fe_return`, including Finding 1's absent-path removal arm;
- the planning-record library's move onto `ucl_artifact`, and the watcher's library list;
- the plugin corpus's move from the `committer` agent to `<commit_call>` and the `--artifact` calls;
- the deleted `plugin/agents/committer.md` (read from `origin/dev`), as the behaviour the new step must preserve.

**De-duplicated against:**

- `harness-runs/code_reviews/feat_committer_as_script_code_review.md` and its two findings;
- `harness-runs/architecture_branch_reviews/feat_committer_as_script_arch_review.md` and its one finding.

There is no parity review, because `phases.parity` is `false`. The planning rounds' `## Incidental findings (not gating)` sections yielded no leads.

**Checks run:**

- **Wiring.** `unit-commit-lib.sh` is in `OUTER_LOOP_SCRIPTS`, is sourced by the wrapper, and is in the watcher's `PLANNING_DRIVER_LIBS` ahead of `planning-record-lib`. Every `ucl_*` function has a caller.
- **Citations.** Every `<scripts_dir>/commit-on-branch.sh` → header citation in `plugin/`, `docs/` and `cli/templates/` was checked against the wrapper's header paragraphs.
- **Runtime behaviour.** The tick-then-restore ordering, the exit-3 path and the landed-exit-1 re-sync were traced, along with:
  - the push failure-line patterns, against `push-branch.sh`'s actual messages;
  - the ledger entry-id charset, against every ledger in `harness-runs/flow_progress/`;
  - the subject and record readers in `statistics-plan-writer.md` and `improvement_observations_instructions.md`.

**Headline.** The front end and the library hold up under these checks. There is one net-new finding: code-review Finding 1's fix renamed the wrapper header `STAGING POLICY, AND THE ONE TRAP IN IT` to `STAGING POLICY`, and two plugin instruction files still cite the old title.

## Phase 2 Readiness — Ordered Fix List

1. [x] **Finding 1** — Two plugin instructions cite the renamed wrapper header `STAGING POLICY, AND THE ONE TRAP IN IT` _(layer: plugin)_

## Must Fix

### 1. Two plugin instructions cite the wrapper header `STAGING POLICY, AND THE ONE TRAP IN IT`, which the code-review fix renamed
→ [finding_1.md](feat_committer_as_script_skeptic_review/finding_1.md)

## Should Fix

_None._

## Nice to Have

_None._

## Out of scope / verified-OK (intentional divergences / call-outs)

`--push` also runs after exit 3, where the deleted committer pushed only after a commit landed. The story plan's `## Context` → **`--push`** settles this, and it is harmless: `push-branch.sh` only fast-forwards commits that already landed. It is not a fix item.
