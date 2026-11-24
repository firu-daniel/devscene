### Task 10 — List the host's new suites under gate 13 and its round files in the roadmap

**Goal:** Bring the two root documents that list what the GraphScene host ships into line with this branch. Gate 13's description in `docs/development.md` names every suite leg 13j runs, and the `GraphScene` row of `ROADMAP.md` lists what the host does. This is the catch-all task (`layers[]` entry `general`, path `.`), and it ships last because it documents what the `devscene-flow-host` tasks built.

**Depends on:** Tasks 1–9. The new suites, all under `devscene-flow-host/tests/`, are:
- `test_round_files.py` (reviewer files);
- `test_round_evidence.py` (round evidence);
- `test_index_evidence.py` (index evidence);
- `test_reviewers.py` (path templates and reviewer lookups);
- `test_refusals.py` (the refusal record);
- `test_resume.py` (the resume rules);
- `test_round_gates.py` (recording a gate);
- `test_re_entry.py` (start and current).

Task 9's README is the host's own description, and this task cites it rather than restating it.

**How this task's implementer reads the conventions.** The catch-all implementer reads `.claude/context/conventions.md` → `## Documents of record` and every layer document, because the edit describes another layer's work.

### Targets

- `docs/development.md` → **Gate 13** — the story index's `## Scope register` row 2.
- `ROADMAP.md` → the `GraphScene` row — row 3.

**Work:**

- [ ] `docs/development.md` → **Gate 13**: in the 13j sentence listing the host's suites, add the eight suites above. Keep the sentence's existing pattern: *"the suites of its records, … of its predicate host, …"*, grouping the three `records` suites with `test_config.py` and `test_ledger.py`. No other sentence of the gate changes.
- [ ] `ROADMAP.md` → `GraphScene` row: in the clause *"the harness's GraphScene host at `devscene-flow-host/` …"*, add that it reads the round and reviewer files, applies the reviewer-file rules (a refused file re-dispatched in the same round, held as `error` on its third refusal), and resumes a round from the files on disk through `Walker.start`'s `RoundResume`, citing `devscene-flow-host/README.md`. Leave *"Left: the walker's port onto the engine"* and the status cell `In progress` unchanged, because the compatibility command is still to come.

**Verification:**

- Every suite file the gate-13 sentence names exists: `git ls-files devscene-flow-host/tests` lists each one, and the sentence names no file outside that output.
- The roadmap row still ends `| In progress |`, and its new clause cites only `devscene-flow-host/README.md`.
