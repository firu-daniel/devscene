### Task 8 — Add a suite for the hand-off's own contract

**Goal:** One new `cli` suite pins what `flow-walker.sh` itself does, as opposed to what the command it hands off to does. It runs against the `init`-shipped copy in a throwaway fixture.

**Depends on:**
- **Task 1**, which fixes the hand-off's contract. The contract is restated here so the cases are written from it:
  - **What runs.** The environment is `<scriptsDir>/python/.venv`, the project is `<scriptsDir>/python/devscene-flow-host`, and `PYTHONPATH` is the two shipped packages' `src/` directories there. All are resolved from the script's own directory through `lib/harness-run-lib.sh`'s `HR_FLOW_HOST_*` names. No environment variable chooses any of them, and an inherited `PYTHONPATH` is replaced.
  - **Unprovisioned refusal.** With `uv` not on `PATH`, `<env>/pyvenv.cfg` absent, or `<env>/bin/devscene-flow-walker` not executable, the hand-off exits `2`. It prints nothing on stdout and exactly one stderr line, which opens `flow-walker: ` and names `bash <scriptsDir>/flow-host-provision.sh` and `outside the sandbox`.
  - **`--flows`.** It is passed for `start`, `next` and `current` only, so `check-round-file --findings <missing>` reaches the command and exits `3`.
  - **Leftover flat file.** For `start`, `next` and `current`, a regular file at `<stateDir>/.flow_walker_state` is deleted before the command runs.
- **Task 2**, which exports these from `cli/test/helpers/walker.mjs`: `walkerFixture` (which links the fixture's environment), `linkWalkerEnv(dir)`, `walk`, `walkerStatePath(dir, branch)` and `walkerUnavailable()`.

### Targets

- `cli/test/flow-walker-hand-off.test.mjs` (new). It reads no tree of repository files, so it is not a tree-reading test and owes no `treeGuards` entry.

**Work:**

- [ ] Header. The rule this suite enforces:
  - the hand-off refuses an unprovisioned checkout with the provisioning remedy and runs nothing;
  - what it executes is chosen by its own directory alone, never by an environment variable;
  - it passes `--flows` only to the walk verbs;
  - it removes a leftover bash state file so the walk starts fresh.

  Record what is deliberately not covered: the command's own routing, which the other `flow-walker*` suites and `devscene-flow-host/tests/` cover; and `--no-cache` inside a real sandbox, which no suite can reach.
- [ ] Unprovisioned cases, each `{ skip: walkerUnavailable() }`. Each asserts `status === 2`, an empty stdout, and one stderr line matching `/^flow-walker: .*bash .*flow-host-provision\.sh.*outside the sandbox/`:
  - the fixture's environment link removed, so `<scriptsDir>/python/.venv` is absent;
  - a `PATH` holding `bash`, `git` and `jq` but no `uv`, built as `cli/test/doctor-flow-host.test.mjs` → `pathWithoutUv` builds one.

  Both also assert that `walkerStatePath(dir)` does not exist afterwards.
- [ ] Variables choose nothing — the trust rule (`<state_dir>/lessons.md` → `## Trust checks`):
  - plant a temporary directory holding a `devscene_flow_host/__init__.py` that raises on import;
  - run `start --skipped none` with `PYTHONPATH` set to that directory and `DEVSCENE_FLOW_HOST_ENV` / `DEVSCENE_FLOW_HOST_PROJECT` set to an empty temporary directory;
  - assert it exits `0` with an `action: dispatch` block.
- [ ] `check-round-file`:
  - `check-round-file --findings <a path that does not exist>` exits `3` with stderr opening `flow-walker: `, and stdout empty;
  - a planted valid `verdict: PASS` file exits `0` with empty stdout;
  - neither run's stderr mentions `--flows`.
- [ ] Leftover flat file:
  - plant a regular file `<stateDir>/.flow_walker_state` holding `step=3\n`;
  - `current` exits `1` with stderr matching `/^flow-walker: no walk in progress at /`, and the flat file is gone;
  - a following `start --skipped none` exits `0` with an `action: dispatch` block;
  - `<stateDir>/.flow_walker_state` is now a directory holding `walkerStatePath(dir)`.

  A second case plants a symbolic link at that path and asserts it is **not** removed by `current`.

**Verification:**

- Run `commands.typecheck`; it must exit 0.
- Run `npm test --workspace cli -- test/flow-walker-hand-off.test.mjs`. It passes with `# skip 0` on a host where `walkerUnavailable()` is false.
