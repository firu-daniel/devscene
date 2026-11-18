# Skeptic Review: feat_init_upgrade

## Context

**Branch:** `feat_init_upgrade`
**Date:** 2026-11-18
**Reviewed:** the whole branch diff against `origin/dev` (this run copy has no local `dev`; merge base `e63fb5f2`): 64 files, covering the write engine, the local additions file, the profile and script planners, the run-registry and plugin-version readers, the `--upgrade` refusals and report, the three new `doctor` checks, and the documents that state the route. 50 run-artifact files excluded from the reviewed diff.

**De-duplicated against:** `harness-runs/code_reviews/feat_init_upgrade_code_review.md` (7 findings) and `harness-runs/architecture_branch_reviews/feat_init_upgrade_arch_review.md` (5 findings), with their finding files, the lessons ledger and the planning rounds' incidental leads. `phases.parity` is `false`, so no parity review exists and check 2's parity leg does not apply.

**`plugin` layer: no net-new finding.** The diff changes one line in each of five files: `plugin/agents/layer-implementer.md`, `plugin/docs/AUTONOMOUS_FLOW.md`, `plugin/instructions/prompt_injection_screen.md`, `plugin/scripts/README.md` and `plugin/scripts/reserve-qa-user.sh`. I read them adversarially against `.claude/context/plugin.md`, and checked each new `init --upgrade` statement against the code:

- `layer-implementer.md`: the sandbox remedy holds. `planProfileUpgrade` renders from the configuration, and `cli/src/generators/sandboxProfile.ts` takes `sandbox.allowedDomains` and `sandbox.optOut` from it. `plugin/agents/test-fix-plan-writer.md` cites this paragraph by its bold title, which did not change.
- `AUTONOMOUS_FLOW.md`: the profile is created under `create-if-absent` and replaced under `replace-if-changed`, and `.claude/settings.autonomous.local.json` is merged into the render.
- `prompt_injection_screen.md`: `prompt-injection-screen.sh` is marked `agentInvocable` in `cli/src/generators/outerLoopScripts.ts`, so the render grants it. A parked run does not block the remedy, because `readActiveRuns` counts only `status: running`.
- `plugin/scripts/README.md`: `carriedPluginRootEntries` matches the carry-forward, both exclusions and the unverified case where no root resolves. `docs/cli.md` → `## 3. The re-run contract` exists.
- `reserve-qa-user.sh`: the template's `sandbox.filesystem.allowWrite` is `{{stateDirAbs}}`, which `renderProfile` builds from the configured `stateDir`.

Under `## Wires: dispatch in, return out`, no dispatch argument or return field changed. Under `## Writing agent prose`, the `layer-implementer.md` edit swaps one flag and adds no words, and no heading another file cites was renamed. Under `## Citation`, the changed lines add no line coordinate and no `${CLAUDE_PLUGIN_ROOT}` path to a file outside the plugin. A search of `plugin/` finds no remaining `init --force` remedy.

**Evidence limit.** Every finding rests on reading the code. A throwaway-fixture run of the compiled CLI was refused by the permission layer, so no behaviour below was observed at run time. No test suite was run.

**Conclusion.** The new path is wired end to end: `init`'s `run` hands over to `runInitUpgrade`, which calls the refusals, both planners and the report, and the three new checks are in `CHECKS`. Four net-new findings follow, two Must Fix and two Should Fix. The Must Fix items are a refusal that counts remote runs, against the task prompt's "active local run", and profile settings outside the entry lists that the upgrade report and `profile-drift` do not see.

---

## Phase 2 Readiness — Ordered Fix List

1. [x] **Finding 4** — Send the carry-forward warning's remedy to the local additions file _(layer: cli)_
2. [x] **Finding 3** — Print a restart command that works on an `npx` adoption _(layer: cli, general)_
3. [ ] **Finding 1** — Exclude remote run records from the upgrade's active-run refusal _(layer: cli, general)_
4. [ ] **Finding 2** — Report and grade profile settings outside the entry lists _(layer: cli, general)_

---

## Must Fix

### 1. A remote run's record blocks `init --upgrade`, although the task prompt limits the refusal to local runs
→ [finding_1.md](feat_init_upgrade_skeptic_review/finding_1.md)

### 2. Profile settings outside the entry lists are dropped without a report, and `profile-drift` passes with them changed
→ [finding_2.md](feat_init_upgrade_skeptic_review/finding_2.md)

---

## Should Fix

### 3. The restart command the upgrade report prints fails on a repository adopted through `npx`
→ [finding_3.md](feat_init_upgrade_skeptic_review/finding_3.md)

### 4. The carry-forward warning tells the adopter to re-add an entry by hand, which the next replacement deletes
→ [finding_4.md](feat_init_upgrade_skeptic_review/finding_4.md)

---

## Nice to Have

None.

---

## Out of scope / verified-OK (intentional divergences / call-outs)

None: `phases.parity` is `false`, so there is no reference implementation to diverge from.
