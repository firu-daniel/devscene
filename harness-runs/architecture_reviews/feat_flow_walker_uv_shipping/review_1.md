# Architecture review — round 1

verdict: PASS
review_mode: full

## Should Fix
1. **`task_4_plan.md` / `task_5_plan.md` / `task_12_plan.md` / `task_13_plan.md` — in this self-adopted repository, the protected flow-host path is only a pair of symlinks** (carried over from round 0; still open). Task 5 protects `<root>/<scriptsDir>/python` through `cli/src/generators/writeProtection.ts` → `protectedPaths`, and `jobSurfacePaths` is derived from that set. Task 12 makes `scripts/python/graphscene` and `scripts/python/devscene-flow-host` relative symlinks to the root packages. Two consequences follow in this repository only:
   - A `denyWrite` / `Edit` rule on `scripts/python` does not name the link targets `graphscene/` and `devscene-flow-host/`.
   - The remote job's surface check compares the repo-relative `scripts/python` entry. A branch that changes `devscene-flow-host/pyproject.toml` at the root leaves that entry unchanged, so the check does not see the change.

   So Task 4's header sentence (*"it builds from the main checkout's protected packages"*) and Task 13's *"write-protected and is a job surface"* do not hold here as written. I did not measure how Seatbelt or bubblewrap resolve a link under a deny entry. This repository also already builds its own packages unsandboxed through `commands.depInstall` → `python-service.sh provision`, so the branch adds no new exposure, and this stays a Should Fix. The fix is either to qualify those sentences for the self-adopted case, or to state the residual in `setup-worktree.sh`'s `THE RESIDUAL` paragraph that Task 4 already edits.

## Nice to Have
1. **`task_1_plan.md`** — `cli/src/flowHost/layout.ts` (the names owner) imports `outerLoopScriptsDir` from `cli/src/generators/outerLoopScripts.ts`. Then `cli/src/generators/flowHostPackages.ts` and `cli/src/generators/writeProtection.ts` import back from `flowHost/`. No conventions document states a rule for edges between areas (`.claude/context/cli.md` → `## Not determined` leaves even `core/` value imports open), so this is not a violation. One sentence in `layout.ts`'s header on why it builds on the generator's path helper would save a reviewer from re-deriving it.
