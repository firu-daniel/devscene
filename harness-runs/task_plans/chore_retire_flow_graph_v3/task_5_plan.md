### Task 5 — Find the walker's graph as `<flows>/<flow>.graph.json` across the flow host, its suites and its README

**Goal:** `devscene-flow-walker` finds its graph as `<flows>/<flow>.graph.json`, the name Task 1 ships the format-4 graph under. The flow host's suites read the checkout's graph at that path, and nothing in `devscene-flow-host/` still cites the retired generator or the `.v4` name.

**Depends on:** Task 1, which moves the format-4 graph to `cli/templates/scripts/flows/task_plan_writing.graph.json` and removes `cli/templates/scripts/flows/task_plan_writing.v4.graph.json`. The contract this task consumes is that path and that file name. Its content is the format-4 graph byte for byte except its `description` string, so every expected value the suites assert from reading the graph still holds. **This task closes the red window** the story index's `## Context` names: from Task 1 until this task lands, these suites and the `cli/test/flow-walker*` suites fail because the graph is not where they look.

**Where this layer stops.** Only the name the command finds changes: `GRAPH_SUFFIX` stays a `Final` constant in `commands/flow_walker.py`, and its exit-status contract is unchanged — a missing graph file is still exit `1` with `unknown flow '<flow>': no <file>`. Do not add a fallback to the `.v4` name: `harness-runs/lessons.md` → *"A rename declared breaking ships no compatibility path"*. Checks 4–7 are **Task 6's**. They are not in the shipped package, and this task adds nothing for them.

### Targets

- `devscene-flow-host/src/devscene_flow_host/commands/flow_walker.py` — `GRAPH_SUFFIX` and the module docstring.
- `devscene-flow-host/src/devscene_flow_host/host/predicates.py` — the module docstring's *"The rule:"* sentence.
- `devscene-flow-host/tests/test_predicates.py`, `test_printed_reads.py`, `test_re_entry.py`, `test_render.py`, `test_resume.py`, `test_reviewers.py`, `test_round_gates.py`, `test_walking.py` — each suite's `_GRAPH` path and the docstring line naming it.
- `devscene-flow-host/tests/test_flow_walker.py` — the missing-graph expectation.
- `devscene-flow-host/README.md` — `## The command line` (the `--flows` row and the exit `1` row) and `## Differences from flow-walker.sh` → **The graph.**

**Work:**

- [ ] `flow_walker.py`: `GRAPH_SUFFIX: Final = ".graph.json"`. In the module docstring's `1:` item, *"no `<flows>/<flow>.v4.graph.json`"* becomes *"no `<flows>/<flow>.graph.json`"*.
- [ ] `predicates.py`: the docstring's *"the two name patterns `scripts/generate-flow-graph-v3.mjs` → `V3_PREDICATES` accepts — "* becomes a statement of the two name patterns themselves, citing no generator. `phase_<p>_off` and `run_mode_skips_<id>`, `PHASE_PREDICATE` and `RUN_MODE_PREDICATE`, and the rest of the rule are unchanged, and so is the code.
- [ ] The eight suites with a `_GRAPH` constant: change its final path segment from `"task_plan_writing.v4.graph.json"` to `"task_plan_writing.graph.json"`. Change the same name in each module docstring that cites `cli/templates/scripts/flows/task_plan_writing.v4.graph.json` (`test_printed_reads.py`, `test_re_entry.py`, `test_render.py`, `test_resume.py`, `test_reviewers.py`, `test_round_gates.py`, `test_walking.py`). Change no expected value.
- [ ] `test_flow_walker.py`: the missing-graph expectation, *"flow-walker: unknown flow 'nope': no {_FLOWS}/nope.v4.graph.json\n"*, becomes `nope.graph.json`. It is a literal written from the new `GRAPH_SUFFIX`, per `.claude/context/devscene-flow-host.md` → `## Tests — what "done" means here`.
- [ ] `devscene-flow-host/README.md`: the `--flows` row and the exit `1` row say `<flow>.graph.json`. **The graph.** says the command reads format 4 at `<flows>/<flow>.graph.json` (`commands/flow_walker.py` → `GRAPH_SUFFIX`). It drops every mention of the `.v4` name, and keeps its contrast with bash's format-3 read and its suite citation.

**Verification:**

- Each test file this task edits passes, run one at a time as `bash scripts/python-service.sh --package devscene-flow-host test tests/<file>.py`, for `test_flow_walker.py`, `test_predicates.py`, `test_printed_reads.py`, `test_re_entry.py`, `test_render.py`, `test_resume.py`, `test_reviewers.py`, `test_round_gates.py` and `test_walking.py`. `test_walking.py` loading the graph through `load_graph_file` is the evidence that the moved file passes every library check under its new name.
- `git grep -n -e 'v4\.graph' -e 'generate-flow-graph' -e 'V3_PREDICATES' -- devscene-flow-host` prints nothing.
- `git grep -n 'GRAPH_SUFFIX' -- devscene-flow-host/src` shows the one definition, `".graph.json"`, and its one use, which builds `<flows>/<flow><suffix>`.
