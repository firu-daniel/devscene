### Task 1 — Bound the writer's provenance line to this pass in `conventions-writer.md`

**Goal:** Rewrite the conventions writer's document-level provenance obligation so it covers a `write` and a `merge`, describes this pass only, names sources at directory or area level, carries no earlier pass forward, and states who maintains the line after a hand edit. Also make the fix dispatch add nothing to the line.

**This task owns the canonical wording.** Tasks 2 (`plugin/agents/conventions-reviewer.md`) and 3 (`plugin/commands/analyze.md`) restate the phrases below byte-for-byte and check them with `grep -F` against this file. Task 4 adds a `cli/test` suite asserting each one, plus the fix-dispatch sentence below, in this file's `## The document` and `## The fix dispatch` sections. Write each phrase exactly as quoted, inside the new bullet:

- `describing this pass only`
- `it replaces the skeleton's footer` and `it replaces the previous provenance line`
- `at directory or area level`
- `never a per-file list`
- `carries no earlier pass forward`
- `edited by hand after #<number>`

**Where this task stops.** It edits only `plugin/agents/conventions-writer.md`. The reviewer's grading of the line is Task 2's, and the command's restatement in (4a), together with the `project` target's (4b) per-section notes, is Task 3's. This task does not touch any `.claude/context/*.md` footer: trimming the existing footers is out of scope per the task prompt, and those files are conventions documents.

### Targets

- `plugin/agents/conventions-writer.md` — `## The document` (the closing-obligation bullet) and `## The fix dispatch` (its opening paragraph).

**Work:**

- [ ] `## The document`, under the lead-in "**Two document-level obligations close the write, on both `write` and `merge`, unconditionally:**". Keep the lead-in and the first bullet ("**Remove that document's `<!-- devscene:unfilled -->` line**") unchanged. Replace the second bullet, the one opening "**Replace the skeleton's footer with a document-level provenance line**", with one bullet carrying this text:

  > **Write a document-level provenance line describing this pass only.** On `write` it replaces the skeleton's footer; on `merge` it replaces the previous provenance line, whoever wrote it. It names the mode and what this pass read at directory or area level — for example *from `<scope>`: README, manifest, source tree, test headers* — never a per-file list: per-file evidence belongs in the per-rule provenance and in `evidence`. It carries no earlier pass forward — no earlier mode, fix pass or hand-edit clause; git history records them. Whoever edits the document by hand may end the line with one short clause naming the change, such as `edited by hand after #<number>`; the next pass replaces it with the rest of the line. It is a different artifact from the per-rule provenance above.

  `<scope>` is the writer's own dispatch value, and `<number>` is the issue or pull-request number a hand editor names. The example uses placeholders, not this repository's directory names (`.claude/context/plugin.md` → `## What this layer is`, *"No adopter's value is ever a literal here"*).
- [ ] `## The fix dispatch`, the paragraph opening "**One pass per dispatch, on either axis, and there is no second inside it.**". After its sentence "Do not re-research the document from scratch, do not disturb what the findings do not target, and never request or expect a re-review.", add one sentence: "**A fix adds nothing to the provenance line:** it belongs to the pass the line already describes." This closes the route by which footers gained *"corrected by the review fix pass"* clauses.
- [ ] Leave the compose-from-nothing paragraph ("**On an `action: write` dispatch whose `document_path` names no existing file.**") and the sweep section's pointer "the two document-level closing obligations" as they are. Both still resolve: the first names the line as part of the shape, and the second points at the pair this task keeps at two members.

**Verification:**

- `grep -F` each canonical phrase listed above against `plugin/agents/conventions-writer.md`, and find each one.
- `grep -nF "Replace the skeleton's footer with a document-level provenance line" plugin/agents/conventions-writer.md` returns no hit, so the old bullet is replaced rather than kept beside the new one.
- `grep -nF "Two document-level obligations close the write" plugin/agents/conventions-writer.md` and `grep -nF "the two document-level closing obligations" plugin/agents/conventions-writer.md` both still hit, so the sweep section's pointer resolves to a pair that still has two members.
- `grep -nF "A fix adds nothing to the provenance line" plugin/agents/conventions-writer.md` hits once, inside `## The fix dispatch`.
- The diff of `plugin/agents/conventions-writer.md` touches only the two sections named under `### Targets`, and adds no rationale beyond the new behaviour (`.claude/context/plugin.md` → `## Writing agent prose`, *"An agent's growth is paid for by behaviour"*).
