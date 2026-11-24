### Task 11 — State in the flow host's README that it ships in the npm package and where it lands

**Goal:** Correct the two sentences in `devscene-flow-host/README.md` that this branch falsifies: the scope register's rows 5 and 6.

**Depends on:**

- **Task 1:** the npm package carries this package's `pyproject.toml`, `uv.lock` and `src/` under `dist/python/devscene-flow-host/`.
- **Task 2:** `init` writes them to `<scriptsDir>/python/devscene-flow-host/`, beside `<scriptsDir>/python/graphscene/`.
- **Task 3:** `bash <scriptsDir>/flow-host-provision.sh` builds the environment `<scriptsDir>/python/.venv` with `uv sync --frozen --no-dev --no-editable`.

**Where this task stops.** Launching the command for every `flow-walker.sh` caller stays #419's. This task says where the command is installed and how its environment is built, not who runs it.

### Targets

- `devscene-flow-host/README.md`.

**Work:**

- [ ] `## What it is`: replace *"It stays in this repository: it is not part of the npm package (`cli/package.json` → `files`), and adopters never import it."* The replacement states:
  - its source stays in this repository;
  - the npm package carries it, with `graphscene/`, under `dist/python/`;
  - `init` copies both under an adopter's `<scriptsDir>/python/`;
  - adopters still never import it and reach it only through the scripts `init` writes.
- [ ] `## The command line`, the closing *"How an adopter launches it is #419's."*: keep that clause. Add before it one sentence naming the adopter-side project path `<scriptsDir>/python/devscene-flow-host` and the provisioning command, in its own fenced block:

  ```
  bash <scriptsDir>/flow-host-provision.sh
  ```

  Add one sentence: the adopter-side environment is `<scriptsDir>/python/.venv`, set through `UV_PROJECT_ENVIRONMENT`, and is not this repository's `scripts/python-service.sh` environment.

**Verification:**

- `grep -n "not part of the npm package" devscene-flow-host/README.md` finds nothing.
- Each new statement matches the paths `cli/src/flowHost/layout.ts` exports and the argv `cli/templates/scripts/lib/harness-run-lib.sh` → `hr_flow_host_provision` runs.
