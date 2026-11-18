### Task 2 — Refuse an invalid round file in the walker and expose the check

**Goal:** A plan round gate's invalid round file never records a verdict and never reaches the plan writer. The walker sends that gate back within the same round, and a prose-routed flow can run the same check.

**Depends on:** Task 1, which provides `fw_round_file_check <file>`: status 0 and no output when valid, status 1 and one reason line on stdout when invalid. It also provides `plantMalformedReview(dir, folder, n, lacking)` in `cli/test/helpers/walker.mjs`, with `lacking` `'Class'` or `'Failure'`, returning the repo-relative path.

**Where this task stops.** The driver test and the state-dir READMEs are Task 3's. The orchestrator prose is Task 12's, and it consumes the `refused:` line and the `check-round-file` command defined here.

### Targets

- `cli/templates/scripts/flow-walker.sh`
- `cli/test/flow-walker-fan-out.test.mjs`

**Source:** `cli/templates/scripts/flow-walker.sh` (`record_in_set`, `render_set`, `close_round`).

**Work:**

- [ ] Add the subcommand `check-round-file --findings <path>`. It takes no `--flow` or `--branch` and refuses them. It runs before configuration and graph loading. A relative path resolves against `hr_repo_root`. A valid file exits 0 and prints nothing. An invalid file, an absent one included, exits 3 with one stderr line, `flow-walker: <path>: <reason>`; no other path through the script exits 3, so that status means only that the walker read the named path and found it invalid. A usage refusal (a refused `--flow` or `--branch`, a missing `--findings`) exits 1 through `refuse`. Outside a repository it exits 2 through `fault`. Update the subcommand errors to name all four subcommands.
- [ ] In `record_in_set`, before a gate's `PASS` or `FAIL` is recorded, run `fw_round_file_check` on `--findings`, an absolute path as given and a relative one under `$ROOT`. On a refusal record no verdict. Increment `round.refused.<gate>`, store the reason in `round.refusal.<gate>`, and mark the gate for re-dispatch with `round.redo.<gate>`. At the third refusal for that gate in the round, set `round.held.<gate>` to `error` instead of marking it. A valid return clears the gate's `round.redo.<gate>`. Name the limit once, as `FW_ROUND_FILE_ATTEMPTS=3`.
- [ ] Separate two sets in the set logic. `render_set` still prints a block for every unrecorded gate, so `current` can recover them. `pending:` lists only gates with no recorded outcome and no redo mark. While any such gate is outstanding, print `wait`; a refusal prints `refused: <gate> attempt <n> of 3: <reason>` where a recorded outcome prints `recorded:`. When none is outstanding, in this order: any held gate prints the existing held binding plus one `refused:` line for each gate held by refusal; otherwise any redo mark clears all redo marks and prints the unrecorded gates' dispatch blocks as one set, with one `refused:` line per gate among the first block's passed-through lines; otherwise the round closes as today.
- [ ] `close_round` clears `round.refused.*`, `round.refusal.*` and `round.redo.*` for every gate. A refusal moves neither the round number nor `counter.iteration`. Update the header's `USAGE`, `ROUNDS`, `OUTPUT`, `EXIT CODES`, `STATE` and `REPRO` blocks. `EXIT CODES` gains `3`, `check-round-file` only: the named round file is invalid, and states that this command's usage refusals stay `1` and its faults `2`. The `REPRO` block must plant real round files, because `--findings` now has to name a valid file.
- [ ] In `cli/test/flow-walker-fan-out.test.mjs`, extend the header rule and add cases, each with literal expected output: a refused gate waits for its siblings, then is dispatched alone at the same `arg.iteration` with no `round:` line and no writer block; a corrected return closes the round and the writer's `arg.findings_file` lines name the replaced file; two refused gates come back as one set; a third refusal prints `binding: <escalate>`, `reason: error`, `held: <gate> error` and its `refused:` line with no writer dispatch; `current` during the wait re-prints the refused gate's block; a `PASS` file with a numbered Must Fix entry is refused; `check-round-file` covers exit 0 on a valid file, exit 3 with its one stderr line on an invalid file and on an absent one, exit 1 on a refused `--flow` and on a missing `--findings`, and exit 2 outside a repository.

**Verification:**

- `npm test --workspace cli -- test/flow-walker-fan-out.test.mjs` passes.
- Following the header's updated `REPRO` in a throwaway fixture produces the outputs it states.
- `grep -n 'FW_ROUND_FILE_ATTEMPTS' cli/templates/scripts/flow-walker.sh` shows one assignment and every use reads that name.
