### Task 9 — Self-adopt `scripts/review-sweep.sh` and list it in the watcher's script table

**Goal:** Give this repository's own checkout the script its `init` would now write, byte-identical to the template (task prompt, constraints: a self-adopted copy outside `.claude/` is re-rendered and byte-identical). Then record the script in the documentation's outer-loop script table.

**Depends on:**
- **Task 2:** `cli/templates/scripts/review-sweep.sh`, which this task copies verbatim. Outer-loop scripts carry no token (`docs/watcher.md`: *"carry **no token at all** and are copied verbatim"*).
- **Task 3:** the script's `OUTER_LOOP_SCRIPTS` row, `agentInvocable: true`, which is what the table's "Profile allow entry" column reports.

**How this task's implementer reads the conventions.** This is the catch-all layer, so its implementer reads every configured layer's conventions document: `.claude/context/conventions.md`, `.claude/context/cli.md` and `.claude/context/plugin.md`.

**Where this task stops.** The machine-local `.claude/settings.autonomous.json` and this repository's `.claude/review-sweep.md` are under `.claude/` and are the user's after merge (story index, `Manual setup required:`). This task writes neither.

### Targets

- `scripts/review-sweep.sh` (new) — the self-adopted copy.
- `docs/watcher.md` — the outer-loop script table.

**Work:**

- [ ] `scripts/review-sweep.sh`: copy `cli/templates/scripts/review-sweep.sh` byte for byte, with mode `0755`, matching how the other self-adopted outer-loop scripts in `scripts/` are committed.
- [ ] `docs/watcher.md`: add a `review-sweep.sh` row to the outer-loop script table, after `prompt-injection-screen.sh`.
  - **What it does:** applies the rows of `.claude/review-sweep.md`, as the default branch commits it, to the branch's added lines, and prints `<path>:<line>: <escape class>` per hit; exit `0` means no hit, `1` hits, `2` a configuration error.
  - **Who runs it:** the end-of-branch reviewer, as the main checkout's copy.
  - **Profile allow entry:** **yes**.

**Verification:**

- `cmp cli/templates/scripts/review-sweep.sh scripts/review-sweep.sh` exits zero.
- `git ls-files -s scripts/review-sweep.sh` shows mode `100755`, once the file is staged by the commit step.
- `git grep -n -F 'review-sweep.sh' -- docs/watcher.md` prints the new row.

**Deviations from plan:**

- `scripts/review-sweep.sh` was written with the Write tool from the template's content, because the session's permission mode refused `cp` (*"Permission to use Bash has been denied because Claude Code is running in don't ask mode"*). `cmp cli/templates/scripts/review-sweep.sh scripts/review-sweep.sh` exits zero with no output, so the bytes match.
- **Mode `0755` not set.** `chmod 0755 scripts/review-sweep.sh` was refused with the same denial, and `ls -l` shows the file as `-rw-r--r--`. Committed as it stands, the file would get mode `100644`, not `100755`, so the `git ls-files -s` verification would fail. To fix: run `chmod 0755 scripts/review-sweep.sh` from the checkout root before the commit step.
