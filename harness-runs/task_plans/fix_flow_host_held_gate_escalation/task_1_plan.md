### Task 1 — State the host's held-gate order in `round_gates.py` and pin it in `test_round_gates.py`

**Goal:** Turn the host's re-dispatch-first order into a stated rule of `devscene_flow_host.host.round_gates`, delete the `TODO: @claude` marker #464 left at `_redispatch`, and pin the order in `devscene-flow-host/tests/test_round_gates.py` with literal expectations. **No executable line changes.** The decision (story index `## Context`) keeps the host's order, so only the module docstring, one comment and the test file move.

**Where this task stops.** This task owns the docstring rule and the tests. The package README is **Task 2's**: the **Recording a gate.** paragraph, the *"One departure from the bash walker remains"* paragraph and the `## Differences from flow-walker.sh` entry. Task 2 cites the two test-case names this task leaves, exactly as written here: `test_a_held_error_beside_a_refused_gate_re_dispatches_first` (existing, kept under that name) and `test_a_held_error_waits_while_its_refused_sibling_is_refused_again` (new).

### Targets

- `devscene-flow-host/src/devscene_flow_host/host/round_gates.py`: the module docstring, and the comment at the top of `_redispatch`.
- `devscene-flow-host/tests/test_round_gates.py`: the module docstring, the existing case's docstring and one new case.

**Work:**

- [ ] `round_gates.py` module docstring, under *"The rule:"*: right after the bullet *"A refused file records nothing in the walk: … every refused gate is re-dispatched as one set in the same round."*, add this bullet, keeping the docstring's line width (≤ 100, ruff):
  > A held gate at a join whose only gates out are refused ones does not escalate there: the refused gates are re-dispatched as one set in the same round, and the held gate escalates at the round's next join, once every re-dispatched gate has a verdict or is held, so the escalation carries the whole round's verdicts. `flow-walker.sh` → `record_in_set` escalates at once instead ("With none out: a held gate escalates"); this order is the host's, chosen in #472, and GraphScene is not changed for it.

  Under *"Deliberately not covered:"*, delete the bullet *"A held gate at a join whose only gates out are refused ones: … Marked by the `TODO` at `_redispatch`."* and keep the rendering / `start` bullet unchanged.
- [ ] `round_gates.py` → `_redispatch`: delete the four-line `# TODO: @claude add a follow up task for this: escalate a held gate …` comment. Leave every statement in `_redispatch`, `_settle`, `_record` and `record_outcome` byte-identical.
- [ ] `test_round_gates.py` module docstring: replace the paragraph *"It pins the one departure from bash as it stands: … (the `TODO` at `round_gates._redispatch`)."* with a statement of the rule it pins: *"It pins the host's held-gate order, chosen over bash's in #472: a held gate whose only siblings out are refused ones waits while they are re-dispatched in the same round, and escalates at the round's next join."* In the closing paragraph, name the source of those cases' literals too: `round_gates`' rule above, and `flow-walker.sh` → `OUTPUT`'s `<escalate>` grammar (*"node: and agent: are the first held gate's in `gates` order, reason: its outcome, then held: <gate> <outcome> per held gate, one refused: line per gate held by refusal"*).
- [ ] `test_a_held_error_beside_a_refused_gate_re_dispatches_first`: keep its name and body. Replace its docstring, which calls it *"The held-gate departure, marked by the `TODO`"*, with one stating the rule: the held `architecture_review` waits while the refused `plan_review` is re-dispatched, and escalates at the round's next join. Bash would escalate it at once.
- [ ] Add `test_a_held_error_waits_while_its_refused_sibling_is_refused_again(tmp_path: Path) -> None`, using the file's own helpers (`_walker`, `_file`, `_record`, `_NO_CLASS_BODY`, `_NO_CLASS`, `_PLAN_DISPATCH`, `_PLAN`, `_PARITY`). Write the expected values as literals from the rule and the `<escalate>` grammar above. Never take them from the code's output. If the code answers otherwise, report it as a finding and do not change the literal to match. Sequence and expectations:
  1. `FAIL` at `plan_review` with the `_NO_CLASS_BODY` file `bad` (attempt 1), then `PASS` at `business_parity_review` with a `PASS_BODY` file.
  2. `error` at `architecture_review` → `HostStep(DispatchSet("plan_round", 0, (_PLAN_DISPATCH,), ()), (Refusal("plan_review", 1, _NO_CLASS),))`. The held gate does not escalate.
  3. `FAIL` at `plan_review` with `bad` again → `HostStep(DispatchSet("plan_round", 0, (_PLAN_DISPATCH,), ()), (Refusal("plan_review", 2, _NO_CLASS),))`. Still no escalation.
  4. `FAIL` at `plan_review` with `bad` a third time → `HostStep(Stop(binding="<escalate>", node="architecture_review", agent="architecture-reviewer", reason="error", summary=None, evidence=None, round_counts=(), held=(GateRecord("architecture_review", "error", None), GateRecord("plan_review", "error", None)), closed_round=(), passed=()), (Refusal("plan_review", 3, _NO_CLASS),))`. The first held gate in `gates` order names the stop, both held gates are listed, and there is one `refused:` refusal for the gate held by refusal.

**Verification:**

- `bash scripts/python-service.sh --package devscene-flow-host test tests/test_round_gates.py` passes. That includes the new case, the existing held-gate case and #465's kept-findings cases (`test_a_non_round_reviewers_findings_file_is_kept_for_the_revision`, `test_a_closing_round_clears_an_earlier_kept_file`, `test_a_held_outcome_at_a_gate_of_an_open_set_keeps_nothing`), unchanged.
- `bash scripts/python-service.sh --package devscene-flow-host lint` reports nothing for the two targets.
- `git grep -n 'TODO: @claude' -- devscene-flow-host/src/devscene_flow_host/host/round_gates.py` prints nothing.
- `git diff -- devscene-flow-host/src/devscene_flow_host/host/round_gates.py` changes only lines inside the module docstring and the deleted comment lines in `_redispatch`. No statement differs. This is the story index's first `Top risks:` entry.
- `git grep -nE 'departure|_redispatch' -- devscene-flow-host/tests/test_round_gates.py devscene-flow-host/src/devscene_flow_host/host/round_gates.py` hits only the `def _redispatch` line and its two call sites. No docstring there still calls the held-gate order a departure or points at a marker.
