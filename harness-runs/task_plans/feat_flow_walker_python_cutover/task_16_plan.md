### Task 16 — Bring the provisioning and bootstrap suites to failing provisioning, and hold the new layout mirror equal

**Goal:** After Task 3, `hr_flow_host_provision` **fails** with no `uv` or no project, so `setup-worktree.sh` step 6 fails the bootstrap. This task brings every existing suite that runs `setup-worktree.sh` or the provisioning route, and asserts its exit status or its step-6 lines, to that outcome. The suites fall into two groups:
- **Provisioning is the subject.** The suite asserts the new failing outcome.
- **Provisioning is not the subject.** The suite's hand-built fixture is given a flow-host project and a stub `uv`, so step 6 passes and the case keeps testing what it tests.

It also holds the gate library's six `HR_FLOW_HOST_*` names equal to their owners.

**Depends on:**
- **Task 3**, which fixes these outcomes in `cli/templates/scripts/lib/harness-run-lib.sh`:
  - **no `uv` on `PATH`:** stderr `flow-host: provision: failed — uv is not on PATH; install uv, then run bash <env_scripts_dir>/flow-host-provision.sh outside the sandbox`, return `1`;
  - **no `<project>/pyproject.toml`:** stderr `flow-host: provision: failed — no flow host at <project>; run npx devscene init --upgrade`, return `1`, with `uv` never run;
  - **in `setup-worktree.sh`:** a non-zero return from step 6 sets `status=1` and prints the existing `step 6 (flow-host provision) failed` line;
  - **the layout names:** `HR_FLOW_HOST_DIRNAME` `python`, `HR_FLOW_HOST_PROJECT` `devscene-flow-host`, `HR_FLOW_HOST_GRAPHSCENE` `graphscene`, `HR_FLOW_HOST_ENV_DIRNAME` `.venv`, `HR_FLOW_HOST_SOURCE_DIRNAME` `src` and `HR_FLOW_HOST_ENV_MARKER` `pyvenv.cfg`. They are set when the library is sourced and mirror `cli/src/flowHost/layout.ts` → `FLOW_HOST_DIRNAME`, `FLOW_HOST_PROJECT`, the `graphscene` entry of `FLOW_HOST_PACKAGES`, `FLOW_HOST_ENV_DIRNAME`, `FLOW_HOST_SOURCE_DIRNAME` (new in Task 3), and `cli/src/flowHost/provision.ts` → `ENV_MARKER_FILE`.
- **Task 4**, which exports `ENV_MARKER_FILE` from `provision.ts`.

**The set of suites, and how it was derived.** Run `git grep -ln 'setup-worktree' -- cli/test`, then keep each suite that runs `setup-worktree.sh` and asserts its status or its step-6 lines. Add `cli/test/flow-host-provision.test.mjs`, which runs the provisioning route directly.

The other hits name the script without running it, or run a stub in its place (`create-worktree.test.mjs` writes `exit 3` over it). The watcher fixture's bootstraps run `init`, so they carry a project, and its stub `uv` answers step 6's sync with `exit 0`. An implementer who finds a further suite meeting the rule brings it in under this task.

### Targets

- `cli/test/flow-host-provision.test.mjs` — the two `SKIPPED` cases, the suite header, and the layout-literal case.
- `cli/test/setup-worktree-flow-host.test.mjs` — cases (c) and (d), and the suite header.
- `cli/test/setup-worktree-clone-target.test.mjs` — the hand-built main checkout its cases bootstrap.
- `cli/test/setup-worktree-checkout-sparse.test.mjs` — the hand-built main checkout its cases bootstrap.

**Work:**

- [ ] `flow-host-provision.test.mjs`:
  - retitle and rewrite *"no flow host is a SKIPPED line and exit 0, with uv never run"* and *"no uv on PATH is a SKIPPED line naming this script, and exit 0"*. Each asserts exit `1` and its exact `failed —` line from Task 3, and the first still asserts that `uv` never ran;
  - restate the suite header's rule, *"a `SKIPPED` line and exit 0"*, to the failing outcomes.
- [ ] `flow-host-provision.test.mjs` → *"the library spells the three layout literals as cli/src/flowHost/layout.ts exports them"*:
  - retitle the case to the six names;
  - source the library in `bash` and print each `HR_FLOW_HOST_*` value;
  - assert each equals its owner's export, imported from `../dist/flowHost/layout.js` and `../dist/flowHost/provision.js` (`ENV_MARKER_FILE`), with `graphscene` taken as the `FLOW_HOST_PACKAGES` entry that is not `FLOW_HOST_PROJECT`.

  This case is the test `layout.ts`'s and `provision.ts`'s `MIRRORS.` notes name.
- [ ] `setup-worktree-flow-host.test.mjs`. Retitle and rewrite (c) *"No uv on PATH is a SKIPPED line and exit 0"* and (d) *"No flow-host project is a SKIPPED line and exit 0, with uv never run"*:
  - each asserts exit `1`, its `flow-host: provision: failed — …` line, and the `step 6 (flow-host provision) failed` line, as (e) asserts it;
  - (d) still asserts that `uv` never ran.

  Restate the header's rule, *"a missing `uv` or a missing project is a `SKIPPED` line and exit 0"*, to the failing outcomes.
- [ ] `setup-worktree-clone-target.test.mjs` and `setup-worktree-checkout-sparse.test.mjs`. Their subject is the bootstrap's git configuration, not provisioning. In each suite's fixture builder for the main checkout:
  - plant a minimal `<scriptsDir>/python/devscene-flow-host/pyproject.toml`;
  - put a stub `uv` that exits `0` first on the `PATH` every `setup-worktree.sh` run uses, written as `cli/test/setup-worktree-flow-host.test.mjs` writes its stub.

  Every case asserting the bootstrap's `status 0` then keeps that assertion unchanged. Add one sentence to each header saying why the fixture carries them: step 6 fails a bootstrap with no `uv` or no project.

**Verification:**

- Run `commands.typecheck`; it must exit 0.
- Run each of this task's four edited test files through `npm test --workspace cli -- test/<name>.test.mjs`: `flow-host-provision`, `setup-worktree-flow-host`, `setup-worktree-clone-target` and `setup-worktree-checkout-sparse`.
- `git grep -n -e 'provision: SKIPPED' -e 'SKIPPED line' -- cli/test/flow-host-provision.test.mjs cli/test/setup-worktree-flow-host.test.mjs cli/test/setup-worktree-clone-target.test.mjs cli/test/setup-worktree-checkout-sparse.test.mjs` prints nothing. The grep is held to this task's four targets on purpose: `cli/test/python-service.test.mjs` keeps its own `SKIPPED` case, which tests `scripts/python-service.sh provision`, a different script this branch does not change, and `cli/test/init-provision-python.test.mjs` is Task 4's.
