# Task plan review — round 0

verdict: PASS
review_mode: full

## Should Fix

1. **`task_6_plan.md` — the Gap 3 decision does not say how it sits on the driver's two failure classes.** The task prompt's boundary says *"Gap 3 maps onto the existing classes. The `error` rule uses the two failure classes the driver already has (`planning-node-lib.sh`'s header: `infra` … ; `agent` …). It adds no third class."* Task 6's **Decision** / **Reason** bullets for `### An agent's own `error:` return becomes an outcome, never `error`` follow that rule in substance: `error` stays the caller's record of a return that keeps failing, and `blocker` plus a non-halting outcome are ordinary returned outcomes. But they never name `infra` or `agent`, and never say that no class is added. A later branch applying the rule would have to re-derive the mapping from `cli/templates/scripts/lib/planning-node-lib.sh` (the `class: "infra"` / `class: "agent"` arms of `PNL_REAP_JQ`). Add one sentence to the decision: `error` is what the caller records after the `infra`-class re-dispatches run out; `blocker` and a non-halting outcome are returns the agent made, which the driver routes and never retries; no third class is added.

2. **`task_3_plan.md` — the jq floor is attributed to a paragraph that does not state it.** The Work bullet reads *"Keep the bash 3.2 / jq 1.5 floors the header's `FLOORS` paragraph states: no regex builtin in jq, every `if` with an `else`, no associative array."* The `FLOORS.` paragraph of `cli/templates/scripts/prompt-injection-screen.sh` states only Bash 3.2, *"no `jq` for `prescan`"*, and the explicit `mktemp` template. The jq-1.5 rules are stated in `cli/templates/scripts/lib/planning-node-lib.sh`'s `BASH 3.2 AND JQ 1.5 ARE THE FLOORS` paragraph. The `jq-floor` tree guard covers only `cli/templates/scripts/**/*.jq`, so it will not catch a regex builtin inside the script's inline jq program. Cite the real source of the jq rules, and add a header bullet amending `FLOORS.` so that it states the jq 1.5 floor the new `verdict` program must hold.

## Nice to Have

1. **`task_3_plan.md` / story index — a schema-valid `blocker` parked under the id `malformed-verdict`.** Keeping today's behaviour is correct for fail-closed. The park's reason line, though, is `PIS_MALFORMED_REASON` (*"the screen's verdict did not match its closed format"*), which misdescribes a well-formed `blocker` to the person reading the park. The cause is still visible in the 1024-byte excerpt. A later branch that turns the screen into a graph node will route `blocker` on its own key. A sentence in the story index's `## Context` acknowledging that wording would save a reader from wondering.
