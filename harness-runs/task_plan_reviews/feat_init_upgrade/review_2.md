# Task plan review — round 2

verdict: FAIL
review_mode: converging

## Must Fix

1. **Scope register: P1 reaches three `docs/cli.md` bullets that have no row — story index (`feat_init_upgrade_story_plan.md`)**
   The revision changed the register, so the derivation duty ran in full. D1 to D7 and P2 close. Re-walking P1 does not (disposition (i)). Its traversal covers the check bullets of `## 7.`, and its decision rule makes a bullet a site when it states what happens to the outer-loop scripts or the profile on a re-run. These three do, and none is a row:
   - `docs/cli.md` → `## 7.` bullet "**The run watcher's absence is a warning**": "`init` writes it and one `init` writes it back".
   - `docs/cli.md` → `## 7.` bullet `task-offer-rules`, the arm "**The script missing**": "the remedy is one `init`, which writes the script create-if-absent and touches nothing else". `task-offer-check.sh` is an outer-loop script (row 95).
   - `docs/cli.md` → `## 7.` bullet `profile-tracked`: "its create-if-absent `init` keeps a present file".

   **Raised against:** "**Closure invariant:** every site each derivation entry reaches appears as a row below."
   **Must hold:** Every site P1 reaches under its stated traversal and decision rule appears as a row with a disposition.
   **Fix:** In the story index, add one row per site above, with P1 as the evidence. Each statement stays true of a plain `init`, so `no-change` with that reason is available; a `change` disposition must name Task 15.

2. **Scope register: no derivation entry reaches the job's list of absent protected paths — story index (`feat_init_upgrade_story_plan.md`) and `task_16_plan.md`**
   Task 3 adds `join(repoRoot, PROFILE_LOCAL_PATH)` to `protectedPaths`, so the base profile gains an exact `denyWrite` entry for a file that is absent from a fresh job checkout. `docs/sandbox-record.md` → residual 12's **Job mode** item 1, "**What the job's profile names.**", enumerates exactly that class: "So the base names that checkout's `.mcp.json`, `.claude/settings.local.json` and a `.git` at each `<scriptsDir>` level as exact `denyWrite` paths, all of them absent in a fresh checkout." Its item 2 then says a kill leaves "those paths" behind as read-only empty files. After Task 3 the list omits one such path. D7 does not search this file, and no other entry reaches the sentence (disposition (ii)).

   This replacement for D7 is strictly wider. It was executed, and it reaches every D7 site plus the sites below:

   `grep -rnIE 'upgraded by re-running .init|the profile itself in the main checkout|paths? of .jobSurfacePaths|Entries you added to this machine|\.claude/settings\.local\.json' cli/scripts/README.md docs/cli.md docs/remote-execution.md docs/watcher.md docs/sandbox-record.md`

   Sites it newly reaches:
   - `docs/sandbox-record.md` → "**What the job's profile names.**" ("all of them absent in a fresh checkout").
   - `docs/sandbox-record.md` → "The files a session loads from its cwd that run code outside the sandbox".
   - `docs/sandbox-record.md` → "A sibling's absent trio paths, by contrast, stay absent during a sandboxed call".
   - `docs/sandbox-record.md` → "counts an untracked leftover `.claude/settings.local.json` as a protected-surface change".
   - `docs/sandbox-record.md` → residual 17, "**Hooks, local MCP servers, plugin monitors, LSP servers, the status line and `apiKeyHelper` run outside the sandbox**".
   - `docs/watcher.md` → "**The pins.**" (the protected paths of `hr_run_protected_rel_paths`).
   - `docs/cli.md` → `### The sandbox block and the permission mode`, "ignores `excludedCommands`, `network.allowedDomains` and `filesystem.allowWrite` in the repository's own `.claude/settings.json`".

   **Raised against:** "`grep -rnIE 'upgraded by re-running .init|the profile itself in the main checkout|paths? of .jobSurfacePaths|Entries you added to this machine' cli/scripts/README.md docs/cli.md docs/remote-execution.md docs/watcher.md`"
   **Must hold:** The derivation entries reach every statement that enumerates the protected set this branch extends, each reached site has a row, and after this branch no document's list of absent exact `denyWrite` paths in a job checkout omits the local additions file.
   **Fix:** In the story index, replace D7 with the command above and add one row per site. Mark "**What the job's profile names.**" `change`, owned by Task 16. In `task_16_plan.md`, add `docs/sandbox-record.md` to `### Targets`, extend the existing `docs/remote-execution.md` bullet to name the local additions file in that sentence, and keep the file at five `**Work:**` bullets. The other sites can take `no-change` with a reason.

## Should Fix

- `task_9_plan.md`: "Entries removed get one warning saying the generator does not produce them, that they were not moved automatically, and that anything still wanted belongs in `PROFILE_LOCAL_PATH`". Task 4 now reports a deliberately deleted local entry through this same `removed` delta, so the adopter who just deleted the entry from the local file is told to put wanted entries back there. Word the warning so it also fits an entry removed from the local file.

## Incidental findings (not gating)

- `task_3_plan.md` and `task_9_plan.md`: `--upgrade` adds an exact `denyWrite` entry for the absent local file and does not write `.gitignore`. On a bubblewrap host, verify whether the placeholder this can leave in a main checkout that lacks the new ignore rule shows up as untracked, and whether the "exists and is not ignored" warning then fires on a file the adopter never created.
- `task_4_plan.md`: the `permissionProfile.ts` header says the module touches no filesystem beyond its templates, the replaced profile and the plugin records. `writePermissionProfile` will also read the local file, and the bullet only asks to update the header's "hand-tuned" statements.
