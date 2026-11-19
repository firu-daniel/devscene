### Task 3 — Bootstrap provisions the Python packages through `commands.depInstall`, and `run-gates.sh`'s gate-13 remedy names `provision`

**Goal:** Give every run copy a synced Python environment before its first gate round, by having the bootstrap that already installs its npm dependencies also run the wrapper's `provision`. Make gate 13's `BLOCKED` remedy name the sub-command that now clears it.

**Depends on:** Task 1. It adds `bash scripts/python-service.sh provision`, which takes no argument and does the following:

- It syncs every package in the wrapper's table (today `docs-retrieval-service`) with `uv sync --frozen --group dev` into `<package>/.venv`, using the machine's shared `uv` cache.
- It prints `python-service: provisioned <package>` per package.
- It exits `0` with one stderr line containing `SKIPPED` when `uv` is not on `PATH`, so a Python-less host still bootstraps.
- It exits `1` when any sync failed.

This task calls that contract and changes no line of the wrapper.

**How the bootstrap reaches it.** `scripts/setup-worktree.sh` step 5 reads `commands.depInstall` from the **main** checkout's `devscene.config.json`. It `eval`s the line in a subshell `cd`'d to the checkout being bootstrapped: the run copy under `--target`, or its own checkout with no argument, which is the GitHub job's `Bootstrap the checkout` and a person's by-hand run. A non-zero status fails the bootstrap, and `create-worktree.sh` then removes the copy. So the relative `bash scripts/python-service.sh provision` runs the copy's own wrapper, unsandboxed and with the network, inside the residual that script's header already names (`THE RESIDUAL --target DOES NOT CLOSE`: a run-written `package.json` lifecycle entry already reaches arbitrary code through `npm ci`). The change takes effect for run copies once this branch is on the main checkout's branch. This branch's own copy was bootstrapped with the old line.

### Targets

- `devscene.config.json` (repository root)
- `scripts/run-gates.sh`

**Work:**

- [ ] `devscene.config.json`: set `commands.depInstall` to `npm ci && bash scripts/python-service.sh provision`. `npm ci` comes first, so a failed install is reported as one, and the `&&` keeps `provision` from running after it. Change no other key.
- [ ] `scripts/run-gates.sh` → `python_gate`'s `BLOCKED` arm: the gate line's reason becomes `uv or the synced Python environment is missing; run bash scripts/python-service.sh provision outside the sandbox (a run copy's bootstrap runs it)`.
- [ ] `scripts/run-gates.sh` → the closing `== gates this script cannot run` block, and the `hand_run` line: where each now says `bash scripts/python-service.sh sync`, it says `bash scripts/python-service.sh provision`, and adds that a run copy's bootstrap runs it wherever `uv` is on `PATH`. The rest of each sentence (the `BLOCKED` list, "ran no Python", "listed here until then") is kept as it is.
- [ ] `scripts/run-gates.sh` → the `# Gate 13's legs.` comment above `python_gate`: one sentence noting that status 3 in a run copy means its bootstrap found no `uv`, or ran before `provision` was wired into `commands.depInstall`. Status 3 stays `BLOCKED` on gate 11's terms. Change no grading, no unit id, no leg command.

**Verification:**

- `jq -r .commands.depInstall devscene.config.json` prints exactly `npm ci && bash scripts/python-service.sh provision`.
- `grep -n 'python-service.sh sync' scripts/run-gates.sh` prints nothing.
- `grep -n 'python-service.sh provision' scripts/run-gates.sh` prints the gate line's reason, the closing block's line and the `hand_run` line.
- `git diff scripts/run-gates.sh` touches only message strings and comments: no `case` arm, no `python_gate` call, no `gr_run_round` argument changed.
