# Task plan review — round 1

verdict: FAIL
review_mode: full

## Must Fix
1. **Task 4's step 6 makes every init-wired watcher suite run a real `uv sync`** — `task_4_plan.md`.
   After Task 2, `init` writes `<scriptsDir>/python/devscene-flow-host/pyproject.toml` into every fixture it wires. `cli/test/helpers/watcher.mjs` → `createWatcherFixture` wires its fixture with a plain `init`, and 30 suites use it. The watcher's task path cuts each run copy with `"$CREATE_WORKTREE" "$branch"` (`cli/templates/scripts/autonomous-watcher.sh`, the `(2a) Task path` arm), with no `--no-bootstrap`, so `create-worktree.sh` hands off to `setup-worktree.sh --target <clone>`.

   With Task 4's step 6 in place, that bootstrap calls `hr_flow_host_provision <main scriptsDir> <clone scriptsDir>`. The function finds the project, and on a host with `uv` on `PATH` it runs a real `uv sync --frozen --no-dev --no-editable`. The suites pass the inherited `PATH` through (`cli/test/watcher-stall-reset-payloads.test.mjs` builds `PATH: ${bin}${delimiter}${process.env.PATH}`). This repository's gate host has `uv`: gate 13 needs it, and the task prompt measured it running inside a run's sandbox.

   - **Inside the gate sandbox**, the sync exits `2` (`Failed to initialize cache at ~/.cache/uv`, measured in the task prompt). It is also refused the network. Step 6 sets `status=1`, and `create-worktree.sh` removes the copy whose bootstrap failed.
   - **Outside a sandbox**, the suite reaches PyPI. `.claude/context/cli.md` → `## What "done" means here` forbids that: *"No test … reaches the network"*.

   Task 4's `### Targets` name only `setup-worktree.sh` and its own new suite, which stubs `uv`. No task names an existing suite that drives the bootstrap on an init-wired fixture. The test-run rule keeps the unit from running those suites, so the break first shows at Run gates.
   **Raised against:** "It calls `hr_flow_host_provision`, and a non-zero return sets `status=1` and prints which step failed."
   **Must hold:** After Tasks 2 and 4, no existing `cli/test/` suite that bootstraps a run copy of an init-wired fixture runs a real `uv`. Each such route (at least `createWatcherFixture`'s watcher launches) is named in a task's `### Targets` and `**Work:**`, and made hermetic there.
   **Class:** Wrong build
   **Failure:** If the Task 4 implementer adds step 6 as written, then at Run gates on a host with `uv` on `PATH`, `cli/test/watcher-stall-reset-payloads.test.mjs` fails `create-worktree.sh cut no working copy`. The bootstrap's real `uv sync` exits `2` inside the sandbox, step 6 sets `status=1`, and `create-worktree.sh` removes the copy. The other `createWatcherFixture` suites that cut a task copy fail the same way.
   **Fix:** In `task_4_plan.md`, add `cli/test/helpers/watcher.mjs` to `### Targets`, with a `**Work:**` bullet that puts a stub `uv` (records nothing, exits `0`) ahead of the inherited `PATH` for every watcher `createWatcherFixture` starts. Before writing the bullet, grep `cli/test/` for every other suite that runs `create-worktree.sh` without `--no-bootstrap`, or `setup-worktree.sh`, against a fixture `init` wired. Name each suite whose run copy step 6 now reaches, and make it hermetic the same way. A suite that copies only the scripts reaches the `no flow host` skip and needs nothing.

## Should Fix
1. **Scope register: sites no derivation entry reaches (disposition ii)** — story index. I re-ran entries 1–3 and re-walked entry 4. Every site they reach is a row. These sites are reached by none, and each describes the tool without giving a failing step:
   - `README.md` → the upgrade passage: *"bring the outer-loop scripts and the permission profile up to the latest release. Nothing else is written"*. Task 2 makes `init --upgrade` replace the Python packages too.
   - `docs/cli.md` → `## 3. The re-run contract`, the `--force` bullet: *"`init --upgrade` replaces the outer-loop scripts and the profile under a policy of its own"*. Entry 4 walks only that section's table.
   - `docs/cli.md` → `### The interaction rule`, *"The questions this contract governs, in the order `init` puts them"*. Task 7 adds a question.
   - `docs/cli.md` → `## 2. \`init\``, *"The fourth of the five questions `init` puts"*.
   - `docs/cli.md` → `## 5. The wrapper-script contract`, *"Two families land in `scriptsDir`"*. Its outer-loop list gains `flow-host-provision.sh` (Task 3), and `scriptsDir` gains `python/` (Task 2).
   - `docs/cli.md` → `## 6.`, *"**Everything that runs outside the sandbox is write-protected on both sides**"*. Its enumeration of the set gains the main checkout's `<scriptsDir>/python` (Task 5).
   - `docs/remote-execution.md`, *"**The job's setup**, in the order `devscene-run.yml` runs it"*. Task 13 edits this passage by grep, but it has no row.
   - `docs/remote-execution.md` → **The step.**, the `jobSurfacePaths` enumeration *"the outer-loop scripts and `<scriptsDir>/lib`, `<githooksDir>`, …"*. Task 5 widens it.
   - `.claude/context/devscene-flow-host.md`, *"the decided but unbuilt route"*, and `.claude/context/cli.md` → its *Owns* list. The Context names both as falsified, but neither is a `no-change` row.

   Corrected derivation entry, strictly wider than entry 4:
   - Widen entry 4's traversal to all of `## 2`, `## 3`, `## 5`, `## 6` and `## 7`. Keep its decision rule, adding *"enumerates the write-protected set"*.
   - Add one read-only command entry, re-run from the checkout root:
     `git grep -nE 'Nothing else is written|outer-loop scripts and the profile|outer-loop scripts and \`<scriptsDir>/lib\`|The job.s setup\*\*|of the five questions|The questions this contract governs|Two families land in|write-protected on both sides|decided but unbuilt' -- 'docs/*.md' README.md .claude/context/`
2. **Row 9, `docs/remote-execution.md` → *"Install the prerequisites beside it"* (disposition iii)** — `task_13_plan.md`. The row's change adds `uv` to the list. The same sentence says every action the two workflows pin *"runs on Node 24 and names that minimum in its release notes"*. Once Task 9 adds `astral-sh/setup-uv`, that claim is unverified: the story index marks the lookup as owed. Qualify it the same way Task 9 rewords the `ACTION PINS` block.
3. **Task 4 overstates what `--target` closes** — `task_4_plan.md`. The header sentence says step 6 is *"outside that residual for `--target`"*. But `UV_PROJECT_ENVIRONMENT` points into the run-written copy (`<clone>/<scriptsDir>/python/.venv`), and `copySurfacePaths` leaves it unprotected. `uv` inspects an existing environment there, and a branch can force-add one. Unverified: whether `uv` runs that environment's interpreter here. Either way, record it as part of the residual, or refuse a pre-existing `.venv` that step 6 did not create.
4. **A sync failure fails the bootstrap before anything needs the walker** — `task_4_plan.md`. `status=1` makes `create-worktree.sh` remove the copy. So a host with `uv` but a transient registry or network error loses every run, for a walker that #419 has not wired yet. That contradicts the Context's *"a host without `uv` loses nothing yet"* stance. A warning until #419 would match Task 8's grading.
5. **Write protection here does not reach the link targets** — `task_5_plan.md`, `task_12_plan.md`. `scripts/python/graphscene` and `scripts/python/devscene-flow-host` are symlinks. The `denyWrite` and `jobSurfacePaths` entries for `scripts/python` cover the links, not `graphscene/` and `devscene-flow-host/`. Task 12 should say so rather than imply the protection holds in this repository.
6. **This repository's own profile is a manual step** — story index → `Manual setup required:`. The gitignored `.claude/settings.autonomous.json` gains Tasks 3 and 5's entries only when a maintainer re-runs the self-adopted `init --upgrade`. Name that step.
7. **Self-cancelling update clauses** — `task_2_plan.md`, `task_5_plan.md`, `task_7_plan.md` and `task_8_plan.md`. *"Update only that expectation, and only in suites this task edits"* names no suite, and no task here edits any existing suite. I verified no break for the sets these four tasks widen. The suites I read assert by `includes`, by table-derived lists or by named adjacency. Still, the clause either names the suites or should go.

## Nice to Have
1. `task_6_plan.md` lists `cli/src/doctor/checks.ts` → `IGNORE_RULES_CHECK` as a conditional target. That check holds no expected-rule list, so the condition never fires. Task 12's stated reason for its `.gitignore` line, that *"`doctor`'s `ignore-rules` reads this block as `init` would write it"*, does not match what that check reads.
