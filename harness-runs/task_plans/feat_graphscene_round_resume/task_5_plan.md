### Task 5 — Record the round entry on the GraphScene roadmap row

**Goal:** Add the round entry to what `ROADMAP.md`'s GraphScene row lists as shipped, so the record of what the library already does matches the tree.

**Depends on:** Task 4. That task makes `RoundResume` public, and it is listed in `graphscene/README.md` → `## What it is` as the input `Walker.start` takes to begin inside a round, at that round's number with its recorded gate outcomes and every counter at 0. This task changes nothing under `graphscene/` and only writes about what Tasks 1–4 built. It ships last because it is the catch-all task.

**How this task's implementer reads the conventions.** This is the catch-all `general` layer, so read `.claude/context/conventions.md`. Read `.claude/context/graphscene.md` too, for the vocabulary the row uses.

### Targets

- `ROADMAP.md`: the GraphScene row (line 162 on the tree as planned), in the `## Scene products` table.

**Work:**

- [ ] `ROADMAP.md` → the GraphScene row's **Shipped** list: after the review-loop clause (*"…and the review loop's checks and walk rules apply only where a graph declares one ([`graphscene/README.md`](graphscene/README.md))"*), append one clause in the row's own pattern. For example: *"; and starting a walk inside a round — `Walker.start` takes a `RoundResume` naming the round, its number and the gate outcomes the host already recorded, dispatches only the gates still out and joins as `next` would, while reading the round's records stays the host's ([`graphscene/README.md`](graphscene/README.md))"*.
- [ ] Leave the row's **Left:** text and its `In progress` status unchanged. The harness-side reading of the round files is #418's and is still left, and this branch does not ship it.

**Verification:**

- The row still renders as one table row, with no new line break inside the cell, and its link resolves to `graphscene/README.md`.
- The new clause names only what the Task 4 README rows state, with no behaviour the README does not document.
- Re-running the story index's `## Scope register` command entry reaches `ROADMAP.md:162`, which is register row 4 and now carries the clause.

**Deviations from plan:** The Work bullet's example clause says `Walker.start` *"dispatches only the gates still out and joins as `next` would"* and that *"reading the round's records stays the host's"*. `graphscene/README.md` → `## What it is` (the `walker.py` entry of the `src/graphscene/engine/` row) states neither in those words: it says `start` *"takes an optional `RoundResume`, starting the walk at that round's number with the given gate outcomes recorded and every counter at 0, the host deciding which round and which records"*. The Verification bullet bars behaviour the README does not document, so the clause carries the README's wording instead: *"; and entering a round on a walk's start — `Walker.start` takes an optional `RoundResume`, starting the walk at that round's number with the given gate outcomes recorded and every counter at 0, the host deciding which round and which records ([`graphscene/README.md`](graphscene/README.md))"*.
