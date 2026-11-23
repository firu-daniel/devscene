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
  - **Recording a gate.** The four reviewer-file rules, and the refusal record's path and lock order. Then the two departures, each in its own marker's wording; `host/round_gates.py` carries a `TODO: @claude` marker for each (Task 7 → **The two departure markers and the docstring.**):
    - **The held-gate escalation.** Its marker sits at the re-dispatch branch: *"escalate a held gate at a join whose only gates out are refused ones, as flow-walker.sh → record_in_set does ("With none out: a held gate escalates") — needs a GraphScene way for a host to set a due gate aside in an open round"*. Say what the host does instead: it re-dispatches the refused gates first.
    - **The non-round findings file.** Its marker sits at `record_outcome`'s non-gate branch: *"keep a findings file given outside a round gate (a non-round reviewer's FAIL, or answered) as flow-walker.sh → next keeps revision_findings, so the writer's revision dispatch carries it as arg.findings_file — needs a host-side record of revision_findings for a non-round reviewer and for answered, cleared as bash clears it on start"*. Say what the host does instead: a findings file given at a non-gate call is required on `FAIL` but not kept, and neither is one given with `answered`, so `ui_review`'s `FAIL` reaches `ui_writer`'s revision with no findings file on it.
  - **Resuming a round.** The resume rules, `start_walk` and `current_step`. Name no departure here; both sit under **Recording a gate**.
- [ ] `## Errors`: add that a malformed refusal record raises `ValueError` naming the file and its lock `TimeoutError`, as the walk's store does, and that a round gate with no `findingsFolder` raises `ValueError`. Every other sentence stays as written.

**Verification:**

- Each symbol and path the README names resolves: `git grep -n` for each new symbol under `devscene-flow-host/src/` finds its definition in the module the README names.
- The README states every departure `host/round_gates.py` carries a `TODO: @claude` marker for, each under **Recording a gate**. List the markers with `git grep -n 'TODO: @claude' -- devscene-flow-host/src/devscene_flow_host/host/round_gates.py`. Each marker the output shows has a README sentence carrying that marker's own wording, and no README departure lacks a marker in that output.
- The README claims bash parity for neither departure: no README sentence says the held-gate escalation, or the keeping of a non-round or `answered` findings file, behaves as `flow-walker.sh` does.
