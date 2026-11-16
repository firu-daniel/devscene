### 1. Task prompt names an absolute home-directory path

**Site:** `harness-runs/task_prompts/fix_planning_node_tool_check_task_prompt.md` — the `- **Plugins loaded:**` bullet under `## Measured, 2026-11-16, Claude Code 2.1.325`, in the quoted JSON object's `"path":` value (near line 32; navigation hint only — find it by the substring `"source":"devscene@inline"`).

**Failing test:** none — run-gates (gate `6a no machine paths`, `scripts/check-machine-paths.sh`, run by `scripts/run-gates.sh`)

**Failure, quoted from the log** (home directory rewritten as `<home>`):

```
  FAIL  6a no machine paths (printed output, which is the finding, 2 s)
        ./harness-runs/task_prompts/fix_planning_node_tool_check_task_prompt.md:32:- **Plugins loaded:** `devscene` once, `{"name":"devscene","path":"<home>/Work/devscene/plugin","source":"devscene@inline","version":"0.7.1"}`, beside Claude Code's built-in plugins. No installed copy was loaded beside the `--plugin-dir` one.
```

**Diagnosis.** Gate 6a (`scripts/check-machine-paths.sh`) greps the working tree for the running user's `$HOME` and fails on any printed hit; it grades output, not exit status. The task prompt, which is tracked (`git ls-files` lists it), quotes the node-1 `init` event's plugin record verbatim, and that record's `"path"` value is the absolute path of the main checkout's `plugin/` directory under the home directory. `.claude/context/conventions.md` states the rule this breaks: "**The self-containment gate binds every commit:** nothing in this tree may name a location on the machine that wrote it". A recursive search of the current tree with the gate's own exclusions finds this file as the only hit, so this one line is the whole failure. Class: no earlier logs — first round.

The same document already writes this location in a machine-neutral form: the `## Measured, …` paragraph gives the launch command as `--plugin-dir <main checkout>/plugin`. The measured fact the bullet records — `devscene` loaded once, from the `--plugin-dir` copy, source `devscene@inline`, version `0.7.1` — does not depend on the literal home path, so neutralising the path invents no result (the prompt's own `## Constraints` forbid inventing one).

**Fix.** In that one bullet, replace the absolute value of the `"path"` key (shown above as `<home>/Work/devscene/plugin`) with `<main checkout>/plugin`, matching the placeholder the same document uses for the `--plugin-dir` argument. The bullet becomes:

```
- **Plugins loaded:** `devscene` once, `{"name":"devscene","path":"<main checkout>/plugin","source":"devscene@inline","version":"0.7.1"}`, beside Claude Code's built-in plugins. No installed copy was loaded beside the `--plugin-dir` one.
```

Leave every other key of the JSON object and every other word of the bullet unchanged.

- [ ] Replace the home-directory path in the `"path"` value with `<main checkout>/plugin`.
- [ ] Confirm with a bare `grep -rlF` of the home directory (from a bare `printenv HOME`) over `harness-runs/task_prompts/` that the file no longer names it.
- [ ] Check that no other file this branch has written carries the home directory — in particular, that no plan or doc file copied this bullet from the prompt with the literal path (for example a record added to `docs/flow-graph-walker.md` for goal 3). Use the same `<main checkout>/plugin` form wherever it was copied.
- **Deviations from plan:** The bare `printenv HOME` the second sub-step asks for was refused by the tool layer (don't-ask mode). The home-directory literal was taken instead from the session's own environment block (the primary working directory sits under it), and that literal was searched for with `grep -rlF` over `harness-runs/` and `docs/` (before the fix: hits only in the task prompt and in the untracked log `harness-runs/test_run_logs/fix_planning_node_tool_check/task_round_1.log`, which `git ls-files` does not list), then with a bare `git grep -lF` over every tracked file after the fix: no output. Gate 6a itself (`scripts/check-machine-paths.sh`) is a gate script `commands.test` runs through `scripts/run-gates.sh`, so it was not run here: deferred to the Run gates phase.
