### 2. An `already passing` outcome that escalates on a row other than `G.4` has nothing for the escalation to quote

**File:** `plugin/instructions/unit_loop_core.md` (`## The unit loop` step 3), in the bullet that opens "An `outcome` of `blocker`, an `outcome` of `already passing` on any other row".

**Problem.**

The escalating bullet routes three cases to `<escalate>`:
- an `outcome` of `blocker`;
- an `outcome` of `already passing` on a row other than `G.4`;
- a third failed routing check.

It then says to escalate "quoting `` `layer-implementer.blocker` `` or naming the check that failed".

The middle case has neither. An `already passing` return carries `cause`, not `blocker`, and it passed the routing check. So the orchestrator escalates with nothing the sentence tells it to quote, and the person reading the park or the surfaced blocker gets no cause. The field that holds the cause, `layer-implementer.cause`, is the one the sentence leaves out.

**Fix.**

In that bullet, replace:

> → stop the whole loop and `<escalate>`, quoting `` `layer-implementer.blocker` `` or naming the check that failed.

with:

> → stop the whole loop and `<escalate>`, quoting `` `layer-implementer.blocker` `` for an `outcome` of `blocker`, `` `layer-implementer.cause` `` for an `outcome` of `already passing`, or naming the check that failed.

No test runs for this prose-only change beyond the tree guards the unit loop selects.
