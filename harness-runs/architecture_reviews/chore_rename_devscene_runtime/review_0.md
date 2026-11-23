# Architecture review — round 0

verdict: PASS
review_mode: full

## Should Fix

1. **`task_1_plan.md` and the story index `## Context`: the single `general` tag on a task whose change includes files under the `devscene-runtime` layer's path is argued, but the argument does not name the rules it departs from.** `.claude/context/conventions.md` → `## The layers` says: *"A change whose files sit under another layer's path belongs to that layer and never to `general`."* `plugin/agents/task-plan-writer.md` → the layer-tag rule says *"A capability spanning layers is split into one task per layer"*. Task 1's `git mv` removes eight tracked files under `devscene-runtime/`. Task 1 and the index justify the tag with *"A `git mv` cannot be split by layer"* and *"Only the catch-all dispatch has every layer path in scope"*. The second claim is true: `plugin/agents/layer-implementer.md` → `## Catch-all layer additions` puts the whole map in scope on a catch-all dispatch. The first claim is not strictly true. A split is possible, but it would leave a commit between the two tasks where `scripts/python-service.sh` → `PACKAGES` names a directory with no `pyproject.toml`. That breaks `.claude/context/conventions.md` → `### The order files are created, so a half-built feature is still coherent`. Every changed path left after the commit sits under `devscene-flow-host/` or `scripts/`, which only the catch-all covers. So I can't complete a failure sentence, and this is not a Must Fix. Still, the justification should cite the two rules it sets aside, and should say why the atomic rename (the coherence rule) wins over the split.

## Nice to Have

1. **Story index `## Context` → manual step 4: say that this step has to happen before any later branch touches `devscene-flow-host/`.** After Task 3, the `tests/test_boundary.py` tree guard covers `devscene-flow-host/src/devscene_flow_host/**` and `devscene-flow-host/pyproject.toml`. Until the `layers` row is renamed, a unit touching those paths is routed to the catch-all layer. `plugin/agents/layer-implementer.md` → `<test_file_cmd>` and `.claude/context/conventions.md` → `## The testing bar` give no `--package devscene-flow-host` form for that layer. So the guard's package-relative `test` value has no command that selects the right package. No task on this branch touches those paths after Task 3, so the gap only opens after merge, until the maintainer's step 4.

Verified against the tree, no finding:
- The scope register's derivations A and B were re-run and give exactly the sites listed in rows 1–16 and 21–22. `git ls-files devscene-runtime` lists the eight files Task 1 moves.
- **Dependency direction:**
  - `[tool.uv.sources]` `graphscene = { path = "../graphscene", editable = true }` still resolves from the sibling directory.
  - `graphscene/tests/test_boundary.py` → `_FORBIDDEN_PREFIX = "devscene"` covers `devscene_flow_host` (row 20).
- **The accompanying set for a Python package** (`.claude/context/conventions.md` → `## What accompanies a new unit of each kind`, row *A Python package*):
  - the package-table row: Task 1;
  - the gate 13 legs in `docs/development.md`: Task 4;
  - the `layers` entry and the conventions document: manual steps 4 and 5. `layers` changes only through `devscene config set layers` (`docs/cli.md`), and a run never writes a conventions document.
- **Tree guards:** Task 3 moves both `covers` values, so the guard stays selectable.
- **Test runs:** Task 1 and Task 2 name only test files they edit. Tasks 3–5 name no test run.
- **Laundering check:** no task tells an agent how to work in a way that doesn't trace to a harness contract. The park in Task 5 traces to `cli/templates/scripts/push-branch.sh` and the task prompt's decided item.
