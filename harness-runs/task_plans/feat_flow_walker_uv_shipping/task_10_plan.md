### Task 10 — Document the shipped packages and the provisioning script in the `cli` package's READMEs

**Goal:** Bring the three `cli/` READMEs that describe what the package ships and writes in line with Tasks 1–9. These are the scope register's rows 8, 11, 12 and 13.

**Depends on:**

- **Task 1:** the staged `dist/python/` tree.
- **Task 2:** `init` writes `<scriptsDir>/python/graphscene/` and `<scriptsDir>/python/devscene-flow-host/`, `create-if-absent`, and replaces them on `--upgrade`.
- **Task 3:** `flow-host-provision.sh`, run outside the sandbox, which builds `<scriptsDir>/python/.venv` with `uv sync --frozen --no-dev --no-editable`.
- **Task 7:** `--provision-python`.

Describe exactly those; invent nothing beyond them.

### Targets

- `cli/README.md`.
- `cli/templates/README.md`.
- `cli/templates/scripts/README.md`.

**Work:**

- [ ] `cli/README.md`:
  - The opening paragraph (*"Node `>=20.11.0`. Licence …"*) states that DevScene requires `uv` on the machines that run it, for its Python flow walker.
  - The layout paragraph (*"TypeScript in `src/` compiles with `tsc` to `dist/` …"*) adds two things:
    - the build stages `graphscene/` and `devscene-flow-host/` into `dist/python/`, and `init` copies them under `<scriptsDir>/python/`;
    - `flow-host-provision.sh` joins the outer-loop list.
- [ ] `cli/templates/README.md`: after the subdirectory table, one sentence: `<scriptsDir>/python/` is not written from this tree. `init` copies it from `dist/python/`, which the build stages from the repository root, so the sources are never committed twice.
- [ ] `cli/templates/scripts/README.md`, the paragraph opening *"**The other family in this directory is not generated.**"*:
  - Add `flow-host-provision.sh` to the copied set.
  - Add one sentence on who runs it: `init` when asked, a person, `doctor`'s remedy and `setup-worktree.sh`'s step 6 through the library, never an agent.
  - Add one sentence: `<scriptsDir>/python/` carries the two packages and the environment `.venv` the script builds.
  - The provisioning command sits in its own fenced block, one command per line (`harness-runs/lessons.md` → `## Adopter-facing documentation`).

**Verification:**

- Each sentence added names only behaviour Tasks 1–9 implement. Compare each against the named source: `cli/src/flowHost/layout.ts`, `cli/templates/scripts/flow-host-provision.sh` and `cli/src/commands/init.ts`'s `--provision-python` row.
- `grep -n "flow-host-provision.sh" cli/README.md cli/templates/scripts/README.md` finds the new mentions, and every command an adopter runs sits in a fenced block.
