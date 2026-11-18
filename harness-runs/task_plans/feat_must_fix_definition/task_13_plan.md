### Task 13 — Record the round-file check decision

**Goal:** The walker's decision record explains the new check, how a refused gate returns within the existing limits, and what an adopter must update together.

**Depends on:** Task 2, whose behaviour this records: `fw_round_file_check`, the `refused:` line, re-dispatch at the join with the round number and loop counter unchanged, the third refusal held as `error`, and the `check-round-file` subcommand. Task 12, whose user-review core runs that subcommand.

### Targets

- `docs/flow-graph-walker.md`

**Work:**

- [ ] After `### Item 8 — a round's gates fan out, and the round node joins`, add `### Item 9 — a round file is checked before its verdict is recorded`, with **Decision.**, **Reason.** and **Cost.** paragraphs matching the neighbouring items. The decision covers the validity rule, the same-round re-dispatch, the three-attempt limit and resume reading an invalid file as `unreadable`. The reason is that no agent meta-reviews a plan round, and the check proves presence only.
- [ ] State the cost: re-dispatches draw on `MAX_TOTAL_DISPATCHES`; `ui_review` and test-fix reviews are not covered; and an adopter must update the walker scripts (`init --force`, under the `create-if-absent` contract `### Item 6` records) together with the plugin, because a new walker beside reviewers that omit the fields refuses every `FAIL` file.
- [ ] Extend **What a second driver must do.** in `### Item 8` with one sentence: a `refused:` line needs no action of its own, and the refused gates arrive as an ordinary dispatch set.

**Verification:**

- Every symbol and heading the new section cites resolves with `git grep` in `cli/templates/scripts/flow-walker.sh`, `cli/templates/scripts/lib/flow-walker-gates.sh` or this document.
