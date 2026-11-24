### Task 3 — Read a story index's escalation evidence

**Goal:** Add `devscene-flow-host/src/devscene_flow_host/records/index_evidence.py`. It reads the escalation evidence a story index carries exactly as `fw_index_evidence` does, so the cap payload's `evidence` lines need only rendering. The evidence is whether the index has a `## Rejected findings` section, its entries that are still open, and whether it has a `## Scope register` section.

**Source:** `cli/templates/scripts/lib/flow-walker-gates.sh` (`fw_index_evidence`).

**Where this layer stops.** This returns a value. It decides nothing about which `## Scope register` rows are in dispute: that judgement stays with the orchestrator, as bash's comment says. Rendering the `evidence:` / `evidence.open:` lines is the `commands` layer's. No task in this branch consumes the value; the compatibility command (#465) is its reader.

### Targets

- `devscene-flow-host/src/devscene_flow_host/records/index_evidence.py` (new)
- `devscene-flow-host/tests/test_index_evidence.py` (new)

**Work:**

- [ ] **The value and the constants.** A frozen dataclass `IndexEvidence` with `rejected_findings: bool`, `open_rejections: tuple[str, ...]` and `scope_register: bool`. `Final` constants: `REJECTED_FINDINGS_HEADING = "## Rejected findings"`, `SCOPE_REGISTER_HEADING = "## Scope register"` and `CALL_STANDS = "call stands"`.
- [ ] **The reader.** `read_index_evidence(path: Path) -> IndexEvidence | None` returns `None` when the path is not a regular file. Otherwise it decodes UTF-8; a decode failure raises `RecordError(f"{path}: not UTF-8 text")`, as `records/ledger.py` → `read_run_mode` does. It then scans line by line:
  - A line starting `## ` is a heading, compared with trailing spaces, tabs and `\r` removed. It sets the in-rejected-findings state, and records `rejected_findings` or `scope_register` when it matches.
  - Inside `## Rejected findings`, a line starting `- ` that does not contain `call stands` is appended to `open_rejections` **as read**, with no stripping, as `awk` prints `$0`. A repeated heading keeps collecting.
- [ ] **The module docstring.** **"The rule:"** names `fw_index_evidence`. **"Deliberately not covered"** names judging scope-register rows.
- [ ] **`tests/test_index_evidence.py`.** It opens with *"The rule this file exists to enforce"* and plants files under `tmp_path`. Cases:
  - `fw_index_evidence`'s own `REPRO` body (`## Rejected findings` with one `call stands` entry and one open entry, then `## Scope register`) → `IndexEvidence(True, ("- **5** (rejected round 2) — r",), True)`;
  - an absent path → `None`;
  - an index with neither heading → `IndexEvidence(False, (), False)`;
  - a heading carrying trailing spaces;
  - the exact `RecordError` message for non-UTF-8 bytes.

**Verification:**

- `tests/test_index_evidence.py` passes with every expectation a literal written from `fw_index_evidence`'s `REPRO` lines.
- An open entry keeps its em-dash and any trailing `\r` byte-for-byte, as the bash line prints it.
