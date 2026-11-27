### Task 9 — Read a branch's top-level answered clarification pairs in `records/clarifications.py`

**Goal:** Give the flow host a record reader for a branch's answered clarification pairs at the top level of `<stateDir>/clarifications/<branch>/`, each with its question's `Raised by:` origin. It reads as `cli/templates/scripts/lib/harness-run-lib.sh` → `hr_top_level_answered_pairs` and `cli/templates/scripts/lib/planning-driver-lib.sh` → `pd_raised_by` do.

**Where this layer stops.** This task reads and decides nothing:

- **Which pairs reach a writer** is Task 14's: it leaves out a `Phase G` origin and a prompt-injection-screen origin, and sends a UI-test origin to `ui_writer`.
- **Rendering the pairs between the untrusted-data markers** and appending them to a prompt is Task 11's.
- **The pair reader never opens an answer file.** `read_pair_text` reads one file's text only when a caller asks for it, after Task 14's filtering. The autonomous fork forbids opening a `Phase G` pair's `answer_<n>.md` before Phase D. An origin is told from the question alone (`plugin/instructions/task_plan_writing_instructions_autonomous.md` → `## Override 2 — resumability`, case (a)).

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
def read_pair_text(repo_root: Path, rel: str) -> str: ...
```

- **Which pairs count.** A pair is a top-level `question_<n>.md`, where `<n>` is all digits, with a sibling `answer_<n>.md` that is a regular file. Subdirectories (`answered/`) are never read.
- **The order** is ascending numeric `<n>`, as `hr_top_level_answered_pairs` orders it with `sort -n`.
- **`raised_by`** is the text after `Raised by: ` on the first such line before the question's first `## ` line, with a trailing CR stripped. With none, it is `None`.
- **A missing directory** returns `()`.
- **A question that is not UTF-8** raises `RecordError(f"{path}: not UTF-8 text")`. A missing file is no pair, and any other `OSError` propagates.
- **`read_pair_text(repo_root, rel)`** returns the full text of one pair file, `repo_root / rel`, where `rel` is an `AnsweredPair.question` or `.answer`. It is the only way the flow host reads a pair file's text: Task 11's `host/agent_prompts.py` calls it and opens no pair file itself (`.claude/context/devscene-flow-host.md` → `## The internal layers`, *"Reading a record into a value is `records`"*).
  - A missing file raises `RecordError(f"the clarification file '{rel}' cannot be read")`.
  - A file that is not UTF-8 raises `RecordError(f"{path}: not UTF-8 text")`.
  - Any other `OSError` propagates.
  - It is called only for pairs the caller has kept. Task 14 leaves out a `Phase G` origin before any pair reaches the builder, so a `Phase G` answer file is never opened before Phase D. `read_answered_pairs` itself stays exactly as above and never opens an answer file.

**Work:**

- [ ] **`records/clarifications.py`.**
  - **The docstring.** Its *"The rule:"* names `hr_top_level_answered_pairs` and `pd_raised_by` as the bash readers, and states that `read_answered_pairs` opens no answer file. It states that `read_pair_text` is called only for pairs the caller has kept, so a `Phase G` answer is never opened before Phase D. Its *"Deliberately not covered"* list names the origin filtering (`host/planning_entry.py`'s) and the rendering (`host/agent_prompts.py`'s).
  - **The code.** Declare `CLARIFICATIONS_DIRECTORY` and the `Raised by: ` prefix as `Final` constants, and implement both functions exactly as the contract spells them.
- [ ] **`tests/test_clarifications.py`.** Open with the header *"The rule this file exists to enforce"*. Plant files under `tmp_path` and cover:
  - pairs `2` and `10` returned in numeric order, not lexical;
  - a question with no answer, left out;
  - a `question_x.md`, left out;
  - a pair under `answered/`, left out;
  - a `Raised by:` line after the first `## ` heading, which gives `None`;
  - a CRLF question;
  - the missing directory;
  - a non-UTF-8 question, with its exact message;
  - an answer file planted with unreadable bytes still yields its pair, which shows the reader never opens it;
  - `read_pair_text` on a planted file, returning its text unchanged;
  - `read_pair_text` on a missing file, with its exact `cannot be read` message;
  - `read_pair_text` on a non-UTF-8 file, with its exact `not UTF-8 text` message.

**Verification:**

- `bash scripts/python-service.sh --package devscene-flow-host test tests/test_clarifications.py` passes.
- `read_answered_pairs` contains no read of an `answer_` path. Grep the module for `read_text` / `read_bytes`: inside `read_answered_pairs` they apply to the question path only, and the one other read is `read_pair_text`'s, of its `rel` argument.
