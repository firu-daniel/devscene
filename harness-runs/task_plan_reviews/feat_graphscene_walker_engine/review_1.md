# Task plan review — round 1

verdict: PASS
review_mode: full

## Should Fix
- **`task_4_plan.md`, `task_5_plan.md`: the test-support contract is named but not restated** (carried from round 0; still unaddressed). Both files use Task 3's `graphscene/tests/engine/walk_support.py`. Task 3 defines it as `planted(nodes, **overrides) -> FlowGraph` and `AnswerTable(answers: dict[tuple[str, str], bool | None])`, a `PredicateHost` that answers `False` for any pair not listed. Task 4 names only `planted` and `AnswerTable`. Task 5 names only the file. Each file should restate:
  - both signatures;
  - the default-`False` rule;
  - what `**overrides` may replace (the top-level keys of `valid_generic.json`);
  - the import form. `graphscene/tests/engine/__init__.py` exists and `graphscene/tests/__init__.py` does not, so under pytest's rootdir insertion the module is `engine.walk_support`.
- **No task updates `graphscene/src/graphscene/model/__init__.py`'s docstring** (carried from round 0). Tasks 1 and 2 add the walk's actions, its state and both Protocols to `model`. The docstring still reads *"the typed flow-graph model and the one error shape every stage reports in"*. Task 5 and Task 7 each update their own layer's `__init__.py` docstring. Add the same kind of one-line edit to Task 1's or Task 2's Targets.
- **`task_9_plan.md`: the never-logs bullet becomes self-contradictory.** `graphscene/README.md` → `## The layers` says *"It reports through return values and `GraphError` only."* Task 9 changes only that bullet's *"keeps no persisted or shared state"* sentence. It then adds a statement that the file store raises `ValueError` and `TimeoutError`. The *"`GraphError` only"* sentence stays, so the README ends up saying both things. Have the bullet that Task 9 restates also revise the *"`GraphError` only"* clause (Scope register row 14).
- **Story index → `## Scope register`, row 1: the reason names only half of what the walker falsifies** (carried from round 0; disposition (iii)). The bullet in `.claude/context/graphscene.md` → `## What this layer owns, and what it is not` also says the library *"reports through return values and `GraphError` only"*. `FileStateStore` raises `ValueError` and `TimeoutError` (Context → *"The file store raises errors of its own"*). Name both clauses in the row's reason and in the `stale-rule` entry in `corpus_staleness`.
- **Story index → `## Scope register`: a conventions-document site that no entry reaches** (disposition (ii)).
  - **The site.** `.claude/context/graphscene.md` → `## The model and its wire form` says *"The only fixed words are the schema's own enums, typed as `Literal` aliases (`NodeKind`, `Primitive`, `Verdict`)"*. Tasks 1 and 2 add fixed words that are not schema enums to `model`: the `Awaiting` alias and the action and passage `kind` literals.
  - **The row it needs.** `no-change`, because it is a conventions document. The reason cell should name the falsified sentence, with a matching `stale-rule` entry in `corpus_staleness`.
  - **A corrected derivation entry**, strictly wider than the one on the page:
    `git grep -nE 'Nothing walks|None exists yet|no persisted|no graph walker|Left: the engine|Checks over the built model|only fixed words|` + "`GraphError` only" + `' -- '*.md' ':!harness-runs' ':!examples'`
    The pattern is the current one with `only fixed words` and `` `GraphError` only `` added, in the single quotes. Of the sites it adds, only `.claude/context/graphscene.md` → `## The model and its wire form` is not yet a row. The other two are `.claude/context/graphscene.md` → `## What this layer owns, and what it is not` (row 1) and `graphscene/README.md` → `## The layers`, never-logs bullet (row 14).

## Nice to Have
- **`task_7_plan.md`.** The case *"make the directory read-only after the first write, then restore it"* does not block a write when the suite runs as root (carried from round 0). Use a failure that holds for any user, or say that the case skips loudly under root.
- **`task_8_plan.md`, concurrency case.**
  - *"The three `Wait`s together name each gate once as `recorded`"* cannot cover a four-gate set (carried from round 0). Say that the three `recorded` gates are distinct, and that together with the joining call's gate they cover all four.
  - State which outcome each of the four threads records, so the expected join result can be written by hand.
- **`task_3_plan.md`, `arrive`.** *"`closed_round` and `passed` from the draft"*: `closed_round` is a keyword argument of `arrive`, not a `WalkDraft` field. Say the `Dispatch` takes `closed_round` from the argument and `passed` from `draft.passed`.
