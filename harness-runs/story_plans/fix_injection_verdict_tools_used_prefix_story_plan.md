# Story: Accept the tools-used line ahead of the hand-back frame in the prompt-injection verdict

## Context

The prompt-injection screen's `verdict` verb parks a run when the reviewer's `Agent` result opens with a `<tools-used-before-summary>` line, even when the reply inside it is `SAFE`. `pis_unwrap_vlines` in `prompt-injection-screen.sh` requires `[Subagent hand-back]` to be the first non-blank line, so it leaves the result wrapped and the parse reports `malformed-verdict`. This branch teaches the unwrap that one exact prefix and keeps every other shape malformed.

**The shape, measured.** The main checkout's 87 recorded run streams, read on 2026-11-18, hold 4752 `Agent` / `Task` results carrying the frame. Ahead of the frame, 4575 have nothing, 113 have the tag line, 57 have a `[harness: subagent output matched instruction-shaped pattern(s): …]` notice, and 7 have the tag line and then that notice. Nothing else occurs. Every recorded tag line is indented by two spaces and followed by a whitespace-only line, so blank lines must be accepted **after** the tag as well as before it. Its content is a tool name or a comma-separated list (`Grep`, `Edit, Write`). The prompt-injection reviewer's own results account for 9 of the tag-prefixed results and none of the notice-prefixed ones.

**The accepted prefix, stated once for every task.** Ahead of the frame, any mix of whitespace-only lines and *tools-used lines*. A tools-used line is exactly `<tools-used-before-summary>`, then one or more characters that are neither `<` nor `>`, then `</tools-used-before-summary>`, at column 0 or indented by exactly two spaces, with nothing else on the line. Column 0 has not been observed; the task prompt asks for it.

**The harness notice stays malformed.** The task prompt's line *"Any other text before the frame stays malformed"* covers it, so a result carrying the notice still parks. The cost is bounded: the run stops, and an `UNSAFE` reply that drew the notice parks as `malformed-verdict` without its findings. Task 1 pins this with a test and Task 4 records it. Widening the prefix to the notice is a separate decision for the maintainer.

**Other readers of `Agent` results.** The task prompt asks whether any has the same assumption. `pis_unwrap_vlines` is the only code that keys on the frame. `autonomous-format-stream.sh` drops `tool_result` bodies, `lib/run-analytics.jq` reads `tool_use_result.agentId` and tool-result metadata rather than the text, and the planning driver reads a node session's `result` text, which is not an `Agent` result. Orchestrating sessions read results through `agent_return_contract.md` → `## Reading a return` step 1, which Task 2 corrects: its sentence *"The reply is the indented lines"* would otherwise take in the indented tag line.

**Delivery.** Task 1 changes the template and its tests, Task 2 the contract, Task 3 this repository's self-adopted copy, and Task 4 the document of record. Runs execute the main checkout's `scripts/prompt-injection-screen.sh`, so the fix reaches this repository's runs only once Task 3's copy is merged there.

**Top risks:** the likeliest failure is a prefix check loose enough to pass something other than the measured line, which would weaken a security parser; Task 1 guards it with a closed line predicate and negative cases for every near miss, including the tag inside and after the reply. The second is the template and the self-adopted copy drifting, which would leave the park in place here while tests pass; Task 3 guards it with a content comparison that tolerates the two files' differing modes, and a separate check that the adopted copy keeps its own. The third is the contract describing the prefix while still defining the reply as "the indented lines", which Task 2 closes by anchoring the reply after the frame.

## Phase 2 Readiness — Ordered Fix List

**This section is the single source of truth for the implementation loop.** The orchestrator walks the `[ ]` entries below top-to-bottom; the commit step flips each one to `[x]` as that task's commit lands. **Only the committing role flips a marker** — the commit step — `commit-on-branch.sh --unit` — in every flow that runs the unit loop, the orchestrator itself in the supervised flow, which runs none: an implementer never changes a marker here, and never edits any other line of this section, in an index a run is iterating. `[ ]` markers anywhere else (sub-step bullets inside per-task files) are informational only, and the commit step never touches them.

Each entry resolves 1:1 to `harness-runs/task_plans/fix_injection_verdict_tools_used_prefix/task_<K>_plan.md`. Ordered bottom-up by ship sequence, with the catch-all layer last.

1. [x] **Task 1** — Accept the tools-used prefix in `pis_unwrap_vlines`, fail-closed, with verdict tests _(layer: cli)_ _(points: 15)_
2. [ ] **Task 2** — Describe the tools-used prefix in `## Reading a return` step 1 _(layer: plugin)_ _(points: 5)_
3. [ ] **Task 3** — Bring this repository's `scripts/prompt-injection-screen.sh` level with the template _(layer: general)_ _(points: 5)_
4. [ ] **Task 4** — Record the measured prefix shapes in `docs/structured-agent-returns.md` _(layer: general)_ _(points: 10)_

## Scope register

**Scope predicate**, quoted verbatim from the task prompt: *"check whether any other reader of `Agent` results has the same assumption."*

**Derivation entry — corpus statements of the result shape (command).** Re-run verbatim from the repository root; each output line is one candidate site:

```
grep -rnE 'Subagent hand-back|pis_unwrap_vlines|Agent. result|Reading a return. step 1' plugin docs evals README.md ARCHITECTURE.md cli/templates/README.md
```

**Closure invariant:** every site the derivation entry reaches appears as a row below.

| # | Site | Copy | Evidence | Disposition | Owning task or reason |
|---|---|---|---|---|---|
| 1 | `plugin/instructions/agent_return_contract.md` → `## Reading a return` step 1 ("Take the reply out of the `Agent` result") | — | matches `Subagent hand-back`, `Agent. result` | `change` | Task 2 |
| 2 | `plugin/instructions/prompt_injection_screen.md` → `## The steps` step 3 ("Write the whole `Agent` result, frame line and trailer included") | — | matches `Agent. result`, `Reading a return. step 1` | `no-change` | "the whole result, verbatim" already includes a prefix, and the step points at the contract for the unwrap rather than restating it |
| 3 | `docs/structured-agent-returns.md` → `### The return shape — one fenced `json` block, last`, **Reason.** ("An orchestrating session reads a fenced block at the end of an `Agent` result") | — | matches `Agent. result` | `no-change` | says only that the session takes the reply out first, which stays true |
| 4 | `docs/structured-agent-returns.md` → `### The return shape — one fenced `json` block, last`, **Cost.** ("does not carry the reply verbatim: it wraps it in a frame line and a trailer") | — | matches `Agent. result` | `no-change` | the frame, trailer and indent it names are unchanged, and the prefix does not alter its conclusion about text after the closing fence |
| 5 | `docs/structured-agent-returns.md` → **Decision — the third path, a script caller.** ("The script unwraps only the whole measured shape") | — | matches `Agent. result`, `pis_unwrap_vlines` | `change` | Task 4 |
| 6 | `docs/structured-agent-returns.md` → `## 3. Measured, and not yet measured` ("Measured, 2026-11-17, Claude Code 2.1.325") | — | matches `Agent. result` | `no-change` | a dated measurement stays as taken; Task 4 adds a new dated entry instead |
| 7 | `docs/structured-agent-returns.md` → `## 3.` item 1 ("A frame line at column 0, verbatim") | — | matches `Subagent hand-back` | `no-change` | part of the same dated measurement |
| 8 | `docs/structured-agent-returns.md` → `## 3.` ("step 1 takes the reply out of this shape") | — | matches `Reading a return. step 1` | `change` | Task 4 keeps this sentence and inserts the new measurement directly after it |
| 9 | `docs/watcher.md` → **The planning driver's unmeasured facts** ("wraps the sub-agent's reply in a frame line") | — | matches `Agent. result` | `no-change` | true as written, and it points at the `## 3.` record for detail |
| 10 | `docs/flow-graph-walker.md` → `### Not yet measured, and the hand step that measures it` ("wraps it between a frame line and an `agentId:` / `<usage>` trailer") | — | matches `Agent. result` | `no-change` | true as written, and it points at the same record |
