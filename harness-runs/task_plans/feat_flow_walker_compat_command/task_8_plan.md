### Task 8 — Record the compatibility command in `ROADMAP.md`'s GraphScene row

**Goal:** Keep the roadmap true: its `GraphScene` row says the host ships *"with no command line yet"*, which this branch falsifies.

**Depends on:** Task 7, which documents the command in `devscene-flow-host/README.md` → `## The command line` — the anchor this row links to. **The catch-all task ships last for this reason**: it records what the `devscene-flow-host` tasks built and changes nothing inside that package. This is the `general` layer (`layers[]` path `"."`), so its rules are `.claude/context/conventions.md`'s, read with every other layer's document as the catch-all contract asks.

### Targets

- `ROADMAP.md` — the `GraphScene` row only.

**Work:**

- [ ] Replace *"with no command line yet"* in the host's clause with *"and `devscene-flow-walker`, `flow-walker.sh`'s compatibility command — its verbs, flags, output and exit codes over the host, its differences from bash listed for #419 ([`devscene-flow-host/README.md`](devscene-flow-host/README.md) → `## The command line`)"*, keeping the row's sentence shape and link style.
- [ ] Leave the row's `Left:` clause and its `In progress` status as they are: the walker's port onto the engine — `flow-walker.sh` handing off for every caller — is #419's and has not landed.

**Verification:**

- `git grep -n 'no command line' -- ROADMAP.md` returns no hit.
- The link target `devscene-flow-host/README.md` → `## The command line` exists as a heading in that file.
