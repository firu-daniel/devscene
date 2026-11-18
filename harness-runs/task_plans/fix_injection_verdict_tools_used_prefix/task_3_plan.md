### Task 3 — Bring this repository's `scripts/prompt-injection-screen.sh` level with the template

**Goal:** Make this repository's self-adopted screen script byte-identical to the template Task 1 changed, because runs here execute this copy from the main checkout.

**Depends on:** Task 1, which changes `cli/templates/scripts/prompt-injection-screen.sh`: the new `pis_is_tools_used_line`, the changed `pis_unwrap_vlines`, and the amended header comments. That file is the source for this task, and this task makes no change of its own to the logic.

**Why an edit and not `init --upgrade`.** An outer-loop script is copied verbatim, so a byte-identical file is what a render produces. The documented self-adopt route (`docs/development.md`, `HARNESS_SELF_ADOPT=1 node cli/dist/cli.js init --upgrade`) also rewrites the permission profile, and neither it nor `cp` is in the unattended profile's allow list.

### Targets

- `scripts/prompt-injection-screen.sh`

**Work:**

- [ ] Read the template, and apply the same changes to `scripts/prompt-injection-screen.sh` with the file-edit tool, so the two files have identical bytes. The two were identical before Task 1, so the changes are exactly that task's diff of the template.

**Verification:**

- **The contents are identical.** `git diff --no-index --numstat cli/templates/scripts/prompt-injection-screen.sh scripts/prompt-injection-screen.sh` reports `0` added and `0` deleted lines. Read those two fields and not the exit status: the command exits 1 on correct work, because the template is mode `100644` and the adopted copy `100755` by design. Change neither mode to make it exit 0.
- **The adopted copy keeps its mode.** While the edit is still uncommitted, `git diff --summary HEAD -- scripts/prompt-injection-screen.sh` prints nothing. A `mode change` line means the edit altered the file's committed mode.
- `git diff --name-only HEAD` lists no other script under `scripts/`.
