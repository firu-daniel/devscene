# Architecture review — round 0

verdict: PASS
review_mode: full

## Should Fix

1. **`task_3_plan.md` / `task_1_plan.md` — which findings files a revision carries is decided in `commands`, not in `host`.** Task 1 keeps the record and hands it out on `HostStep.revision_findings`. Its **Where this layer stops.** paragraph then gives the precedence to Task 3: *"Task 3 (`commands/render.py`) owns the precedence when it prints: `revision_findings` when non-empty, otherwise the `detail`s of the action's `closed_round`"*. `.claude/context/devscene-flow-host.md` → `## The internal layers` gives `host` *"the harness's rules over its records"* and gives `commands` the rendering. Choosing which kept file is the revision's findings file is a rule over the host's own record. It is the counterpart of bash's single `revision_findings` key, and Task 1 already writes and clears that record to make the rule hold. With the choice made in `render`, any other consumer of `HostStep` has to re-derive it. Two acceptable shapes:
   - Task 1 resolves the effective findings files on the `HostStep` it returns, and `render` prints them.
   - Task 3's docstring states why this choice counts as rendering.

   This is not a Must Fix: the import direction stays legal (`commands` over `host`), and no step in the plan produces a wrong result, because `render` is the only consumer this branch adds.

## Nice to Have

1. **`task_5_plan.md` — the no-saved-walk check reads the walk store outside the host's entry points.** For `next` and `current`, the plan runs *"`walk_store(repo_root, state_dir, branch).read() is None` refuses as no saved walk before the host is called"*. That is legal, since `commands` may import `host/store.py`. But it is a fourth read path beside the story's *"re-reads only through `current_step`"*. A one-line note in `commands/flow_walker.py`'s docstring rule saying that this check is the command's own exit-1 mapping and not a walk read would keep the story's claim literally true.
