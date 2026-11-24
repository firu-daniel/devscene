### Task 4 — Pin `current` against a file written after the step in `test_flow_walker.py`

**Goal:** Show through the command itself, `devscene_flow_host.commands.flow_walker.main`, that `current` prints what `start` or `next` printed even when a findings file or the story index changes in between. Two differences close this way:
- a non-round reviewer's `arg.iteration`;
- a finished cap's `rounds:` and evidence lines.

Bash re-prints its saved `out=` lines on `current` (`cli/templates/scripts/flow-walker.sh` → `load_state`, the `current)` arm).

**Depends on:** Task 3, the last of the chain that makes this hold:
- Task 1's `PrintedReadsStore` keeps the values at `<stateDir>/.flow_walker_state/printed_reads/<percent-encoded branch>.json`.
- Task 2's `start_walk` / `record_outcome` write them, and `current_step` returns them.
- Task 3's `render` prints them from `HostStep.printed`, reading no file.

This task adds cases only and changes no source.

### Targets

- `devscene-flow-host/tests/test_flow_walker.py`

**Work:**

- [ ] **The non-round reviewer case**, `test_current_reprints_a_ui_reviewers_index_after_its_file_is_written`:
  - drive the walk to `ui_review` with the suite's `_repo` and `_at_ui_review`;
  - plant `review_0.md` (`FAIL_BODY`) in `devscene/ui_test_plan_reviews/feat_x/` with `round_fixtures.plant_review`, as the reviewer in flight would;
  - assert `current` prints the literal block the repro walk prints at `ui_review`: `action: dispatch`, `node: ui_review`, `agent: ui-tests-plan-reviewer`, `arg.iteration: 0`, `heartbeat: [ui-test-write · iter 0] → ui-tests-plan-reviewer  (#<total_dispatches>)`.

  The file being on disk would make a fresh read give `1`.
- [ ] **The cap case**, `test_current_reprints_the_plan_rounds_cap_after_a_fail_and_an_index_edit`:
  - **Before the cap.** Plant the story index `devscene/story_plans/feat_x_story_plan.md` with `flow-walker-gates.sh` → REPRO's `i.md` body, the body `tests/test_render.py` → `_STORY_INDEX_BODY` holds. Plant two `FAIL_BODY` files in `devscene/architecture_reviews/feat_x/`.
  - **Drive to the cap.** `start`, then repeat: `returned` for the writer, then for every `node:` line of the printed set, a verdict at that gate — `FAIL` with `f0.md` for `architecture_review`, `PASS` with the fixture's `p0.md` / `b0.md` otherwise. Stop at the first output starting `action: binding`. Read the gates from the printed set rather than assuming all three, because the round converges from `convergingFrom`.
  - **The cap's literal**, written from the graph's `plan_round` `onCap` and `take_binding`:
    - `action: binding`, `binding: <escalate>`, `node: plan_round`, `reason: cap`;
    - the closed round's `findings_file:` lines;
    - `rounds: business_parity_review 0`, `rounds: architecture_review 2`, `rounds: plan_review 0`;
    - `evidence: <root>/devscene/story_plans/feat_x_story_plan.md ## Rejected findings`, `evidence.open: - **5** (rejected round 2) — r`, `evidence: … ## Scope register`;
    - the `summary:` line, from the template `the plan loop reached its {cap}-revision cap; the gates open when it fired: {open_gates}`.
  - **After the cap.** Plant a third `FAIL_BODY` file in the architecture folder. Append `- **9** (rejected round 5) — r` under the index's `## Rejected findings`. Assert `current` prints the same literal.
- [ ] **The module docstring.** Extend its rule paragraph by one sentence: `current` prints the values the step read from disk as they were when it was printed.

**Verification:**

- `tests/test_flow_walker.py` passes, run as `bash scripts/python-service.sh --package devscene-flow-host test tests/test_flow_walker.py` from the repository root, the existing cases included.
- In both new cases the expected text is written out as literals, never captured from a first call and compared with a second.
