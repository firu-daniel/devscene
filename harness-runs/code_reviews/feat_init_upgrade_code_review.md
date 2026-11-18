# Code Review: feat_init_upgrade

## Context

**Branch:** `feat_init_upgrade`
**Date:** 2026-11-18
**Reviewed:** the whole branch diff against `origin/dev` (this run copy has no local `dev`): 64 files, covering the `replace-if-changed` write policy, the local additions file and its protection, the profile and script upgrade planners, the run-registry and plugin-version readers, the `--upgrade` refusals, report and command, the three new `doctor` checks, and the templates, plugin contracts, documents and example that state the new route. 41 run-artifact files excluded from the reviewed diff.

**Conclusions.** The core design holds up on reading: atomic replacement, backups under the git common directory, the closed local-file key set, the carry-forward exclusion for local entries, and the job-surface and write-protection additions all do what the story index asks. Every new module and command change ships with tests. **Tests were not run by this review**; the Run gates phase establishes whether they pass. A throwaway-fixture run of the CLI was refused by the permission layer, so every finding rests on reading the code. **Pass 0 sweep:** 1 hit, 0 findings; the hit (`CLAUDE_CONFIG_DIR` at `cli/src/generators/permissionProfile.ts`) is a reworded doc comment, not a retyped name in code or a message. **New-export caller check:** every new exported value has a caller outside its defining file; `renderCurrentProfile`'s only callers are tests (Finding 7). **Parity:** `phases.parity` is `false`, so no parity review applies. **Planning leads:** the `--force`-wording note and both stale `permissionProfile.ts` header statements are fixed in the diff. The bubblewrap placeholder lead produces a true "not ignored" warning whose remedy works, so it is no finding. **Per-unit carry-over:** `harness-runs/task_plan_point_reviews/feat_init_upgrade_task_plan/` does not exist, so Pass 2 had nothing to reconcile.

**`plugin` layer: clean pass, no finding.** The diff changes `plugin/agents/layer-implementer.md`, `plugin/docs/AUTONOMOUS_FLOW.md`, `plugin/instructions/prompt_injection_screen.md`, `plugin/scripts/README.md` and `plugin/scripts/reserve-qa-user.sh`, checked against `.claude/context/plugin.md`. `## Writing agent prose` (the growth rule): the `layer-implementer.md` edit swaps `init --force` for `init --upgrade` inside the existing blocker remedy, and the file is 5087 words before and after. `## Wires: dispatch in, return out`: none of the five changes a dispatch key, a return field or an `outcome` value, and nothing under `plugin/schemas/` changes. `## What this layer is` (text is behaviour, and no adopter value as a literal): `init --force` no longer appears anywhere under `plugin/`, no other file under `plugin/` or `cli/test/` quotes the three changed sentences, and the one new path, `.claude/settings.autonomous.local.json`, is the CLI's fixed `PROFILE_LOCAL_PATH` rather than an adopter's value. The new statements match the code: `init --upgrade` re-renders the profile through `renderProfile`, which applies the `sandbox` configuration and carries plugin-root entries forward as `plugin/scripts/README.md` now says. The `reserve-qa-user.sh` change is one word in a comment.

**`general` layer: clean pass, apart from the `docs/cli.md` fixes Findings 1 and 2 carry.** The diff changes `README.md`, `.gitignore`, eight documents under `docs/` and three files under `examples/notes-app/`, checked against `.claude/context/conventions.md` and `harness-runs/lessons.md`. `## Documents of record`: the three example files are `.claude/settings.autonomous.json`, `.gitignore` and `README.md`, all on the live side of the frozen-versus-live split; no file under its `devscene/` tree, its `.claude/CLAUDE.md` or its `.claude/context/` changes, and the README's new counts (137 lines, 150 `/workspace/notes-app` occurrences) match the rendered profile. The ledger's fenced-command rule: every command the added text tells an adopter to run has a fenced block. The remaining inline `init --upgrade` mentions either describe behaviour or name the route beside, or with a pointer to, such a block.

Seven findings follow: two Must Fix and five Should Fix.

---

## Phase 2 Readiness — Ordered Fix List

**This section is the single source of truth for the per-item fix loop.** The orchestrator walks the `[ ]` entries below top to bottom; the committing role flips each one to `[x]` as that fix lands. Each entry resolves to `harness-runs/code_reviews/feat_init_upgrade_code_review/finding_<K>.md`. The leading number is the fix order and `K` is the finding's stable identity.

1. [x] **Finding 6** — Use the shared `lstatOrUndefined` probe in `writePermissionProfile` _(layer: cli)_
2. [ ] **Finding 5** — Correct `doctor`'s comments that call the profile the adopter's file _(layer: cli)_
3. [ ] **Finding 4** — Print the pinned command in the upgrade report's version warning _(layer: cli)_
4. [ ] **Finding 3** — Stop asking for a daemon restart after a permission-bits repair _(layer: cli)_
5. [ ] **Finding 7** — Remove the test-only `renderCurrentProfile` export _(layer: cli)_
6. [ ] **Finding 2** — Name the working route for restoring reference-toolchain entries _(layer: cli, general)_
7. [ ] **Finding 1** — Refuse `init --upgrade` in a run copy _(layer: cli, general)_

---

## Must Fix

### 1. `init --upgrade` accepts a run copy, so it reports success without touching the profile runs load and skips the active-run refusal
→ [finding_1.md](feat_init_upgrade_code_review/finding_1.md)

### 2. An upgrade without `--reference-toolchain-path` removes a parity repository's toolchain grants, and the toolchain warning's command does not restore them
→ [finding_2.md](feat_init_upgrade_code_review/finding_2.md)

---

## Should Fix

### 3. A permission-bits repair on the watcher or a library tells the operator to restart a daemon whose code did not change
→ [finding_3.md](feat_init_upgrade_code_review/finding_3.md)

### 4. The upgrade report's version-mismatch warning prints an unpinned command, unlike `doctor` and the documented route
→ [finding_4.md](feat_init_upgrade_code_review/finding_4.md)

### 5. `doctor`'s check comments still say the profile is the adopter's hand-tuned file
→ [finding_5.md](feat_init_upgrade_code_review/finding_5.md)

### 6. `writePermissionProfile` calls `lstatSync` directly beside the shared "what is at this path" probe
→ [finding_6.md](feat_init_upgrade_code_review/finding_6.md)

### 7. `renderCurrentProfile` is exported for `init --upgrade` and `doctor`, but only a test calls it
→ [finding_7.md](feat_init_upgrade_code_review/finding_7.md)

---

## Nice to Have

None.

---

## Out of scope / verified-OK (intentional divergences / call-outs)

None: `phases.parity` is `false`, so there is no reference implementation to diverge from.
