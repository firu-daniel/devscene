### 1. The driver parks a round gate's `PASS` with no `findings_file` at once, where the contract and the orchestrator path re-dispatch it up to three times

**File:** `cli/templates/scripts/lib/planning-node-lib.sh` (`PNL_REAP_JQ`) — `then $r + { kind: "error", class: "agent", reason: ($d.outcome + " carries no findings_file") }`

**The problem.** This branch states one bound for a return that fails its check, on both drivers:

- `plugin/instructions/agent_return_contract.md` → `## A return that fails the check`: a failing return is re-dispatched, the third consecutive failure takes the `error` route, and *"The driver's bound is the same three attempts, taken as its infrastructure class."*
- `docs/structured-agent-returns.md` → `### A return that fails its check` → **Reason**: *"one bound of three on both paths treats it alike"*. `docs/flow-graph-walker.md` → `### The return schema, the graph's outcomes, and the \`init\` check` → **Reason** says the same.
- The story index's `## Context` decision 6 (*"Same bound on both paths, never a guess"*) and its second `Top risks:` entry (*"the driver and the orchestrator diverging on what a valid return is, or on what a failed one does"*).

`architecture-reviewer` and `business-parity-reviewer` both declare `findings_file` **optional** on their `PASS` variant. It is absent in implemented-solution mode and, for the architecture reviewer, in sub-case (c). Both are round gates of the planning graph. So a `PASS` from either with no `findings_file` passes its own `## Return schema`.

The two drivers then handle that one return differently:

- **Orchestrator path.** `plugin/instructions/task_plan_writing_instructions_core.md` → `## The walker` reads `` `architecture-reviewer.findings_file` `` / `` `business-parity-reviewer.findings_file` `` on an `outcome` of `PASS` from a plan gate. So step 3 of `## Reading a return` ("every field that section reads for that outcome is present and not empty") fails. The return is not a return, the dispatch goes out again, and only the third consecutive failure passes `--outcome error`.
- **Driver path.** `PNL_REAP_JQ` reaches its `($r.findings | blank) and (… $d.outcome == "PASS" and any($gates[]; . == $node))` branch and returns `class: "agent"`. `pd_reap_one` retries only `class=infra`, so the node is recorded `error` on its first attempt and planning parks once its siblings finish. `cli/test/planning-driver-walk.test.mjs` pins this behaviour (*"an architecture_review PASS with no findings_file is an agent error: held once while its siblings finish, then parks"*). So does the header of `cli/test/helpers/planning-driver.mjs` (*"is an agent `error` — recorded and parked at once, never retried"*).

So an unattended script-driven run parks on a reply that the orchestrated run, and the contract both paths share, would re-dispatch. The same branch also catches a `FAIL` whose `findings_file` is blank. The fix below keeps that check and changes only the class it is recorded under.

**Fix.**

1. In `cli/templates/scripts/lib/planning-node-lib.sh` → `PNL_REAP_JQ`, make the missing-findings branch an infrastructure error that records nothing, like the other malformed-return branches beside it. Replace

   ```jq
   | if ($r.findings | blank) and ($d.outcome == "FAIL" or ($d.outcome == "PASS" and any($gates[]; . == $node)))
     then $r + { kind: "error", class: "agent", reason: ($d.outcome + " carries no findings_file") }
     else $r + { kind: "returned", outcome: $d.outcome, reason: "" } end
   ```

   with

   ```jq
   | if ($r.findings | blank) and ($d.outcome == "FAIL" or ($d.outcome == "PASS" and any($gates[]; . == $node)))
     then $m + { kind: "error", class: "infra", reason: ($d.outcome + " carries no findings_file") }
     else $r + { kind: "returned", outcome: $d.outcome, reason: "" } end
   ```

   Use `$m`, not `$r`: a return that fails the check is not a return, so `return_file=` and `object_file=` stay empty, as they do for a schema failure.

2. In the same file's header, change the sentence that lists the `infra` class. It now reads *"and a result whose return block is missing, not one JSON object or fails the schema — infrastructure because …"*. Make it *"a result whose return block is missing, not one JSON object or fails the schema, and a `FAIL` — or a round gate's `PASS` — that carries no non-blank `findings_file` — infrastructure because …"*, and leave the rest of the sentence as it is.

3. In `cli/test/planning-node-lib.test.mjs`, find the test titled `rule 7: FAIL anywhere, or PASS at a round gate, without a non-blank findings_file is error, agent`. Change the end of its title to `is error, infra`. Change both `assert.equal(….keys.class, 'agent')` lines in it to `'infra'`. After the `pass` reason assertion, add `assert.equal(pass.keys.object_file, '');`.

4. In `cli/test/planning-driver-walk.test.mjs`, find the test titled `an architecture_review PASS with no findings_file is an agent error: held once while its siblings finish, then parks`. Rename it to `an architecture_review PASS with no findings_file on all three attempts is held as error and parks`. Give `heldCase` three entries instead of one, as the neighbouring `a return failing its schema on all three attempts …` case does:

   ```js
   const noFile = { outcome: 'PASS', findings: 'FAIL' };
   await heldCase(t, 'architecture-reviewer', [noFile, noFile, noFile], 'architecture_review error', 'PASS carries no findings_file');
   ```

5. In `cli/test/helpers/planning-driver.mjs`, find the header paragraph that opens *"`findings`, on a gate, is the verdict …"*. Replace its last sentence, from *"a mismatched `PASS` at `architecture_review` or `business_parity_review` …"* to *"… never retried."*, with: *"a mismatched `PASS` at `architecture_review` or `business_parity_review` (whose `PASS` leaves it optional) passes the schema and is caught by the round-gate `findings_file` check instead — also an infrastructure `error`, retried up to `PD_MAX_ATTEMPTS`."*

6. In `docs/structured-agent-returns.md` → `### A return that fails its check` → **Decision**, change *"a return with no block, a block that is not one JSON object, or an object that fails its schema is the existing infrastructure class"* to *"a return with no block, a block that is not one JSON object, an object that fails its schema, or a `FAIL` or round gate's `PASS` carrying no non-blank `findings_file` is the existing infrastructure class"*.

7. In `docs/watcher.md` → **What parks or pauses the driver, and what it retries.**, change the item *"a return that carries no return block or fails its agent's `## Return schema`"* in the infrastructure list to *"a return that carries no return block, fails its agent's `## Return schema`, or names no `findings_file` where its gate's outcome needs one"*.

**Verification:** run the two test files this fix edits, each as its own plain foreground command from the repository root:

```
npm test --workspace cli -- test/planning-node-lib.test.mjs
npm test --workspace cli -- test/planning-driver-walk.test.mjs
```

Also run the tree guards the unit loop selects for the changed paths. The full suite runs in the Run gates round, not here.
