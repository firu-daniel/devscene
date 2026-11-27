# Architecture review — round 0

verdict: PASS
review_mode: full

## Should Fix

1. **`finding_1.md` leaves the `host/node_sessions.py` module docstring's rule stating end-of-session writes** — `.claude/context/devscene-flow-host.md` → `## Shared code and constants`: *"A module states the rule it holds in its docstring, under "The rule:""*.
   Finding 1 moves `seq` allocation to `open`, writes the node file and the formatted log live through a `LiveStream`, and adds a single long-lived formatter process and `NodeSessions.close()`. Its sub-steps update the docstrings of `host/session_process.py` and `host/claude_executor.py`, but not that of `host/node_sessions.py`. That docstring's opening paragraph and its `record(usage)` rule bullet still say that `usage.stream` goes to `<seq>-<node>.stream.jsonl` and that *"the formatter run as one argv word with the stream on stdin"* happens at record time. Its first bullet also says the numbering is taken at record time. Add a sub-step to `finding_1.md` that restates those bullets: `NodeSessions` is also the `StreamSink`, `open` takes the `seq`, the node file and the formatted log are written live with whole lines only through one formatter per `NodeSessions`, `record(usage)` writes them only when no live stream was opened, and `close()` drains the formatter. This is graded Should Fix because a stale doc comment is never a Must Fix on its own (`finding_grades.md` → `## Never a Must Fix on its own`).
