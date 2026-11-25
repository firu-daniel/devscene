### Task 5 — Grade a missing `uv` as a `doctor` failure

**Goal:** With the walker needed, `doctor`'s `uv` check reports an absent `uv` as a **failure**, where it has been a warning since #478 (task prompt, *"Decided (2026-11-24, after #478)"*). The `flow-host` check's unprovisioned-environment finding is re-argued, because its stated reason, *"nothing runs the walker yet"*, is no longer true:
- **It stays a `warn` by default.** Run copies build their own environment at `setup-worktree.sh` step 6, which now fails without `uv`. A session in the main checkout gets the walker's own exit-2 refusal, which names the same provisioning command.
- **It becomes a `fail` where `execution.scriptDrivenPlanning` is `true`.** Task 6 makes the planning driver run the main checkout's walker and environment, so an unprovisioned main checkout stops that flow.

**Depends on:** Task 3, which makes `setup-worktree.sh` step 6 fail the bootstrap with no `uv` or no project, rather than printing `SKIPPED` and passing. That is what lets a run copy's missing environment be graded there rather than here. Task 6 comes later and depends on this grading; this task states the dependency rather than consuming it.

### Targets

- `cli/src/doctor/checks.ts` — `UV_CHECK` and `FLOW_HOST_CHECK`, with their doc comments.
- `cli/test/doctor-flow-host.test.mjs` — the uv-absent case and the unprovisioned cases.

**Work:**

- [ ] `UV_CHECK`. `uv` not resolving on `PATH` returns `fail`. Its message keeps *"DevScene requires uv to run its flow walker"* and the install URL, and replaces *"A warning rather than a failure because nothing runs the walker yet"* with the reason it fails: every walker call refuses without it, and a run copy's bootstrap fails. The two findings where `uv` resolves but `uv --version` gives no usable answer stay `warn`s: `uv` is present and may work. Rewrite the doc comment's *"Every finding is a `warn` until #419 makes the walker needed"* to the grading above.
- [ ] `FLOW_HOST_CHECK`:
  - the unprovisioned branch returns `fail` when `scriptDrivenPlanningEnabled(ctx.config)` is true (`cli/src/config/model.ts`, imported rather than re-reading the key), with a message naming the command and that script-driven planning runs the main checkout's walker;
  - otherwise it returns `warn`, with the reason that run copies are built by `setup-worktree.sh` step 6, and that a session in this checkout is refused by the walker with this same command;
  - the package-drift findings stay `warn`s;
  - rewrite the doc comment's *"Every finding warns, for UV_CHECK's reason"* to this grading.
- [ ] `doctor-flow-host.test.mjs`:
  - the `PATH`-without-`uv` case asserts a `FAIL` line for `uv` matching `/DevScene requires uv/`, the `flow-host` line still naming *"install uv first"*, and a summary with at least one fail and exit status `1`;
  - the unprovisioned case asserts `WARN` without `execution.scriptDrivenPlanning`;
  - a new case sets `execution: { scriptDrivenPlanning: true }` in the fixture's `devscene.config.json` and asserts `FAIL` naming the provisioning command, then `PASS` once `plantEnvironment(dir)` has run;
  - update the suite header's rule.

**Verification:**

- Run `commands.typecheck`; it must exit 0.
- Run `npm test --workspace cli -- test/doctor-flow-host.test.mjs`.
- `git grep -n 'nothing runs the walker yet' -- cli/src` prints nothing.
