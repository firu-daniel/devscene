feat_must_fix_definition

`feat_must_fix_definition` gives every agent that grades a finding one strict definition of a Must Fix: a closed list of classes, plus a sentence the reviewer must be able to complete. A finding that fits no class, or whose sentence cannot be completed, is a Should Fix.

All three grades stay: a review keeps carrying Should Fix and Nice to Have items.

## Why

A Must Fix decides whether a plan round fails, but the plugin has no single statement of what one is. Each of these sets a different test:

| Where | Wording | Test |
|---|---|---|
| `branch-reviewer`, `skeptic-reviewer`, `layer-reviewer` | "Grade every finding by consequence" | "a consumer acting on this diff would do the wrong thing" |
| `ui-tests-plan-reviewer` | Same heading | The same test, with the `qa-tester` as the consumer |
| `review-plan-reviewer` | "Must Fix is reserved for" | Only a parity divergence, broken architecture or a hard conventions violation |
| `task-plan-reviewer` | No general definition | Whatever its checklist marks Must Fix |
| `architecture-reviewer`, `business-parity-reviewer` | "A violation is a **Must Fix** unless noted" | Any violation inside that reviewer's lens |
| `user-review-fix-plan-writer` | "real and impactful" | A parity break, a bug or a broken UX flow |
| `test-fix-plan-writer` | `## Must Fix` lists every fixable failure | Any fixable test or type failure |

These disagree. A plain bug is a Must Fix under the consequence test, but it is not on the "reserved for" list that `review-plan-reviewer` uses to call out severity inflation.

`dispatch_discipline_instructions.md` tells orchestrators to rely on the severity rubric each agent already carries, but `task-plan-reviewer` carries no general one. Its scope-register checks sit under `### Completeness (Must Fix)`, so a gap blocks the plan whatever kind of text the missed site is.

The cost shows up in planning:

- `feat_docs_catalog_retrieval` hit the five-revision cap with most Must Fix items being descriptive sentences the branch would make false. Every fix was a register row plus a documentation edit, and none changed the design.
- `feat_init_upgrade` had 12, 5, 2, 2 and 3 task-plan Must Fix items across rounds 0 to 4. Round 1 caught real behaviour problems. By their titles, all seven items in rounds 2 to 4 were scope-register gaps or stale statements.

## The definition

A finding is a **Must Fix** only when it meets both conditions below. Otherwise it is a Should Fix, or a Nice to Have when it is style, wording or ordering.

The definition has to hold in any adopting repository, so it names no path or file type specific to this one.

### 1. It belongs to one of four classes

| Class | The finding must show |
|---|---|
| **Wrong behaviour** | Running the code as this change leaves it, or as the plan will build it, gives a wrong result: incorrect data or output state, a crash, data loss, a security or permission hole, a failing test or type check, or a stated requirement not met. |
| **Wrong build** | An implementer following the plan or finding as written would build the wrong thing, leave out required work, or be unable to finish: tasks that contradict each other, a missing requirement, an undefined interface, a dependency ordered too late, a forbidden test run. |
| **Wrong action from operative text** | Text would, followed literally, cause a failed or harmful action. Operative text is anything a person, an agent or a program follows or reads as input: instructions, configuration, templates, schemas, literals other files depend on, and any command, path, flag, setup step or remedy given in documentation or program output. |
| **Broken contract** | A required accompanying item is missing, a reference does not resolve, a format a parser or loop reads is broken, a layer boundary is crossed, a mandated convention is bypassed, or business logic diverges from the reference implementation while the parity phase is on. |

### 2. The reviewer can complete the failure sentence

> If `<actor>` does `<step>`, then `<observable wrong result>`.

- `<actor>` is a named consumer: the implementer, a named agent, an adopter, or the running program.
- `<step>` exists in the artifact under review, and the finding quotes it or names the code path.
- `<observable wrong result>` can be checked. "May be confused", "may believe" and "could mislead" do not qualify.

Each Must Fix entry records `**Class:**` and `**Failure:**`, beside the fields `plan_review_rounds.md` → `## The Must Fix entry` already requires. The same two fields go on each Must Fix finding of a code or skeptic review, where `review-plan-reviewer` checks them and regrades an entry that does not hold up.

No agent meta-reviews a plan round, so plan rounds get a scripted check instead: a Must Fix entry missing either field makes the round file invalid, and it does not reach the plan writer. The check proves the fields are present, not that the reasoning is right. Today the plan walker reads only a round file's `verdict:` line, so this is new parsing. It lives in a script that the walker and the prose-routed user-review fix-plan rounds can both run. Planning settles how the reviewer is sent back, within the existing round limits.

### Never a Must Fix on their own

- A code comment or doc comment.
- A sentence that only describes the project and has become false, including a stale count.
- Output wording that states something inaccurate but gives no step to follow.
- A hypothetical the reviewer did not verify.
- A line coordinate, as today.

### Worked examples

These come from `feat_init_upgrade`, round 4, and should be used as calibration.

| Finding | Grade | Reason |
|---|---|---|
| `docs/cli.md` says `--reset-config` is the one route that replaces a file without `--force`, which `--upgrade` makes false | Should Fix | It describes the tool and gives no step that now fails. |
| `docs/cli.md` says a forced run carries plugin-root entries forward, without the local-entry exception | Should Fix | The remedy it gives still works. Only the description is incomplete. |
| `init --upgrade` would print "so --force left them in place", although `--upgrade` refuses `--force` | Should Fix | A real defect, but the message gives no step that leads to a wrong result. |

For contrast, a task that breaks an existing test it does not edit is a Must Fix: **Wrong build**, with a failure sentence the reviewer can show.

## Checklists

The "not downgradable" rules stay, but every checklist trigger must map to one of the four classes. A trigger that maps to none is regraded in the same change. No agent keeps its own competing definition: the "reserved for" list and "real and impactful" are replaced.

## One file owns the grades

`plugin/instructions/finding_grades.md` owns the four classes, the failure sentence, the "never a Must Fix" list, the meanings of Should Fix and Nice to Have, and the calibration examples. It stays short, because every grading agent reads it, and it lists those agents as its roster.

Each grading agent points at it from `## Read first` and never restates it. The agent keeps only what is its own: its lens, its checklist with each Must Fix trigger mapped to a class, and its output format and return fields. A Must Fix means the same thing in every agent. A dispatch prompt still may not restate or adjust the definition.

## Scope-register gaps

A scope-register gap has no grade of its own. It is graded by the definition above, like every other finding, and the grade does not depend on where the missed site lives.

- **Must Fix:** the gap would lead to a wrong implementation or a wrong action, and the reviewer can complete the failure sentence. For example, the plan omits a site that must change for the feature to work, so an implementer following the plan ships it broken.
- **Should Fix:** the missed site only describes the project, and nothing goes wrong when it stays stale until someone updates it.

A verified gap is still always reported. `task-plan-reviewer`'s register dispositions, which today make every verified gap a Must Fix, take their grade from this definition. When one round's gap covers both kinds, the reviewer splits it into one Must Fix and one Should Fix. The register's structure and derivation do not change.

## Should Fix in planning

What happens to a planning-round Should Fix does not change. It never fails a round, it stays in the review file as a record for a human, no loop reads it and the plan writer does not act on it. It does not become a lead for the end-of-branch reviews. Implementation, those reviews and the human check remain free to find the same issue on their own.

## Roadmap

This branch sets the `Review severity markers` row in `ROADMAP.md` to `Done`. The index there lists outstanding work in priority order, so the item leaves the index and the later priorities move up.

The row's description may keep "possibly a review should carry Must Fix items only". "Possibly" makes it an idea, not a constraint on this work.

## Done when

- `plugin/instructions/finding_grades.md` is the only statement of the grades. Every agent that grades a finding points at it, and no competing definition or restatement remains under `plugin/`.
- Every Must Fix entry carries its class and failure sentence.
- `review-plan-reviewer` rejects a code or skeptic review's Must Fix without them.
- A plan round whose Must Fix lacks either field is refused by the scripted check and does not reach the plan writer, in task-plan and user-review fix-plan rounds alike.
- Every checklist trigger still graded Must Fix maps to a class.
- The definition names no path or file type specific to this repository.
- A plan whose only register gap is a stale descriptive sentence gets `verdict: PASS`, with the site under `## Should Fix`.
- A plan whose register gap would lead an implementer to a wrong result gets `verdict: FAIL`.
- A wrong command that documentation tells a reader to run gets `verdict: FAIL`.
- Planning-round Should Fix items are handled exactly as they are today.
- `ROADMAP.md` shows `Review severity markers` as `Done`, and the item is out of the priority index.