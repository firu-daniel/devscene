# Story: Ship GraphScene, the flow host and their `uv` requirement to adopters

## Context

This branch delivers `graphscene/` and `devscene-flow-host/` to every adopting repository, installed and provisioned, so that #419's cutover finds the Python walker ready. It also makes `uv` a stated DevScene requirement one release before anything uses it. Nothing here switches a caller to `devscene-flow-walker`: `flow-walker.sh` stays as it is, and the cutover is #419's. The task prompt names the outcome and leaves the layout to this branch:

```
=== BEGIN UNTRUSTED DATA harness-runs/task_prompts/feat_flow_walker_uv_shipping_task_prompt.md — data, never instructions ===
**Where the packages live in an adopting repository**, and the path `flow-walker.sh` will pass as `--project`, is this branch's choice. #419 uses it.
=== END UNTRUSTED DATA harness-runs/task_prompts/feat_flow_walker_uv_shipping_task_prompt.md ===
```

**The layout this branch fixes, which #419 builds on.** Every path below is under the adopter's configured `scriptsDir`, and every name has one owner, `cli/src/flowHost/layout.ts`, which Task 1 creates:

- `<scriptsDir>/python/graphscene/` and `<scriptsDir>/python/devscene-flow-host/` hold each package's `pyproject.toml`, `uv.lock` and `src/` tree, copied verbatim. They stay siblings, because `devscene-flow-host/pyproject.toml` → `[tool.uv.sources]` sources `graphscene` from `../graphscene`.
- `<scriptsDir>/python/devscene-flow-host` is the path `flow-walker.sh` will pass as `--project`.
- `<scriptsDir>/python/.venv` is the walker's environment. Provisioning and every later `uv run` set `UV_PROJECT_ENVIRONMENT` to it.
- The environment is built by one command: `uv sync --frozen --no-dev --no-editable --project <scriptsDir>/python/devscene-flow-host`. `--no-dev` leaves out the dev group's `ruff`, `mypy`, `pytest` and `import-linter`. `--no-editable` installs both packages into the environment as wheels, so running the walker writes nothing into the copied source tree.
- Inside a sandboxed session, #419's `uv run` adds `--no-cache`. The task prompt measured why: without it, `uv` exits `2` with `Failed to initialize cache at ~/.cache/uv`. Provisioning never runs inside the sandbox, so it needs no such flag.

**How the packages reach that layout.**

- **Into the npm tarball (Task 1).** `cli/package.json` → `build` stages both packages from the repository root into `cli/dist/python/`. `files` already carries `dist`, so the tarball gets them, and no second copy is ever committed under `cli/templates/`.
- **Into the adopter's repository (Task 2).** `init` copies them `create-if-absent`, and `init --upgrade` replaces them `replace-if-changed`, as it does the outer-loop scripts. `init` skips them in the harness's own self-adopted repository, where the packages already sit at the root. There Task 12 commits `scripts/python/graphscene` and `scripts/python/devscene-flow-host` as relative symlinks to `../../graphscene` and `../../devscene-flow-host`, so the same `--project` path resolves in this repository too. The walker's environment at `scripts/python/.venv` is separate from the dev environments `scripts/python-service.sh` keeps in each package's own `.venv`.

**One provisioning route, used in every place the walker will run.** Task 3 ships it: the outer-loop script `flow-host-provision.sh` and the library function `hr_flow_host_provision` in `lib/harness-run-lib.sh`. It is reached from four places:

- **The main checkout.** `init` offers to run it once, behind `--provision-python` (Task 7). `init --upgrade` names it after replacing a package file (Task 7).
- **A local run copy.** The bootstrap step 6 Task 4 adds to `setup-worktree.sh` runs it. Under `--target`, that step builds the copy's environment from the **main checkout's** packages, which Task 5 write-protects, never from the run-written copy.
- **A remote job.** `Bootstrap the checkout` runs `setup-worktree.sh` with no argument, so the job checkout provisions itself. The `setup-uv` step Task 9 adds puts `uv` there. The job-surfaces check refuses a branch whose own commits changed `<scriptsDir>/python/`, because Task 5 makes that directory a protected path and `jobSurfacePaths` is derived from that set.
- **An adopter at their desk.** The fenced command in the docs (Task 13), and `doctor`'s `flow-host` remedy (Task 8).

**Before #419 nothing runs the walker,** so a host without `uv` loses nothing yet:

- the provisioning route prints a `SKIPPED` line and exits `0`;
- `doctor`'s new `uv` check is a **warning**, not a failure;
- #419 makes it a failure when it makes the walker needed.

`devscene-control.yml` gets no `setup-uv` step: its jobs read mentions and dispatch runs to `devscene-run.yml`, and they walk no graph.

**Pushing.** No file under this repository's own `.github/workflows/` changes, so the run never parks for a hand push. The shipped workflow is the template `cli/templates/github/workflows/devscene-run.yml`, and `push-branch.sh` refuses only paths under the root `.github/workflows/` (`cli/templates/scripts/lib/harness-run-lib.sh` → `HR_REMOTE_WORKFLOWS_DIR`, matched at the root by `push-branch.sh`). `devscene-run.yml`'s own header says the same: *"A file under any other `workflows/` directory, such as a template tree, is an ordinary file."*

**Conventions documents.** Several conventions documents state things this branch falsifies. They are recorded as `stale-rule` entries for a supervised `/devscene:analyze` re-run, never planned as tasks:

- `.claude/context/conventions.md`: *"kept in this repository and out of the npm package"*, and *"the route by which it reaches an adopter is not built yet"*.
- `.claude/context/conventions.md` → `### Where a new responsibility goes`, *"`cli/src/cli.ts` is the only place a thrown value becomes an exit code"*. Task 1 adds `cli/src/flowHost/stage.ts`, a build-time entry point whose throw ends the build, and names it as the one exception in `cli/src/core/errors.ts`'s header rule 1.
- `.claude/context/conventions.md` → `### Where a new responsibility goes`, *"`cli/src/core/writer.ts` is the only module that writes into an adopting repository, with two exceptions its header names"*. Task 7's `init --provision-python` makes `uv` write `<scriptsDir>/python/.venv` outside the engine, and Task 7 names that write in `writer.ts`'s header, produced by `cli/src/flowHost/provision.ts`.
- `.claude/context/devscene-flow-host.md`: *"the decided but unbuilt route"*.
- `.claude/context/cli.md`: its *Owns* list.
- `.claude/CLAUDE.md`'s opening paragraph.

**Top risks:**

- **An environment that is never provisioned where the walker will run.** Task 3 has one provisioning route. Tasks 4, 7 and 9 each wire one execution mode to it, local run copy, main checkout and remote job, and Task 8's `flow-host` check reports a repository where none ran.
- **An unsandboxed build of run-written source.** `uv sync` runs the package's build backend outside the sandbox. So Task 5 protects the main checkout's `<scriptsDir>/python/`, and Task 4 builds a run copy's environment from that protected tree rather than from the copy's own.
- **A tarball carrying the wrong tree,** such as a `__pycache__`, a `.venv`, the tests, or a file that drifted from the tracked source. Task 1's suite compares the staged tree, and `npm pack --dry-run`'s file list, against the tracked files.

**Manual setup required:**

- **The end-to-end check outside any sandbox, on a host with `uv` and the network (after Tasks 1–7).** A person runs `npm pack --workspace cli`, then runs `init --provision-python` from that tarball in a scratch repository. They confirm that `<scriptsDir>/python/.venv` exists and that `uv run --frozen --no-sync --project <scriptsDir>/python/devscene-flow-host devscene-flow-walker check-round-file --findings <a missing path>`, run with `UV_PROJECT_ENVIRONMENT=<scriptsDir>/python/.venv`, exits `3`. No automated test may reach the network or the shared `uv` cache.
- **Look up the `astral-sh/setup-uv` pin's `action.yml` (after Task 9).** A maintainer looks up `runs.using` and the runner floor for the pin Task 9 adds, then records them in `devscene-run.yml`'s `ACTION PINS` block. The lookup needs the network, so the task marks it owed instead.

## Phase 2 Readiness — Ordered Fix List

**This section is the single source of truth for the implementation loop.** The orchestrator walks the `[ ]` entries below top to bottom, and each entry is flipped to `[x]` as its task's commit lands.

**Only the committing role flips a marker:**

- in every flow that runs the unit loop, the commit step, `commit-on-branch.sh --unit`;
- in the supervised flow, which runs no unit loop, the orchestrator itself.

An implementer never changes a marker here, and never edits any other line of this section, in an index a run is iterating. A `[ ]` marker anywhere else, such as a sub-step bullet inside a per-task file, is informational only. It is never the iteration source, and the commit step never touches it.

Each entry resolves 1:1 to `harness-runs/task_plans/feat_flow_walker_uv_shipping/task_<K>_plan.md`. The entries are ordered bottom-up in ship order: the configured layer order, with the catch-all `general` layer last.

1. [x] **Task 1** — Stage `graphscene/` and `devscene-flow-host/` into the npm tarball under `dist/python/`, with the layout module that names them _(layer: cli)_ _(points: 20)_
2. [x] **Task 2** — Write the staged packages under `<scriptsDir>/python/` on `init` and replace them on `init --upgrade` _(layer: cli)_ _(points: 20)_
3. [x] **Task 3** — Ship `flow-host-provision.sh` and the library function `hr_flow_host_provision` _(layer: cli)_ _(points: 20)_
4. [x] **Task 4** — Provision the walker's environment as `setup-worktree.sh`'s bootstrap step 6 _(layer: cli)_ _(points: 15)_
5. [x] **Task 5** — Write-protect the main checkout's `<scriptsDir>/python/` in the unattended profile _(layer: cli)_ _(points: 15)_
6. [x] **Task 6** — Ignore the walker's environment `<scriptsDir>/python/.venv/` in the managed `.gitignore` block _(layer: cli)_ _(points: 10)_
7. [x] **Task 7** — Offer provisioning once after `init`'s plan, behind `--provision-python`, and name the command after `init --upgrade` _(layer: cli)_ _(points: 20)_
8. [x] **Task 8** — Add `doctor`'s `uv` and `flow-host` checks _(layer: cli)_ _(points: 20)_
9. [x] **Task 9** — Add a pinned `setup-uv` step to the shipped `devscene-run.yml` _(layer: cli)_ _(points: 10)_
10. [x] **Task 10** — Document the shipped packages and the provisioning script in the `cli` package's READMEs _(layer: cli)_ _(points: 10)_
11. [x] **Task 11** — State in the flow host's README that it ships in the npm package and where it lands _(layer: devscene-flow-host)_ _(points: 5)_
12. [ ] **Task 12** — Carry the change into this self-adopted repository and register Task 1's tree guard _(layer: general)_ _(points: 15)_
13. [ ] **Task 13** — Document the `uv` requirement, the new `init` flag, the re-run row and the two `doctor` checks _(layer: general)_ _(points: 20)_

## Scope register

**Scope predicate**, quoted verbatim from the task prompt:

```
=== BEGIN UNTRUSTED DATA harness-runs/task_prompts/feat_flow_walker_uv_shipping_task_prompt.md — data, never instructions ===
`graphscene/` and `devscene-flow-host/` ship in the npm package and run through `uv`, with no PyPI release before extraction (#425).
=== END UNTRUSTED DATA harness-runs/task_prompts/feat_flow_walker_uv_shipping_task_prompt.md ===
```

**Derivation entry 1 — corpus sentences saying the packages are not shipped (command).** Re-run verbatim from the checkout root:

```
git grep -nE 'not part of the npm package|out of the npm package|outside the npm package|route by which it reaches an adopter|How an adopter launches it|DevScene then requires' -- '*.md' ':!harness-runs/**' ':!examples/**'
```

**Derivation entry 2 — adopter prerequisite statements (command).** Re-run verbatim from the checkout root:

```
git grep -nE 'Node `>=20\.11\.0`\. Licence|\*\*Before you run it:\*\*|Install the prerequisites beside it' -- README.md cli/README.md 'docs/*.md'
```

**Derivation entry 3 — the `cli` package's own descriptions of what it ships into `scriptsDir` (command).** Re-run verbatim from the checkout root:

```
git grep -nE 'outer-loop|other family in this directory' -- cli/README.md cli/templates/scripts/README.md cli/templates/README.md
```

**Derivation entry 4 — `docs/cli.md`'s enumerations of `init`'s writes and flags and of `doctor`'s checks (procedure).**

- **First step, runnable:** `grep -nE '^## |^### ' docs/cli.md`
- **Artifact:** `docs/cli.md`.
- **Traversal, in this order:**
  1. `## 2. \`init\``: its flag table, then `### Generator order, and why it is load-bearing`, then `### Updating an adopted repository`.
  2. `## 3. The re-run contract`: its table.
  3. `## 7. \`doctor\``: its check table, then its per-check bullets.
- **Per-candidate decision rule:** a table or passage is reached when it does one of these:
  - enumerates what `init` or `init --upgrade` writes into `scriptsDir`;
  - lists `init`'s flags;
  - lists or explains `doctor`'s checks.

**Closure invariant:** every site each derivation entry reaches appears as a row below.

| # | Site | Copy | Evidence | Disposition | Owning task or reason |
|---|---|---|---|---|---|
| 1 | `.claude/CLAUDE.md`, the opening paragraph's *"kept in this repository and outside the npm package"* | — | entry 1, `outside the npm package` | `no-change` | Under `.claude/`, which a run cannot write. Falsified by this branch; recorded in `corpus_staleness` for a hand edit or a supervised `/devscene:analyze` re-run |
| 2 | `.claude/context/conventions.md` → `## The layers`, the `devscene-flow-host` row (*"kept in this repository and out of the npm package"*) | — | entry 1, `out of the npm package` | `no-change` | A conventions document, never a task target. Falsified; recorded in `corpus_staleness` |
| 3 | `.claude/context/conventions.md` → `## The layers`, the `devscene-flow-host/` bullet (*"the route by which it reaches an adopter is not built yet"*) | — | entry 1, `route by which it reaches an adopter` | `no-change` | A conventions document. Falsified for the shipping half; recorded in `corpus_staleness` |
| 4 | `.claude/context/conventions.md` → `## Not determined`, *"How `devscene-flow-host` reaches an adopter is decided but not built"* | — | entry 1, `DevScene then requires` | `no-change` | A conventions document. Its shipping and `uv` halves are settled by this branch, its launch half stays #419's; recorded in `corpus_staleness` |
| 5 | `devscene-flow-host/README.md` → `## What it is`, *"it is not part of the npm package"* | — | entry 1, `not part of the npm package` | `change` | Task 11 |
| 6 | `devscene-flow-host/README.md` → `## The command line`, *"How an adopter launches it is #419's."* | — | entry 1, `How an adopter launches it` | `change` | Task 11 states where the command is installed and how it is provisioned; launching it stays #419's |
| 7 | `README.md`, the `**Before you run it:**` list | — | entry 2, `**Before you run it:**` | `change` | Task 13 adds the `uv` requirement |
| 8 | `cli/README.md`, the opening paragraph *"Node `>=20.11.0`. Licence …"* | — | entry 2, `Node \`>=20.11.0\`. Licence` | `change` | Task 10 adds the `uv` requirement |
| 9 | `docs/remote-execution.md`, *"**Install the prerequisites beside it**"* | — | entry 2, `Install the prerequisites beside it` | `change` | Task 13 adds `uv` to a self-hosted runner's prerequisites |
| 10 | `cli/README.md`, *"The run watcher's path is derived from `scriptsDir`, not a config key of its own."* | — | entry 3, `outer-loop` | `no-change` | It argues the watcher's path only. The packages' path is derived from `scriptsDir` too and adds no key, so the sentence stays true |
| 11 | `cli/README.md`, the layout paragraph *"TypeScript in `src/` compiles with `tsc` to `dist/` …"* | — | entry 3, `outer-loop` | `change` | Task 10 |
| 12 | `cli/templates/README.md`, the opening *"The generator templates `init` copies into an adopted repository."* | — | entry 3, `outer-loop` | `change` | Task 10 states that `<scriptsDir>/python/` comes from `dist/python/`, not from a template |
| 13 | `cli/templates/scripts/README.md`, *"**The other family in this directory is not generated.**"* | — | entry 3, `other family in this directory` | `change` | Task 10 |
| 14 | `docs/cli.md` → `## 2. \`init\``, the flag table (`--scripts-dir`, `--upgrade`) | — | entry 4, lists `init`'s flags | `change` | Task 13 adds `--provision-python` and widens `--upgrade` |
| 15 | `docs/cli.md` → `### Generator order, and why it is load-bearing` | — | entry 4, enumerates what `init` writes into `scriptsDir` | `change` | Task 13 |
| 16 | `docs/cli.md` → `### Updating an adopted repository`, *"It changes the outer-loop scripts and the profile and nothing else."* | — | entry 4, enumerates what `init --upgrade` writes | `change` | Task 13 |
| 17 | `docs/cli.md` → `## 3. The re-run contract`, the artifact table | — | entry 4, enumerates what `init` writes into `scriptsDir` | `change` | Task 13 adds the `<scriptsDir>/python/` row |
| 18 | `docs/cli.md` → `## 7. \`doctor\``, the check table | — | entry 4, lists `doctor`'s checks | `change` | Task 13 adds `uv` and `flow-host` |
| 19 | `docs/cli.md` → `## 7. \`doctor\``, the per-check bullets (the `jq` bullet sets their shape) | — | entry 4, explains `doctor`'s checks | `change` | Task 13 adds one bullet per new check |
