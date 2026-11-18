# Architecture review — round 0

verdict: PASS
review_mode: full

## Should Fix

1. **`task_12_plan.md` — an out-of-date walker's usage refusal is read as an invalid round file.** Rule source: `.claude/context/conventions.md` → `## The layers` ("`cli/` writes what an adopting repository gets, `plugin/` reads what is there").
   Task 12 treats exit 1 from `check-round-file` as a reviewer's failed return, and every other exit or a missing script as an immediate held binding. `cli/templates/scripts/flow-walker.sh` today exits 1 through `refuse` for an unknown subcommand, and outer-loop scripts are `create-if-absent`, so a repository that updates the plugin before re-running `init --force` keeps that walker. Each user-review gate is then dispatched three times for a fault no reviewer can fix, before the held binding fires. The story's top risks and Task 13 describe only the opposite pairing, a new walker beside older reviewers.
   **Raised against:** "Exit 1 is a return that fails the check"
   **Must hold:** Only the walker's report that this round file is invalid sends a gate back; any other failure of the command is a held binding at once.
   **Fix:** In Task 12, route exit 1 to the re-dispatch only when its stderr line has the form `flow-walker: <path>: <reason>` for the `--findings` path, and take the held binding for any other exit-1 line. Add this new-plugin, older-walker pairing to Task 13's **Cost.** paragraph.

2. **`feat_must_fix_definition_story_plan.md`, `task_6_plan.md` — the validator lands before the format it validates.** Rule source: `.claude/context/conventions.md` → `### The order files are created, so a half-built feature is still coherent` ("Contract before consumer, always").
   Task 6 makes `review-plan-reviewer` require `**Class:**` and `**Failure:**`, but Task 7 is what makes `branch-reviewer` and `skeptic-reviewer` write them, and Task 11 is what adds them to `sample_code_review/finding_1.md`. `plugin/agents/review-plan-reviewer.md` → `## Read first` names that sample as its format specification and says the fixture wins where a check disagrees with it, so between Tasks 6 and 11 the new check contradicts the file that overrides it. The final state is coherent; the intermediate commits are not.
   **Raised against:** "Task 7 makes `branch-reviewer` and `skeptic-reviewer` write these fields in each Must Fix `finding_<N>.md`, directly after the site anchor. Task 11 adds them to `sample_code_review/finding_1.md`, the format this reviewer validates against."
   **Must hold:** The per-finding format, its sample and its producers land no later than the reviewer that enforces them.
   **Fix:** Order the plugin tasks so the sample edit and Task 7 precede Task 6, keeping every `plugin` task between the `cli` and `general` tasks, and update the `**Depends on:**` lines of the moved tasks to match.
