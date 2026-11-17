### 1. The docs phase's INDEX step now inherits a review it never had and still says "commit it"

**File (plugin layer):** `plugin/instructions/docs_phase_instructions.md` → `## Loop`, step 3 **INDEX.**, the sentence this branch added: "Its return routes as step 2's **Write** bullet states; on its `error` route, log it and commit nothing for the INDEX."

**Problem.** Step 3 dispatches `docs-writer` (`mode: update`, target = the INDEX) and, in its unchanged first sentence, says "commit it". Before this branch, nothing reviewed the INDEX in the docs phase. The branch added a pointer that sends the INDEX return to step 2's **Write** bullet. That bullet's `written` arm reads:

> An `outcome` of `written` → review and commit `` `docs-writer.doc_path` ``

So the step now gives two routes for the same `written` return:

- "commit it", from the step's own sentence: no review;
- "review and commit", from the pointer: a `docs-reviewer` dispatch, the step 2 **Fix loop (cap 3)** and the **Missed-doc ripple**.

An orchestrator that follows the pointer adds up to four `docs-reviewer` dispatches and three writer re-dispatches per run, and they count against `MAX_TOTAL_DISPATCHES`. It also has nothing to put in `findings_path`. The **Review** bullet builds `findings_path = <state_dir>/docs_catalog/reviews/<slug>/review_<i>.md`, and the INDEX target in this phase has no `<slug>`: the docs phase never names one, unlike the catalog's `doc_slug: index`. A missed-doc ripple from that review would also add `update` targets after the per-target walk has already finished.

**Why this is net-new, and why the fix keeps the old behaviour.** The task prompt asks only to move callers onto the new return form (`harness-runs/task_prompts/feat_structured_outputs_docs_qa_task_prompt.md` → `## The goal`, item 2). It asks for no change to routing. The story index's `## Context` → **How the callers route** lists the docs phase's routes, and none of them reviews the INDEX. `## Where the plan and the task prompt differ, and why` records no such change either. Task 3's plan does put "Write and the INDEX" under one `written → review … and commit` bullet. That grouping is the source of the change, and nothing authorizes it, so the branch-reviewer, which grades the diff against the plan, could not flag it. The behaviour from before this branch is the one to restore.

**Fix.** In `plugin/instructions/docs_phase_instructions.md`, step 3 **INDEX.**, replace

```
Its return routes as step 2's **Write** bullet states; on its `error` route, log it and commit nothing for the INDEX.
```

with

```
Read its return as step 2's **Write** bullet states, except that an `outcome` of `written` is committed without a review; on its `error` route, log it and commit nothing for the INDEX.
```

Change no other sentence. The `docs-writer` field citations do not change, so `cli/test/agent-return-schemas.test.mjs` needs nothing.
