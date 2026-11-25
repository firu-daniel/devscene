### 1. The hand-off lets Python write `__pycache__` into the shipped sources, and the next unit commit stages the bytecode under `<scriptsDir>/python/`

**File:** `cli/templates/scripts/flow-walker.sh` (the launch at the end of the script) — "UV_PROJECT_ENVIRONMENT=\"$fw_env\" PYTHONPATH=\"$fw_sources\" \\"
**Class:** Wrong behaviour
**Failure:** If the orchestrating session in an adopter's run copy runs `bash <scripts_dir>/flow-walker.sh start --flow task_plan_writing --branch <branch> …`, then Python writes `__pycache__/*.pyc` under `<scriptsDir>/python/devscene-flow-host/src/` and `<scriptsDir>/python/graphscene/src/`, and the next `commit-on-branch.sh --unit` commits those bytecode files to the branch.

**The problem.** The hand-off puts the shipped sources first on `PYTHONPATH` (`HAND-OFF` step 4: `PYTHONPATH=<py>/devscene-flow-host/src:<py>/graphscene/src`). It does not turn off bytecode writing. CPython writes a `__pycache__/<module>.cpython-<ver>.pyc` beside every module it imports from a writable `PYTHONPATH` directory. Before this branch the code ran from the non-editable wheel inside `<scriptsDir>/python/.venv`, and that directory is ignored. The sources beside the walker are not ignored:

- In an adopting repository `<scriptsDir>/python/devscene-flow-host/` and `<scriptsDir>/python/graphscene/` are real directories that `init` copied there.
- The generated `.gitignore` has no `__pycache__` or `*.pyc` rule. `cli/templates/repo/gitignore` ignores only `{{flowHostEnvPath}}` under that tree.
- A run copy's `<scriptsDir>/python/` can be written from inside the sandbox (story `## Context`, **The trust rule behind Task 6**), so the write succeeds there on the first walker call.

`commit-on-branch.sh --unit` builds its stage set from `ls-files -z --others --exclude-standard` (`cli/templates/scripts/commit-on-branch.sh` → "ls-files -z --others --exclude-standard" in the unit path; `cli/templates/scripts/lib/unit-commit-lib.sh` → `ucl_stage_set` adds every `--others` record). So the next unit commit stages every new `.pyc` file and commits it.

That bytecode is tied to one machine and one interpreter. It also lands under `<scriptsDir>/python/`, the tree the task prompt says the job-surfaces check refuses a branch for changing (task prompt, **What #478 left for this branch** → *"The job-surfaces check refuses a branch whose commits changed `<scriptsDir>/python/`"*). The same write also reaches a supervised session in the main checkout. There it leaves untracked `.pyc` files in the adopter's committed tree.

This repository does not show the defect, and that is why no suite caught it. Here the two package paths are committed symbolic links, and `git ls-files --others` does not descend through a link.

**How it was confirmed.**
- A probe was run: `bash scripts/scratch-run.sh harness-runs/scratch/pyc_probe.py <checkout>/scripts/python/.venv/bin/python`. Its child process, the walker environment's own interpreter (Python 3.14.7), imported a planted package through `PYTHONPATH` with no other `PYTHON*` variable set. It printed `pycache_written: True ['__init__.cpython-314.pyc']`, beside the planted source.
- Confirmed only by reading, not executed:
  - the unit stage set's `--others` listing (`commit-on-branch.sh`, `ucl_stage_set`);
  - the generated `.gitignore` template having no bytecode rule;
  - the job-surfaces refusal, taken from the task prompt.
- No end-to-end run of an adopter's unit commit was executed.

**Fix.**

1. In `cli/templates/scripts/flow-walker.sh`, turn bytecode writing off on the launch, beside the two variables it already sets:

   ```bash
   unset VIRTUAL_ENV
   UV_PROJECT_ENVIRONMENT="$fw_env" PYTHONPATH="$fw_sources" PYTHONDONTWRITEBYTECODE=1 \
     exec uv run --frozen --no-sync --no-cache --project "$fw_project" \
     devscene-flow-walker "$@" ${fw_flows[@]+"${fw_flows[@]}"}
   ```

   This also keeps a test from writing bytecode into this checkout. Every walker suite links the fixture's environment to this checkout's `scripts/python/.venv` (`cli/test/helpers/walker.mjs` → `linkWalkerEnv`), so without the variable Python's cache files for the environment's own dependencies would land there.

2. In the same file's header, `# HAND-OFF` step 4, add the variable to the quoted launch. The two lines become:

   ```
   #        UV_PROJECT_ENVIRONMENT=<py>/.venv \
   #        PYTHONPATH=<py>/devscene-flow-host/src:<py>/graphscene/src \
   #        PYTHONDONTWRITEBYTECODE=1 \
   ```

   Add one sentence after the `THE SHIPPED SOURCES LEAD PYTHONPATH` paragraph: "`PYTHONDONTWRITEBYTECODE=1` keeps Python from writing `__pycache__` beside those sources, which sit in a committed tree no ignore rule covers, so a unit commit's untracked listing would otherwise pick the bytecode up."

3. In `devscene-flow-host/README.md` → `## The command line`, add `PYTHONDONTWRITEBYTECODE=1` to the fenced launch line after the `PYTHONPATH=…` assignment, so it matches the script.

4. In `cli/test/flow-walker-hand-off.test.mjs`, add a case that drives a `start` and then asserts that no `__pycache__` directory exists under either shipped package's `src/`. For example:

   ```js
   test('the hand-off writes no bytecode beside the shipped sources', { skip: SKIP }, async (t) => {
     const dir = await fixture(t);
     assertDispatch(await walk(dir, startArgs));
     const python = join(dir, INIT_SCRIPTS_DIR, 'python');
     for (const pkg of ['devscene-flow-host', 'graphscene']) {
       const src = join(python, pkg, 'src');
       const caches = readdirSync(src, { recursive: true }).filter((p) => String(p).split(/[\\/]/).includes('__pycache__'));
       assert.deepEqual(caches, [], `${src} gained bytecode: ${caches.join(', ')}`);
     }
   });
   ```

   Add `readdirSync` to the file's `node:fs` import. Name the new rule in the suite's header sentence: "and it writes no bytecode beside the shipped sources". That test file is one this fix edits, so it is the only test file the fix runs. The full suite runs in the Run gates phase.
