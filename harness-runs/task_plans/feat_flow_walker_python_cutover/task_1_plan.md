### Task 1 — Hand `flow-walker.sh` to `devscene-flow-walker`, ship the format-4 graph and retire the gate library

**Goal:** Replace the bash walker's body in `cli/templates/scripts/flow-walker.sh` with a hand-off to `devscene-flow-host`'s compatibility command. Ship `flows/task_plan_writing.v4.graph.json` into `scriptsDir` beside the walker. Retire `lib/flow-walker-gates.sh` from the template tree and from the shipped table.

**Depends on:** Task 3, which defines the flow host's layout names in `cli/templates/scripts/lib/harness-run-lib.sh` → `THE FLOW HOST'S ENVIRONMENT`, as the one declared shell mirror of their owners. This task reads them and spells none of them:
- `HR_FLOW_HOST_DIRNAME` (`python`), `HR_FLOW_HOST_PROJECT` (`devscene-flow-host`), `HR_FLOW_HOST_GRAPHSCENE` (`graphscene`), `HR_FLOW_HOST_ENV_DIRNAME` (`.venv`) and `HR_FLOW_HOST_SOURCE_DIRNAME` (`src`), mirroring `cli/src/flowHost/layout.ts`;
- `HR_FLOW_HOST_ENV_MARKER` (`pyvenv.cfg`), mirroring `cli/src/flowHost/provision.ts` → `ENV_MARKER_FILE`.

The values in parentheses are for the reader only; the script uses the variables.

**Where this task stops.** This task owns the hand-off script and the shipped set. It does **not** edit any test file, and it does not edit `harness-run-lib.sh`:
- Task 2 points the walker-driving helpers at this hand-off.
- Task 17 updates `cli/test/outer-loop-scripts.test.mjs` → `WALKER_FILES` to the shipped set this task leaves.
- Task 7 moves the suite cases that pinned bash.
- Task 8 adds the suite for the hand-off's own contract.

It does not touch this repository's self-adopted `scripts/flow-walker.sh`, `scripts/lib/flow-walker-gates.sh` or `scripts/flows/`: the user re-renders those after merge (story index `## Context`).

### Targets

- `cli/templates/scripts/flow-walker.sh` — rewritten as the hand-off.
- `cli/templates/scripts/lib/flow-walker-gates.sh` — deleted.
- `cli/src/generators/outerLoopScripts.ts` — `OUTER_LOOP_SCRIPTS`: the format-4 graph row added and the gate-library row removed; the module header's set description.

**The interface this task defines, which Tasks 2, 6, 8 and 11 restate:**

- **Environment, project and sources — from the script's own directory only.** With `<dir>` the script's own directory and `<py>` = `<dir>/$HR_FLOW_HOST_DIRNAME`:
  - the environment is `<py>/$HR_FLOW_HOST_ENV_DIRNAME`;
  - the project is `<py>/$HR_FLOW_HOST_PROJECT`;
  - `PYTHONPATH` is set on the command to `<py>/$HR_FLOW_HOST_PROJECT/$HR_FLOW_HOST_SOURCE_DIRNAME` then `<py>/$HR_FLOW_HOST_GRAPHSCENE/$HR_FLOW_HOST_SOURCE_DIRNAME`, joined with `:`, **replacing** any inherited value.

  The hand-off reads **no** environment variable to choose an environment, a project or a source path. That is the trust rule `<state_dir>/lessons.md` → `## Trust checks` states: *"An unsandboxed script takes its mode and the path of every trust input from a record the session cannot write … never from … an environment variable"*. The watcher's planning driver runs this script outside the sandbox (Task 6), and from the main checkout everything it executes then sits under `<main>/<scriptsDir>/python/`, which `cli/src/generators/writeProtection.ts` write-protects.

  The sources come first on `PYTHONPATH` because a run copy's environment is built from the **main checkout's** packages as wheels (`--no-editable`, #478). Putting the shipped sources beside the script first makes the code that runs the code `init` shipped there. In a test fixture, that code is this checkout's own, staged at build (task prompt, *"The suites test the branch's Python, not main's"*).
- **The unprovisioned refusal.** The hand-off exits `2` with exactly one stderr line, nothing on stdout, and runs nothing, when any of these holds:
  - `uv` is not on `PATH`;
  - `<env>/$HR_FLOW_HOST_ENV_MARKER` is absent;
  - `<env>/bin/devscene-flow-walker` is not executable.

  The line opens `flow-walker: ` and names the command `bash <scriptsDir>/flow-host-provision.sh`, with the words `outside the sandbox`. `<scriptsDir>` is the walker's own directory as given. This is the remedy that #478's provisioning line and `doctor`'s `flow-host` check already print, so the advice and the refusal share one predicate (`<state_dir>/lessons.md` → *"A remedy never sends an adopter to a place the CLI refuses"*).
- **The leftover bash state file.** For `start`, `next` and `current` only:
  - the hand-off resolves the root with `hr_repo_root` and `stateDir` with `hr_state_dir`, both from `lib/harness-run-lib.sh`;
  - it then deletes `<root>/<stateDir>/.flow_walker_state` when that path is a regular file and not a symbolic link, and prints nothing about it;
  - if either value does not resolve, it deletes nothing and leaves the cause to the command.
- **An old library.** The hand-off refuses with exit `2` and the existing words `flow-walker: <file> predates this walker` when either of these holds:
  - `lib/harness-run-lib.sh` cannot be sourced;
  - once sourced, it defines no `hr_repo_root` or no `hr_state_dir`, or leaves any of the six `HR_FLOW_HOST_*` names above unset or empty.

  This happens before anything else runs, for **every** verb, `check-round-file` included: that verb now needs the library too, for the layout names.
- **The launch.** The script unsets `VIRTUAL_ENV`, then runs `UV_PROJECT_ENVIRONMENT=<env> PYTHONPATH=<sources> exec uv run --frozen --no-sync --no-cache --project <project> devscene-flow-walker "$@"`.
  - It appends `--flows <dir>/flows` for `start`, `next` and `current` only, because `check-round-file` refuses a flag it does not take.
  - Every other argument is passed through unchanged.
  - The command's stdout, stderr and exit status are the caller's answer.

**Work:**

- [ ] `flow-walker.sh` body:
  - resolve its own directory from `${BASH_SOURCE[0]}`;
  - source `lib/harness-run-lib.sh` from beside itself, and apply the old-library refusal above;
  - delete the leftover flat state file for `start` / `next` / `current`;
  - apply the unprovisioned refusal;
  - launch as above, building every path from the library's `HR_FLOW_HOST_*` names.

  Keep the body bash-3.2-safe under `set -u`: an empty `--flows` array must expand without an unbound-variable error, as in `${flows[@]+"${flows[@]}"}`. No `jq` call, no graph read, no state write and no layout literal (`python`, `.venv`, `devscene-flow-host`, `graphscene`, `src`, `pyvenv.cfg`) remain in the script.
- [ ] `flow-walker.sh` header. Keep the caller-facing sections that callers cite by name — `USAGE`, `ROUNDS`, `A REFUSED ROUND FILE`, `OUTPUT` and `EXIT CODES` (`cli/templates/scripts/lib/planning-driver-lib.sh` cites *"`flow-walker.sh`'s own `ROUNDS`, `OUTPUT`, `EXIT CODES`"*). Restate each to what the command does:
  - `EXIT CODES` lists exit `1` and exit `2` as `devscene-flow-host/README.md` → `## The command line` does, plus this script's own exit-`2` refusals;
  - `ROUNDS` takes the held-gate order from `## Differences from flow-walker.sh` → **The held-gate escalation.**;
  - the graph is `<this script's dir>/flows/<flow>.v4.graph.json`.

  Replace `STATE`, `CONCURRENCY` and `BASH 3.2 AND JQ 1.5 ARE THE FLOORS` with a `HAND-OFF` section. It states:
  - the launch line;
  - that every layout name comes from `harness-run-lib.sh`'s declared mirror, and the script spells none;
  - why no environment variable chooses what runs (the trust rule above) and why the shipped sources lead `PYTHONPATH`;
  - why `--no-cache` is always passed;
  - the leftover-file deletion;
  - that the walk's state, locks and records are the command's, pointing at `devscene-flow-host/README.md` → `## What it reads, answers and keeps`.

  Close with a `REPRO` block, run in a throwaway fixture, for: a provisioned `start`; the unprovisioned refusal; `check-round-file` with a missing file (exit `3`); and a planted flat state file removed by `current`.
- [ ] Delete `cli/templates/scripts/lib/flow-walker-gates.sh`. Its readers are ported into `devscene-flow-host/src/devscene_flow_host/records/round_files.py`, `records/round_evidence.py` and `records/index_evidence.py`, and pinned by `devscene-flow-host/tests/test_round_files.py`, `test_round_evidence.py` and `test_index_evidence.py`.
- [ ] `outerLoopScripts.ts` → `OUTER_LOOP_SCRIPTS`:
  - remove the `flow-walker-gates.sh` row and its comment;
  - add `Object.freeze({ file: 'task_plan_writing.v4.graph.json', subdir: 'flows', mode: 0o644, agentInvocable: false })` before the `flow-walker.sh` row, with a comment saying the hand-off passes this directory as `--flows`;
  - reword the format-3 row's comment: it stays shipped because `lib/planning-node-lib.sh` and `lib/planning-driver-lib.sh` read its node list, and its retirement is #459's.

  Update the module header's list (*"the flow walker with its gate library and flow graph"*) to the new set. No `cli/src/core/writer.ts` row is owed: its row *"The outer-loop scripts and their `lib/` files"* already covers every `OUTER_LOOP_SCRIPTS` file, the format-3 graph included.

**Verification:**

- Run `commands.typecheck`; it must exit 0.
- In a throwaway `git init` fixture under the system temp directory, run `init` against the built CLI and confirm:
  - `scripts/flows/task_plan_writing.v4.graph.json` landed byte-identical to the template, with mode `0644`;
  - `scripts/lib/flow-walker-gates.sh` was not written.
- Walk the header's `REPRO` block in that fixture. To provision it, link the fixture's `scripts/python/.venv` to this checkout's provisioned `scripts/python/.venv`. Each outcome must print what the block says:
  - `start` prints an `action: dispatch` block;
  - with the link removed, the call exits `2` with the remedy line;
  - `check-round-file` on a missing path exits `3` with no `--flows` error;
  - a planted flat `<stateDir>/.flow_walker_state` makes `current` exit `1` with `no walk in progress at …`, and leaves the path absent.
- `git grep -n -e "'python'" -e "'\.venv'" -e 'pyvenv\.cfg' -e "'devscene-flow-host'" -- cli/templates/scripts/flow-walker.sh` prints nothing.
- `git grep -n 'flow-walker-gates' -- cli/src cli/templates` prints only the deleted file's mentions in Task 9's READMEs, which Task 9 owns.

**Deviations from plan:**
- The fixture was built by `cli/test/helpers/fixture.mjs` → `createFixture` and `runCli(d, ['init', '--no-provision-python', '--no-analyze'])`, run by `bash scripts/scratch-run.sh harness-runs/scratch/fw_task1_probe.mjs`. That init wrote the default `scriptsDir` `devscene-scripts` and `stateDir` `devscene`, so the checks read `devscene-scripts/flows/task_plan_writing.v4.graph.json` (byte-identical, mode `644`) and `devscene-scripts/lib/flow-walker-gates.sh` (absent) rather than `scripts/…`. The fixture's `<scriptsDir>/python/.venv` was replaced by a symlink to this checkout's `scripts/python/.venv`.
- REPRO outcomes, as measured with an inherited `PYTHONPATH=/nonexistent/should-be-replaced` and no `VIRTUAL_ENV`: `start` exit 0, `action: dispatch` / `node: plan_writer`; with the link removed, `current` exit 2, empty stdout, `flow-walker: the flow host is not provisioned (no environment at …/python/.venv): run bash devscene-scripts/flow-host-provision.sh outside the sandbox`; `check-round-file --findings absent.md` exit 3, `flow-walker: absent.md: no single verdict line`; a planted flat `devscene/.flow_walker_state` made `current` exit 1 with `no walk in progress at …/devscene/.flow_walker_state/feat_x.json`, and the flat path was gone afterwards. Also probed: a symlinked flat path is left in place; an emptied `HR_FLOW_HOST_ENV_MARKER` fails `check-round-file` with exit 2, `predates this walker (it sets no HR_FLOW_HOST_ENV_MARKER)`; a deleted library fails with exit 2, `predates this walker (it cannot be sourced)`; no arguments at all reaches the command (exit 1, `missing subcommand`).
- Evidence downgrade: the probe ran the script under the `bash` on `PATH`, not explicitly under `/bin/bash` 3.2. Under bash 3.2 the script was only parsed, by `commands.typecheck`'s `check-shell-parse` (`/bin/bash (bash 3.2.57(1)-release)`), not run; the `${!name-}` and `${fw_flows[@]+"${fw_flows[@]}"}` forms were not run under 3.2.
- The header's REPRO uses `npx devscene init` with `<scripts_dir>` / `<state_dir>` placeholders, not a literal `scripts/`, because the directory comes from the adopter's config. The HAND-OFF section prints the launch line with the layout words, as the Work item asks. The script body spells none of them, and the quoted-literal `git grep` prints nothing.
