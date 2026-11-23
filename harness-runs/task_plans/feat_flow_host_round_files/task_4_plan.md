### Task 4 — Render a graph path template and find a reviewer's round and next index

**Goal:** Give the `host` layer four things:
- the rendering of a graph's path templates (`{state_dir}`, `{branch}`, `{round}`), which GraphScene leaves to the host (`.claude/context/graphscene.md` → *"rendering path templates … are the host's"*);
- the lookup of the round a node is a gate or the writer of;
- the next free index for a reviewer that sits **outside** a round. That index comes from `DispatchNode.findings_folder`, an opaque field the engine never reads.

**Depends on:**
- Task 1, which provides `devscene_flow_host.records.round_files.next_review_index(folder: Path) -> int`.
- Task 2, which owns the `{round}` placeholder literal: `devscene_flow_host.records.round_evidence.ROUND_PLACEHOLDER: Final = "{round}"`. This task imports it from there and never retypes it. The import points down, from `host` to `records`, as `.claude/context/devscene-flow-host.md` → `## The internal layers` allows.

**Source:** `cli/templates/scripts/flow-walker.sh` (`render_path`, `subst`, `round_of_gate`, `round_of_writer`, and `render_block`'s `elif g_get "nodes.$node.findingsFolder"` branch).

**Where this layer stops.** These are lookups and renderings with no state. Task 6 uses `render_path`, `round_of_writer` and `round_of_gate` to place a resume. Task 7 uses `round_of_gate` to know a round gate. Printing `arg.iteration:` is the `commands` layer's. A round gate's `arg.iteration` is its round number, which the `Dispatch` GraphScene returns already carries, so `review_iteration` answers `None` for it.

### Targets

- `devscene-flow-host/src/devscene_flow_host/host/paths.py` (new)
- `devscene-flow-host/src/devscene_flow_host/host/reviewers.py` (new)
- `devscene-flow-host/tests/test_reviewers.py` (new)

**Work:**

- [ ] **`paths.py`.** Add `Final` constants `STATE_DIR_PLACEHOLDER = "{state_dir}"` and `BRANCH_PLACEHOLDER = "{branch}"`, which this module owns. Import `ROUND_PLACEHOLDER` with `from devscene_flow_host.records.round_evidence import ROUND_PLACEHOLDER`, and do not define a second `Final` for `"{round}"`. Add `render_path(template: str, state_dir: str, branch: str, round_number: int | None = None) -> str`. It replaces **every** `{state_dir}`, then every `{branch}`, then, only when `round_number` is given, every `{round}`, as `subst` does. It returns the repo-relative result unchanged otherwise, trailing `/` included. The module docstring has two parts:
  - **"The rule:"** cites `render_path` and `subst` in `flow-walker.sh`: every occurrence of each placeholder is replaced, in that order, and `{round}` only when a round number is given.
  - **"Deliberately not covered"** names two things. It never resolves a rendered path against the repository root, which is the caller's job. It substitutes no placeholder other than the three it names.
- [ ] **`reviewers.py`, round lookups.** `round_of_gate(graph: FlowGraph, node: str) -> RoundNode | None` returns the round whose `gates` list the node. `round_of_writer(graph: FlowGraph, node: str) -> RoundNode | None` returns the round whose `writer` is the node. Both scan `graph.nodes` in order and return the first match. Import `FlowGraph` and `RoundNode` from `graphscene` only.
- [ ] **`reviewers.py`, the index outside a round.** `review_iteration(graph: FlowGraph, repo_root: Path, state_dir: str, branch: str, node: str) -> int | None` returns `None` in three cases: the node is not a `DispatchNode`, it is a round gate, or its `findings_folder` is `None`. Otherwise it returns `next_review_index(repo_root / render_path(node.findings_folder, state_dir, branch))`.
- [ ] **`reviewers.py`, the module docstring.** It has two parts:
  - **"The rule:"** names the rule the module holds and the bash functions it reads as (`round_of_gate`, `round_of_writer`, and `render_block`'s `findingsFolder` branch in `flow-walker.sh`). A node's round is the first round in `graph.nodes` order that lists the node. A reviewer's index outside a round is read only from `DispatchNode.findings_folder`.
  - **"Deliberately not covered"** names a round gate's iteration, which is GraphScene's round number.
- [ ] **`tests/test_reviewers.py`.** It opens with *"The rule this file exists to enforce"*. It loads `cli/templates/scripts/flows/task_plan_writing.v4.graph.json` (one fixed file, read from a path built off `__file__`), with literal expectations read off that file:
  - `render_path("{state_dir}/plan_revisions/{branch}/task_plan_revision_{round}.md", "state", "feat_x", 4)` gives `"state/plan_revisions/feat_x/task_plan_revision_4.md"`, and the same call without a round leaves `{round}` in place.
  - `round_of_gate(graph, "plan_review").id == "plan_round"`, `round_of_writer(graph, "plan_writer").id == "plan_round"`, and both give `None` for `ui_review`.
  - `review_iteration` for `ui_review` with `review_0.md` and `review_2.md` planted under `tmp_path/state/ui_test_plan_reviews/feat_x/` gives 3, and with none gives 0.
  - It gives `None` for `plan_review` (a round gate) and for `plan_writer` (no folder).

**Verification:**

- `tests/test_reviewers.py` passes, and every expected value is written from reading the graph file, never from the code's output.
- `git grep -n 'ROUND_PLACEHOLDER: Final' devscene-flow-host/src` finds no definition outside `records/round_evidence.py`, and `paths.py` imports the constant from there.
- `reviewers.py` names `graphscene` only as `from graphscene import …` with names in `graphscene.__all__`.
