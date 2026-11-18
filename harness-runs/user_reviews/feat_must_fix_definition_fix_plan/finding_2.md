### 2. Nothing keeps the `### Must Fix triggers` tables aligned with the checks their agents grade

**File:** `cli/test/must-fix-triggers-corpus.test.mjs` (new, the whole file); `devscene.config.json` (`treeGuards`) — "\"test\": \"test/agent-return-schemas.test.mjs\""

**Depends on:** Finding 1, whose row this test names.

Eight agents under `plugin/agents/` state their Must Fix triggers twice: the checklist grades a check, and `### Must Fix triggers` gives it a class. No test under `cli/test/` reads those tables, and this branch has already drifted three times. Finding 1 is a fourth case, still live. This is a Should Fix: the missing guard produces no wrong result by itself, and the user asked for it explicitly.

## Fix

- [ ] `cli` layer: create `cli/test/must-fix-triggers-corpus.test.mjs` as specified below.
- [ ] `general` layer: add the two `treeGuards` entries below to `devscene.config.json`.

The test reads a tree of files, so it registers itself in this same unit (`plugin/instructions/unit_loop_core.md` → `## The test-run rule` point 8). Add these after the last existing `treeGuards` entry:

```json
{
  "test": "test/must-fix-triggers-corpus.test.mjs",
  "covers": "plugin/agents/*.md"
},
{
  "test": "test/must-fix-triggers-corpus.test.mjs",
  "covers": "plugin/instructions/finding_grades.md"
}
```

## The test file

Use `node:test`, `node:assert/strict` and `WORKSPACE_ROOT` from `./helpers/fixture.mjs`, as `cli/test/untrusted-input-corpus.test.mjs` does.

**Header.** Open with the rule: every check an agent definition grades Must Fix is covered by a row of that agent's `### Must Fix triggers` table, and every row names a real class and real sections. State what is deliberately not covered:

- A trigger graded outside the agent's own file. `plugin/instructions/untrusted_input.md` → `## Where a report goes` is one such source.
- A row whose check carries no grading phrase in the file, so deleting that row is not detected.
- Whether a row's class is the right one.
- A second ungraded check added to a line that is already covered, because matching is per line.

**One pure function.** Write `audit(name, text, classes)`, returning an array of violation strings, each `<name>: <kind>: <detail>`. The corpus test and every drift test below call it, so the drift tests edit strings in memory and never touch a file.

**Parsing.** Walk the lines, skipping fenced blocks (a fence may be indented). Track:

- the current `###` heading, cleared at each `##`;
- the current group label: the bold text opening the latest line that starts with `**`, cleared at each heading;
- the table: lines starting with `|` under `### Must Fix triggers`, minus the header and separator. A row's first and last cells, split on ` | `, are its `cell` and its `class`.

**Section references in a `cell`:**

- Heading references: `` /(`+)\s*(### .+?)\s*\1/g ``. Remove them from the cell before the next step.
- Bold references: `/\*\*(.+?)\*\*/g`.
- A cell opening `Check <N>:` references the bold text `**<N>. `.

A row is a **group row** when its cell starts with `Every ` or `Each `, or when nothing is left after removing its references, the word `Checks`, `–` and `and`. Any other row is an own row, even if it cites a section in passing.

**Graded lines.** Scan every line outside fences, outside the table and outside a `### Return fields` section. Do not exclude any other section: `branch-reviewer` grades a check inside `## Output contract` and `task-plan-reviewer` grades one inside `## Read first`. Skip a line containing a `NOT_A_GRADE` string. Remove inline code spans, then test:

```js
const GRADE =
  /\*\*Must Fix\b|\b(?:is a|is its own|are) Must Fix\b|→ Must Fix\b|— Must Fix\b|: Must Fix\b|\(Must Fix(?:[);]| when)/;
```

**Violations, by kind:**

| Kind | When |
|---|---|
| `bad-class` | A row's `class` is not one of the four. Parse the four from the `| **<class>** |` rows of `plugin/instructions/finding_grades.md` → `### 1. It belongs to one of four classes`, and assert there are exactly four. |
| `stale-reference` | A heading reference matches no heading that equals it or starts with `<reference> (`, or a bold reference has no `**<reference>` in a line outside the table. |
| `stale-own-row` | An `OWN_ROWS` entry's `check` is on no graded line, or its `row` is no row's `cell`. |
| `stale-exemption` | A `NOT_A_GRADE` entry for this agent occurs on no line. |
| `no-table` | The text contains `finding_grades.md`, has no table, and has at least one graded line. |
| `uncovered` | A graded line is not covered, by the rule below. Quote the line. |

**A graded line is covered when any of these holds:**

1. It contains the `check` of an `OWN_ROWS` entry for this agent.
2. It is a `###` heading, and any row, group or own, references that heading.
3. A group row references its section: a heading reference equal to the enclosing heading or followed there by ` (`, or a bold reference equal to the line's own opening bold label or the current group label, or a prefix of either followed by a space. Strip a trailing `.` or `:` from a label before comparing. A leading `- ` does not stop a label being the line's own.

**The two lists.** These are the complete lists for the corpus once Finding 1 has landed. `'*'` applies to every agent, and is checked for staleness only in the corpus test.

```js
const NOT_A_GRADE = [
  ['*', 'If there are Must Fix issues'],
  ['*', 'Only **Must Fix**'],
  ['architecture-reviewer', '**Only architecture violations,'],
  ['business-parity-reviewer', '**Only parity violations,'],
  ['review-plan-reviewer', 'Findings are grouped into **Must Fix**'],
  ['skeptic-reviewer', 'Prefer fewer, higher-confidence **Must Fix**'],
  ['user-review-fix-plan-writer', '**Valid (Must Fix)**'],
];

const LAUNDERING = 'A laundering-check failure';
const LAUNDERING_LINE = 'A plan or task file carrying an instruction that fails';
const PLAN_TEST_RUN = 'A plan\'s forbidden test run (**No plan asks for a test run**)';

const OWN_ROWS = {
  'architecture-reviewer': [
    ['A quoted absolute checkout-root or home-directory path', 'A quoted machine path in sub-case (c)'],
    ['**No plan asks for a test run.**', PLAN_TEST_RUN],
    [LAUNDERING_LINE, LAUNDERING],
    ['**Verify justifications', 'A claimed exception its cited source does not license (**Verify justifications**)'],
  ],
  'business-parity-reviewer': [
    ['**Verify the exclusion basis', 'An exclusion basis that fails **Verify the exclusion basis**'],
    ['**No plan asks for a test run.**', PLAN_TEST_RUN],
    [LAUNDERING_LINE, LAUNDERING],
    ['**Leg 1 —', 'A failed leg of the **Obvious-reference-bug exception**'],
    ['**Leg 2 —', 'A failed leg of the **Obvious-reference-bug exception**'],
    ['**Either** leg fails', 'A failed leg of the **Obvious-reference-bug exception**'],
  ],
  'branch-reviewer': [
    ['**Cross-check business logic against', 'A `<reference_impl>` behaviour missing from the diff, or waived by a fabricated or miscited authorization (Pass 1 step 5), while `phases.parity` is `true`'],
    ['**Zero callers', 'A new exported symbol with zero callers (Pass 0 half (b))'],
    ['A required accompanying test missing or skipped (', 'A required accompanying test missing or skipped'],
    ['A tree-reading test the branch adds', 'A tree-reading test with no registration in the branch diff'],
    ['A file over the first size threshold', 'A file over the second size threshold'],
    ['An item in this section with no explicit grade', 'A `<state_dir>/lessons.md` entry'],
    ['**A divergence earns a call-out rather than a Must Fix', 'A `<reference_impl>` divergence failing either leg of the call-out two-leg test, while `phases.parity` is `true`'],
  ],
  'layer-reviewer': [
    ['a new unit of behaviour landing without the test', 'A required test missing, or a test off the stated idiom (**Testing**)'],
    ['a tree-reading test the unit adds', 'A tree-reading test with no registration (**Testing**)'],
    ['**Size**', 'A file over the second **Size** threshold'],
  ],
  'review-plan-reviewer': [
    ['one positioned after the findings sections', 'Index structure graded Must Fix under **Index (`review_path`)**'],
    ['a finding file that only restates the title', 'Per-finding structure: a finding file that only restates its title or omits its site anchor or fix, so an implementer cannot act on it'],
    ['A finding whose fix or sub-step asks for a test run', 'A forbidden test run'],
    ['**Index ↔ finding correspondence (Must Fix):**', 'A pointer or readiness entry with no finding file, an orphan finding file or a count mismatch (**Index ↔ finding correspondence**)'],
    ['A pointer with no matching file', 'A pointer or readiness entry with no finding file, an orphan finding file or a count mismatch (**Index ↔ finding correspondence**)'],
    ['An orphan detail file', 'A pointer or readiness entry with no finding file, an orphan finding file or a count mismatch (**Index ↔ finding correspondence**)'],
    ['The round suffix on the index name', 'The round-suffix match (**Index ↔ finding correspondence**)'],
  ],
  'skeptic-reviewer': [
    ['**never invoked from the path that should invoke it**', 'Check 1: new code unwired, dead or orphaned'],
    ['**Parity leg.**', 'Check 2: a runtime failure copied from the spec, or an invalid runtime address'],
    ['A fabricated citation (for example', 'Check 3: an authorization that does not hold'],
    ['Apply the two-leg test to every divergence', 'Check 4: a divergence failing either leg'],
    ['**Security gating:**', 'Check 5: a runtime fault or a client-only gate'],
  ],
  'task-plan-reviewer': [
    ['a plan that re-plans a ledger mistake', 'A repeated `<state_dir>/lessons.md` lesson'],
    ['**Cross-task interfaces are restated on both sides**', 'The cross-task-interface bullet of `### Per-task-file structure`'],
    ['**Tasks sequence bottom-up**', 'The **Tasks sequence bottom-up** bullet of `### Architecture`'],
    ['**Every unit the plan introduces carries its required accompanying set**', 'A required-set item missing (`### Architecture`, `### Completeness`)'],
    ['a missing requirement is a Must Fix', 'A task-prompt requirement missing'],
    ['**Each omitted item is its own Must Fix**', 'A required-set item missing (`### Architecture`, `### Completeness`)'],
    ['A client-only gate is a Must Fix', 'A client-only or missing server-side gate'],
    ['An unconsumed path is a Must Fix', 'An unconsumed unit'],
    ['a silent infrastructure assumption is a Must Fix', 'A silent infrastructure assumption'],
    ['The plan does not repeat a', 'A repeated `<state_dir>/lessons.md` lesson'],
    ['asks for a test run the rule forbids', 'A forbidden test run, in each form `### Completeness` lists'],
    [LAUNDERING_LINE, LAUNDERING],
  ],
  'ui-tests-plan-reviewer': [
    ['A behaviour the branch adds with no covering test', 'A coverage gap (`### Completeness`)'],
    [LAUNDERING_LINE, LAUNDERING],
  ],
};
```

If the first run reports a line these lists miss, read that line. Add an entry only when a row really covers it or it really grades nothing. Otherwise the report is real drift, so add the row to the agent's table only if this unit's layer owns that file; if not, return a blocker naming the line.

## The cases

1. **The corpus is clean.** Audit every `plugin/agents/*.md`; the violations array is empty. Every `'*'` `NOT_A_GRADE` string occurs in at least one agent.
2. **The check is not vacuous.** At least 8 agents have a table, each with at least one row.
3. **Drift is caught.** Each edit below is applied to the real text in memory, and `audit` must return a violation of the named kind:

| Agent | Edit | Kind |
|---|---|---|
| `branch-reviewer` | Delete the row `` | A tree-reading test with no registration in the branch diff | Broken contract | `` | `stale-own-row` |
| `ui-tests-plan-reviewer` | Delete the row `` | `### Capability/MCP correctness` | Wrong build | `` | `uncovered` |
| `task-plan-reviewer` | Insert `- A new probe check is a Must Fix.` after the heading `### Completeness (Must Fix)` | `uncovered` |
| `task-plan-reviewer` | Change the class of the row `A client-only or missing server-side gate` to `Wrong thing` | `bad-class` |
| `ui-tests-plan-reviewer` | Rename the heading `### Backend-name parity (Must Fix)` to `### Backend names (Must Fix)` | `stale-reference` |
| a synthetic `probe-agent` | Text citing `finding_grades.md`, with a `## Checks` section holding `- A skipped step is a Must Fix.` and no table | `no-table` |

4. **Prose does not count.** Each insertion into `review-plan-reviewer`'s text leaves `audit` with no violation:
   - `- probe — FAIL when there is a Must Fix.` under `### Return fields`;
   - the same line inside a fenced block;
   - `A stale hint is never a Must Fix.` under `## What to check`;
   - ``Write the `## Must Fix` section.`` under `## What to check`.

**Verification:** `cli/test/must-fix-triggers-corpus.test.mjs` passes, and each case in 3 fails if its edit's violation is not reported.
