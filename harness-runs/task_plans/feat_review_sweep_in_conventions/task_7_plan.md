### Task 7 — Run the `sweep` target last in `/devscene:analyze`

**Goal:** Make `/devscene:analyze` fill `.claude/review-sweep.md`. It is a reserved target, `sweep`, run last in a no-argument run, after the corpus pass, because its rows are derived from the finished conventions documents. It goes through one write → review → fix chain and is never a member of the corpus pass.

**Depends on:**
- **Task 1:** `sweep` is a reserved analyze target in `RESERVED_ANALYZE_TARGETS`, and `init` writes the skeleton at `.claude/review-sweep.md` carrying both halves of the two-part test.
- **Task 5:** `conventions-writer` accepts `pass: document`, `target: sweep`, with `scope` the repository root, and returns its ordinary return object.
- **Task 6:** `conventions-reviewer` accepts `pass: document`, `target: sweep`, and returns ordinary `document_reviewed` findings.

The dispatch block this command sends is the existing write / review / fix block, unchanged in its fields: `pass`, `target`, `document_path`, `action`, `scope`, `mode`, `excluded_paths`, `harvested_sources`, `demand_set`, `shared_document`, `parity` when on, and on review and fix the three `prior_*` fields.

**Where this task stops.** It edits the command only. The decisions of record go into `docs/analyze.md`, which is **Task 10's**.

### Targets

- `plugin/commands/analyze.md`

**Work:**

- [ ] `## Resolved values` → the `<layer_names>` row: the targets `$ARGUMENTS` may name are the names "beside the four reserved words". In `## Context`, add the reserved word `sweep` to the targets paragraph, as the review-sweep document `.claude/review-sweep.md`, and change "one of the three reserved words" to the four. The path is spelled literally, as the plugin already spells `.claude/qa_test_scenarios.md`.
- [ ] `## Steps` → step 1:
  - the no-argument order becomes `layers`, `project`, `conventions`, each `layers[]` row, then `sweep`;
  - the sweep document is **not** part of the conventions **document set**, so the document-set derivation and the `shared_document` rules are unchanged;
  - the announcement and `--dry-run` report name the `sweep` target and its planned action.
- [ ] `## Steps` → step 4: add **(4e) The `sweep` target**, which runs after (4d) has finished, or after the last document wave when (4d) does not run.
  - **Classification.** It reuses (4a)'s rule. An untouched skeleton is `action: write` without asking. A path with no file is `action: write`, the writer's compose-from-nothing case. Anything else is asked, merge by default, `skip` always available, and `--yes` takes the default. `skip` sends nothing.
  - **Dispatch.** Send the step 3 write block with `target: sweep`, `document_path` the absolute `.claude/review-sweep.md`, and `scope` the repository root. `shared_document` takes the on-disk value step 1 states: the shared document's path when it exists and does not carry `<!-- devscene:unfilled -->`, otherwise `none`. **`demand_set` is sent unchanged**, the run's one derivation, because the closed block carries it on every dispatch. State in (4e) that this target has no `demand_set` scope of its own, so the writer answers none of it and the reviewer skips check (5). That is the exception `plugin/agents/conventions-writer.md` → `## The sweep document` defines (Task 5), in the words step 4 already uses for the `project` target.
  - **Review and fix.** Then one (4c) review and at most one fix, exactly as (4c) defines them. Step 3's closed-block rule binds all three.
  - **Not a corpus member.** In (4d)'s corpus-set bullets, add one bullet: the sweep document is never a member of `corpus_documents`.
- [ ] `## Steps` → step 4 (4b) banner rule and step 6. The setup-pending banner is deleted only when every target of a no-argument run, `sweep` included, has completed.
  - Report the `sweep` target as a delegated document, from its writer and fix returns, with its review line, in the announced target order, so it comes last.
  - In the next actions, name `npx devscene doctor` as also confirming the sweep document, and name the commit of `.claude/review-sweep.md` on the default branch as what makes the reviewer's sweep read it.
- [ ] Re-derive every citer of the edited anchors with `git grep -n -F 'three reserved' -- plugin` and `git grep -n -F '(4d)' -- plugin`. Confirm that no other plugin file restates the target list or (4d)'s membership rule. Any that does is an edit in this same task, and is named in the commit.

**Verification:**

- `git grep -n -F 'sweep' -- plugin/commands/analyze.md` shows the target in `## Resolved values`, `## Context`, step 1, (4d), (4e) and step 6.
- `git grep -n -F 'three reserved' -- plugin` prints nothing.
- `git grep -n -F 'no `demand_set` scope of its own' -- plugin/commands/analyze.md` prints the existing `project`-target line and the new (4e) line.
- The (4e) dispatch names only fields that `plugin/agents/conventions-writer.md` → `## Invocation contract` and `plugin/agents/conventions-reviewer.md` → `## Invocation contract` already list. Check each field name by grep in those two files.
