### Task 5 — Record the command line in `ROADMAP.md` and `docs/development.md`

**Goal:** Bring the two root documents of record that describe GraphScene up to date with the command line this branch shipped. The roadmap's GraphScene row lists it as shipped. Gate 13's paragraph stops saying flatly that `graphscene` "has no console script", which would now be false of the package even though the wrapper row still names none.

**Depends on:** Task 4, which adds `graphscene/README.md` → `## The command line`. That section documents the `graphscene` console script (`graphscene = "graphscene.facade.cli:main"` in `graphscene/pyproject.toml`, Task 3), its commands `check`, `start`, `next` and `current`, and its invocation `uv run --frozen --no-sync --project graphscene graphscene …`. This task links to that section and restates none of it.

**How this task's implementer reads the conventions.** This is the catch-all (`general`) task, so read `.claude/context/conventions.md` first. Its `## Documents of record` holds the rule a roadmap entry follows. Read `.claude/context/graphscene.md` for the vocabulary the two sentences use.

### Targets

- `ROADMAP.md`: the `GraphScene` row of the table.
- `docs/development.md`: the **Gate 13** paragraph, its `graphscene` wrapper-row sentence only.

**Work:**

- [ ] `ROADMAP.md`, the `GraphScene` row, in its *Shipped:* list. Append a clause after the `RoundResume` clause, in the row's own style: *"and GraphScene's command line, `graphscene` — `check`, and `start` / `next` / `current` over a state file the caller names, printing JSON, for hosts not written in Python ([`graphscene/README.md`](graphscene/README.md) → `## The command line`)"*. Leave the *Left:* list and the status cell unchanged.
- [ ] `docs/development.md`, the **Gate 13** paragraph, the sentence *"`graphscene` is that second row; it has no console script and no compose project, so `run` and `container-test` on it exit `2`"*.
  - Reword it so it describes the **row** rather than the package: the row names no console script and no compose project, so the refusals and their exit `2` are unchanged.
  - Add one clause saying that the package's own `graphscene` command is run with `uv run --frozen --no-sync --project graphscene graphscene …`, not through `run`, citing `graphscene/README.md` → `## The command line`.
  - Change nothing else in the paragraph. The `devscene-flow-host` sentence after it stays as written: that package still has no console script.

**Verification:**

- Re-run the story index's `## Scope register` derivation entries A and B. Every hit they print appears as a register row, and the two rows this task owns (the **Gate 13** sentence and the `GraphScene` roadmap row) now read as described above.
- `docs/development.md`'s refusal facts still match `scripts/python-service.sh` → `package_row`, whose `graphscene` row still sets `row_console_script=""`.
- The roadmap clause's link resolves to the heading Task 4 added, spelled byte-for-byte.
