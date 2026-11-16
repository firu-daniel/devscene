# Code review — feat_committer_as_script

Branch `feat_committer_as_script`, reviewed 2026-11-16 against its merge base with `dev`. The run copy has no local `dev` branch, so the base was `origin/dev`. **Scope:** 118 changed files, in five segments:

- The new `cli/templates/scripts/lib/unit-commit-lib.sh` and the `--unit` / `--artifact` / `--push` front end of `commit-on-branch.sh`.
- The planning-record library's move onto `ucl_artifact`, and the watcher's sourcing list.
- The new and edited `cli/test` suites, with the `treeGuards` registration of `test/commit-step-calls.test.mjs`.
- The plugin corpus's move from the `committer` agent to `<commit_call>` and literal `--artifact` calls.
- The re-rendered self-adopted `scripts/` and `harness-runs/*/README.md` copies, plus `docs/`, `ROADMAP.md` and `evals/`.

37 run-artifact files excluded from the reviewed diff.

**Headline conclusions:**

- **Verified:**
  - The self-adopted `scripts/` copies are byte-identical to their templates.
  - Every `--artifact` kind cited in `plugin/` exists in `ucl_artifact`'s table, with the flags its row needs.
  - Each artifact row's path set matches the paths the replaced prose staged, including the fix-plan and fix-plan-round suffixes.
  - Every readiness-entry shape in the samples and the writing agents (`**Task K**`, `**Finding K**`, `**Test K**`) is one `ucl_entry_find` resolves.
  - No `plugin/`, `cli/src` or `cli/templates` file still dispatches the deleted agent.
- **Tests:** every new behaviour has a suite (`unit-commit-lib.test.mjs`, `commit-on-branch-unit.test.mjs`, `commit-step-calls.test.mjs`, `planning-subjects-drift.test.mjs`).
- **Not done:** no test was run in this review.
- **Parity:** off (`phases.parity: false`).
- **Pass 0:** the grep sweep list is empty, so only the new-export caller check ran. It found no un-wired symbol.
- **Pass 2:** no-op. The per-unit findings root does not exist, because per-unit review was off.

One gating finding: the stage set refuses a top-level deletion, and silently drops a deletion whose parent directory is gone.

## Phase 2 Readiness — Ordered Fix List

1. [x] **Finding 2** — `OUTER_LOOP_SCRIPTS` comment names only one sourcer of `unit-commit-lib.sh` _(layer: cli)_
2. [x] **Finding 1** — A deletion at the repository top is refused, and one whose parent directory is gone is never committed _(layer: cli, general)_

## Must Fix

### 1. A unit's deletion at the repository top is refused, and one whose parent directory is gone is never committed
→ [finding_1.md](feat_committer_as_script_code_review/finding_1.md)

## Should Fix

_None._

## Nice to Have

### 2. The `OUTER_LOOP_SCRIPTS` comment names only one sourcer of `unit-commit-lib.sh`
→ [finding_2.md](feat_committer_as_script_code_review/finding_2.md)

## Out of scope / verified-OK (intentional divergences / call-outs)

_None. `phases.parity` is `false`, so there is no reference implementation to diverge from._
