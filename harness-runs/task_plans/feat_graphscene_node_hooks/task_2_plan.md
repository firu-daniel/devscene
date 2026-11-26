### Task 2 — Raise the flow-graph format to 5 with hook and prompt-source declarations in the schema, model and builder

**Goal:** Raise GraphScene's flow-graph format to 5 and let a graph declare four new things:

- hook names under `vocabulary.hooks`;
- a dispatch node's `promptSource`;
- `before` / `after` hooks on dispatch and round nodes;
- `before` hooks on a terminal node.

The schema, the typed model and the builder all carry them, and every committed fixture moves to format 5 with them.

**Depends on:** Task 1, which authored the harness's planning graph to the contract below (`formatVersion` 5, `vocabulary.hooks`, `promptSource`, `before`, `after`). This task makes that graph schema-valid. It does not edit the planning graph.

**Why a format bump.** The schema's `formatVersion` description reads *"A change to the key set raises it, so a walker never routes on a graph whose shape it does not know."* This task adds keys.

**Where this layer stops.** This task only declares and builds the new keys. Three things belong to later tasks:

- **Checking that a named hook is declared** is Task 3's vocabulary check.
- **The types a hook is called with, and running hooks,** are Tasks 4–6's.
- **Making `HookDeclaration` public and describing format 5 in `graphscene/README.md`** is Task 7's.

**`promptSource` is opaque here.** GraphScene stores it and never parses it. `prompts` stays the list of variants, so `graphscene/src/graphscene/engine/references.py` → `_prompt_known` is unchanged.

### Targets

- `graphscene/src/graphscene/schemas/flow-graph.schema.json`
- `graphscene/src/graphscene/model/flow_graph.py`
- `graphscene/src/graphscene/adapters/builder.py`
- Docstring-only edits that rename *"format-4"* to *"format-5"*:
  - `graphscene/src/graphscene/adapters/schema.py`
  - `graphscene/src/graphscene/facade/loading.py`
  - `graphscene/src/graphscene/engine/references.py`
  - `graphscene/src/graphscene/engine/static_check.py`
- Every file under `graphscene/tests/fixtures/flow_graph/` except `schema_negative_format_version_3.json`. That one stays at 3 and is still refused. Each moves to format 5 and gains no hook.
- `graphscene/tests/fixtures/flow_graph/valid_hooks.json` (new): the one committed fixture that uses the new keys.
- `graphscene/tests/adapters/test_builder.py`
- `graphscene/tests/test_flow_graph_schema.py`
- `graphscene/tests/engine/test_references.py` and `graphscene/tests/engine/test_static_check.py`: the header's *"format-4 mapping"* and each planted mapping's `formatVersion`.

**The contract this task produces.** Tasks 3, 6 and 7 and the `devscene-flow-host` tasks read it.

| Serialized | Where | Schema | Model attribute |
|---|---|---|---|
| `formatVersion` | root | `"const": 5` | `FlowGraph.format_version: Literal[5]` |
| `hooks` | `vocabulary` | optional object, `propertyNames` a new `hookName` definition (`^[a-z][a-z0-9_]*$`, *"A key of vocabulary.hooks."*), each value `{"type": "object", "additionalProperties": false}` | `Vocabulary.hooks: Mapping[str, HookDeclaration] \| None`, a `MappingProxyType` in declaration order |
| `promptSource` | dispatch node | optional string, `minLength` 1 | `DispatchNode.prompt_source: str \| None` |
| `before`, `after` | dispatch node, round node | optional array, `minItems` 1, `uniqueItems`, items `hookName` | `DispatchNode.before`, `DispatchNode.after`, `RoundNode.before`, `RoundNode.after`: `tuple[str, ...] \| None` |
| `before` | terminal node | as above | `TerminalNode.before: tuple[str, ...] \| None` |

- **`HookDeclaration`** is a new `@dataclass(frozen=True)` with no fields, in `model/flow_graph.py`. It sits beside `PredicateDeclaration` and leaves room for the declaration to grow.
- **New attributes are appended after the existing ones**, in the order the table gives: `Vocabulary(outcomes, bindings, predicates, hooks)`, `DispatchNode(…, skip, prompt_source, before, after)`, `RoundNode(…, outcomes, before, after)` and `TerminalNode(id, binding, before)`. The builder is their only constructor.
- **An absent key is `None`**, per the model's absent-key rule (`graphscene/src/graphscene/model/flow_graph.py` module docstring).

**Work:**

- [ ] **`flow-graph.schema.json`.**
  - Make `formatVersion` `"const": 5`.
  - Add the `hookName` definition and the keys the table gives.
  - Write each new `description` in GraphScene's words. For example, `promptSource`: *"Where the host reads this node's agent prompt from. GraphScene stores it and reads nothing in it."* `before` / `after`: *"Hooks the host runs in run mode before / after this node."*
  - No description may name a word `graphscene/tests/test_flow_graph_schema.py` → `_HARNESS_NAMES` lists, or the forbidden prefix.
  - In the top-level `description`, change *"format 4"* to *"format 5"*, and state that hooks are host-run in run mode.
- [ ] **`model/flow_graph.py` and `adapters/builder.py`.**
  - Add `HookDeclaration` and the attributes, exactly as the table spells them, and update the module docstrings' absent-key notes.
  - In `builder.py`, build each key with the existing `_opt_str` / `_opt_strs` / `_object` helpers, keep the *"Attribute names"* docstring list in step (`promptSource` → `prompt_source`), and set `format_version=5`.
  - Rename *"format-4"* to *"format-5"* in the docstrings of `model/flow_graph.py` and `adapters/builder.py`, and in the four docstring-only source files listed under Targets.
- [ ] **Fixtures.**
  - Set `"formatVersion": 5` in every existing fixture listed under Targets, and change nothing else in them. **No existing fixture names a hook.** `graphscene/tests/facade/test_run_mode.py` and `graphscene/tests/facade/test_execution_rules.py` drive `valid_generic.json` through `start_run` / `continue_run` with no `hooks` argument, and Task 6 refuses a graph that names a hook when no hook host is given. So `valid_generic.json` and the `static_negative_*.json` copies of it stay hook-free.
  - Create `valid_hooks.json`: a copy of `valid_generic.json` at format 5 that declares `vocabulary.hooks` with at least two names and uses them in four places: `promptSource` and both `before` and `after` on one dispatch node, `after` on its round node, and `before` on its terminal node. No run-mode suite loads it.
  - **Its accompanying set** (`.claude/context/graphscene.md` → `## What accompanies a new module`, *"A new valid graph fixture lands with"*): its `_FIXTURE_NAMES` entry in `graphscene/tests/test_flow_graph_schema.py`, which this task adds, and its listing in the root `package.json` → `validate:graphscene-schema`. The root file is the `general` layer's, outside this task's layer, so **this task does not edit `package.json`**. Task 17 adds the listing.
- [ ] **`test_builder.py`.**
  - Assert `format_version == 5`.
  - Extend `test_every_optional_key_lands_on_its_snake_case_attribute`, or add a sibling case over `valid_hooks.json`, with each new attribute's hand-written value read from `valid_hooks.json`.
  - Assert that an absent `hooks`, `promptSource`, `before` and `after` build as `None`, reading `valid_generic.json`, which carries none of them.
  - Give the `TerminalNode(...)` equality assertion its `before`.
  - Check `test_the_model_is_immutable` covers `Vocabulary.hooks` as a read-only mapping, built from `valid_hooks.json`.
- [ ] **`test_flow_graph_schema.py`.** Assert `const == 5`, and rename the header's *"format-4"*. Add `"valid_hooks.json"` to `_FIXTURE_NAMES` after `"valid_plain_round.json"`, so the suite validates it against the schema. Bump the planted mappings and the header phrases in `test_references.py` and `test_static_check.py`. Their graphs go through `build_flow_graph`, which reads no `formatVersion`, so only the literal and the header change.

**Verification:**

- `tests/adapters/test_builder.py`, `tests/test_flow_graph_schema.py`, `tests/engine/test_references.py` and `tests/engine/test_static_check.py` pass, each run as `bash scripts/python-service.sh --package graphscene test tests/<path>.py`.
- `git grep -nE '"formatVersion": ?4' -- graphscene` prints nothing.
- `git grep -n '"formatVersion": 3' -- graphscene/tests/fixtures` prints only `schema_negative_format_version_3.json`.
- `git grep -lE '"(before|after|promptSource|hooks)"' -- graphscene/tests/fixtures` prints only `valid_hooks.json`.
- `git grep -nE 'format 4|format-4' -- graphscene/src` prints only `engine/vocabulary.py`, whose docstring is Task 3's.
