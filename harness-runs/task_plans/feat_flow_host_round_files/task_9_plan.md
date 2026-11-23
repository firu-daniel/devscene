### Task 9 — Describe the round and reviewer files in the package README

**Goal:** Bring `devscene-flow-host/README.md` up to date with what Tasks 1–8 shipped. The README is the package's own statement of what it reads, answers and keeps, and right now it says the host reads only the configuration and the ledger.

**Depends on:** Tasks 1–8. This task describes these modules and changes none of them:
- `records/round_files.py` (`review_verdict`, `round_file_problem`, `next_review_index`, `fail_count`, `round_file_path`);
- `records/round_evidence.py` (`read_round_evidence`);
- `records/index_evidence.py` (`read_index_evidence`);
- `host/paths.py` (`render_path`);
- `host/reviewers.py` (`round_of_gate`, `round_of_writer`, `review_iteration`);
- `host/refusals.py` (`RefusalStore`, at `<stateDir>/.flow_walker_state/round_refusals/<percent-encoded branch>.json`);
- `host/resume.py` (`round_resume`);
- `host/round_gates.py` (`record_outcome`, `HostStep`);
- `host/re_entry.py` (`start_walk`, `current_step`).

### Targets

- `devscene-flow-host/README.md` — the story index's `## Scope register` row 1.

**Work:**

- [ ] `## What it is`: add to the sentence listing what the host does that it reads the round and reviewer files, applies the reviewer-file rules, and resumes a round from the files on disk. Keep *"it has no command line yet"*.
- [ ] `## The layers`: name the new modules in the `host` and `records` rows' *Holds* cells, in the existing `` `symbol` (`path`) `` form.
- [ ] `## What it reads, answers and keeps`: add three paragraphs in the section's bold-lead style.
  - **Round and reviewer files.** Each reader reads as the bash function it names (`fw_review_verdict`, `fw_round_file_check`, `fw_next_review_index`, `fw_fail_count`, `fw_round_evidence`, `fw_index_evidence`). A missing round file is a value.
  - **Recording a gate.** The four reviewer-file rules, and the refusal record's path and lock order.
  - **Resuming a round.** The resume rules, `start_walk` and `current_step`, and the one departure the `TODO: @claude` marker in `host/round_gates.py` names.
- [ ] `## Errors`: add that a malformed refusal record raises `ValueError` naming the file and its lock `TimeoutError`, as the walk's store does, and that a round gate with no `findingsFolder` raises `ValueError`. Every other sentence stays as written.

**Verification:**

- Each symbol and path the README names resolves: `git grep -n` for each new symbol under `devscene-flow-host/src/` finds its definition in the module the README names.
- The README states the departure with the same wording as the marker in `host/round_gates.py`, and nowhere claims bash parity for that case.
