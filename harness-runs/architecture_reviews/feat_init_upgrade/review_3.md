# Architecture review — round 3

verdict: PASS
review_mode: converging

## Incidental findings (not gating)
- **After `--upgrade` lands, two statements in `cli/src/generators/permissionProfile.ts` that say `--force` is the only route to replacing the profile are false, and no task amends them.** The module header, under `## What this module deliberately does not do`, says "`--force` is the one flag that suspends that contract, and therefore the one run under which those hand-added entries can be lost". The doc comment on `RenderProfileOptions.force` says "the only condition under which the profile on disk is replaced, and therefore the only run whose hand-added plugin-root entries can be lost". Task 5's `planProfileUpgrade` enqueues the profile under `replace-if-changed`, and its `renderCurrentProfile` sets `force` from `carryForward`, so `init --upgrade` replaces the profile too. Task 4's amendment list covers only what the carry-forward exclusion and the local-file read make untrue, and Tasks 5 and 10 do not edit this module's comments. The rule at stake is `.claude/context/cli.md` → `## What "done" means here` ("A reviewer holds a change to its module's own header"). This is outside this round's scope because the revision did not change the text that causes it. Lead for the end-of-branch review: check both statements against the diff.
