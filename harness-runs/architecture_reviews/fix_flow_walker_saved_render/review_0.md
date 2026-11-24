# Architecture review — round 0

verdict: PASS
review_mode: full

## Should Fix

1. **`task_1_plan.md` — the record's version literal is not named as a `Final` constant.** `.claude/context/devscene-flow-host.md` → `## Shared code and constants` requires *"A record's fixed file name, directory name and fixed in-record literals are module-level `Final` constants in the module that reads or writes them"*. Task 1 names `PRINTED_READS_DIRECTORY: Final`, but specifies the document's `"version": 1` and the cause `version <json> is not 1` with no constant, while its precedent `host/revision_findings.py` carries `_VERSION: Final = 1` (and `_DOCUMENT_KEYS`). Add to the **`printed_reads.py` — the store.** bullet a module-level `_VERSION: Final = 1`, used by both the write and the version check. (Should Fix, not Must Fix: an implementer who reads the conventions document adds it anyway, so no failure sentence completes.)

## Nice to Have

1. **`task_3_plan.md` — the `graph.paths` lookup stays in two places.** After Task 3, `render._cap_lines` and `host/printed_reads.py` → `read_printed` both look up `graph.paths.get(stop.evidence)` and raise `graph has no 'paths.{stop.evidence}'`. `render` needs the rendered path to print `index`, so the lookup is justified. A one-line note in Task 3's **Evidence** bullet would make it clear that this repeat is deliberate and that the two messages must stay byte-identical.

## Checked and holding

- **Layer placement.** Every target sits under `devscene-flow-host/`. The new module goes in `host/`, beside `RefusalStore` and `RevisionFindingsStore`, which are the records the host keeps beside the walk (`.claude/context/devscene-flow-host.md` → `## The internal layers`, `## Records, and which one is the truth`). Its suite is `tests/test_printed_reads.py`, per the **Python test suite** naming row.
- **Dependency direction.** `host/printed_reads.py` imports `host.{paths,reviewers,store}`, `records.{index_evidence,round_files}`, `graphscene`'s public `Step`/`FlowGraph` and the standard library. `round_gates` and `re_entry` import it, and `commands/render.py` stops importing `review_iteration`, `fail_count` and `read_index_evidence`. No upward edge appears and no cycle forms: `host/reviewers.py` and `host/store.py` import nothing from `round_gates`. `commands` → `host` → `records` holds.
- **State placement and the lock.** The record follows the stated rule. It is a per-branch JSON file in the `Final`-named subdirectory `printed_reads/` of `<stateDir>/.flow_walker_state/`, written whole through `os.replace`. It is written only inside `with store.lock():` on `RefusalStore`, in `record_outcome` and `start_walk`, and only on a non-`Refused` action. `current_step` takes no lock and writes nothing (`.claude/context/devscene-flow-host.md` → `## Records, and which one is the truth`; verified against `host/round_gates.py` → `record_outcome` and `host/re_entry.py` → `start_walk`, `current_step`).
- **Business-logic placement.** The disk reads leave the `commands` renderer and move to `host`, so `render` only renders (`## The internal layers`: *"rendering and exit statuses are `commands`"*).
- **Accompanying set.** The new module carries a docstring with its rule and a **Deliberately not covered** list, and the boundary test needs no registration. The new test file opens with *"The rule this file exists to enforce"*. The README `## The layers` `host` row is updated (Task 5). No new layer or import rule is introduced, so no `[tool.importlinter]` change is owed.
- **Errors.** Decoding raises `ValueError(f"{path}: {cause}")`, the same shape as the `RevisionFindingsStore` precedent, which `commands/flow_walker.py` already maps to exit `2`.
- **No plan asks for a test run.** Every **Verification:** bullet names only a test file its own task creates or edits, run through `bash scripts/python-service.sh --package devscene-flow-host test tests/<file>.py`.
- **Laundering check.** The one task-prompt quotation (story index → `## Scope register`) sits between the markers. No line outside them tells an agent how to work.
