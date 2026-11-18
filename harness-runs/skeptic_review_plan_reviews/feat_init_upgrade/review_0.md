# Review plan meta-review — iteration 0

## Must Fix

1. **Finding 3's fix breaks a test it does not name** — refers to review finding #3. Offending file: `harness-runs/skeptic_reviews/feat_init_upgrade_skeptic_review/finding_3.md`.

   Finding 3 changes the restart line to `DEVSCENE_CLI="<cli command>" bash <scriptsDir>/restart-watcher.sh`, and its step 4 updates only `cli/test/upgrade-report.test.mjs`. `cli/test/init-upgrade.test.mjs` → the test `the restart line appears when the watcher changes, and not otherwise` also pins the old wording, through the compiled CLI:

   ```js
   const restart = scriptInvocation(repo.scriptsDir, RESTART_WATCHER_SCRIPT_NAME);
   assert.ok(preview.stdout.includes(`restart the daemon afterwards with ${restart}`), preview.stdout);
   assert.ok(applied.stderr.includes(`restart it with ${restart}`), applied.stderr);
   ```

   `restart` is `bash scripts/restart-watcher.sh`. After the fix, both phrases are followed by `DEVSCENE_CLI=...`, so both assertions fail. The fix loop runs only the test files a fix edits, so this failure would first appear in the Run gates phase. A finding file must be implementable from that file alone, and this one leaves the suite red.

   **Fix:** in `finding_3.md`, add a sub-step to step 4 for `cli/test/init-upgrade.test.mjs`. In that test, add `const { name, version } = readJson(join(PACKAGE_ROOT, 'package.json'));` and `const pinned = `DEVSCENE_CLI="npx ${name}@${version}" ${restart}`;`, then change the two assertions to `restart the daemon afterwards with ${pinned}` and `restart it with ${pinned}`. `readJson`, `join` and `PACKAGE_ROOT` are already imported there. Keep the `!quiet.stderr.includes(restart)` assertion unchanged.

2. **The diff touches the `plugin` layer, and the review shows no check drawn from that layer's rules** — refers to "Structure". Offending file: `harness-runs/skeptic_reviews/feat_init_upgrade_skeptic_review.md`.

   The diff changes `plugin/agents/layer-implementer.md`, `plugin/docs/AUTONOMOUS_FLOW.md`, `plugin/instructions/prompt_injection_screen.md`, `plugin/scripts/README.md` and `plugin/scripts/reserve-qa-user.sh`. No finding has a `plugin` tag or a fix under `plugin/`. The index's Context mentions only "the documents that state the route", and neither names the layer nor cites `.claude/context/plugin.md`. The `cli` and `general` layers are covered by findings whose fixes land there. Naming the code review under "De-duplicated against" does not show that this review examined the layer.

   **Fix:** in the index's Context, add a `plugin` layer paragraph stating the result of an adversarial pass over those five files against `.claude/context/plugin.md`, naming the sections applied (for example `## Wires: dispatch in, return out` and `## Writing agent prose`) and what was confirmed. It must also cover whether each new `init --upgrade` statement is true of the code. If the pass finds a net-new defect, add it instead as a new `finding_<N>.md` with its index pointer and readiness entry tagged `_(layer: plugin)_`.

## Nice to Have

1. **Finding 2's real-run warning is ungrammatical for one setting** — refers to review finding #2. Offending file: `harness-runs/skeptic_reviews/feat_init_upgrade_skeptic_review/finding_2.md`.

   Step 4 prints `${counted(settingChanges.length, 'profile setting')} outside the entry lists were reset`, which reads "1 profile setting outside the entry lists were reset". Finding 2's own `env` case produces exactly that count.

   **Fix:** in step 4 of `finding_2.md`, choose `was` or `were` from `settingChanges.length`.
