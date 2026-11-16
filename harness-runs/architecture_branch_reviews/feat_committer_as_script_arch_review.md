# Architecture review — feat_committer_as_script

## Context

Branch `feat_committer_as_script`, reviewed 2026-11-16, against the merge base with `dev`. The checkout has no local `dev` branch, so the base was taken from `origin/dev`. The review covers 112 changed files. 35 run-artifact files were left out of the reviewed diff. The changes fall into five groups:

- **The new front end.** `cli/templates/scripts/commit-on-branch.sh` gains a `--unit` / `--artifact` front end, and a new sourced library, `cli/templates/scripts/lib/unit-commit-lib.sh`, comes with it. The library has its `OUTER_LOOP_SCRIPTS` row in `cli/src/generators/outerLoopScripts.ts`.
- **New `cli/test` suites.** The new suites build their fixtures under the system temp directory.
- **The plugin rewrite.** `plugin/agents/committer.md` is deleted. The `<committer_push>` binding becomes `<commit_call>`, and every commit point now makes one literal wrapper call.
- **Self-adopted copies.** This repository's own copies are re-rendered: `scripts/` is byte-identical to `cli/templates/scripts/`, and `harness-runs/*/README.md` is re-rendered too.
- **Prose re-pointing.** `docs/`, `ROADMAP.md` and `evals/` now point at the commit step.

**Headline: the layering holds.** The specific checks:

- **Shell code.** The new library sits in the `cli` layer's `scripts/` template home under `lib/`, and it sets no shell option. Its only caller sources it from `${BASH_SOURCE[0]}` next to `lib/harness-run-lib.sh`, and the wrapper takes every configuration and repository answer from that shared library rather than working it out again.
- **Plugin cores.** The cores use `<commit_call>` only as a binding. `<MAIN_REPO>` and `--push` are spelled only in forks and in the family-neutral `dispatch_discipline_instructions.md`, whose literal call was already there.
- **Stale references.** No plugin, `cli/src` or `cli/templates` file still dispatches or cites the deleted agent.

There is one non-gating finding: the planning driver's library and the new library now each declare the same fixed artifact subjects and path sets.

The conventions documents still cite `plugin/agents/committer.md` (five citations in `.claude/context/plugin.md`, two in `.claude/context/conventions.md`). The plan deliberately sends these to `## Corpus staleness`, so they are not raised here.

## Phase 2 Readiness — Ordered Fix List

1. [ ] **Finding 1** — Planning-record library re-declares the artifact table's subjects and path sets _(layer: cli, general)_

## Should Fix

### 1. Planning-record library re-declares the artifact table's subjects and path sets
→ [finding_1.md](feat_committer_as_script_arch_review/finding_1.md)
