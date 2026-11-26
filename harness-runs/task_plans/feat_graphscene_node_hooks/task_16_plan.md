### Task 16 — Document the prompt builder, the planning hooks and the entry decision in `devscene-flow-host/README.md`

**Goal:** Describe in the flow host's README what this branch added to it: the prompt builder, the planning hooks, the commit points, the entry decision and the readers beneath them. Move the README's format statements to format 5. Update the seven suite headers that still call the planning graph *"format-4"*.

**Depends on:**

- **Task 8:** `records/prompt_blocks.py`.
- **Task 9:** `records/clarifications.py`.
- **Task 10:** `records/ledger.py` → `read_planning_marks`.
- **Task 11:** `host/agent_prompts.py` → `CorePromptBuilder`: construction refusals, the cache, `pnl_prompt`'s token order, pairs appended once to the first writer dispatch, and `consumed`.
- **Task 12:** `host/commit_points.py` → `commit_artifact`, `flip_ledger_entry`, `CommitPointError`.
- **Task 13:** `host/planning_hooks.py` → `PlanningHooks`. Its hooks are `commit_plan_round`, `flip_ledger` and `commit_convergence`, carrying Overrides 6, 5 and 3–4 with `P3`.
- **Task 14:** `host/planning_entry.py` → `decide_planning_entry`, which returns `PlanningDone`, `ContinueWalk` or `StartWalk`.
- **Task 15:** core-agreement check 10.

This task restates each module's *"The rule:"*. It adds no rule a module does not state.

### Targets

- `devscene-flow-host/README.md`
- The header docstrings only of these seven suites:
  - `devscene-flow-host/tests/test_printed_reads.py`
  - `devscene-flow-host/tests/test_reviewers.py`
  - `devscene-flow-host/tests/test_re_entry.py`
  - `devscene-flow-host/tests/test_walking.py`
  - `devscene-flow-host/tests/test_round_gates.py`
  - `devscene-flow-host/tests/test_resume.py`
  - `devscene-flow-host/tests/test_render.py`

**Work:**

- [ ] **`## The executor` → **The agent prompt.**** Replace the sentence ending *"belongs to the later branch that makes prompt sources and node hooks declarations, not yet merged"* with the builder: `CorePromptBuilder` cuts each dispatch node's `promptSource` blocks through `records/prompt_blocks.py`, refuses an unbuildable source at construction, and fills `pnl_prompt`'s tokens in its order. It appends the pairs it was given once, to the first writer dispatch, and returns the same text for an equal dispatch.

  State that `Dispatch.prompt` keeps its name. Renaming it raises GraphScene's walk-state document version, refusing every saved walk, and changes both packages in one change.
- [ ] **New sections** `## The planning hooks` and `## Where a planning walk enters`, placed after `## The executor`.
  - **The hooks section.** Each hook, the override it carries, the call kinds it takes, the commit points it makes through `commit_artifact` (the main checkout's wrapper path being the caller's input), and why each is repeatable.
  - **The entry section.** The decision order and the derived ledger loops.

  Both sections say that nothing in production calls these until the run-mode cutover (#424). Until then, the bash planning driver makes the same commits, flips and entry decisions itself. Add each new module to `## The layers` / `## What it reads, answers and keeps` where those sections list the package's modules.
- [ ] **`## Differences from flow-walker.sh` → **The graph.**** Change *"The command reads format 4"* to format 5. Note that format 5's `vocabulary.hooks`, `promptSource`, `before` and `after` change nothing the command prints.
- [ ] **The seven suite headers.** Replace *"format-4 graph"* with *"format-5 graph"* in each header, with no other change.

**Verification:**

- `git grep -nE 'format 4|format-4|not yet merged' -- devscene-flow-host/README.md devscene-flow-host/tests` prints nothing. One exception: a *"not yet merged"* left in the README must name the usage-to-`Launch` pairing or the stream writing, which stay the run driver's.
- Every statement in the two new sections traces to a clause of `host/planning_hooks.py`'s or `host/planning_entry.py`'s *"The rule:"*. Read them side by side.
