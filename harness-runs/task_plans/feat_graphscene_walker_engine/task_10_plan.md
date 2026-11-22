### Task 10 — Record the walker engine as shipped in `ROADMAP.md`'s GraphScene row

**Goal:** Keep the roadmap's GraphScene row true. It currently says the library has "no graph walker" and lists "the engine" as left. This task owns row 2 of the story index's `## Scope register`. This is the catch-all task (the `layers[]` entry whose `path` is `"."`), so it ships last.

**Depends on:** Task 9, which describes the walker in `graphscene/README.md`. That README section is the link target. This task points at it and restates none of it.

### Targets

- `ROADMAP.md`

**Work:**

- [ ] **`ROADMAP.md` → `## Scene products`, the GraphScene row.**
  - In the "Shipped:" list, drop "with no graph walker" from the skeleton clause.
  - Append a clause: the walker engine, which walks a loaded graph through fan-out and join rounds, counters and caps, host-answered skips and interrupts, keeping its state through a `StateStore`, with a file store `FileStateStore`. Link it to [`graphscene/README.md`](graphscene/README.md).
  - In "Left:", replace "the engine, the walker's port onto it, and the harness-side package" with "the review loop's rules on the engine, the walker's port onto it, and the harness-side package".
  - Keep the format-4 cutover clause and the `In progress` status unchanged.

**Verification:**

- [ ] Re-run the story index's command derivation entry. `ROADMAP.md`'s row no longer matches `no graph walker` or `Left: the engine`.
- [ ] The row's new link resolves to `graphscene/README.md`, and the row is still one table line.
