# Architecture review — `feat_init_upgrade`

## Context

Branch `feat_init_upgrade`, reviewed 2026-11-18 against the diff base `dev`. This run copy has no local `dev`, so the base resolved to `origin/dev`, the only ref of that name (merge base `e63fb5f2`, 27 commits ahead, none behind). The review covered the `cli`, `plugin` and `general` hunks of the branch against `.claude/context/cli.md`, `.claude/context/plugin.md`, `.claude/context/conventions.md` and the lessons ledger. 35 run-artifact files excluded from the reviewed diff.

The layering holds. The new `cli/src/upgrade/` area sits above `generators/`, `core/` and `machine/`, and imports `commands/registry.ts` type-only. Every write goes through one `WritePlan`, the new policy lives in `core/writer.ts`, the git probe lives in `core/git.ts`, and no import crosses between `cli/` and `plugin/`. The three Must Fix findings are second copies of something that already has an owner. Two Should Fix findings cover one single-caller grading placed on the shared floor and one adopter-facing command spelling.

## Phase 2 Readiness — Ordered Fix List

1. [x] **Finding 1** — Use the shared stringsAt instead of a private copy in the permission profile _(layer: cli)_
2. [ ] **Finding 2** — Give the two lstatOrUndefined copies one owner in core _(layer: cli)_
3. [ ] **Finding 3** — Resolve daemon-loaded script paths through the outer-loop table's owner _(layer: cli)_
4. [ ] **Finding 4** — Print the upgrade report's commands with the npx prefix _(layer: cli)_
5. [ ] **Finding 5** — Move the upgrade refusal's run grading out of core _(layer: cli)_

## Must Fix

### 1. Use the shared stringsAt instead of a private copy in the permission profile
→ [finding_1.md](feat_init_upgrade_arch_review/finding_1.md)

### 2. Give the two lstatOrUndefined copies one owner in core
→ [finding_2.md](feat_init_upgrade_arch_review/finding_2.md)

### 3. Resolve daemon-loaded script paths through the outer-loop table's owner
→ [finding_3.md](feat_init_upgrade_arch_review/finding_3.md)

## Should Fix

### 4. Print the upgrade report's commands with the npx prefix
→ [finding_4.md](feat_init_upgrade_arch_review/finding_4.md)

### 5. Move the upgrade refusal's run grading out of core
→ [finding_5.md](feat_init_upgrade_arch_review/finding_5.md)

## Nice to Have

None.
