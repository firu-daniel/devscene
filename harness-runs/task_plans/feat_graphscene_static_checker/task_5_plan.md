### Task 5 — Describe the static checker and the new loading order in `graphscene/README.md`

**Goal:** Make the package README true again. The `engine` layer now holds the vocabulary check, the reference check and the static checker, all reading the built `FlowGraph`. Loading is schema → build → vocabulary → static, and `graphscene.static_violations` is public.

**Depends on:** Task 4, which makes `static_violations` public from the package root. Behind it: Task 3's loading order and `"static"` stage, Task 2's `graphscene/src/graphscene/engine/static_check.py` (checks `reachable-from-start`, `reaches-terminal`, `fail-cycle-capped`, `gate-in-round`, `round-fan-out`, each reason opening with its check id), and Task 1's `graphscene/src/graphscene/engine/references.py` (`reference_violations`, unexported, run first inside `static_violations`). This task describes those and changes no code.

**Where this task stops.** The root documents of record (`docs/development.md`, `ROADMAP.md`) are Task 6's. The conventions documents `.claude/context/graphscene.md` and `.claude/context/conventions.md` are **not** edited by any task. Their stale statements go to a supervised `/devscene:analyze` re-run or a hand edit, recorded in the plan's return.

### Targets

- `graphscene/README.md`

**Work:**

- [ ] `## What it is`, opening paragraph: replace *"its `engine` layer holds only the vocabulary check"*. Say the `engine` layer holds the vocabulary check and the static checker, and that loading composes the schema adapter, the builder, the vocabulary check and the static checker, in that order, before returning the typed graph.
- [ ] `## What it is`, the table rows:
  - the `src/graphscene/engine/` row adds `references.py` (`reference_violations`, that every node, counter, path, report-slot and prompt name exists and `start` is in `entries`; not public) and `static_check.py` (`static_violations`, the reference check, then the five graph checks, each reason opening with its check id);
  - the `vocabulary.py` entry says it reads the built `FlowGraph`;
  - the `src/graphscene/facade/` row says `load_graph` validates against the schema, builds, then runs the vocabulary check and the static checker;
  - the `src/graphscene/model/` row's `errors.py` entry stays as it is: `Stage` is still named there.
- [ ] `## The layers`:
  - the `engine` row's *Holds* cell becomes *"Checks over the built model: the vocabulary check and the static checker."*;
  - replace the bullet *"The vocabulary check reads the parsed mapping, after the schema check and before the build."* with: every engine check reads the built `FlowGraph`; loading runs schema → build → vocabulary → static; a graph `load_graph` returns has passed all three checks; and a graph failing one stage never reaches the next.

**Verification:**

- Re-run the story index's `## Scope register` command entry. Every `graphscene/README.md` hit it prints matches the new wording, and no hit still says the vocabulary check reads the parsed mapping or that the engine holds only the vocabulary check.
- Each module path and public name the README now cites exists: `graphscene/src/graphscene/engine/references.py`, `graphscene/src/graphscene/engine/static_check.py`, and `static_violations` in `graphscene/src/graphscene/__init__.py` → `__all__`.
