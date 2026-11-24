### Task 4 — Make `init` build the walker's environment by default, with `--no-provision-python` to opt out

**Goal:** `init` builds `<scriptsDir>/python/.venv` after the plan by default, as the task prompt decides (*"`init` builds the environment by default instead of behind `--provision-python`"*). This task settles what it leaves open, as the story index `## Context` records:
- **The default.** Every `init` that is neither `--dry-run` nor `--upgrade` runs `provisionFlowHost`, whether or not it can prompt, unless the environment already exists and no shipped package file changed. The terminal question is removed.
- **The opt-out.** `--no-provision-python` skips the build, with the note naming the command.
- **The old flag.** `--provision-python` stays accepted as the explicit form of the default, and changes nothing.
- **`--upgrade`.** It refuses both flags, as it refuses `--provision-python` today. `--upgrade` still builds nothing, and its report already names the rebuild.

The `cli` suite must not reach the network on every fixture `init`. So `init` honours a probe variable that the suite's isolated environment sets to `off`, which no shipped path ever sets. This follows the `KEEP_AWAKE_LOCK_PROBE_ENV` and `NESTED_USERNS_PROBE_ENV` precedent in `cli/test/helpers/fixture.mjs` → `ISOLATED_ENV`.

**Depends on:** Task 3. That task makes `hr_flow_host_provision` return `1` with `flow-host: provision: failed — uv is not on PATH; …` and `failed — no flow host at …` where it used to print `flow-host: provision: SKIPPED — …` and return `0`. So the `SKIPPED` branch of `provisionFlowHost` and its mirror note are dead code, and this task removes them. Task 3 also declares `HR_FLOW_HOST_ENV_MARKER` (`pyvenv.cfg`) in that library as the shell mirror of `ENV_MARKER_FILE`, which this task exports.

### Targets

- `cli/src/commands/init.ts`:
  - `PROVISION_PYTHON_FLAG` and a new `NO_PROVISION_PYTHON_FLAG`;
  - their rows in the flag table (`key: 'provisionPython'` and a new one);
  - `resolveProvisionPython`;
  - the post-plan *"flow walker environment"* step;
  - the `--upgrade` refusal.
- `cli/src/flowHost/provision.ts`:
  - the module header;
  - `SKIPPED_MARKER` and its branch removed;
  - a new exported constant `FLOW_HOST_PROVISION_PROBE_ENV`, with the value `'DEVSCENE_FLOW_HOST_PROVISION_PROBE'`;
  - `ENV_MARKER_FILE` exported. Its value `'pyvenv.cfg'` stays unchanged. Task 2's `cli/test/helpers/walker.mjs` and Task 16's `cli/test/flow-host-provision.test.mjs` import it from `dist/flowHost/provision.js`.
- `cli/test/helpers/fixture.mjs` — `ISOLATED_ENV` gains `[FLOW_HOST_PROVISION_PROBE_ENV]: 'off'`, with its paragraph in the doc comment above it.
- `cli/test/init-provision-python.test.mjs` — the suite's rule and cases.

**Work:**

- [ ] `init.ts` — the decision:
  - `resolveProvisionPython` becomes a pure decision with no prompt;
  - it answers `false` under `--no-provision-python`, and `false` when `process.env[FLOW_HOST_PROVISION_PROBE_ENV] === 'off'`;
  - otherwise it answers `true` when the environment is not provisioned (`flowHostProvisioned`), or when the plan changed a shipped package file (the existing `flowHostChanged > 0`);
  - else it answers `false`.

  Because the changed-file count is known only after `plan.apply`, split the decision into the pre-plan flag read (kept before the plan for init's no-answer-after-write rule) and the post-plan step. Rewrite the doc comment, which argues *"The default without a terminal is no because the build reaches the network"*, to the new default and its reason: the walker is required, and a repository left without its environment cannot plan.
- [ ] `init.ts` — flags and messages:
  - add the `NO_PROVISION_PYTHON_FLAG` row (`'--no-provision-python'`, switch), with a summary;
  - reword the `provisionPython` row's summary to *"the default; accepted for scripts written before it was"*;
  - refuse `--provision-python` and `--no-provision-python` given together, and either one with `--upgrade`, each as an ordinary `HarnessError` naming the flags.

  The post-plan notes keep naming `flowHostProvisionInvocation(effective)`. Where they told the reader to *"pass --provision-python to init"*, they now name the opt-out instead: the note under `--no-provision-python` or the probe says the environment was not built and names the command to run outside the sandbox.
- [ ] `provision.ts`:
  - remove `SKIPPED_MARKER`, the `skipped` lookup in the `status === 0` branch, and the `MIRROR.` paragraph;
  - add `FLOW_HOST_PROVISION_PROBE_ENV` with a doc comment saying it exists for the test suite alone, that no shipped path sets it, and that `off` makes `init` skip the default build exactly as `--no-provision-python` does;
  - export `ENV_MARKER_FILE`, and give it a `MIRRORS.` note: `cli/templates/scripts/lib/harness-run-lib.sh` → `HR_FLOW_HOST_ENV_MARKER` (Task 3) spells it for the shell, and `cli/test/flow-host-provision.test.mjs` holds the two equal.

  A failed child — exit `1`, including the two new `failed —` lines — is already a warning carrying its last stderr line, and stays one: provisioning never fails `init`.
- [ ] `fixture.mjs`: import `FLOW_HOST_PROVISION_PROBE_ENV` from `../../dist/flowHost/provision.js`, add it to `ISOLATED_ENV` as `'off'`, and add its paragraph to the comment above `ISOLATED_ENV`, beside the two probe paragraphs, with the same *"a case whose subject is … passes `{ [ENV]: '' }` explicitly"* sentence.
- [ ] `init-provision-python.test.mjs`. Every case whose subject is the build passes `{ [FLOW_HOST_PROVISION_PROBE_ENV]: '' }`. The cases:
  - a plain `init` runs the stub `uv` once with the provisioning argv;
  - `--no-provision-python` runs nothing and leaves the note naming the command;
  - `--provision-python` behaves as plain `init`;
  - `--dry-run` runs nothing;
  - a second plain `init` over a provisioned environment with unchanged packages runs nothing;
  - with `PATH` holding no `uv`, the warning carries `flow-host: provision: failed — uv is not on PATH`;
  - `--upgrade` refuses each flag and writes nothing;
  - the two flags together are refused;
  - with the suite's default isolated environment (probe `off`), a plain `init` runs nothing.

  Restate the suite header's rule to these outcomes.

**Verification:**

- Run `commands.typecheck`; it must exit 0.
- Run `npm test --workspace cli -- test/init-provision-python.test.mjs`.
- `git grep -n -e 'SKIPPED_MARKER' -e 'provision: SKIPPED' -- cli/src cli/test/init-provision-python.test.mjs` prints nothing. The provisioning and bootstrap suites' `SKIPPED` lines are Task 16's, which ships after this task.
- `git grep -n 'askYesNo' -- cli/src/commands/init.ts` no longer shows the walker-environment question.
