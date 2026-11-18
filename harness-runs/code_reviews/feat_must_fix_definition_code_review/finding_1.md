### 1. `current` re-prints a refused gate the walker still counts as not out, so the gate is dispatched twice

**File:** `cli/templates/scripts/flow-walker.sh` (`render_set`) — "SET_PENDING=\"${SET_PENDING}pending: $g$NL\""; the same function in `scripts/flow-walker.sh`; the test in `cli/test/flow-walker-fan-out.test.mjs` — "(11) `current` during the wait re-prints the refused gate's block"

`render_set` builds two different things from one loop. `SET_PENDING` leaves out a gate carrying `round.redo.<gate>`, because that gate "is not out". The blocks in `OUT` still include it, and on `action: wait` those blocks are saved through `SAVE_OUT` as what `current` re-prints. So after a refusal, `current` tells the caller to dispatch a gate that the walker will also re-dispatch itself at the join.

`plugin/instructions/task_plan_writing_instructions_core.md` → `## The walker` sends callers down this path in ordinary operation: for **A dispatch that did not return**, and after an auto-compaction, it says to issue `current` and dispatch again. Traced with gates `plan_review`, `architecture_review` and `business_parity_review`:

1. `plan_review` returns a malformed file. The walker marks `round.redo.plan_review` and prints `action: wait`, listing the other two as pending.
2. `architecture_review` did not return, so the orchestrator issues `current`. It prints the blocks of all unrecorded gates, `plan_review` included, and the orchestrator dispatches them.
3. The sibling returns are recorded first. When the last one is recorded, `SET_PENDING` is empty because `plan_review` is still marked, so `record_in_set` clears the mark and prints `action: dispatch` for `plan_review`, although that gate's dispatch from step 2 is already out or already returned and unrecorded.
4. The core says to send a printed set, so `task-plan-reviewer` runs a second time for the same round and replaces the same `review_<n>.md`.
5. The first of its two returns closes the round. The second `next --node plan_review` is refused with exit 1 because the gate is no longer pending, and the core's **A non-zero exit is a blocker** turns that into `<escalate>`.

The planning driver is not exposed to the double run, because it waits for every session of a set before acting on the walker's output. Its infrastructure retry does, however, re-launch the refused gate alongside the node it says is "re-dispatched alone".

**Fix:** make a marked gate absent from the blocks as well, so the join is the only place it is re-dispatched. A `wait` always has at least one unmarked gate pending, so the join is still reached, and `record_in_set` clears the marks before its re-dispatch call to `render_set`, so that call still prints them.

In `render_set`, in both `cli/templates/scripts/flow-walker.sh` and `scripts/flow-walker.sh`, replace the loop body's tail with:

```bash
    fw_id_in_list "$g" "$gates" || continue
    gate_recorded "$g" && continue
    st_get "round.redo.$g"
    [ -z "$SV" ] || continue
    render_block "$g" "" "$pass"
    OUT="$OUT$BLOCK"
    pass=""
    SET_PENDING="${SET_PENDING}pending: $g$NL"
```

Update the comment above `render_set` in both copies to:

```bash
# Set OUT to the blocks of round <rn>'s set gates with no recorded outcome and
# no re-dispatch mark, in `gates` order, the first carrying the fan-out's
# passed-through lines and then <extra>. Set SET_PENDING to those gates, one
# `pending: <gate>` line each.
```

In the `# STATE` header paragraph of both copies, change "the blocks of the gates with no recorded outcome" to "the blocks of the gates with no recorded outcome and no re-dispatch mark".

In `cli/test/flow-walker-fan-out.test.mjs`, rename case (11) to "(11) `current` during the wait leaves out the refused gate, which the join re-dispatches" and change its assertion to:

```js
assert.deepEqual(blocksOf(current.action), [PARITY_BLOCK(), ARCH_BLOCK()]);
```

That test file is the one this fix edits, so it is the only test file the fix runs.
