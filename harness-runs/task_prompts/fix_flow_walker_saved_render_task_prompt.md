`fix_flow_walker_saved_render` makes `devscene-flow-walker`, the compatibility command #465 added, print three things the way `flow-walker.sh` does, and removes the three `TODO: @claude` markers #465 left for them in `devscene-flow-host/src/devscene_flow_host/commands/render.py`. Part of #376.

## Why

#465 rebuilds a `current` from the files on disk instead of re-printing what the step printed, as bash does. That leaves three differences, listed as **Still open**, with no owner, in `devscene-flow-host/README.md` → `## Differences from flow-walker.sh`. They don't go away when #419 retires the bash walker. Each one is the command's own behaviour:

- A `current` can answer differently from the step it re-reads.
- A story index that repeats a heading gets its `evidence.open:` lines under the wrong heading.

#419 is large on its own, so they get their own branch, ordered before it.

## The three differences

- **A non-round reviewer's `arg.iteration` on `current`.** Bash re-prints the saved index. The command re-reads the reviewer's findings folder (`host/reviewers.py` → `review_iteration`), so a findings file written after the step was printed changes the index on `current`. Marker: `render.py` → `_block`. Suite: `cli/test/flow-walker-resume.test.mjs` → *"(4) a UI reviewer in flight is re-dispatched, and the UI plan is not rewritten"*.
- **A finished cap's `rounds:` and evidence lines on `current`.** Bash re-prints them (`flow-walker.sh` → `take_binding`). The command re-reads the findings folders' `FAIL` counts and the story index (`records/round_files.py` → `fail_count`, `records/index_evidence.py` → `read_index_evidence`), so an edit after the cap changes what `current` prints. Marker: `render.py` → `_cap_lines`, the first one. Suites: `cli/test/flow-walker.test.mjs` → *"(3) architecture FAILs every round until the cap"*; `cli/test/flow-walker-ui-and-reentry.test.mjs` → *"(4) UI reviewer FAILs until the cap escalate with no round counts"*.
- **`evidence.open:` lines under a repeated `## Rejected findings` heading.** Bash prints each heading's open entries under that heading's `evidence:` line (`flow-walker.sh` → `fw_index_evidence`). The command prints every `evidence.open:` line after the first heading's `evidence:` line. This happens on every cap, not only on `current`. Marker: `render.py` → `_cap_lines`, the second one. No suite pins a repeated heading.

## Leads

_Starting points from #465's run and its review, not requirements. The planning session decides what holds._

- **Re-printing needs a record of what was printed.** GraphScene's saved walk doesn't hold the rendered index or counts. #465's `RevisionFindingsStore` (`host/revision_findings.py`, beside the walk under `<stateDir>/.flow_walker_state/`) and #464's refusal record are the precedents for a host-side record kept next to the walk. Another route is saving the rendered bytes, which is what bash does (`out=`). The README's **Chosen** entry *"`current` re-renders"* records why #465 re-renders. Whichever route is taken, that entry and the **Still open** entries change with it.
- **Locks.** A new record written by `start` / `next` is written under the locks they already take: `RefusalStore`'s, then the walk store's. `current` takes neither.
- **The evidence order** may be a `records` change, where `read_index_evidence` keeps each heading's entries with that heading, rather than a `render` one.
- **Evidence:** each fix comes with a literal-expectation case in `devscene-flow-host/tests/test_render.py` or `tests/test_flow_walker.py`. The `flow-walker*` suites above are #419's to run against the command.

## Depends on

#465. Ordered after #472 and before #419, so the suites above pass on the command unchanged at the switch-over.
