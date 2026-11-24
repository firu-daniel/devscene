### Task 15 — Document `init`'s default provisioning in `docs/cli.md` and the root README

**Goal:** The adopter-facing documents say what Tasks 4 and 5 made true:
- `init` builds the flow walker's environment by default, `--no-provision-python` opts out, and `--provision-python` is accepted as the default's explicit form;
- a run that cannot be prompted builds too;
- `uv` is required: `doctor` fails without it, and `setup-worktree.sh` step 6 fails a bootstrap without it.

**Depends on:**
- **Task 4.** `init` runs `bash <scriptsDir>/flow-host-provision.sh` after the plan unless one of these holds: `--dry-run`; `--upgrade`; `--no-provision-python`; or an environment that already exists with no shipped package file changed. `--upgrade` refuses both flags, and the two flags together are refused. A failed build is a warning naming the command, and never fails `init`.
- **Task 5.** `doctor`'s `uv` check fails when `uv` is absent. `flow-host` warns on an unprovisioned environment, or fails where `execution.scriptDrivenPlanning` is on.
- **Task 3.** `setup-worktree.sh` step 6 fails without `uv` or a project.

### Targets

- `docs/cli.md`:
  - the flag table's `--provision-python` row, and a new `--no-provision-python` row;
  - the `init` step list's item 6, *"Build the flow walker's Python environment"*;
  - the paragraph opening *"Building the flow walker's environment is a post-plan step too"*.
- `README.md` — the install block carrying `npx devscene init --provision-python`.

**Work:**

- [ ] `docs/cli.md` flag table:
  - the `--provision-python` row: accepted, and the default's explicit form;
  - a `--no-provision-python` row: skip the build, leaving a note naming the command;
  - both rows say `--upgrade` refuses them.
- [ ] `docs/cli.md` item 6 and the post-plan paragraph:
  - the default is now *built*, in every run, prompted or not, because the walker is required and a repository without its environment cannot plan;
  - the build still reaches the network and takes minutes, still runs after the plan and before the adoption commit, never runs under `--dry-run`, and never fails `init`;
  - a failure is a warning naming `bash <scriptsDir>/flow-host-provision.sh` to run outside the sandbox.

  Remove the sentence that says the default is *"not built"*.
- [ ] `README.md`: the install block's `npx devscene init --provision-python` becomes `npx devscene init`, alone on its line in the same fenced block. One sentence beside the block says `uv` must be on `PATH`, because `init` builds the flow walker's environment with it.

**Verification:**

- `git grep -n -e 'default: not built' -e 'init --provision-python' -- docs/cli.md README.md` prints nothing.
- Every command these edits hand a reader sits in its own fenced block, one command per line (`<state_dir>/lessons.md` → *"Every command an adopter is meant to run sits in a fenced block"*).
- The flag names in `docs/cli.md` match `cli/src/commands/init.ts` → `PROVISION_PYTHON_FLAG` and `NO_PROVISION_PYTHON_FLAG` byte for byte.
