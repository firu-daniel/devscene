### Task 1 — Refuse a node session only on `init` tools its agent does not declare, and report the withheld ones as `withheld=`

**Goal:** Make `pnl_reap` refuse a node session for its tools only when the session's `system`/`init` event carries a tool the agent's `tools:` line does not name. A declared tool the session lacks is no longer refused. It is reported on a new `withheld=` output line, so the driver can log it.

**Where this layer stops.** This task changes the decision and adds one key to `pnl_reap`'s output. It writes no `[plan-drive]` line and reads no `withheld=` value: `cli/templates/scripts/lib/planning-driver-lib.sh` → `pd_reap_one` reads the key and logs it, and that is **Task 2's**. The decision of record in `docs/flow-graph-walker.md` is **Task 3's**. Do not edit either file here.

### Targets

- `cli/templates/scripts/lib/planning-node-lib.sh` — `PNL_REAP_JQ`, `pnl_reap` and its doc comment, and the module header (the rule paragraph and the `REPRO` `reap` line).
- `cli/test/planning-node-lib.test.mjs` — the suite header and the `rule 2` case, plus one assertion in the `pnl_launch … pnl_reap copies its stream once` case.

**The contract this task produces** (Task 2 restates and consumes it):

- `pnl_reap` prints one new line, **`withheld=<names>`**, placed **after `denials=` and before `reason=`**, so `reason=` stays the last line. `<names>` is the agent's declared tools that the `init` event lacks, **`mcp__` tools excluded** (the same exclusion `$missing` already applies), in the order of the agent's `tools:` line, joined with `", "` (comma and space), e.g. `withheld=Glob, Grep`. The value is empty when nothing is withheld, and empty when there is no `init` event.
- `withheld=` is printed for every `kind`, `returned`, `undelivered` and `error` alike, because a session can withhold tools and then end any way.
- The tools refusal fires **only when `$extra` is non-empty**. It stays `kind: "error"`, `class: "agent"`, at the same position in the fixed order (after the no-`init` rule, before the no-`result` rule). Its reason literal becomes:
  `the init event grants tools the agent does not declare: [<extra joined ", ">]`
  e.g. `the init event grants tools the agent does not declare: [Edit]`. The old literal `the agent tools do not match its init event: missing […], extra […]` is retired. Its only other quoters are this task's test file and the `REPRO` comment, both edited here.

**Work:**

- [ ] `PNL_REAP_JQ`: keep the `$missing` and `$extra` bindings exactly as computed today. Add `withheld: ""` to the base object `$m`. In the `else` branch that follows the `init`-type test, rebind `$m` with `withheld: ($missing | join(", "))` before the decision chain, so every later outcome carries it. Change the condition `($missing | length) > 0 or ($extra | length) > 0` to `($extra | length) > 0`, and change the reason to the literal above. Stay inside jq 1.5: no regex, and every `if` keeps its `else`.
- [ ] `pnl_reap`: add `"withheld=" + (.withheld | oneline)` to the final `jq -r` print list, between `denials=` and `reason=`. Update the doc comment above `pnl_reap`, which enumerates the printed keys, so it names `withheld=` and says when it is empty.
- [ ] Module header. State the tools rule beside the class sentence in the rule paragraph (*"Every `error` carries its class …"*): a session is refused when its `init` tools carry one the agent does not declare, and a declared tool the session lacks is reported on `withheld=` and never refused, because a missing tool cannot widen what the session does. Then fix the `REPRO` `reap` line. With `init` tools `[]` and no `result` event it now yields `kind=undelivered`, with `withheld=` naming the reviewer's non-MCP tools and `reason=no result event`. Write it in the same `-> …` shape the other `REPRO` lines use.
- [ ] `cli/test/planning-node-lib.test.mjs`, case `rule 2`. Rename it to state the new rule, for example *"rule 2: init tools the agent does not declare are error; declared tools the init lacks are withheld, not refused"*, and assert, writing every literal in the test:
  - `init(['Read', 'Bash'])` for `task-plan-reviewer` (`Read, Grep, Bash, mcp__docs__search_docs`) gives `kind=returned`, `class=` empty and `withheld=Grep`.
  - `init([...REVIEWER_TOOLS, 'Edit'])` gives `kind=error`, `class=agent`, `reason=the init event grants tools the agent does not declare: [Edit]` and `withheld=` empty.
  - `init(['Read', 'Bash', 'Edit'])` gives `kind=error`, `class=agent`, a reason naming `[Edit]` only, and `withheld=Grep`. This is the story index's first top risk: losing a declared tool must not mask an extra one.
  - The existing `withMcp` assertion stays, and the declared `mcp__docs__search_docs` absent from `init` (`REVIEWER_TOOLS`) never appears in `withheld=`.
- [ ] In the same file: add `assert.equal(r.keys.withheld, '')` to the `pnl_launch … pnl_reap copies its stream once` case, and `assert.equal(r.keys.withheld, '')` to the `rule 1` case (no `init` event). Reword the suite header's fixed-order list (*"no `init` event, a tools mismatch, …"*) to *"no `init` event, an `init` tool the agent does not declare, …"*, and add one sentence saying that `withheld=` reports declared tools the `init` event lacks and refuses nothing.

**Verification:**

- `cli/test/planning-node-lib.test.mjs` passes. It is this task's own test file, and its `rule 2` case shows a lacking-only session returned with `withheld=` set, an extra-only session refused, and the mixed session refused on its extra tool alone.
- `bash scripts/typecheck.sh` exits 0.
- `git grep -n 'do not match its init event'` returns no hit under `cli/`. The retired literal survives nowhere this task owns.
- Read `PNL_REAP_JQ` once more against the header's `BASH 3.2 AND JQ 1.5 ARE THE FLOORS` line: no `test(`/`match(`/`capture(`, and every `if` carries an `else`.
