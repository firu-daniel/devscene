### Task 7 — Export the hook surface, document hooks and format 5 in the README, and drive a hooked walk as a caller

**Goal:** Make the hook seam public, so a host (`devscene-flow-host`) and an adopter of GraphScene alone can use it. Describe format 5, the declarations and the firing points in `graphscene/README.md`. Prove it through the public surface with a caller-side run-mode walk.

**Depends on:**

- **Task 2:** `HookDeclaration` in `graphscene.model.flow_graph`, and the `promptSource`, `before` and `after` declarations.
- **Task 4:** `HookHost`, `HookCall`, `BeforeDispatch`, `AfterDispatch`, `BeforeRound`, `AfterRound` and `BeforeEnd` in `graphscene.model.hooks`.
- **Task 5:** `execute_set`'s `before_dispatch`.
- **Task 6:** `start_run` / `continue_run`'s `hooks` keyword, its two `ValueError` refusals, and the firing points in `graphscene/src/graphscene/engine/run_loop.py` → *"The rule:"*.

This task restates those rules in the README and changes no behaviour.

### Targets

- `graphscene/src/graphscene/__init__.py`
- `graphscene/src/graphscene/facade/__init__.py`
- `graphscene/tests/test_public_surface.py`
- `graphscene/README.md`
- `graphscene/tests/facade/test_run_mode.py`
- `graphscene/tests/facade/test_execution_rules.py` (header only)

**The names this task makes public.** `devscene-flow-host` imports them from `graphscene`, never from a submodule (`.claude/context/devscene-flow-host.md` → `## What it may depend on`).

- `HookDeclaration` goes right after `"PredicateDeclaration"` in `__all__`.
- `HookHost`, `HookCall`, `BeforeDispatch`, `AfterDispatch`, `BeforeRound`, `AfterRound` and `BeforeEnd` go, in that order, right after `"continue_run"`.

**Work:**

- [ ] **Both `__init__.py` files.** Add the imports and the `__all__` entries, in the same order in both, as `graphscene/src/graphscene/facade/__init__.py` → *"The rule:"* requires.
- [ ] **`test_public_surface.py`.** Add each name to `_EXPECTED` in that position. Add `_DEFINED_IN` entries: `HookDeclaration` → `graphscene.model.flow_graph`, and the other seven → `graphscene.model.hooks`.
- [ ] **`graphscene/README.md`.**
  - In `## What it is`, the schema row becomes *"The format-5 flow-graph schema"*. Give `src/graphscene/model/hooks.py` its place where the README lists the `model` layer's modules and protocols. Update every *"format-4"* or *"format 4"* statement there.
  - Where the README describes run mode (`start_run` / `continue_run`), add a hooks paragraph. It covers the four declarations (`vocabulary.hooks`, `promptSource` as an opaque host string, `before` / `after` and which node kinds take which), `HookHost` and its refusal, the firing points and their order, the once-per-attempt rule, the re-run on `current`, the repeatable-side-effects rule and the exception rule. Spell each as `run_loop.py` and `set_execution.py` state it.
  - In `## The layers`, add `HookHost` to the `model` layer's protocols.
- [ ] **`test_run_mode.py`.** Add one case written as a caller importing only from `graphscene`:
  - it `load_graph`s a planted mapping at `formatVersion` 5 that declares `vocabulary.hooks` and uses hooks on a dispatch node, a round node and a terminal node;
  - it drives `start_run` with `StubExecutor` and a `HookHost` written in the test;
  - it asserts the exact hook call sequence, hand-written from the planted graph;
  - it asserts `load_graph` refuses the same mapping with one hook undeclared, at stage `vocabulary`.
- [ ] **`test_execution_rules.py`.** In the header's *"Deliberately not covered"*, replace *"the host's, and the run loop's (#423)"* with *"the host's, run through its `HookHost` in run mode"*.

**Verification:**

- `tests/test_public_surface.py`, `tests/facade/test_run_mode.py` and `tests/facade/test_execution_rules.py` pass, each run as `bash scripts/python-service.sh --package graphscene test tests/<path>.py`.
- `git grep -nE 'format 4|format-4' -- graphscene/README.md graphscene/src` prints nothing.
- Every hook statement in the README traces to a clause of `run_loop.py`'s or `set_execution.py`'s *"The rule:"*. Read them side by side, and find no README claim the code's rule does not make.

**Deviations from plan:**

- `HookDeclaration`'s `_DEFINED_IN` entry is made by widening the existing `graphscene.model.flow_graph` slice from `_EXPECTED[7:28]` to `_EXPECTED[7:29]`, not by a separate key: inserting the name after `PredicateDeclaration` shifts `TerminalNode` to index 28, so the slice had to widen either way, and a separate key would duplicate it.
- The README's hooks paragraph also restates `graphscene.model.hooks`'s *"The rule:"* (node kinds, repeatable side effects, `Walker` runs none), the vocabulary check's undeclared-hook refusal (`graphscene.engine.vocabulary` → *"The rule:"*) and the schema's `promptSource` description, beside `run_loop.py`'s and `set_execution.py`'s rules.
- Out of this layer's path and left unchanged: `.claude/context/graphscene.md` still says *"format-4"* in its `> **Read this when:**` line and in `## What this layer owns, and what it is not`.
