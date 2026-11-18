### Task 15 — Sync the self-adopted copies and run the closure checks

**Goal:** This repository's own walker and state-dir READMEs match the templates, and the finished branch satisfies the scope register.

**Depends on:** Task 1 (`cli/templates/scripts/lib/flow-walker-gates.sh`), Task 2 (`cli/templates/scripts/flow-walker.sh`), Task 3 (the three state-dir README templates mirrored here), and Tasks 4–12 and 14, whose edits the closure checks read. This task edits none of those files.

### Targets

- `scripts/flow-walker.sh`
- `scripts/lib/flow-walker-gates.sh`
- `harness-runs/task_plan_reviews/README.md`
- `harness-runs/architecture_reviews/README.md`
- `harness-runs/architecture_user_review_reviews/README.md`

**Work:**

- [ ] Copy `cli/templates/scripts/flow-walker.sh` and `cli/templates/scripts/lib/flow-walker-gates.sh` over their `scripts/` counterparts, keeping each file's existing git mode.
- [ ] In each of the three `harness-runs` READMEs, apply the sentence Task 3 applied to its template: "re-running a round that was interrupted, or whose file the round-file check refused".
- [ ] Re-run every command entry and re-walk every procedure entry of the story index's `## Scope register`. If an entry reaches a site with no row, stop and report it as a blocker rather than editing a file outside this task's targets.

**Verification:**

- `cmp cli/templates/scripts/flow-walker.sh scripts/flow-walker.sh` and `cmp cli/templates/scripts/lib/flow-walker-gates.sh scripts/lib/flow-walker-gates.sh` print nothing.
- Each of the three READMEs is byte-identical to its `cli/templates/state-dir/` template, by `cmp`.
- Register entry E1's command lists only `plugin/agents/layer-implementer.md`, the one `no-change` site whose phrase is unrelated to grading.
- `git grep -l 'finding_grades.md' -- plugin` lists every path on the `## Who may cite this` roster of `plugin/instructions/finding_grades.md`, plus that file only if it names itself.
- `git status --porcelain -- scripts` lists only this task's two script targets.

**Deviations from plan:** The plan says to copy the two script templates. Both `cp` calls were refused by the run's permission mode, so the same content was applied to the two targets with the file-edit tool, hunk by hunk from `diff`. Both `cmp` checks print nothing and `git diff --summary` reports no mode change.
