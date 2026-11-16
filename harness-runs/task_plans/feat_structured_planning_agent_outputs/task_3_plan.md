### Task 3 — Give `ui-tests-plan-writer` a `## Return schema`, rewrite its `## Output contract`, and move the two planning writers' untrusted-input report into `questions`

**Goal:** Make `plugin/agents/ui-tests-plan-writer.md` return one JSON object in all three of its modes (initial write, augment after user-review fixes, revision), declared once in a `## Return schema` section, and update the one shared-module row that tells both planning writers where an untrusted-instruction report goes.

**Depends on:** Task 1 (the dialect, the canonical sentence in `plugin/instructions/agent_return_contract.md` → `## The return block`, the `### Return fields` rule), and Task 2, whose `task-plan-writer` now reports an `Untrusted instruction not followed — …` line as one `questions` item — the `untrusted_input.md` row below states that for both writers at once.

**The return this task declares** (the story index `## Context` field table, `ui-tests-plan-writer` rows — Tasks 6, 7, 9 and 11 read exactly these names):

- `outcome` `returned`: required `ui_test_index` (string), `ui_test_files_dir` (string), `tests_count` (integer, `minimum` 0).
- `outcome` `no_ui`: required `reason` (string, one line). No `tests_count`, no paths: the outcome is the signal.
- `outcome` `questions`: required `questions` (array of non-empty strings, `minItems` 1); optional `ui_test_index`, `ui_test_files_dir`, `tests_count` — present when an augment wrote or revised files before it stopped to ask, which `plugin/instructions/user_review_fixes_instructions_autonomous.md` → `## Override L — commit the QA.0 UI-test plan augment (autonomous fork only)` commits before routing the questions (Task 9).
- `outcome` `blocker`: required `blocker` (string).

**Where this task stops.** Every reader of this return is a later task (6, 7, 9, 11). The augment-mode rules (add, revise, leave byte-identical) are unchanged; only how the result is returned changes.

### Targets

- `plugin/agents/ui-tests-plan-writer.md`
- `plugin/instructions/untrusted_input.md` → `## Where a report goes`

**Work:**

- [ ] `## Output contract`: replace the two fenced `key: value` blocks and the `## Questions` paragraph with the canonical sentence, one paragraph per outcome (when each is returned, in which mode), and a `### Return fields` subsection with one bullet per property — `outcome`, `ui_test_index`, `ui_test_files_dir`, `tests_count`, `reason`, `questions`, `blocker`. The `no_ui` rules move onto the outcome without loss: no files written, the disabled-phase case returns it with the disabled phase as `reason`, and "a routing signal, not an error — never decorate or rename it" now binds the `outcome` value `no_ui`. The augment zero-change case returns `returned` with the unchanged `tests_count`.
- [ ] Add `## Return schema` directly after `## Output contract`: one fenced `json` block, a `oneOf` of the four variants above, each with `additionalProperties: false`, in the closed dialect.
- [ ] Rewrite every in-body reference to the retired forms so it names the outcome or field: the phase-gate paragraph under the opening ("return the no-UI block" → the `no_ui` outcome); `## Invocation contract` → the augment bullets (`no_ui: true`, `tests_count: <unchanged count>`) and **How the caller consumes your return.**; `## Read first` → **A cited path you cannot read is a finding, not a fallback.** (the `blocker` outcome in place of every plan file); `## No-UI determination (do this FIRST, before enumerating tests)` ("Do NOT emit a `## Questions` section", "Return the no-UI contract", the ambiguous-case clarification); `## Process` and `## Quality checks before saving` where they say to raise something in `## Questions`; `## Clarification questions`.
- [ ] `plugin/instructions/untrusted_input.md` → `## Where a report goes`: split the first row. `task-plan-writer` and `ui-tests-plan-writer` → *one item of its return object's `questions`, then stop as for any question; the caller's existing `<ask>` route parks the run (or asks the user live)*. `user-review-fix-plan-writer` and `test-fix-plan-writer` keep today's cell (*one entry of its `## Questions` return section …*) unchanged — their returns are #380's. Keep the report literal and every other row byte-identical, and keep `## Who may cite this` as it is (no new citer).
- [ ] Hold the word budget as Task 2 does (`.claude/context/plugin.md` → `## Writing agent prose`): the schema replaces the retired blocks; no capability-guidance, test-data or locator rule is cut.

**Verification:**

- `git grep -nE 'no_ui: true|## Questions|tests_count: |ui_test_index: |blocker:' -- plugin/agents/ui-tests-plan-writer.md` prints no line instructing the writer to emit a retired line or section.
- Every `## Return schema` property has exactly one `### Return fields` bullet and the reverse; the four `outcome` values appear in `## Output contract`; the canonical sentence is byte-identical to Task 1's.
- The schema matches the `ui-tests-plan-writer` rows of the story index `## Context` field table, variant by variant.
- `git grep -n 'Questions' -- plugin/instructions/untrusted_input.md` shows the `## Questions` cell only on the `user-review-fix-plan-writer` / `test-fix-plan-writer` row, and every reader the table named before still has a row.
