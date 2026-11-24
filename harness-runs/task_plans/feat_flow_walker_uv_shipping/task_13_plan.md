### Task 13 — Document the `uv` requirement, the new `init` flag, the re-run row and the two `doctor` checks

**Goal:** Bring the root documentation in line with what Tasks 1–9 built. These are the scope register's rows 7, 9 and 14–19.

**Depends on:** Tasks 1–9. Each fact below is restated from its owner:

- **Task 2:** `init` writes `<scriptsDir>/python/graphscene/` and `<scriptsDir>/python/devscene-flow-host/` `create-if-absent`, and `init --upgrade` replaces them `replace-if-changed`. Both are skipped in the harness's own self-adopted repository.
- **Task 3:** `bash <scriptsDir>/flow-host-provision.sh`, no argument, run outside the sandbox, builds `<scriptsDir>/python/.venv` with `uv sync --frozen --no-dev --no-editable`. With no `uv` it prints `SKIPPED` and exits `0`.
- **Task 4:** `setup-worktree.sh` step 6 runs the same route. With `--target` it builds from the main checkout's packages.
- **Task 5:** the main checkout's `<scriptsDir>/python/` is write-protected and is a job surface.
- **Task 7:** `--provision-python`; without it, a TTY is asked and a non-interactive run skips with a note. `init --upgrade` names the command after replacing a package file.
- **Task 8:** `doctor`'s `uv` and `flow-host` checks, both warnings, never failures.
- **Task 9:** the `Set up uv` step, before `Preflight with doctor`.

### Targets

- `README.md`.
- `docs/cli.md`.
- `docs/remote-execution.md`.

**Work:**

- [ ] `README.md`, the `**Before you run it:**` list: add a bullet stating that DevScene requires `uv` on every machine that runs it, for its Python flow walker, with one fenced block per command an adopter runs, one command per line (`harness-runs/lessons.md` → `## Adopter-facing documentation`). Name `uv`, not "the flow host", as the term an adopter arrives with.
- [ ] `docs/cli.md` → `## 2. \`init\``:
  - The flag table gains a `--provision-python` row, and the `--upgrade` row's replaced set gains the Python packages.
  - `### Generator order, and why it is load-bearing` places the packages beside the outer-loop scripts and states the self-adoption skip.
  - `### Updating an adopted repository`'s *"It changes the outer-loop scripts and the profile and nothing else."* names the Python packages too, and gives the provisioning command, in its own fenced block, to run after an upgrade.
- [ ] `docs/cli.md` → `## 3. The re-run contract`: a row for `<scriptsDir>/python/` with its two policies and why, matching `cli/src/core/writer.ts`'s header row word for word in substance. `## 7. \`doctor\``: two check-table rows, `uv` and `flow-host`, with the titles `cli/src/doctor/checks.ts` gives them. Then one per-check bullet each, in the `jq` bullet's shape, stating why each is a warning before #419 and what each remedy runs.
- [ ] `docs/remote-execution.md`, *"**Install the prerequisites beside it**"*: add `uv` to a self-hosted runner's list. Next to the passage that describes the run job's steps before `Bootstrap the checkout`, add one sentence on `Set up uv`: pinned, cache off, after the job-surfaces refusal. Locate that passage with `grep -n "Bootstrap the checkout\|Preflight with doctor" docs/remote-execution.md`.

**Verification:**

- Every flag, check id, check title and command named matches its source: `cli/src/commands/init.ts` → `INIT_OPTIONS`, `cli/src/doctor/checks.ts` → `UV_CHECK` and `FLOW_HOST_CHECK`, and `cli/templates/scripts/flow-host-provision.sh`.
- Every command an adopter runs sits alone in a fenced block.
- Re-run the story index's derivation entries 1, 2 and 4. Every site they reach is a register row, and rows 7, 9 and 14–19 now read as this task states.
