### Task 2 — Add `## The verdict` to `plan_review_rounds.md` and make `## The writer's revision` Must-Fix-only

**Goal:** Make `plugin/instructions/plan_review_rounds.md` the single statement of the task prompt's three rules. **(1)** A plan review's verdict keys on Must Fix alone. **(3)** Should Fix and Nice to Have stay in the review file as a record for a human that no loop reads. **(2)** The writer acts on the round's Must Fix items only. Rules 1 and 3 go in a new section that every plan reviewer can point at; rule 2 goes where the old item 3 of `## The writer's revision` stood.

**Where this task stops.** It changes this one module. The agents that point at it are later tasks:
- Task 3 drops the writers' paraphrase of the old item 3.
- Task 4 points `architecture-reviewer` and `business-parity-reviewer` at `## The verdict`.
- Task 5 points `ui-tests-plan-reviewer` at it.

Those tasks cite the two headings below **byte-for-byte**, so the headings are the contract this task hands on: `## The verdict` (new) and `## The writer's revision` (existing, heading text unchanged). Leave `## The round file`, `## The Must Fix entry`, `## Converging mode`, `## Incidental findings — where they go and who reads them` and `## A rejection recorded under precedence` as they are. In particular, the incidental section's existing "a round whose only findings are incidental is a `PASS`" stays as it is.

### Targets

- `plugin/instructions/plan_review_rounds.md`

**Work:**

- [ ] Add a `## The verdict` section, placed after `## The round file` and before `## The Must Fix entry`. It must state:
  - A plan review returns `verdict: FAIL` only when it raises at least one Must Fix, and a review with none returns `verdict: PASS`, whatever Should Fix, Nice to Have or incidental findings it carries.
  - Those Should Fix and Nice to Have items stay in the review file as a record for a human. No loop reads them, and no writer acts on them (`## The writer's revision`).

  Word it for any plan reviewer's review file, not only a round file: `ui-tests-plan-reviewer` and `architecture-reviewer` sub-case (c) write files without the round file's `verdict:` line and will cite this section too. Keep it to those sentences. It states no per-agent file format, because each reviewer's own `## Output contract` owns that.
- [ ] `## The writer's revision`: delete item 3 (*"Each Should Fix of the round is applied, or recorded under `## Rejected findings` with its reason; none is held for a go-ahead the loop does not relay."*). In its place, state rule 2 **once**: the writer acts on the round's Must Fix items only, and never applies, records under `## Rejected findings` or names in the revision note a Should Fix or Nice to Have item, whichever gate's file it sits in.
  - Item 1 already groups the round's Must Fix items. Change its "Read every finding on a file" to read every Must Fix on a file, so no line of the section directs the writer to any other item.
  - Keep the list's numbering consistent after the edit.
- [ ] `## The writer's revision`, after the revision-note template: "One line per finding." becomes one line per Must Fix. Keep the user-feedback sentence ("A user-feedback revision writes one line per feedback item, its reviewer field `user`.") unchanged.
- [ ] `## Who may cite this`: add `${CLAUDE_PLUGIN_ROOT}/agents/ui-tests-plan-reviewer.md` to the roster, after `${CLAUDE_PLUGIN_ROOT}/agents/business-parity-reviewer.md`. Task 5 makes it a citer, and the section's own rule is that a new citer joins the list.

**Verification:**

- `git grep -nE "Should Fix of the round|One line per finding" -- plugin` prints no line.
- `git grep -n "^## The verdict$" -- plugin/instructions/plan_review_rounds.md` prints exactly the new heading, and `git grep -n "^## The writer's revision$" -- plugin/instructions/plan_review_rounds.md` still prints its heading. These are the two anchors Tasks 3–5 cite.
- In `## The writer's revision`, no line still directs the writer to apply or record a Should Fix or Nice to Have item. The only place in the file that states rule 1 is `## The verdict`, apart from the incidental section's pre-existing sentence.
- The file still opens on `# Plan-review rounds` with no frontmatter fence, as `.claude/context/conventions.md` → `## The stack, in the words the rules below use` requires of an instruction document.
