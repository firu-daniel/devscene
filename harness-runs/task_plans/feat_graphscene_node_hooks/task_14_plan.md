### Task 14 — Port `pd_entry` as `decide_planning_entry`, the host's entry and resume decision

**Goal:** Decide where a planning walk enters, from four inputs: the saved walk, the ledger's `P1`–`P3`, the branch's answered clarification pairs, and which drafts exist on disk. The decision reads as `cli/templates/scripts/lib/planning-driver-lib.sh` → `pd_entry`, `pd_pairs`, `pd_walk_usable` and `pd_block_usable` decide it. It hands GraphScene what run mode starts or continues with: an entry and a `RoundResume`, or the outcome to continue a saved walk with. This is Override 5's resume half and Override 2 of `plugin/instructions/task_plan_writing_instructions_autonomous.md`, as a host function.

**Depends on:**

- **Task 9:** `read_answered_pairs(repo_root, state_dir, branch) -> tuple[AnsweredPair, ...]`, where `AnsweredPair(index, question, answer, raised_by)`.
- **Task 10:** `read_planning_marks(repo_root, state_dir, branch) -> PlanningMarks(p1, p2, p3)`, each `"x" | "-" | " " | None`.
- **The existing host:**
  - `host/re_entry.py` → `current_step(walker, repo_root, branch) -> HostStep`, which re-reads the saved step as bash's `current` does, refused gates left out;
  - `host/resume.py` → `round_resume(graph, host, repo_root, state_dir, branch, entry)`;
  - `HostStep.revision_findings`.

**Where this layer stops.** This task returns a decision and acts on none of it:

- **Calling `start_run` / `continue_run`** with it, constructing `CorePromptBuilder` (Task 11) with its `pairs`, and archiving consumed pairs are the run driver's (#424).
- **A `PlanningDone` result.** The driver falls straight through to implementation.

### Targets

- `devscene-flow-host/src/devscene_flow_host/host/planning_entry.py` (new)
- `devscene-flow-host/tests/test_planning_entry.py` (new)

**The contract this task produces.** The README (Task 16) describes it.

```python
@dataclass(frozen=True)
class PlanningDone: ...

@dataclass(frozen=True)
class ContinueWalk:
    outcome: str | None                 # None: continue_run(outcome=None); else the interrupt's resume outcome
    pairs: tuple[AnsweredPair, ...]

@dataclass(frozen=True)
class StartWalk:
    entry: str
    resume: RoundResume | None
    pairs: tuple[AnsweredPair, ...]

PlanningEntry: TypeAlias = PlanningDone | ContinueWalk | StartWalk

def decide_planning_entry(walker: Walker, repo_root: Path, state_dir: str, branch: str) -> PlanningEntry: ...
```

**The decision**, in `pd_entry`'s order:

1. **Planning is done.** If `P1`, `P2` and `P3` are all resolved (`"x"` or `"-"`), the result is `PlanningDone()`.
2. **The writer pairs** are `read_answered_pairs`, minus two kinds of pair, as `pd_pairs` leaves them out:
   - a pair whose `raised_by` starts with `Phase G`;
   - a pair whose `raised_by` starts with `prompt-injection-reviewer (prompt-injection screen)`.

   *UI pairs* is true when a kept pair's `raised_by` contains `ui-tests-plan-writer` or `ui-tests-plan-reviewer`.
3. **The saved walk.** The step is `current_step(...).action`. A `Refused` (no saved walk) falls through.
   - **A pending dispatch.** A `Dispatch` or `DispatchSet` that is *usable* gives `ContinueWalk(None, pairs)`. The pairs are carried only when its node declares `prompts` (a writer); otherwise `()`.
   - **A parked interrupt.** An `Interrupt` gives `ContinueWalk(interrupt.resume_outcome, pairs)` when there are writer pairs and it is *usable*. This is what keeps a parked writer's saved variant, the #325 case.
   - **Anything else falls through.** That covers a binding that is not usable or has no pairs, a `Stop` and an `End`.
4. **The start.** Otherwise the result is `StartWalk(entry, round_resume(walker.graph, walker.host, repo_root, state_dir, branch, entry), pairs)`, where `entry` is the first of these that holds:
   1. with writer pairs, `ui_writer` when *UI pairs*, else `plan_writer`;
   2. `P1` `"x"` and `P2` resolved: `convergence`;
   3. `P1` `"x"` and the UI-test index exists: `ui_review`;
   4. `P1` `"x"`: `ui_writer`;
   5. the story index exists: `plan_round`;
   6. otherwise: `plan_writer`.

**Usable** reads as `pd_walk_usable` and `pd_block_usable`:

- **The ledger loops are derived from the graph, not listed.** The loop of entry `L` is every node with an outcome `RouteEdge` whose `ledger` is `L`, plus, for each such round node, its `gates` and `writer`. On the planning graph:
  - `P1`'s loop is `{plan_round, business_parity_review, architecture_review, plan_review, plan_writer}`;
  - `P2`'s loop is `{ui_writer, ui_review}`.
- **The step's first node** is the `Dispatch`'s node, the `DispatchSet`'s first dispatch's node, or the `Interrupt`'s node.
- **A step is unusable** when any of these holds:
  - `P1` is `"x"` and the first node is in `P1`'s loop;
  - `P2` is resolved and the first node is in `P2`'s loop;
  - `P1` is not `"x"`, the first node is in `P2`'s loop, and the step's `passed` carries no `LedgerPassage("P1")`.
- **A dispatch is unusable** when its required artifact is absent under `repo_root`. The table is `pd_block_usable`'s, keyed by `(node, variant)`, where the variant is as `render.py` → `_block` reads it:
  - the story index (`paths["story_index"]`) is required by every `P1` gate, by `plan_writer` with variant `revision`, and by `ui_writer` with variant `initial`;
  - the UI-test index (`paths["ui_test_index"]`) is required by `ui_review`, and by `ui_writer` with variant `revision`.
- **A revision is unusable** when a findings file its revision carries (`HostStep.revision_findings` when non-empty, else `closed_round` details) exists neither as given nor under `repo_root`.

**The constants.** The entry ids, the two path keys, the two origin prefixes and the two UI agent names are `Final` constants in the module. Each is a value `pd_entry` hard-codes.

**Work:**

- [ ] **`host/planning_entry.py` — the decision.** Implement the three result types, `PlanningEntry` and `decide_planning_entry` exactly as the contract spells them, with the loop derivation and the usable checks as private helpers.
- [ ] **`host/planning_entry.py` — the docstring.**
  - Its *"The rule:"* names the bash functions it reads as and states the order.
  - Its *"Deliberately not covered"* list names four things: acting on the decision (the run driver's, #424), the ledger's creation and `P0` (the fork's Setup), archiving consumed pairs (the watcher's), and a flow other than the planning graph.
- [ ] **`tests/test_planning_entry.py` — the decision order.** Open with the header *"The rule this file exists to enforce"*. Use planted repositories under `tmp_path` (config, ledger, story index, UI-test index, clarifications) and the real planning graph `cli/templates/scripts/flows/task_plan_writing.graph.json`, read-only, through `open_walker`. Saved walks are produced by driving the real `Walker`. Cover one case per decision step:
  - all resolved gives `PlanningDone`;
  - a usable pending dispatch, with pairs carried for a writer and dropped for a gate;
  - **the #325 case:** a walk parked at `<ask>` after a `revision` dispatch of `plan_writer`, with an answered pair, gives `ContinueWalk("answered", pairs)`. Recording `answered` through the walker then dispatches `plan_writer` with `prompt == "revision"`;
  - a parked walk with no pairs falls through;
  - each of the six start entries;
  - `Phase G` and screen pairs left out;
  - a UI pair sending the entry to `ui_writer`.
- [ ] **`tests/test_planning_entry.py` — usability and the constants.** Add these cases:
  - each unusable clause on its own: `P1` `x` against a `P1`-loop node, `P2` resolved against a `P2`-loop node, `P1` open against a `P2`-loop node with and without the `LedgerPassage("P1")`, a missing story index, and a missing findings file;
  - the derived loops on the real graph, asserted as the two literal sets above;
  - every entry constant is in the real graph's `entries`, and both path keys are in its `paths`.

**Verification:**

- `bash scripts/python-service.sh --package devscene-flow-host test tests/test_planning_entry.py` passes.
- The #325 case shows the answered park resumes the writer with the variant its walk saved, never `initial`.
