### Task 7 — Offer provisioning once after `init`'s plan, behind `--provision-python`, and name the command after `init --upgrade`

**Goal:** Let an adopter end `init` with the walker's environment already built, without making an unattended or piped `init` reach the network. This is an interactive decision, so it gets the three parts `.claude/context/cli.md` → `## How a module in this layer is written` requires:

- **a flag:** `--provision-python`, a switch that answers yes;
- **a non-interactive default:** skip, with a note naming the command;
- **a prompt:** shown only when the flag is absent, both descriptors are a TTY, and the environment does not exist yet.

**Depends on:**

- **Task 3** ships `<scriptsDir>/flow-host-provision.sh`. It takes no argument. Exit `0` means provisioned or skipped; a skip prints a `flow-host: provision: SKIPPED — …` line on **stderr**. Exit `1` means it failed, exit `2` means usage. This task runs the script and never re-implements the sync.
- **Task 2** gives `init` its `writeFlowHostPackages` result, `{ written }`, and skips under self-adoption.
- **Task 1**'s `flowHostEnvDir(config)` locates `<scriptsDir>/python/.venv`. Its `pyvenv.cfg` is the "already provisioned" test.

**Where this task stops.** It never makes `init` fail: a skip or a failure is a warning or a note, as `retrieval/setup.ts`'s post-plan steps are. `doctor`'s report of an unprovisioned repository is Task 8's.

### Targets

- `cli/src/flowHost/provision.ts` (new).
- `cli/src/commands/init.ts`.
- `cli/src/upgrade/report.ts`.
- `cli/src/core/writer.ts`: the header's out-of-engine paragraph (`**Three writes are deliberately outside this engine.**`) only. Task 2 owns the header's re-run table row in the same file, and this task, which depends on Task 2, leaves that table alone.
- `cli/test/init-provision-python.test.mjs` (new).

**Work:**

- [ ] `provision.ts`, its header stating its rule: it is `init`'s one caller of the provisioning script. It exports `provisionFlowHost({ repoRoot, config, dryRun })`, which returns `{ notes, warnings }`.
  - It runs `bash <repoRoot>/<scriptsDir>/flow-host-provision.sh` with a fixed argument vector. The path comes from `outerLoopScriptPath`, and the display string from `scriptInvocation`.
  - It uses `spawnSync`, for the reason `cli/src/commands/doctor.ts` → `runNotifier` argues: the skip line arrives on stderr with exit `0`.
  - Results:
    - exit `0` with a `SKIPPED` line: a warning carrying that line;
    - exit `0` otherwise: a note;
    - any other exit: a warning with the last stderr line and the command to re-run outside the sandbox;
    - under `dryRun`: a note saying what would run, and nothing spawned.
  - `cli/src/core/writer.ts`'s header, the out-of-engine paragraph: rename it to four writes and add the fourth. The walker's environment `<scriptsDir>/python/.venv` is written into the adopting repository by `uv`, in the `flow-host-provision.sh` child that `cli/src/flowHost/provision.ts` → `provisionFlowHost` spawns. It is written after the plan and never under `--dry-run`, its one path comes from `cli/src/flowHost/layout.ts` → `flowHostEnvDir`, and `provision.ts` is the **one** module of this package that causes it. It is no `init` artifact and has no re-run policy. Extend the paragraph's closing sentence on what `.claude/context/conventions.md` does not record so that it names this write too: a `stale-rule` entry in the story index, never an edit here.
- [ ] `init.ts`, the flag and the decision:
  - Add an `INIT_OPTIONS` switch row `{ key: 'provisionPython', flag: '--provision-python', summary: … }`, shaped like `--git-init`'s.
  - Resolve the answer **before `plan.apply`**: init's rule is that no answer is taken after anything is written.
    - The flag means yes.
    - Otherwise, when both descriptors are a TTY and `<scriptsDir>/python/.venv/pyvenv.cfg` is absent, ask through `cli/src/core/prompt.ts`, defaulting to yes.
    - Otherwise no.
  - Check whether `--upgrade`'s refusal list (`assertUpgradeFlagsUsable`) refuses the new flag, and confirm it does.
- [ ] `init.ts`, the post-plan step: after `pointHooksPath` and before `commitGeneratedFiles`, beside the retrieval step.
  - Its comment says, unlike the retrieval step's *"this step writes nothing into the repository"*, that this step **does** write into the repository: `uv` creates `<scriptsDir>/python/.venv` in the spawned child. It says why it runs after the plan: the environment is built from the packages the plan has just written, a sync takes the network and minutes, and it is no plan artifact, so it is never enqueued and never runs under `--dry-run`. It names `cli/src/core/writer.ts`'s header as where the exception is recorded.
  - On yes, push `provisionFlowHost`'s notes and warnings.
  - On no, when the environment is absent or Task 2's `written` is non-empty, push one note: the walker's environment is not provisioned, and here is the command to run outside the sandbox.
  - The prompt text and the note use adopter vocabulary: "the Python environment the flow walker runs in", and "uv" (`harness-runs/lessons.md` → `## Adopter-facing documentation`).
- [ ] `upgrade/report.ts`: when the upgrade replaced or created a file under `<scriptsDir>/python/`, print one next-step line naming `bash <scriptsDir>/flow-host-provision.sh`, run outside the sandbox, because a `--no-editable` environment keeps the old code until rebuilt. Build the command from `scriptInvocation`, the same producer the script's own message uses (`harness-runs/lessons.md` → *"derive the advice from the same predicate as the refusal"*).
- [ ] `init-provision-python.test.mjs`, its header stating the rule. It uses a stub `uv` on `PATH` that records its argv, and asserts:
  - With `--provision-python`, the stub ran once with Task 3's argv, and `init` exits `0`.
  - Without the flag and with stdin piped, the stub never ran, and the note names the command.
  - With `--dry-run --provision-python`, nothing ran.
  - With the stub exiting `1`, `init` still exits `0` with a warning naming the command.
  - `init --upgrade` after an edit under `<scriptsDir>/python/` prints the next-step line.

**Verification:**

- `npm test --workspace cli -- test/init-provision-python.test.mjs` passes.
- `node cli/dist/cli.js init --help` lists `--provision-python`.
- Existing `init` suites whose expected output now carries the new note: update only that expectation, and only in suites this task edits.
