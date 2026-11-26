### Task 9 — Read a branch's top-level answered clarification pairs in `records/clarifications.py`

**Goal:** Give the flow host a record reader for a branch's answered clarification pairs at the top level of `<stateDir>/clarifications/<branch>/`, each with its question's `Raised by:` origin. It reads as `cli/templates/scripts/lib/harness-run-lib.sh` → `hr_top_level_answered_pairs` and `cli/templates/scripts/lib/planning-driver-lib.sh` → `pd_raised_by` do.

**Where this layer stops.** This task reads and decides nothing:

- **Which pairs reach a writer** is Task 14's: it leaves out a `Phase G` origin and a prompt-injection-screen origin, and sends a UI-test origin to `ui_writer`.
- **Rendering the pairs between the untrusted-data markers** and appending them to a prompt is Task 11's.
- **The reader never opens an answer file.** The autonomous fork forbids opening a `Phase G` pair's `answer_<n>.md` before Phase D. An origin is told from the question alone (`plugin/instructions/task_plan_writing_instructions_autonomous.md` → `## Override 2 — resumability`, case (a)).

### Targets

- `devscene-flow-host/src/devscene_flow_host/records/clarifications.py` (new)
- `devscene-flow-host/tests/test_clarifications.py` (new)

**The contract this task produces.** Tasks 11 and 14 read it.

```python
CLARIFICATIONS_DIRECTORY: Final = "clarifications"

@dataclass(frozen=True)
class AnsweredPair:
    index: int
    question: str          # repo-relative: <state_dir>/clarifications/<branch>/question_<n>.md
    answer: str            # repo-relative: <state_dir>/clarifications/<branch>/answer_<n>.md
    raised_by: str | None  # the question's `Raised by: ` value, or None

def read_answered_pairs(repo_root: Path, state_dir: str, branch: str) -> tuple[AnsweredPair, ...]: ...
```

- **Which pairs count.** A pair is a top-level `question_<n>.md`, where `<n>` is all digits, with a sibling `answer_<n>.md` that is a regular file. Subdirectories (`answered/`) are never read.
- **The order** is ascending numeric `<n>`, as `hr_top_level_answered_pairs` orders it with `sort -n`.
- **`raised_by`** is the text after `Raised by: ` on the first such line before the question's first `## ` line, with a trailing CR stripped. With none, it is `None`.
- **A missing directory** returns `()`.
- **A question that is not UTF-8** raises `RecordError(f"{path}: not UTF-8 text")`. A missing file is no pair, and any other `OSError` propagates.

**Work:**

- [ ] **`records/clarifications.py`.**
  - **The docstring.** Its *"The rule:"* names `hr_top_level_answered_pairs` and `pd_raised_by` as the bash readers, and states that no answer file is opened. Its *"Deliberately not covered"* list names the origin filtering (`host/planning_entry.py`'s) and the rendering (`host/agent_prompts.py`'s).
  - **The code.** Declare `CLARIFICATIONS_DIRECTORY` and the `Raised by: ` prefix as `Final` constants, and implement the reader exactly as the contract spells it.
- [ ] **`tests/test_clarifications.py`.** Open with the header *"The rule this file exists to enforce"*. Plant files under `tmp_path` and cover:
  - pairs `2` and `10` returned in numeric order, not lexical;
  - a question with no answer, left out;
  - a `question_x.md`, left out;
  - a pair under `answered/`, left out;
  - a `Raised by:` line after the first `## ` heading, which gives `None`;
  - a CRLF question;
  - the missing directory;
  - a non-UTF-8 question, with its exact message;
  - an answer file planted with unreadable bytes still yields its pair, which shows the reader never opens it.

**Verification:**

- `bash scripts/python-service.sh --package devscene-flow-host test tests/test_clarifications.py` passes.
- `records/clarifications.py` contains no read of an `answer_` path. Grep the module for `read_text` / `read_bytes`, and find them applied to the question path only.
