### 2. The story's top risk "resume a half-recorded round … over a real `FileStateStore`" has no case: `test_run_mode.py` only halts between sets

**File:** `graphscene/tests/facade/test_run_mode.py` (`test_a_stop_after_the_draft_halts_and_continue_run_finishes_from_the_state_file`) — "The draft's set of 1 asks STOP once"

The story index's first `Top risks:` entry, *"Wrong recording order or a dropped record after a mid-set `Halt`"*, states its mitigation: "Task 3 … resumes a half-recorded round with `continue_run`. Task 4 repeats that over a real `FileStateStore`." Task 3 delivered its half in `graphscene/tests/engine/test_run_loop.py` → `test_a_stop_on_a_retry_pass_saves_the_recorded_gate_and_continue_run_finishes`, over the in-memory store. Task 4's suite does not deliver the other half. Its only halt case stops **between** the draft's set and the edit-check set, so no round is open when the walk is saved. It cannot do otherwise on `valid_generic.json`, whose `review_round` has a single gate, `edit_check`. So the path the risk names has never been tested through the real JSON codec and file store: a round saved with some gates recorded (`awaiting: "set"`, an `open_round` with records, a pending `DispatchSet` cut down to the unrecorded gates) and then read back by a fresh `Walker` in `continue_run`.

The path works today. A probe run through `bash scripts/python-service.sh --package graphscene probe harness-runs/scratch/run_loop_probe.py <repo_root>`, over `valid_plain_round.json` and a `FileStateStore` in a temporary directory, printed every value asserted below. The halt was `Halt(reason='stop', detail='stop requested before a set of 1')`. The state file carried `"open_round": {… "records": {"license": {"gate": "license", "outcome": "accepted", "detail": "license.md"}}}`. `continue_run` returned `End(binding='<finish>', node='published', reports=(), passed=(RoundPassage(round='checks', number=0, verdict='pass'),))` with the one row `Launch(seq=1, node='lint', agent='lint-checker', attempt=1, max_attempts=3, result=Completed(outcome='accepted', detail=None))`. What is missing is the case.

**Fix:** In `graphscene/tests/facade/test_run_mode.py`:

1. Add `from types import MappingProxyType` beside `import asyncio`, and add `Completed`, `Dispatch` and `DispatchSet` to the `from graphscene import (...)` list, in its alphabetical order.
2. Below `_FIXTURE`, add:
   ```python
   _PLAIN_ROUND = Path(__file__).parents[1] / "fixtures" / "flow_graph" / "valid_plain_round.json"
   ```
3. Append this case:
   ```python
   def test_a_stop_mid_round_saves_the_recorded_gate_and_continue_run_finishes_from_the_state_file(
       tmp_path: Path,
   ) -> None:
       state_file = tmp_path / "walk.json"
       stub = _stub(
           {
               "lint": [
                   ScriptedFailure("infra", "session ended in error"),
                   ScriptedOutcome("accepted"),
               ],
               "license": [ScriptedOutcome("accepted", "license.md")],
           }
       )

       def walker() -> Walker:
           return Walker(load_graph_file(_PLAIN_ROUND), FileStateStore(state_file), DictHost({}))

       # The first pass's clear asks STOP once per gate; lint's retry pass's first ask is the third.
       assert asyncio.run(
           start_run(
               walker(),
               stub,
               signals=Signals(stop_after=2),
               counter=Counter(),
               sink=Rows(),
               limits=ExecutionLimits(backoff_seconds=0),
               failure_outcome=_HELD,
               entry="checks",
           )
       ) == Halt("stop", "stop requested before a set of 1")
       lint = Dispatch(
           node="lint",
           agent="lint-checker",
           prompt=None,
           counters=MappingProxyType({}),
           round_number=0,
           converging=None,
           closed_round=(),
           passed=(),
       )
       assert walker().current() == DispatchSet("checks", 0, (lint,), ())

       rows = Rows()
       assert asyncio.run(
           continue_run(
               walker(),
               stub,
               signals=Signals(),
               counter=Counter(),
               sink=rows,
               limits=ExecutionLimits(backoff_seconds=0),
               failure_outcome=_HELD,
           )
       ) == End("<finish>", "published", reports=(), passed=(RoundPassage("checks", 0, "pass"),))
       assert rows.rows == [Launch(1, "lint", "lint-checker", 1, 3, Completed("accepted"))]
   ```
4. In the module docstring, change "drives the committed graph `valid_generic.json` end to end" to "drives the committed graphs `valid_generic.json` and `valid_plain_round.json` end to end". Change "or a `Halt` that a later `continue_run` resumes from the saved walk" to "or a `Halt`, between sets or mid-round, that a later `continue_run` resumes from the saved walk". Change "from reading `valid_generic.json`" to "from reading the fixture".

Every expected literal comes from reading `valid_plain_round.json`. `checks` is an entry, and its gates are `lint` and `license`. Both declare `accepted` and lead to `checks`, whose `accepted` goes to `published` under `<finish>`. The graph declares no counters and `reports: []`, and `checks` declares no `writer`, so `converging` is `None`. This test file is the one the fix edits, so it is the only test the fix runs.
