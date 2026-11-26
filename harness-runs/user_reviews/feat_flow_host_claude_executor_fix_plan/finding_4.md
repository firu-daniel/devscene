### 4. `ClaudeExecutor.run` hands GraphScene's prompt variant to `claude -p` as the agent prompt

**File:** `devscene-flow-host/src/devscene_flow_host/host/claude_executor.py` (`ClaudeExecutor.run`) — "dispatch.prompt," and "the dispatch carries no prompt"
**Class:** Wrong behaviour
**Failure:** If the running program passes `ClaudeExecutor.run` a reviewer dispatch walked from `scripts/flows/task_plan_writing.graph.json`, then `run` raises `ValueError("<node>: the dispatch carries no prompt")` instead of launching a session, because none of those reviewer nodes declares `prompts`, so the `Dispatch.prompt` it carries is `None`. A writer's revision dispatch launches `claude -p revision`.

**Problem.** GraphScene's `Dispatch.prompt` (`graphscene/src/graphscene/model/walk_actions.py` → `Dispatch`) is not prompt text. It is the node's prompt variant. `graphscene/src/graphscene/engine/transitions.py` sets it from `draft.prompts.get(node.id)`, and a route edge's `prompt` (`initial` or `revision`, one of the target node's `prompts`) is the only thing that fills it. It is `None` for a node reached by an edge that carries no `prompt`, and always `None` for a node that declares no `prompts`. `devscene-flow-host/src/devscene_flow_host/commands/render.py` → `_block` reads it that way: `variant = dispatch.prompt if dispatch.prompt is not None else "initial"`, and only when `node.prompts is not None`.

In `scripts/flows/task_plan_writing.graph.json`:
- `business-parity-reviewer`, `architecture-reviewer`, `task-plan-reviewer` and `ui-tests-plan-reviewer` declare no `prompts`. Every one of their dispatches makes `run` raise.
- The two writers, `task-plan-writer` and `ui-tests-plan-writer`, declare `["initial", "revision"]`. Only the revision edges carry a `prompt` (`"revision"`), so an initial writer dispatch also carries `None` and raises, and a revision launches with `-p revision`. The review says the writers would be launched with `-p initial`; the code shows an initial writer raises instead, which is the same defect.

`devscene-flow-host/tests/test_claude_executor.py` misses this because `_dispatch` passes the literal text `"Review the plan."` as `Dispatch.prompt`.

The pilot builds the real text in `cli/templates/scripts/lib/planning-node-lib.sh` → `pnl_prompt`. It fills the `PNL_CORE_BLOCKS` dispatch blocks, cut from `plugin/instructions/task_plan_writing_instructions_core.md`, with the branch, the iteration, the review mode and the findings files. `cli/templates/scripts/lib/planning-driver-lib.sh` then appends answered clarification pairs to a writer's prompt.

**Fix.** Ship the seam: a builder the host supplies at construction, from `Dispatch` to the text the session is given. Call that text the **agent prompt** (`agent_prompt`) everywhere this change touches (code, tests, README) so it is never confused with GraphScene's variant. Do **not** port `pnl_prompt` or the core's blocks, and do **not** rename GraphScene's `Dispatch.prompt`. Both belong to the later branch that makes prompt sources and node hooks declarations, which is not yet merged. Name no issue or PR number anywhere in this change (Finding 3).

**The three open questions, settled as follows.**
- **Repeatability.** The builder must return the same agent prompt for a repeated run of the same dispatch. A run may be repeated (a retry, an interrupt's resume), and `graphscene/src/graphscene/model/execution.py` requires an executor's side effects to be repeatable. This is the builder's obligation, stated in the docstring and the README. The executor cannot verify it. The executor calls the builder exactly once per `run` and keeps nothing between runs.
- **An unbuildable agent prompt is raised as a defect at `run`, not caught at construction.** At construction the executor has no dispatch, so it has nothing to build. A return schema is a static input, while an agent prompt is a function of the dispatch. Checking the prompt sources belongs to the host's builder when the host constructs it, which is the later branch's work. In `run`, an exception from the builder propagates unchanged, and a builder that returns anything other than a non-blank `str` raises `ValueError`. Both happen before the launch, so nothing is launched and the usage sink is not called, as for an agent with no contract. Neither becomes a `Failed`: retrying cannot repair a defect, and an exception out of `run` is a defect (`execution.py`).
- **The agent prompt goes on `SessionUsage`** as `agent_prompt: str`. The record is the host's only view of a session after `run` returns, and a stored stream is unreadable without the text that produced it. The prompt is built before the launch, so it is present on every recorded path, the launch error included.

**Code: `devscene-flow-host/src/devscene_flow_host/host/claude_executor.py`.**
1. Add, beside `UsageSink`:

   ```python
   class AgentPromptBuilder(Protocol):
       """Builds the agent prompt, the text a session is given, for one dispatch; the same
       dispatch gives the same agent prompt."""

       def __call__(self, dispatch: Dispatch) -> str: ...
   ```

2. Add the constructor keyword `agent_prompt_builder: AgentPromptBuilder`. It is required, sits directly after `usage_sink`, is stored as `self._agent_prompt_builder` and has no construction check.
3. In `run`, after the contract lookup, delete the `if dispatch.prompt is None: raise ValueError(...)` block and build the prompt instead:

   ```python
   agent_prompt = self._agent_prompt_builder(dispatch)
   if not isinstance(agent_prompt, str) or not agent_prompt.strip():
       raise ValueError(f"{dispatch.node}: the agent prompt builder returned no agent prompt")
   ```

   The argument vector passes `"-p", agent_prompt`. The executor no longer reads `dispatch.prompt` at all: the builder reads it to choose the variant.
4. Add `agent_prompt: str` to `SessionUsage` directly after `agent`, and set it in both `SessionUsage(...)` constructions (the launch-error one and the session one).
5. Module docstring, *"The rule:"* bullets:
   - Replace `- A dispatch whose agent has no contract, or that carries no prompt, is a defect and is raised.` with two bullets. The first says that `dispatch.prompt` is the node's prompt variant (`initial`, `revision`) or `None`, never the text a session is given; that the agent prompt comes from the host's `AgentPromptBuilder`, called exactly once per `run` before the launch, with nothing kept between runs; and that the builder must return the same agent prompt for a repeated run of the same dispatch. The second says that a dispatch whose agent has no contract raises `LookupError`, an exception out of the builder propagates unchanged, and a builder that returns no non-blank string raises `ValueError`, each before the launch, so nothing is launched and the sink is not called.
   - In the bullet beginning `- The usage record also carries`, add "the agent prompt it was given".
6. Module docstring, *"Deliberately not covered:"*: add these two bullets.

   ```
   - Building an agent prompt from the instruction core's dispatch blocks and appending answered
     clarification pairs, as `cli/templates/scripts/lib/planning-node-lib.sh` → `pnl_prompt` and
     `cli/templates/scripts/lib/planning-driver-lib.sh` do, and refusing a prompt source that
     cannot be built when the host constructs its builder: the later branch that makes prompt
     sources and node hooks declarations, not yet merged.
   - Renaming GraphScene's `Dispatch.prompt`: that same later branch's.
   ```

**Tests: `devscene-flow-host/tests/test_claude_executor.py`.** Every case uses an in-test builder, and every expected value is a literal.
- Add `def _agent_prompt(dispatch: Dispatch) -> str: return f"{dispatch.node}: review the plan."`. Pass it as `agent_prompt_builder` from `_executor`, from the `arguments` dict of `test_the_constructor_refuses_each_caller_defect` and from the direct `ClaudeExecutor(...)` in `test_through_execute_set_the_usage_record_precedes_its_launch_row`.
- Rename `_dispatch`'s `prompt` parameter to `variant: str | None = None` (still passed as `Dispatch(prompt=variant, …)`). Its default now matches a reviewer node, which declares no `prompts`.
- `test_the_argument_vector_passes_the_hosts_args_through_in_place`: the expected vector opens `"-p", "plan_review: review the plan."`.
- `test_a_completed_session_returns_its_absolute_detail_and_one_usage_record`: also assert `usage.agent_prompt == "plan_review: review the plan."`.
- `test_a_launch_error_is_an_infra_failure_with_empty_usage`: add `usage.agent_prompt` to the asserted tuple, expected `"plan_review: review the plan."`.
- Delete `test_run_raises_for_a_dispatch_with_no_prompt`. Add these cases:
  - `test_a_dispatch_with_no_prompt_variant_launches_with_the_built_agent_prompt`: `_dispatch()` (variant `None`) with an `argv_file`. The result is `Completed("PASS", None)`, and the recorded argv's first two words are `["-p", "plan_review: review the plan."]`.
  - `test_the_builder_receives_the_dispatch_and_the_variant_never_reaches_claude`: a builder that appends each dispatch it receives to a list and returns `"Revise the plan."`, run with `_dispatch(variant="revision")`. The list equals `[_dispatch(variant="revision")]`, the recorded argv opens `["-p", "Revise the plan."]`, and `"revision"` is not in the recorded argv.
  - `test_an_exception_from_the_builder_propagates_before_any_launch`: a builder that raises `RuntimeError("no dispatch block for plan_review")`. `pytest.raises(RuntimeError)` matches that exact message, `sink.records == []`, and the `argv_file` does not exist.
  - `test_a_blank_agent_prompt_is_raised_before_any_launch`: a builder that returns `" \n"`. It raises `ValueError` with the exact message `"plan_review: the agent prompt builder returned no agent prompt"`, `sink.records == []`, and the `argv_file` does not exist.
- `test_a_repeated_run_launches_the_same_vector_and_reports_twice`: use a builder that counts its calls and also assert it was called exactly twice.
- In the test module docstring, change "its constructor and `run` refuse each caller defect with an exact message" so that it also covers building the agent prompt through the host's builder, never from `Dispatch.prompt`.

**README: `devscene-flow-host/README.md`.**
- `## The layers` → the `host` row: change `ClaudeExecutor`, `UsageSink` and `SessionUsage` (`host/claude_executor.py`) to `ClaudeExecutor`, `UsageSink`, `AgentPromptBuilder` and `SessionUsage` (`host/claude_executor.py`).
- `## The executor` → **What it is given.** table: add a row after `usage_sink`:

  ```
  | `agent_prompt_builder` | The host's `AgentPromptBuilder`: given a `Dispatch`, returns the agent prompt, the text the session is given; it must return the same agent prompt for a repeated run of the same dispatch | The host |
  ```

- Replace the sentence that begins "A dispatch whose agent has no contract raises" and contains "one that carries no prompt raises" with a new paragraph headed **The agent prompt.**. It states:
  - that `Dispatch.prompt` is GraphScene's prompt variant (`initial`, `revision`, or `None` for a node with no `prompts`), as `commands/render.py` → `_block` reads it, and never the text a session is given;
  - that `run` calls `agent_prompt_builder` once per run, before the launch;
  - that a dispatch whose agent has no contract raises `LookupError`, an exception from the builder propagates, and a builder that returns no non-blank string raises `ValueError`, each before the launch and with no usage record: defects in the caller, not a node's result;
  - that building the prompt from the instruction core's blocks, as `pnl_prompt` does, is the later branch that makes prompt sources and node hooks declarations.
- **The flags it adds.**: in "then `-p <prompt>`", change `<prompt>` to `<agent prompt>`.
- **The usage sink.**: in the list of what `SessionUsage` carries, add "the agent prompt" after "the agent".
