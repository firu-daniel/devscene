### Task 2 — Expose the predicate host's last refusal reason as `HarnessPredicateHost.last_refusal`

**Goal:** Let the command print the host's reason when a walk is refused because a predicate cannot be answered — `cannot resolve phases.<p> in <root>/devscene.config.json`, or the run-mode reason — instead of GraphScene's generic `the host cannot answer predicate '<p>' for node '<n>'`, as `flow-walker.sh` → `eval_skip` refuses with the reason itself.

**Why the host has to carry it.** GraphScene's `_taken_skip` (`graphscene/src/graphscene/engine/transitions.py`) returns a `Refused` naming only the predicate and the node, and `open_walker` builds the `HarnessPredicateHost` inside itself, so the caller cannot ask `refusal_reason(predicate)` without parsing GraphScene's text. The host remembers the reason of the answer it could not give.

**The contract this task produces:** `HarnessPredicateHost.last_refusal: str | None` — read-only (a property over a private attribute), `None` on a fresh host; every `answer` call that returns `None` sets it to that predicate's reason (the same text `refusal_reason` gives), and every `answer` that returns a boolean resets it to `None`. A `None` answer is always the walk's last question before its `Refused`, so after a `Refused` step it names the cause. **Task 5** reads it as `walker.host.last_refusal` after narrowing `walker.host` with `isinstance(…, HarnessPredicateHost)`, and prints it in place of the `Refused` reason when it is not `None`.

### Targets

- `devscene-flow-host/src/devscene_flow_host/host/predicates.py`
- `devscene-flow-host/tests/test_predicates.py`

**Work:**

- [ ] `host/predicates.py`: add the `last_refusal` property and set it in `answer` from `_resolve`'s result, as the contract states; `refusal_reason` is unchanged. Add the rule to the module docstring and replace the *"Deliberately not covered"* line about rendering a refusal with: rendering stays the `commands` layer's, which reads `last_refusal`.
- [ ] `tests/test_predicates.py`: a fresh host's `last_refusal` is `None`; after `answer("phase_qa_off", …)` against a planted config with no `phases.qa`, it is `cannot resolve phases.qa in <root>/devscene.config.json`; a following answer that resolves resets it to `None`; after `answer("run_mode_skips_qa", …)` with no ledger and no skipped ids it is `no run-mode record: no flow-progress ledger for '<branch>' and no skipped ids given`. One case walks the real graph through `open_walker(root, branch, graph, skipped=None)` with no ledger: `start` returns a `Refused`, and `walker.host.last_refusal` holds the run-mode text. Literals written from `host/predicates.py` → `_resolve` and `records/ledger.py` → `read_run_mode`, never from the output.

**Verification:**

- `bash scripts/python-service.sh --package devscene-flow-host test tests/test_predicates.py` passes, run as one foreground command from the repository root.
- `refusal_reason`'s existing cases pass unchanged: the new attribute adds a reading, it changes no answer.
