### 1. Three return-field reads use a bare field name instead of the `<agent>.<field>` citation form

**Files (all three edits are in the `plugin` layer):**

- `plugin/instructions/docs_orchestration_instructions_autonomous.md` (`## Per-entry loop`, step 3 **Fix loop (cap 3).**): "record `<slug>` + the open `findings_file` in"
- `plugin/instructions/plan_orchestration_instructions_core.md` (`### D.2 Done summary`, the **QA (Phase E)** bullet): "taken from the `blocked_tests` items"
- `plugin/instructions/user_review_fixes_instructions_core.md` (the Done summary's **QA (Phase QA)** bullet): "taken from the `blocked_tests` items"

**Problem.** `docs/structured-agent-returns.md` → `### Citing a field` says that a document other than the agent's own definition names a return field it reads as `` `<agent>.<field>` ``. It also says *"A static check holds each such citation … to the named agent's schema file, so this is the only spelling a caller uses."* This branch moved every reader of these five agents onto that form. Three reads it added or edited still use the bare field name:

- **The docs catalog's exhausted fix cap** records the last reviewer return's findings file as "the open `findings_file`". The sentence before it in the same step already spells the field `` `docs-reviewer.findings_file` ``.
- **Both Done-summary QA bullets** were rewritten by Task 1 to take each blocked test's id and cause "from the `blocked_tests` items". E.2 in the same core spells the same read `qa-tester.blocked_tests.test_id` / `qa-tester.blocked_tests.cause`.

The text routes correctly today, so this is not Must Fix. The cost is the one the citation rule exists to prevent. `cli/test/agent-return-schemas.test.mjs` only holds a field to its schema when the agent name is in front of it. If `docs-reviewer.findings_file` or `qa-tester.blocked_tests` is renamed later, these three sites go stale with no failing check.

**Fix.** Edit only the quoted substrings:

1. In `plugin/instructions/docs_orchestration_instructions_autonomous.md`, step 3, replace

   ```
   record `<slug>` + the open `findings_file` in
   ```

   with

   ```
   record `<slug>` + the last `` `docs-reviewer.findings_file` `` in
   ```

2. In `plugin/instructions/plan_orchestration_instructions_core.md`, the `### D.2 Done summary` **QA (Phase E)** bullet, replace

   ```
   taken from the `blocked_tests` items
   ```

   with

   ```
   taken from the `qa-tester.blocked_tests.test_id` and `qa-tester.blocked_tests.cause` items
   ```

3. In `plugin/instructions/user_review_fixes_instructions_core.md`, the Done summary's **QA (Phase QA)** bullet, make the same replacement as in edit 2.

Use the single-backtick form in edits 2 and 3, which is what E.2 of `plan_orchestration_instructions_core.md` already uses for the same fields. Use the double-backtick form in edit 1, which matches the rest of `docs_orchestration_instructions_autonomous.md`.
