### Task 1 — Add the round-file check to the walker's gate library

**Goal:** Give `lib/flow-walker-gates.sh` one function that decides whether a plan round file may be used, and make round evidence treat a file that fails it as `unreadable`, so a resumed walk can never hand such a file to the plan writer.

**Where this task stops.** This task adds the check and the evidence change. Task 2 calls the check from `flow-walker.sh`. This task does not edit the walker.

### Targets

- `cli/templates/scripts/lib/flow-walker-gates.sh`
- `cli/test/flow-walker-gates.test.mjs`
- `cli/test/flow-walker-resume.test.mjs`
- `cli/test/helpers/walker.mjs`
- `cli/test/helpers/planning-driver.mjs`

**Source:** `cli/templates/scripts/lib/flow-walker-gates.sh` (`fw_review_verdict`, `fw_round_evidence`).

**Work:**

- [ ] Add `fw_round_file_check <file>`. It prints nothing and returns 0 when the file is valid. Otherwise it prints one reason line on stdout and returns 1. Use `fw_review_verdict` for the verdict, then one `awk` pass, tolerating a trailing CR. A `## Must Fix` section runs from that exact column-0 heading to the next column-0 `## ` heading. An entry starts at a column-0 line matching `<digits>. `. A field line is optional leading whitespace, then `**Class:**` or `**Failure:**`, then at least one non-space character. Print exactly these reasons: `no single verdict line`; `verdict: FAIL with no numbered entry under ## Must Fix`; `verdict: PASS with a numbered entry under ## Must Fix`; `Must Fix entry <k> lacks **Class:**`; `Must Fix entry <k> lacks **Failure:**`, where `<k>` is the entry's 1-based position and the first problem found wins. The script does not validate the class name, because `finding_grades.md` owns the class list.
- [ ] In `fw_round_evidence`, print `unreadable` for a present file that fails `fw_round_file_check`, and otherwise print its verdict as today. Leave `fw_review_verdict` and `fw_fail_count` unchanged, so `rounds:` still counts `verdict: FAIL` files.
- [ ] Update the library header: the sentence saying the two functions read a round file's verdict line "and nothing else" becomes true of those two only, and it names `fw_round_file_check` as the function that reads the `## Must Fix` section. Update the `REPRO` block so its FAIL fixture carries a valid entry, and add one line reproducing a refusal. Keep bash 3.2 and the no-`jq` rule.
- [ ] In `cli/test/helpers/walker.mjs`, make `plantReview` write a valid entry whenever `verdict` is `FAIL`: `## Must Fix`, then `1. **fixture finding**`, an indented `**Class:** Wrong build` and an indented `**Failure:** If the writer follows the plan, then the build fails.`. Export `plantMalformedReview(dir, folder, n, lacking)`, where `lacking` is `'Class'` or `'Failure'`; it writes a `verdict: FAIL` file whose one entry omits that field and returns the same repo-relative path as `plantReview`. Update the doc comment that says the walker reads only the `verdict:` line. In `cli/test/helpers/planning-driver.mjs`, give the stub's `FAIL` file the same valid entry, and write the entry without `**Class:**` when the script entry sets `malformedMustFix: true`. Add the valid entry to `FAIL_BODY` in `cli/test/flow-walker-resume.test.mjs`.
- [ ] In `cli/test/flow-walker-gates.test.mjs`, add the valid entry to the shared `FAIL` constant, name `fw_round_file_check` in the header rule, and add cases for: a valid FAIL; a PASS with no section; each of the five refusal reasons; a CRLF file; an entry whose fields sit after a multi-line description; `## Must Fix` text inside `## Should Fix` not counting as the section; and `fw_round_evidence` printing `unreadable` for a `verdict: FAIL` file whose entry lacks `**Failure:**`.

**Verification:**

- `npm test --workspace cli -- test/flow-walker-gates.test.mjs` passes.
- `npm test --workspace cli -- test/flow-walker-resume.test.mjs` passes, which shows a resume still closes a valid FAIL round.
- `git grep -n 'nothing else' -- cli/templates/scripts/lib/flow-walker-gates.sh` shows no sentence claiming the library reads only verdict lines.
