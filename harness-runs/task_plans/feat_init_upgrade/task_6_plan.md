### Task 6 — Add the outer-loop script upgrade planner and drift reader

**Goal:** Let `init --upgrade` bring every row of `OUTER_LOOP_SCRIPTS` to its shipped bytes and mode, and let `doctor` report the rows that differ.

**Depends on:** Task 1, for the `replace-if-changed` policy.

**Where this task stops.** The wrapper scripts in `WRAPPER_SCRIPTS` are deliberately outside this task: each holds this repository's own commands. Task 10 calls the planner and Task 11 calls the drift reader.

### Targets

- `cli/src/generators/outerLoopScripts.ts`
- `cli/test/outer-loop-upgrade.test.mjs` (new)

**Work:**

- [ ] Factor `writeOuterLoopScripts` over a private helper taking the write policy, so its `create-if-absent` behaviour and its notes stay as they are.
- [ ] Export `planOuterLoopScriptUpgrade({ repoRoot, config, plan }): OuterLoopScriptsResult`, which enqueues the same directories and rows under `replace-if-changed`, with each row's mode.
- [ ] Export `outerLoopScriptDrift(repoRoot: string, config: HarnessConfig): { readonly missing: readonly string[]; readonly changed: readonly string[] }`. Paths are relative to `scriptsDir`, in table order, compared by bytes against `readTemplate`. A row whose executable bit differs from its table mode counts as changed. It writes nothing.
- [ ] Update the module header's re-run paragraph and the `writeOuterLoopScripts` doc comment to name both contracts.
- [ ] `outer-loop-upgrade.test.mjs`: with compiled imports and a wired fixture, assert the planned requests cover every table row and no `WRAPPER_SCRIPTS` file, and that the drift reader reports nothing on a fresh fixture, then a deleted row, an edited row and a row in `lib/`.

**Verification:**

- `cli/test/outer-loop-upgrade.test.mjs` passes.
- The planner names no `typecheck.sh`, `test.sh`, `start-dev-server.sh` or `deploy.sh` target.
- A plain `init` over an edited script still reports that script as kept.
