### Task 5 — Record the printed reads and close the three Still open entries in the README

**Goal:** Bring `devscene-flow-host/README.md` in line with what Tasks 1–4 built, so #419 reads no difference that no longer exists:
- the host's new record and where it lives;
- what `start_walk`, `record_outcome` and `current_step` do with it;
- the narrowed **Chosen** entry;
- the three **Still open** entries, closed.

This task owns rows 1–4 of the story index's `## Scope register`.

**Depends on:** Task 4. The names this task documents are:
- `read_printed` and `PrintedReadsStore` in `host/printed_reads.py`, the record at `<stateDir>/.flow_walker_state/printed_reads/<percent-encoded branch>.json` (Task 1);
- `HostStep.printed` and its write in `record_outcome` and `start_walk`, under `RefusalStore`'s lock and only on a non-`Refused` action. `current_step` returns the record unchanged and reads disk only when no record exists (Task 2).
- `render` printing from `HostStep.printed` and reading no file (Task 3);
- the end-to-end cases in `tests/test_flow_walker.py` (Task 4).

### Targets

- `devscene-flow-host/README.md`

**Work:**

- [ ] **`## The layers` → the `host` row:** add `read_printed` and `PrintedReadsStore` (`host/printed_reads.py`) to the `Holds` cell, in that cell's existing form.
- [ ] **`## What it reads, answers and keeps`.**
  - Add a **Printed reads.** paragraph after **Kept findings files.** It says:
    - The values a step read from disk when printed are kept as the host's record `PrintedReadsStore`, at `<stateDir>/.flow_walker_state/printed_reads/<percent-encoded branch>.json`. They are a non-round reviewer's next free index, a cap's `FAIL` counts and the story index's evidence.
    - `record_outcome` and `start_walk` write the record under `RefusalStore`'s lock, only when the action is not `Refused`. `HostStep.printed` carries it, and `render` prints from it.
    - `current_step` returns it as kept. It reads the files only when no record exists.
  - In **Resuming a round.**, extend the `current_step` sentence to say that it returns the printed reads as kept.
- [ ] **`## Differences from flow-walker.sh` → **Chosen** → *"`current` re-renders."*:** narrow the entry. The command re-renders the saved step, but the values bash would have read from disk at print time come from the printed-reads record, so a file written since the step was printed changes nothing on `current`. Keep the suites it names, and add `flow-walker-resume.test.mjs` → *"(4) a UI reviewer in flight is re-dispatched"*, `flow-walker.test.mjs` → *"(3) architecture FAILs every round until the cap"* and `flow-walker-ui-and-reentry.test.mjs` → *"(4) UI reviewer FAILs until the cap"* as suites that now hold unchanged. Cite `tests/test_flow_walker.py`'s two new cases as the host's pins.
- [ ] **`## Differences from flow-walker.sh` → **Still open**:**
  - **Remove the three `— #475` entries.** Keep the heading and state under it that no difference is open.
  - **Add one sentence on the withdrawn `evidence.open:` entry.** It was not a difference: `fw_index_evidence` prints one `evidence:` line however many `## Rejected findings` headings an index carries, and every open entry after it in file order, as the command does. Cite `tests/test_index_evidence.py` and `tests/test_render.py`, which pin it.

  The heading stays because `.claude/context/devscene-flow-host.md` names **Chosen** and **Still open** as the two places a difference is recorded.

**Verification:**

- `git grep -n '#475' -- devscene-flow-host/README.md` prints no line inside a **Still open** entry, and `git grep -n 'TODO' -- devscene-flow-host/README.md` prints nothing.
- Every name the README now cites — `read_printed`, `PrintedReadsStore`, `HostStep.printed`, `printed_reads`, and the two new `test_flow_walker.py` case names — exists under `devscene-flow-host/` (`git grep -n` each, from the repository root).
- Re-run the story index's `## Scope register` command entry. Its output lists no file beyond the register's rows, and rows 1–4 read as their dispositions say.
