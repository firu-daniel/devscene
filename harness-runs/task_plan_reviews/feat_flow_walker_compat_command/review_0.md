# Task plan review — round 0

verdict: PASS
review_mode: full

## Should Fix

1. **The run-mode refusal cases do not say where the walk enters** — `task_2_plan.md` (the `open_walker` case) and `task_5_plan.md` (the case *"a run-mode refusal → exit 1 with the host's text"*).
   Task 2 says *"One case walks the real graph through `open_walker(root, branch, graph, skipped=None)` with no ledger: `start` returns a `Refused`"*. The graph's `start` is `plan_writer` (`cli/templates/scripts/flows/task_plan_writing.v4.graph.json` → `"start": "plan_writer"`). `plan_writer` declares no `skip`, so a plain `start` dispatches it and asks no predicate. It never refuses, and `last_refusal` stays `None`. The first run-mode predicate is asked only when `plan_round` opens: `business_parity_review` → `run_mode_skips_parity`. Task 5's command-level case has the same gap: a plain `start` with no `--skipped` and no ledger exits `0`.
   Fix: in both files, name the entry. Either `start` with `entry`/`--entry plan_round`, or `start` followed by `next --outcome returned`, which is where bash's `eval_skip` refuses as well.

2. **The Scope register's procedure reaches README sections that are not rows** — story index (`feat_flow_walker_compat_command_story_plan.md`), `## Scope register`, the *"the package README's sections (procedure)"* entry.
   I re-walked that entry. Its traversal includes the bold paragraph leads inside `## What it reads, answers and keeps`. Its decision rule reaches a section that *"names what the `commands` or `host` layer holds"*. That clause also reaches three paragraphs that name host units, and none of them is a row:
   - **Predicates.** — names `HarnessPredicateHost` and `refusal_reason`, which Task 2 extends with `last_refusal`.
   - **The walk.** — names `walk_store`.
   - **Resuming a round.** — names `start_walk` and `current_step`. Task 1 makes them clear and carry the kept findings record.
   This is disposition (i). None of these sites has to change for the work to function, and each still reads true, only incomplete; hence Should Fix.
   Fix: add the three sites as rows, `change` (Task 7) or `no-change` with a reason. Or narrow the decision rule to what was meant, for example: *"a section is reached when it states that the package has no command line, is `## The layers`, describes the non-round findings-file departure, or leaves an exit status to the caller"*.

3. **Task 4's tab case expects a `--flow` value with a tab to pass parsing, which the plan's own refusal order prevents** — `task_4_plan.md`, `**Work:**` → the `tests/test_arguments.py` bullet: *"`--findings` with a tab refused while a `--flow` value with a tab is not"*.
   The refusal list ends with *"last `unknown flow '<flow>'` for a flow outside `[a-z0-9_]`"*. A tab is outside that set, so `parse` refuses such a `--flow` as `unknown flow`. It is not accepted. Bash does the same (`flow-walker.sh` → `# --- Arguments`: the tab check is `--findings` only, and the flow check comes later).
   Fix: put the tab in a flag the later checks do not reject, such as `--branch`. Or assert that the `--flow` case is refused with `unknown flow '<value>'` and not with the tab text.

## Nice to Have

1. **Task 8's new ROADMAP text points the differences list at the wrong heading** — `task_8_plan.md`, `**Work:**` → *"its differences from bash listed for #419 ([`devscene-flow-host/README.md`] → `## The command line`)"*. Task 7 writes the differences under `## Differences from flow-walker.sh`, not under `## The command line`. Link both headings, or reword the clause so it points only at the command line.

2. **Task 2's ordering claim is stronger than the code supports** — `task_2_plan.md`, the contract: *"A `None` answer is always the walk's last question before its `Refused`"*. `host/resume.py` → `_skipped` asks the same host before `Walker.start`, and goes on when the answer is `None`. Because `Walker.start` asks the same predicates in the same gate order on arrival, the reason still matches in practice. The sentence would be accurate as: the last `None` answer belongs to the predicate whose refusal the walk returned.
