### Task 1 — Read a reviewer file: its verdict, the round-file check, the next free index and the FAIL count

**Goal:** Add the `records` reader of a reviewer's file, `devscene-flow-host/src/devscene_flow_host/records/round_files.py`. It answers four questions exactly as `cli/templates/scripts/lib/flow-walker-gates.sh` answers them:

- the file's verdict;
- whether a round gate's file may be used, and if not, the first reason why;
- the next free `review_<n>.md` index in a findings folder;
- how many files in a folder read `FAIL`.

**Source:** `cli/templates/scripts/lib/flow-walker-gates.sh` (`fw_review_verdict`, `fw_round_file_check`, `fw_next_review_index`, `fw_fail_count`), and `cli/templates/scripts/flow-walker.sh` (`round_file_path`).

**Where this layer stops.** These functions return values and decide nothing about the walk. Task 2 builds round evidence from them. Task 4 turns a graph's `findingsFolder` into a folder. Task 7 records or refuses a gate with them. Nothing here imports `graphscene` (`.claude/context/devscene-flow-host.md` → `## The internal layers`).

### Targets

- `devscene-flow-host/src/devscene_flow_host/records/round_files.py` (new)
- `devscene-flow-host/tests/round_fixtures.py` (new): the test-support module that plants reviewer files and git repositories. Tasks 2, 6, 7 and 8 import it and none of them edits it.
- `devscene-flow-host/tests/test_round_files.py` (new)

**Work:**

- [ ] **Constants and the verdict.** Add `Final` constants in `round_files.py`:
  - `REVIEW_FILE_PREFIX = "review_"` and `REVIEW_FILE_SUFFIX = ".md"`;
  - `MUST_FIX_HEADING = "## Must Fix"`;
  - `NO_SINGLE_VERDICT_LINE = "no single verdict line"`.

  Add `review_verdict(path: Path) -> Literal["PASS", "FAIL"] | None`. It returns `"PASS"` or `"FAIL"` when the file holds exactly one line that is byte-exactly `verdict: PASS` or `verdict: FAIL`, after stripping one trailing `\r`. It returns `None` when the path is not a regular file (`is_file()` false), when no line matches, or when more than one does.
  - Read the file as **bytes** and split on `b"\n"`. Never decode, so any file `awk` reads is read the same way.
  - Only `FileNotFoundError` or a non-file reads as absent. Any other `OSError` propagates (`.claude/context/devscene-flow-host.md` → `## Errors`).
- [ ] **The check.** `round_file_problem(path: Path) -> str | None` returns `None` when the file may be used. Otherwise it returns the first reason, in `fw_round_file_check`'s precedence and with its exact texts:
  - `NO_SINGLE_VERDICT_LINE` when `review_verdict` is `None`.
  - Otherwise, scan the lines with one trailing `\r` stripped:
    - A line starting `## ` closes any open entry and sets "in section" to whether the line equals `## Must Fix`. Sections may repeat.
    - Inside the section, a line matching `^[0-9]+\. ` opens entry *k*, counting from 1 across sections.
    - While an entry is open, `^[ \t]*\*\*Class:\*\*[ \t]*[^ \t]` marks its class and `^[ \t]*\*\*Failure:\*\*[ \t]*[^ \t]` marks its failure.
    - Closing an entry records the first problem: `Must Fix entry <k> lacks **Class:**`, otherwise `Must Fix entry <k> lacks **Failure:**`.
  - At the end, with the last entry closed:
    - a FAIL with no entry is `verdict: FAIL with no numbered entry under ## Must Fix`;
    - otherwise a PASS with an entry is `verdict: PASS with a numbered entry under ## Must Fix`;
    - otherwise it is the first recorded problem, or `None`.
- [ ] **The folder answers and the path.**
  - `next_review_index(folder: Path) -> int` returns one past the highest `<n>` among the folder's entries named exactly `review_<digits>.md`. It returns `0` when the folder is absent or holds none. A gap is never back-filled, `<digits>` are read as base 10 (`review_007.md` is 7), and every directory entry is listed, not only files.
  - `fail_count(folder: Path) -> int` counts the entries with that name shape whose `review_verdict` is `"FAIL"`. It is `0` for an absent folder.
  - `round_file_path(repo_root: Path, findings: str) -> Path` returns `Path(findings)` when it is absolute, and `repo_root / findings` otherwise.
  - The module docstring:
    - **"The rule:"** names the four bash functions it reads as.
    - **"Deliberately not covered"** lists: the class name inside `**Class:**` (`plugin/instructions/finding_grades.md` owns that list); a non-missing `OSError` (it propagates, where `awk` would print nothing); and absence, which is a value and never a `RecordError`, because the walk routes on it.
- [ ] **`tests/round_fixtures.py`.** Its module docstring states its rule: records are planted under the test's `tmp_path` only, and git runs isolated from the machine's configuration. It provides these, each typed for `mypy` `strict`:
  - `PASS_BODY = "verdict: PASS\n"`.
  - `FAIL_BODY = "verdict: FAIL\n## Must Fix\n1. **f**\n   **Class:** c\n   **Failure:** x\n"`.
  - `plant_review(folder: Path, n: int, body: str) -> Path`, which creates the folder and writes `review_<n>.md`.
  - `git(root: Path, *args: str) -> str`, which runs `git -C <root> -c user.name=r -c user.email=r@r -c commit.gpgsign=false <args>` with `GIT_CONFIG_GLOBAL` set to `os.devnull` and `GIT_CONFIG_NOSYSTEM=1`, and returns stdout.
  - `init_repo(root: Path) -> None` and `commit(root: Path, paths: Sequence[Path], message: str) -> None`.
- [ ] **`tests/test_round_files.py`.** It opens with the *"The rule this file exists to enforce"* docstring. Every expected value is a literal written from the rules above. It holds one case per clause:
  - a single PASS and a single FAIL;
  - a `\r\n` verdict line;
  - two verdict lines, none, and an absent path;
  - each of the five check reasons, using the `bad.md` body from `flow-walker.sh`'s `REPRO` for `lacks **Class:**`;
  - a valid FAIL and a valid PASS;
  - the index of a folder holding `review_0.md` and `review_3.md` (4) and of an absent folder (0), plus a non-matching name ignored;
  - `fail_count` over a mixed folder;
  - both `round_file_path` forms.

**Verification:**

- `tests/test_round_files.py` passes. Its reasons are asserted as exact strings, and they are the texts `flow-walker.sh` prints after `<path>: `.
- A file whose bytes are not UTF-8 but carry `verdict: PASS` on its own line reads as `"PASS"`, which proves the reader never decodes.
- `round_files.py` imports nothing outside the standard library and `devscene_flow_host.records`.
