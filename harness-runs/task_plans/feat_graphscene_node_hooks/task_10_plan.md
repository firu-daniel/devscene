### Task 10 — Read the ledger's `P1`–`P3` marks in `records/ledger.py`

**Goal:** Let the flow host read the flow-progress ledger's three planning entries, `P1`, `P2` and `P3`, as `cli/templates/scripts/lib/planning-driver-lib.sh` → `pd_ledger_read` reads them. The entry decision (Task 14) and the convergence hook (Task 13) need them.

**Where this layer stops.** This task reads and decides nothing about a mark:

- **What a mark means** is Task 14's (`[x]` and `[-]` are *resolved*) and Task 13's (`P2` `x` with a UI-test index on disk means a plan was written).
- **Writing a mark** (a flip) is Task 12's.

### Targets

- `devscene-flow-host/src/devscene_flow_host/records/ledger.py`
- `devscene-flow-host/tests/test_ledger.py`

**The contract this task produces.** Tasks 13 and 14 read it.

```python
PlanningMark: TypeAlias = Literal["x", "-", " "] | None   # None: no line for the entry

@dataclass(frozen=True)
class PlanningMarks:
    p1: PlanningMark
    p2: PlanningMark
    p3: PlanningMark

def read_planning_marks(repo_root: Path, state_dir: str, branch: str) -> PlanningMarks: ...
```

- **The path.** It reads `ledger_path(repo_root, state_dir, branch)`, the module's existing path function.
- **The match.** Every line of the file is matched against `- [x] P1.`, `- [-] P1.` and `- [ ] P1.` (and likewise for `P2` and `P3`). `pd_ledger_read` sets the mark on every match, so the last matching line wins.
- **A missing ledger** raises `RecordError(f"no flow-progress ledger at {path}")`.
- **A ledger that is not UTF-8** raises `RecordError(f"{path}: not UTF-8 text")`, the module's existing wording.

**Work:**

- [ ] **`records/ledger.py`.**
  - **The code.** Add `PlanningMark`, `PlanningMarks` and `read_planning_marks` exactly as the contract spells them, with the line prefixes as `Final` constants.
  - **The docstring.** Extend *"The rule:"* to name `pd_ledger_read` as the bash reader of the marks. Remove *"its `P1`-`P3` entries"* from *"Deliberately not covered"*, which keeps *"The ledger's other blocks"*.
- [ ] **`tests/test_ledger.py`.** Add these cases on ledgers planted under `tmp_path`:
  - each of the three marks, for each entry;
  - an entry with no line, which gives `None`;
  - two lines for one entry, where the last wins;
  - a line that only contains `- [x] P1.` after leading text, which does not match;
  - the missing ledger and the non-UTF-8 ledger, each asserting the exact message.

  Write the expected values as literals.

**Verification:**

- `bash scripts/python-service.sh --package devscene-flow-host test tests/test_ledger.py` passes, the existing run-mode cases included without edit.
