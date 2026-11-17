### Task 2 — Give the two mobile `qa-tester` stubs a `blocker`-only schema and an `## Output contract`, and retire the semi-autonomous commands' "1-3 line contract"

**Goal:** `qa-tester-mobile-maestro` and `qa-tester-mobile-mcp` return, on every dispatch, the object `qa-tester`'s `blocker` variant declares, and nothing else. Each gains `plugin/schemas/<agent>.return.json` — the `blocker` variant of `plugin/schemas/qa-tester.return.json` alone, with the same field name — and the `## Output contract` the static check requires, carrying the canonical return-block sentence and its `### Return fields`. Their `tools:` allowlist stays `Read` alone. `plugin/agents/README.txt`'s description of what the three variants return moves onto the new form. The two semi-autonomous implement commands stop telling their orchestrator to read a *"1-3 line contract"* from every agent.

**Depends on:** Task 1, which declares `qa-tester`'s four outcomes and the field this task's schemas subset:

- an `outcome` of `blocker` — nothing in the run can proceed — with `blocker` (string, non-empty), the one-line reason;
- and `PASS`, `FAIL` (`findings_file`, `must_fix_count`) and `blocked` (`blocked_tests`), which a stub never returns.

Task 1 keeps the heading `### 4. The run cannot proceed` of `qa-tester.md` → `## Output contract` byte-identical, so the stubs' pointer at it still resolves. It moves every caller onto the `blocker` route — halt, reporting `` `qa-tester.blocker` `` — so this task changes no caller. No instruction file dispatches either stub by name: flows dispatch `qa-tester` (`plugin/agents/README.txt`, the interactive-test paragraph). This task shares no file with Task 1.

### Targets

- `plugin/schemas/qa-tester-mobile-maestro.return.json` (new).
- `plugin/schemas/qa-tester-mobile-mcp.return.json` (new).
- `plugin/agents/qa-tester-mobile-maestro.md` — the phase-gate, driver-gate and not-implemented paragraphs, `## What it must never do`'s unreachable-target bullet, `## Operating contract — inherited by pointer`'s first paragraph, and a new `## Output contract` at the end of the file.
- `plugin/agents/qa-tester-mobile-mcp.md` — the same sentences, plus `## Tool closure — why the allowlist is `Read` only today`'s *"every dispatch stops at the not-implemented `error:` above"*, and a new `## Output contract` at the end of the file.
- `plugin/agents/README.txt` — in the interactive-test paragraph, *"returns its blocked `error:` line naming the configured driver"* and *"each returns the same blocked `error:` on every dispatch"*; in the report-don't-substitute paragraph, *"through its own `error:` / blocker return"*. **No other line of this file.**
- `plugin/commands/branch-implement-plan-semi-autonomous.md` — the orchestrator paragraph's *"you do not review specialist output beyond reading the 1-3 line contract each agent returns"*. **No other sentence of this file.**
- `plugin/commands/branch-implement-user-review-semi-autonomous.md` — the same clause of its orchestrator paragraph. **No other sentence of this file.**

**Work:**

- [ ] **The two schemas.** Write each in the closed dialect of `docs/structured-agent-returns.md` → `### The return schema`: `$schema` `http://json-schema.org/draft-07/schema#`, `title` `<agent> return`, `description` (naming it the `blocker` subset of `qa-tester`'s return), `type: "object"`, and a `oneOf` of one variant — `outcome` `{ "const": "blocker" }` and `blocker` `{ "type": "string", "minLength": 1 }`, both required, `additionalProperties: false`. Copy the `blocker` property's `description` from `plugin/schemas/qa-tester.return.json`. No other keyword.
- [ ] **`plugin/agents/qa-tester-mobile-maestro.md`.**
  - The phase gate's *"return the `error:` line with the disabled phase as its one-line reason"* becomes *"return an `outcome` of `blocker` whose `blocker` names the disabled phase"*.
  - The driver gate's *"return the `error:` line naming the configured driver …"* becomes *"return an `outcome` of `blocker` naming the configured driver …"*; keep the two variant pointers.
  - The not-implemented paragraph's *"return the single-line run-level `error:` shape of `${CLAUDE_PLUGIN_ROOT}/agents/qa-tester.md` → `## Output contract` → "4. The run cannot proceed"; for its own driver the line is exactly:"* becomes *"return an `outcome` of `blocker`, the shape of `${CLAUDE_PLUGIN_ROOT}/agents/qa-tester.md` → `## Output contract` → "4. The run cannot proceed"; for its own driver the `blocker` is exactly:"*. The fenced sentence under it drops its leading `error: ` and is otherwise byte-identical: `qa.driver is mobile-maestro; the mobile-maestro variant of the interactive-test agent is declared but not implemented in this release — no test was executed`.
  - *"an unreachable target is an `error:`"* becomes *"is a `blocker`"*.
  - In `## Operating contract — inherited by pointer`, *"the **four return shapes** the caller parses word for word"* becomes *"the **four outcomes** its `## Output contract` declares"*.
  - Add `## Output contract` as the file's last section: the canonical sentence, verbatim from `docs/structured-agent-returns.md` → `### The return block`, then `### Return fields` with two bullets — `outcome` — always `blocker`; `blocker` — the one-line reason: the disabled phase, the configured driver and the variant that implements it, or the not-implemented sentence above. Add no other words.
- [ ] **`plugin/agents/qa-tester-mobile-mcp.md`.** The same five rewrites and the same `## Output contract`, with `mobile-mcp` in the fenced sentence: `qa.driver is mobile-mcp; the mobile-mcp variant of the interactive-test agent is declared but not implemented in this release — no test was executed`. In `## Tool closure — why the allowlist is `Read` only today`, *"every dispatch stops at the not-implemented `error:` above"* becomes *"every dispatch stops at the not-implemented `blocker` above"*. Leave `tools: Read` in both files' frontmatter untouched.
- [ ] **`plugin/agents/README.txt`.**
  - *"returns its blocked `error:` line naming the configured driver"* becomes *"returns a `blocker` outcome naming the configured driver"*.
  - *"each returns the same blocked `error:` on every dispatch rather than running a test"* becomes *"each returns that same `blocker` outcome on every dispatch rather than running a test"*.
  - *"through its own `error:` / blocker return, naming the path and the refusal"* becomes *"through its return object — a `blocker` outcome, or the outcome its schema names for that case — naming the path and the refusal"*. After Task 1 no agent here returns an `error:` line.
  - Keep every other line, and keep the file's line wrapping style.
- [ ] **The two semi-autonomous implement commands.** In each orchestrator paragraph, *"beyond reading the 1-3 line contract each agent returns"* becomes *"beyond reading the return object each agent ends in, as the instruction section that dispatches it states"*. Keep every other word of the paragraph, including the user-review command's dev-server parenthesis. The rewrite names no agent and no field, so it holds at the end of every task: after Task 1 `qa-tester` and the reviewers end in a return object, and the docs pair — which neither command dispatches directly — move in Tasks 3 and 4, read as their own dispatching sections state.

**Verification:**

- `jq -e . plugin/schemas/qa-tester-mobile-maestro.return.json` and the same for `qa-tester-mobile-mcp.return.json` exit 0; each declares exactly one variant, `outcome` const `blocker`, and its property set `outcome`, `blocker` is a subset of `plugin/schemas/qa-tester.return.json`'s `blocker` variant, with the same `type` and `minLength`.
- `grep -nE 'error:' plugin/agents/qa-tester-mobile-maestro.md plugin/agents/qa-tester-mobile-mcp.md plugin/agents/README.txt` has no hit.
- `grep -n '^tools:' plugin/agents/qa-tester-mobile-maestro.md plugin/agents/qa-tester-mobile-mcp.md` prints `tools: Read` for each.
- Each stub's `## Output contract` carries the canonical sentence byte-for-byte as `docs/structured-agent-returns.md` → `### The return block` fixes it, and a `### Return fields` with exactly the bullets `outcome` and `blocker`.
- `grep -rnE '1-3 line|line contract' plugin/commands/` has no hit, and `git diff -- plugin/commands/` touches only the orchestrator paragraph of each of the two command files.
- The not-implemented sentence in each stub differs from its pre-task fenced line only by the dropped `error: ` prefix (`git diff` on each file).
