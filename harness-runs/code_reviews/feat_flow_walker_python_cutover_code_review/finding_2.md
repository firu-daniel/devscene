### 2. `doctor --remote-job` fails `flow-host` where script-driven planning is on, so a remote job stops at its preflight, before the step that builds the environment

**File:** `cli/src/doctor/checks.ts` (`FLOW_HOST_CHECK`) — "if (scriptDrivenPlanningEnabled(ctx.config)) {"
**Class:** Wrong behaviour
**Failure:** If an adopter whose `devscene.config.json` sets `execution.scriptDrivenPlanning: true` and `execution.target: "github-actions"` dispatches a remote run, then the job's `Preflight with doctor` step exits 1 on `!! FAIL flow-host` ("has not been provisioned … A failure because execution.scriptDrivenPlanning is true"), and the job stops before its session.

**The problem.** This branch makes an unprovisioned `<scriptsDir>/python/.venv` a `fail` whenever `scriptDrivenPlanningEnabled(ctx.config)` is true, with no carve-out for `ctx.remoteJob`. `docs/cli.md` → the `flow-host` bullet states this explicitly: *"which fails**, `--remote-job` included"*.

In a remote job that environment cannot exist when doctor runs. Its order is fixed in `cli/templates/github/workflows/devscene-run.yml`:

1. `Set up uv`.
2. `Preflight with doctor`, which runs `doctor --cwd "$GITHUB_WORKSPACE" --remote-job`.
3. `Bootstrap the checkout`, which runs `bash "$SCRIPTS_DIR/setup-worktree.sh"`. Its step 6 is the only thing that builds `<scriptsDir>/python/.venv` in the job checkout.

The checkout is fresh and the environment is gitignored. So the check grades an environment that the next step builds. Doctor exits 1 on a `fail`, the preflight step fails, and the job's later steps never run. This repository is one such adopter: its own `devscene.config.json` sets `"scriptDrivenPlanning": true`.

Before this branch every `flow-host` finding was a `warn`, so the preflight passed. In the job the guarantee that a `fail` would add is already enforced one step later. This branch makes `setup-worktree.sh` step 6 fail the bootstrap when it cannot build the environment.

Confirmed by reading `FLOW_HOST_CHECK`, the workflow template's step order and the `docs/cli.md` bullet. No remote job or `doctor --remote-job` run was executed.

**Fix.**

1. In `cli/src/doctor/checks.ts` → `FLOW_HOST_CHECK`, keep the failure for local runs only, and under `--remote-job` warn with the reason. Replace the block after `const finding = …`:

   ```ts
         if (ctx.remoteJob) {
           return warn(
             `${finding}. A warning rather than a failure under --remote-job because the job builds this environment at its \`Bootstrap the checkout\` step (setup-worktree.sh step 6), which runs after this preflight and fails the job without it`,
           );
         }
         if (scriptDrivenPlanningEnabled(ctx.config)) {
           return fail(
             `${finding}. A failure because execution.scriptDrivenPlanning is true, so script-driven planning runs this checkout's walker and environment and stops without them`,
           );
         }
         return warn(
           `${finding}. A warning rather than a failure because a run copy builds its own environment at setup-worktree.sh step 6, and a session in this checkout is refused by the walker with this same command`,
         );
   ```

   In the doc comment above `FLOW_HOST_CHECK`, extend the grading sentence: "Under {@link CheckContext.remoteJob} it warns in every case, because the job's `Bootstrap the checkout` step builds the environment after the preflight and fails the job without it."

2. In `docs/cli.md`, rewrite the `flow-host` bullet's opening and its grading sentence:
   - The opening becomes: "**`flow-host` is a warning, except for an unprovisioned environment where `execution.scriptDrivenPlanning` is on, which fails — but not under `--remote-job`, where it warns.**"
   - The sentence "That finding is a failure where script-driven planning is on, … at `setup-worktree.sh` step 6." gains: "Under `--remote-job` it is a warning in every case, because the job's `Bootstrap the checkout` step builds the environment after the preflight and fails the job without it."

3. In `cli/test/doctor-flow-host.test.mjs`, add a case beside *"fails on flow-host naming the provisioning command where script-driven planning is on"*. It is the same set-up run with `--remote-job`, and it asserts on the `flow-host` line only, because a fixture fails other `--remote-job` checks:

   ```js
     it('warns rather than fails on flow-host under --remote-job where script-driven planning is on', async (t) => {
       const dir = await wired(t);
       enableScriptDrivenPlanning(dir);
       const result = await runCli(dir, ['doctor', '--remote-job'], { PATH: await uvStubPath(t, STUB_VERSION) });
       assert.equal(checkLine(result, 'FAIL', FLOW_HOST_CHECK), undefined, result.stderr);
       assert.match(line(result, 'WARN', FLOW_HOST_CHECK), /Bootstrap the checkout/);
     });
   ```

   Add "under `--remote-job` it warns, because the job builds the environment after its preflight" to the suite header's rule sentence. That test file is one this fix edits, so it is the only test file the fix runs. The full suite runs in the Run gates phase.
