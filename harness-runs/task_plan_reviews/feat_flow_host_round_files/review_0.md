# Task plan review — round 0

verdict: FAIL
review_mode: full

## Must Fix
1. **`task_7_plan.md` — a non-round reviewer's findings are dropped with no entry-point deferred-work marker**
   `record_outcome` sends every non-gate call to `walker.next(outcome, node, None)`, so a findings file given with `ui_review`'s `FAIL` (and one given with `answered`) is discarded. `flow-walker.sh` → `next` keeps it: the `dispatch)` arm runs `elif [ -n "$A_FINDINGS" ]; then st_set revision_findings "$A_FINDINGS"`, the `answer)` arm does the same, and `render_block` prints it as `arg.findings_file:` on `ui_writer`'s revision. In the v4 graph, `ui_review` → `FAIL` routes to `ui_writer` with `"prompt": "revision"`. So this is a divergence from the implementation being ported that clients can see. The plan justifies it only with the story index's "Not this branch's" list and a module docstring's "Deliberately not covered". The task prompt excludes nothing here: #465 takes the command and its rendering, not the host's record of the file. The only marker Task 7 plans covers the held-gate departure.
   **Raised against:** "Carrying a non-round reviewer's findings file to its writer's revision is not covered: GraphScene refuses a `detail` outside a round, so a non-round `FAIL`'s findings are required here and not passed on."
   **Must hold:** Every divergence from `flow-walker.sh` that Task 7's `record_outcome` builds in must be backed by a task-prompt exclusion or by a planned entry-point `# TODO: @claude add a follow up task for this: …` marker naming what reverts it. A docstring entry is not enough.
   **Class:** Broken contract
   **Failure:** If the implementer builds Task 7 as written, then `record_outcome(walker, …, "FAIL", node="ui_review", findings=…)` discards the findings file, and `host/round_gates.py` carries no `TODO: @claude` marker for it, only a "Deliberately not covered" line. That repeats the `harness-runs/lessons.md` → *Ports and parallel implementations* rule: "A client-visible divergence from the implementation being ported is justified only by a task-prompt exclusion or an entry-point deferred-work marker naming what reverts it; a test-file comment or a code comment is never an exclusion basis."
   **Fix:** In `task_7_plan.md`, do one of two things. Either keep the non-round findings in the host's own record (beside the refusal record, cleared as bash's `revision_findings` is) so a later revision dispatch can carry it. Or add a second planned entry-point marker at the non-gate branch of `record_outcome`, naming the change that reverts it: a host-side record of `revision_findings` for a non-round reviewer and for `answered`. Restate it in Task 7's docstring bullet and test list (a case pinning the behaviour as it stands), and in the story index's "Not this branch's" bullet.

2. **`task_4_plan.md` — `ROUND_PLACEHOLDER` is retyped in `host/paths.py` when Task 2 already defines it**
   Task 2 adds `ROUND_PLACEHOLDER: Final = "{round}"` to `records/round_evidence.py`. Task 4 adds a second `ROUND_PLACEHOLDER = "{round}"` `Final` to `host/paths.py`. `host` may import `records`, so the second copy is avoidable. `.claude/context/devscene-flow-host.md` → `## Shared code and constants` requires that fixed literals are `Final` constants "in the module that reads or writes them, and another module imports them from there". `.claude/context/conventions.md` → `### Where a new responsibility goes` adds "A responsibility that already has a home does not get a second one".
   **Raised against:** "Add `Final` constants `STATE_DIR_PLACEHOLDER = "{state_dir}"`, `BRANCH_PLACEHOLDER = "{branch}"` and `ROUND_PLACEHOLDER = "{round}"`."
   **Must hold:** The literal `"{round}"` has exactly one `Final` owner in the package, and every other module imports it from that owner.
   **Class:** Broken contract
   **Failure:** If the implementer builds Tasks 2 and 4 as written, then `git grep -n 'ROUND_PLACEHOLDER: Final' devscene-flow-host/src` finds two definitions, in `records/round_evidence.py` and `host/paths.py`. That bypasses the layer's import-from-the-owner rule.
   **Fix:** In `task_4_plan.md`, import `ROUND_PLACEHOLDER` from `devscene_flow_host.records.round_evidence` instead of defining it. Add Task 2 to `**Depends on:**` with that import restated. Keep `STATE_DIR_PLACEHOLDER` and `BRANCH_PLACEHOLDER` in `paths.py`, which owns them.

3. **`task_8_plan.md` — the refusal cases call `record_outcome` without restating its contract**
   The refusal-case bullet says "Using `record_outcome` from `round_gates`". `**Depends on:**` restates only `HostStep` from Task 7. It gives neither `record_outcome`'s signature nor the `RefusedWait` answer the "during a refusal wait" case drives. The other test bullet plants records "through `round_fixtures`" without naming the helpers used. The implementer has to open `task_7_plan.md` / `task_1_plan.md`, or the landed code, to write a case.
   **Raised against:** "**`tests/test_re_entry.py`, the refusal cases.** Using `record_outcome` from `round_gates`:"
   **Must hold:** `task_8_plan.md` restates every cross-task contract its work calls, including the test-side calls.
   **Class:** Wrong build
   **Failure:** If the Task 8 implementer writes the refusal cases from `task_8_plan.md` and the story `## Context` alone, then the file gives them no parameters for `record_outcome` (walker, repo_root, branch, outcome, keyword-only node and findings) and no return shape (`HostStep` whose action is a `RefusedWait(round, refusal, pending)`). They cannot write the first refusal case without reading another task's file.
   **Fix:** In `task_8_plan.md` → `**Depends on:**` Task 7, add `record_outcome(walker: Walker, repo_root: Path, branch: str, outcome: str, *, node: str | None = None, findings: str | None = None) -> HostStep` and `RefusedWait(round: str, refusal: Refusal, pending: tuple[str, ...])`. Add a Task 1 entry naming the `round_fixtures` helpers the cases use (`init_repo`, `commit`, `plant_review`, `PASS_BODY`, `FAIL_BODY`), as `task_6_plan.md` does.

## Should Fix

1. **`task_1_plan.md`, `task_4_plan.md` — units with no consumer on this branch, and no consumer named.** `fail_count` (Task 1) and `review_iteration` (Task 4) are not called by any task. Their bash counterparts feed the cap payload's `rounds:` lines and a non-round reviewer's `arg.iteration:` (`flow-walker.sh` → `take_binding`, `render_block`), so their reader is #465's `commands` layer. `task_3_plan.md` names #465 as `read_index_evidence`'s reader, but these two files name none. State the consumer (#465) in each "Where this layer stops" paragraph so the unconsumed surface is a recorded decision.
2. **`task_3_plan.md` — a non-UTF-8 index raises where `fw_index_evidence` prints.** `fw_index_evidence` is `awk` over bytes and never refuses a file, but Task 3 decodes UTF-8 and raises a `RecordError`. Task 1 rejects decoding for this reason ("Never decode, so any file `awk` reads is read the same way"). Either read bytes as Task 1 does, or list the departure in the module's "Deliberately not covered".
3. **`task_8_plan.md` — case (12) of `cli/test/flow-walker-resume.test.mjs` is not carried.** The task prompt cites cases (7)–(12). Task 8's list carries (7)–(11), but not (12): after a pause at the join, `current` re-returns the pending revision or UI-writer dispatch unchanged and `returned` continues from it. Add a `current_step` case for it, or say why it is GraphScene's alone.

## Nice to Have

1. **`task_6_plan.md`** — "Ask `host.answer(entry.when, g)` over the gate's `skip` entries" reuses `entry`, the name of `round_resume`'s own parameter. Name the skip entry differently (for example `skip.when`).
