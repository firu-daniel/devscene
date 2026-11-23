# Architecture review — round 0

verdict: PASS
review_mode: full

## Should Fix

1. **`task_7_plan.md` / `task_2_plan.md` — the branch settles one of the layer's open questions (the error type) but leaves the others its first behaviour also decides unrecorded.** `.claude/context/devscene-flow-host.md` → `## Not determined` says the open conventions are *"owed by this layer's first module that carries behaviour or by a line in `devscene-flow-host/README.md`"*. Among them: *"the mandated logger and output surface"*, *"storage-key and environment-variable constants"*, *"wire-surface types and how a serialized field name relates to its Python attribute"* and *"which store is the source of truth for shared state"*. This branch's modules are that first behaviour, and they decide each of these in practice:
   - nothing in the package prints;
   - `LEDGER_DIRECTORY`, `STATE_DIRECTORY` and `CONFIG_FILENAME` each live in the module that owns its path;
   - `stateDir` becomes `HarnessConfig.state_dir`;
   - the saved walk is the source of truth, and the configuration and ledger are re-read on every arrival.

   Task 7 records only the error type in the README. The naming one needs a decision, not just a record. `.claude/context/conventions.md` → `## Configuration is the source of truth, and it is read at run time` → **Serialized names and in-language names are the same identifiers.** says *"the property of the interface that reads it carries that key verbatim … There is no mapping layer and none may be introduced"*. Its examples are `cli/src/config/model.ts`'s, and the layer document lists the Python mapping as open, so this is a Should Fix and not a Must Fix. **Fix:** add one short paragraph to Task 7's README work, under `## What it reads, answers and keeps` or `## Errors`, stating the four answers above. In Task 2's `records/config.py` docstring, either state the `stateDir` → `state_dir` mapping as a deliberate rule for this layer, giving its reason, or keep the key's own spelling. That way the conventions pass after this branch has a source to read instead of having to infer one.

2. **`task_1_plan.md` (the three layer `__init__.py` docstrings) and `task_7_plan.md` (the README's `## The layers` table) — future contents are described with no roadmap citation.** The plan rightly drops issue numbers, but it still writes deferrals into durable text with no reference at all. Examples are `records`'s *"and later the round and reviewer files"*, `commands`'s *"It holds no module yet"*, and the README's "Holds next" column. `.claude/context/conventions.md` → `## Documents of record` says *"A deferral cites a numbered roadmap item, and the number owes a row."* A row already exists: `ROADMAP.md` item 14, **GraphScene**, whose `Left:` list carries *"the walker's port onto the engine"*. **Fix:** where Task 1's docstrings and Task 7's README name a layer's later contents, cite roadmap item 14 (`ROADMAP.md` → `GraphScene`). Do not cite an issue number.

3. **`task_4_plan.md` — the refusal text gives a file name without saying where the name comes from.** `refusal_reason` must produce `cannot resolve phases.<p> in <repo_root>/devscene.config.json`. Task 4 says to import `PHASES` from `records.config` *"rather than retyped"*, but says nothing like that for the file name, which `records/config.py` owns as `CONFIG_FILENAME` (Task 2). `.claude/context/conventions.md` → `## Configuration is the source of truth, and it is read at run time` says *"a value is imported from its owner rather than retyped"*. **Fix:** in Task 4's `refusal_reason` bullet, have the text built from `records.config.CONFIG_FILENAME`, with the test still asserting the literal.

## Nice to Have

1. **`feat_devscene_flow_host_walker_story_plan.md` → `## Context`** says *"one `test_<module>.py` per module"*, but `records/errors.py` gets no `test_errors.py`. `RecordError` is exercised through `tests/test_config.py` and `tests/test_ledger.py`, which is enough. The sentence should say that, so it does not promise a file nobody is going to write.
2. **`task_3_plan.md` — choosing between the ledger and the caller's argument.** That choice is made in `records` (`read_run_mode`). The `host` docstring Task 1 writes says the host *"holds the harness's rules over its records"*. Keeping it in `records` is defensible, because it mirrors one bash reader, `fw_run_mode_skipped`, as a whole. Task 1's `records` docstring could say that a reader may combine a record with a caller-given fallback, so the two docstrings don't seem to disagree.
