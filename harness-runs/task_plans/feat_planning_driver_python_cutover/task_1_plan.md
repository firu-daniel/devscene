### Task 1 — Launch a flow-host console script through one library route, and hand `flow-walker.sh` to it

**Goal:** Give `cli/templates/scripts/lib/harness-run-lib.sh` the one route that checks the flow host's environment and execs one of its console scripts under `uv`. `flow-walker.sh` uses it for `devscene-flow-walker`, and the watcher uses it for `devscene-planning-driver` (Task 2). The `uv` launch stays stated once.

**Where this task stops.** This task adds the route and moves `flow-walker.sh` onto it. It does not touch the watcher: calling the route for the planning driver is **Task 2's**. The console script `devscene-planning-driver` itself is **Task 18's**, which also adds the test holding this task's name constant equal to `devscene-flow-host/pyproject.toml` → `[project.scripts]`.

### Targets

- `cli/templates/scripts/lib/harness-run-lib.sh` — `THE FLOW HOST'S ENVIRONMENT` block: one new name and two new functions.
- `cli/templates/scripts/flow-walker.sh` — `HAND-OFF` steps 3 and 4 call the new functions.

**Work:**

- [ ] `harness-run-lib.sh`: beside the six `HR_FLOW_HOST_*` names, add `HR_FLOW_HOST_DRIVER='devscene-planning-driver'`.
  - Add a mirror line to the block's header table naming its owner: the planning driver's entry in `devscene-flow-host/pyproject.toml` → `[project.scripts]`, held equal by `devscene-flow-host`'s own suite. Name no test file: Task 18 adds both the entry and the test.
  - It is not a `cli/src/flowHost/layout.ts` name, so `layout.ts`'s `MIRRORS.` header does not change.
- [ ] `harness-run-lib.sh`: add `hr_flow_host_missing <scripts_dir_abs> <console_script>`.
  - It prints nothing and returns 0 when the environment can run `<console_script>`.
  - Otherwise it prints the one cause `flow-walker.sh` prints today, in the same words (`uv is not on PATH`, `no environment at <env>`, `<env> has no <console_script>`), and returns 1.
  - It checks in `flow-walker.sh`'s order: `uv` on `PATH`, then the environment's `HR_FLOW_HOST_ENV_MARKER` file, then `bin/<console_script>` executable.
- [ ] `harness-run-lib.sh`: add `hr_flow_host_exec <scripts_dir_abs> <console_script> [<arg>…]`.
  - It is `flow-walker.sh`'s `HAND-OFF` step 4, for any console script: it unsets `VIRTUAL_ENV`, then runs `UV_PROJECT_ENVIRONMENT=<py>/.venv PYTHONPATH=<py>/devscene-flow-host/src:<py>/graphscene/src PYTHONDONTWRITEBYTECODE=1 exec uv run --frozen --no-sync --no-cache --project <py>/devscene-flow-host <console_script> <arg>…`. Every name comes from the `HR_FLOW_HOST_*` mirror.
  - It never returns.
  - It sets no shell option, as the library's rule requires.
  - Its header comment carries the `NO ENVIRONMENT VARIABLE CHOOSES WHAT RUNS` and `--no-cache` reasons, moved here from `flow-walker.sh`'s header rather than copied. `flow-walker.sh` keeps a pointer to them.
- [ ] `flow-walker.sh`: `HAND-OFF` steps 3 and 4 become one call to `hr_flow_host_missing "$fw_dir" devscene-flow-walker` and one to `hr_flow_host_exec "$fw_dir" devscene-flow-walker "$@" ${fw_flows[@]+"${fw_flows[@]}"}`.
  - The refusal line `flow-walker: the flow host is not provisioned (<cause>): run bash <given>/flow-host-provision.sh outside the sandbox` and its exit `2` are byte-identical.
  - Step 1's predates-check also requires `hr_flow_host_missing` and `hr_flow_host_exec` to be defined, as it requires `hr_repo_root`.
  - Update the header's `HAND-OFF` text to say step 4 is the library's.

**Verification:**

- `flow-walker.sh`'s header `REPRO` block, run in a throwaway fixture that `npx devscene init` provisioned, gives each line's stated result. That covers the exit `0` start, the exit `2` unprovisioned refusal with its exact stderr line, and both `check-round-file` lines.
- `grep -n 'uv run' cli/templates/scripts/flow-walker.sh` prints nothing outside comments. The one `exec uv run` line under `cli/templates/scripts/` is `hr_flow_host_exec`'s.
- `bash -n` passes on both files, and the library still sets no shell option (`grep -nE '^set ' cli/templates/scripts/lib/harness-run-lib.sh` prints nothing new).
