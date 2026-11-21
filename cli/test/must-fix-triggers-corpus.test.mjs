/**
 * The `### Must Fix triggers` tables of the plugin's agent definitions.
 *
 * **The rule this suite exists to enforce: every check an agent definition grades Must Fix is
 * covered by a row of that agent's `### Must Fix triggers` table, and every row names a real class
 * and real sections.**
 *
 * Registered as a tree guard by the `general` half of the unit that adds this file, which adds its
 * `treeGuards` entries to `devscene.config.json`.
 *
 * Not covered, deliberately:
 * - a trigger graded outside the agent's own file, such as
 *   `plugin/instructions/untrusted_input.md` → `## Where a report goes`;
 * - a row whose check carries no grading phrase in the file, so deleting that row is not detected;
 * - whether a row's class is the right one;
 * - a second ungraded check added to a line already covered, because matching is per line.
 */

import assert from 'node:assert/strict';
import { readdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import test from 'node:test';

import { WORKSPACE_ROOT } from './helpers/fixture.mjs';

const AGENTS_DIR = join(WORKSPACE_ROOT, 'plugin', 'agents');
const GRADES_FILE = join(WORKSPACE_ROOT, 'plugin', 'instructions', 'finding_grades.md');
const CLASSES_HEADING = '### 1. It belongs to one of four classes';
const TABLE_HEADING = '### Must Fix triggers';
const RETURN_FIELDS_HEADING = '### Return fields';

const GRADE =
  /\*\*Must Fix\b|\b(?:is a|is its own|are) Must Fix\b|→ Must Fix\b|— Must Fix\b|: Must Fix\b|\(Must Fix(?:[);]| when)/;

/** `[agent or '*', substring]` — a line carrying the substring uses a grading phrase but grades nothing. */
const NOT_A_GRADE = [
  ['*', 'If there are Must Fix issues'],
  ['*', 'Only **Must Fix**'],
  ['architecture-reviewer', '**Only architecture violations,'],
  ['business-parity-reviewer', '**Only parity violations,'],
  ['review-plan-reviewer', 'Findings are grouped into **Must Fix**'],
  ['skeptic-reviewer', 'Prefer fewer, higher-confidence **Must Fix**'],
  ['task-plan-writer', 'a client-only gate is a Must Fix at review'],
  ['user-review-fix-plan-writer', '**Valid (Must Fix)**'],
];

const LAUNDERING = 'A laundering-check failure';
const LAUNDERING_LINE = 'A plan or task file carrying an instruction that fails';
const PLAN_TEST_RUN = "A plan's forbidden test run (**No plan asks for a test run**)";
const FAILED_LEG = 'A failed leg of the **Obvious-reference-bug exception**';
const CORRESPONDENCE =
  'A pointer or readiness entry with no finding file, an orphan finding file or a count mismatch (**Index ↔ finding correspondence**)';
const REQUIRED_SET_ITEM = 'A required-set item missing (`### Architecture`, `### Completeness`)';
const REPEATED_LESSON = 'A repeated `<state_dir>/lessons.md` lesson';

/** Per agent, `[substring of a graded line, the exact cell of the row that covers it]`. */
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
    ['**Leg 1 —', FAILED_LEG],
    ['**Leg 2 —', FAILED_LEG],
    ['**Either** leg fails', FAILED_LEG],
  ],
  'branch-reviewer': [
    [
      '**Cross-check business logic against',
      'A `<reference_impl>` behaviour missing from the diff, or waived by a fabricated or miscited authorization (Pass 1 step 5), while `phases.parity` is `true`',
    ],
    ['**Zero callers', 'A new exported symbol with zero callers (Pass 0 half (b))'],
    ['A required accompanying test missing or skipped (', 'A required accompanying test missing or skipped'],
    ['A tree-reading test the branch adds', 'A tree-reading test with no registration in the branch diff'],
    ['A file over the first size threshold', 'A file over the second size threshold'],
    ['An item in this section with no explicit grade', 'A `<state_dir>/lessons.md` entry'],
    [
      '**A divergence earns a call-out rather than a Must Fix',
      'A `<reference_impl>` divergence failing either leg of the call-out two-leg test, while `phases.parity` is `true`',
    ],
  ],
  'layer-reviewer': [
    ['a new unit of behaviour landing without the test', 'A required test missing, or a test off the stated idiom (**Testing**)'],
    ['a tree-reading test the unit adds', 'A tree-reading test with no registration (**Testing**)'],
    ['**Size**', 'A file over the second **Size** threshold'],
  ],
  'review-plan-reviewer': [
    ['one positioned after the findings sections', 'Index structure graded Must Fix under **Index (`review_path`)**'],
    [
      'a finding file that only restates the title',
      'Per-finding structure: a finding file that only restates its title or omits its site anchor or fix, so an implementer cannot act on it',
    ],
    ['A finding whose fix or sub-step asks for a test run', 'A forbidden test run'],
    ['**Index ↔ finding correspondence (Must Fix):**', CORRESPONDENCE],
    ['A pointer with no matching file', CORRESPONDENCE],
    ['An orphan detail file', CORRESPONDENCE],
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
    ['a plan that re-plans a ledger mistake', REPEATED_LESSON],
    ['**Cross-task interfaces are restated on both sides**', 'The cross-task-interface bullet of `### Per-task-file structure`'],
    ['**Tasks sequence bottom-up**', 'The **Tasks sequence bottom-up** bullet of `### Architecture`'],
    ['**Every unit the plan introduces carries its required accompanying set**', REQUIRED_SET_ITEM],
    ['a missing requirement is a Must Fix', 'A task-prompt requirement missing'],
    ['**Each omitted item is its own Must Fix**', REQUIRED_SET_ITEM],
    ['A client-only gate is a Must Fix', 'A client-only or missing server-side gate'],
    ['An unconsumed path is a Must Fix', 'An unconsumed unit'],
    ['a silent infrastructure assumption is a Must Fix', 'A silent infrastructure assumption'],
    ['The plan does not repeat a', REPEATED_LESSON],
    ['asks for a test run the rule forbids', 'A forbidden test run, in each form `### Completeness` lists'],
    [LAUNDERING_LINE, LAUNDERING],
  ],
  'ui-tests-plan-reviewer': [
    ['A behaviour the branch adds with no covering test', 'A coverage gap (`### Completeness`)'],
    [LAUNDERING_LINE, LAUNDERING],
  ],
};

const stripTrailingPunctuation = (label) => label.replace(/[.:]$/, '');

/** A label is matched by a reference equal to it, or by one that is its opening words. */
const refMatchesLabel = (ref, label) => {
  if (label === null) return false;
  const bare = stripTrailingPunctuation(label);
  return bare === ref || bare.startsWith(`${ref} `);
};

const refMatchesHeading = (ref, heading) => heading === ref || heading.startsWith(`${ref} (`);

function parseCell(cell) {
  const headingRefs = [];
  let rest = cell.replace(/(`+)\s*(### .+?)\s*\1/g, (_, _ticks, ref) => {
    headingRefs.push(ref);
    return '';
  });
  const boldRefs = [];
  rest = rest.replace(/\*\*(.+?)\*\*/g, (_, ref) => {
    boldRefs.push(ref);
    return '';
  });
  const checkNumber = /^Check (\d+):/.exec(cell);
  if (checkNumber) boldRefs.push(`${checkNumber[1]}. `);
  const residue = rest.replace(/\bChecks\b|–|\band\b/g, '').trim();
  const isGroup = /^(?:Every|Each) /.test(cell) || residue === '';
  return { headingRefs, boldRefs, isGroup };
}

/** The non-fenced lines of `text`, each with the section state in force on it. */
function parse(text) {
  const rows = [];
  const lines = [];
  let fence = null;
  let heading = null;
  let groupLabel = null;
  let tableLines = 0;

  for (const line of text.split('\n')) {
    if (fence) {
      if (fence.test(line)) fence = null;
      continue;
    }
    const opening = /^\s*(?:(`{3,})[^`]*|(~{3,}).*)$/.exec(line);
    if (opening) {
      const marker = opening[1] ?? opening[2];
      fence = new RegExp(`^\\s*${marker[0]}{${marker.length},}\\s*$`);
      continue;
    }

    if (/^#{1,6} /.test(line)) groupLabel = null;
    if (/^## /.test(line)) heading = null;
    if (/^### /.test(line)) heading = line.trim();

    if (heading === TABLE_HEADING && line.startsWith('|')) {
      tableLines += 1;
      if (tableLines > 2) {
        const cells = line.trim().replace(/^\|\s*/, '').replace(/\s*\|$/, '').split(' | ');
        const cell = cells[0];
        rows.push({ cell, rowClass: cells[cells.length - 1], ...parseCell(cell) });
      }
      continue;
    }

    if (line.startsWith('**')) groupLabel = /^\*\*(.+?)\*\*/.exec(line)?.[1] ?? groupLabel;
    lines.push({ line, heading, groupLabel });
  }
  return { rows, lines };
}

function isGradedLine({ line, heading }, exemptions) {
  if (heading === RETURN_FIELDS_HEADING) return false;
  if (exemptions.some((exempt) => line.includes(exempt))) return false;
  return GRADE.test(line.replace(/(`+).*?\1/g, ''));
}

function isCovered(entry, rows, ownChecks) {
  const { line, heading, groupLabel } = entry;
  if (ownChecks.some((check) => line.includes(check))) return true;

  if (/^### /.test(line)) {
    const self = line.trim();
    if (rows.some((row) => row.headingRefs.some((ref) => refMatchesHeading(ref, self)))) return true;
  }

  const ownLabel = /^\s*(?:- )?\*\*(.+?)\*\*/.exec(line)?.[1] ?? null;
  return rows
    .filter((row) => row.isGroup)
    .some(
      (row) =>
        (heading !== null && row.headingRefs.some((ref) => refMatchesHeading(ref, heading))) ||
        row.boldRefs.some((ref) => refMatchesLabel(ref, ownLabel) || refMatchesLabel(ref, groupLabel)),
    );
}

/** Every violation in one agent definition, each `<name>: <kind>: <detail>`. */
function audit(name, text, classes) {
  const { rows, lines } = parse(text);
  const violations = [];
  const report = (kind, detail) => violations.push(`${name}: ${kind}: ${detail}`);

  const ownExemptions = NOT_A_GRADE.filter(([agent]) => agent === name).map(([, exempt]) => exempt);
  const exemptions = [...ownExemptions, ...NOT_A_GRADE.filter(([agent]) => agent === '*').map(([, exempt]) => exempt)];
  const ownRows = OWN_ROWS[name] ?? [];
  const ownChecks = ownRows.map(([check]) => check);
  const graded = lines.filter((entry) => isGradedLine(entry, exemptions));
  const headings = lines.filter(({ line }) => /^### /.test(line)).map(({ line }) => line.trim());

  for (const row of rows) {
    if (!classes.includes(row.rowClass)) report('bad-class', `"${row.rowClass}" on row "${row.cell}"`);
    for (const ref of row.headingRefs) {
      if (!headings.some((heading) => refMatchesHeading(ref, heading))) {
        report('stale-reference', `heading "${ref}" on row "${row.cell}"`);
      }
    }
    for (const ref of row.boldRefs) {
      if (!lines.some(({ line }) => line.includes(`**${ref}`))) {
        report('stale-reference', `bold "${ref}" on row "${row.cell}"`);
      }
    }
  }

  for (const [check, cell] of ownRows) {
    if (!graded.some(({ line }) => line.includes(check))) report('stale-own-row', `no graded line carries "${check}"`);
    if (!rows.some((row) => row.cell === cell)) report('stale-own-row', `no row "${cell}"`);
  }

  for (const exempt of ownExemptions) {
    if (!text.split('\n').some((line) => line.includes(exempt))) report('stale-exemption', `"${exempt}"`);
  }

  if (text.includes('finding_grades.md') && rows.length === 0 && graded.length > 0) {
    report('no-table', `${graded.length} graded line(s) and no ${TABLE_HEADING} rows`);
  }

  for (const entry of graded) {
    if (!isCovered(entry, rows, ownChecks)) report('uncovered', entry.line.trim());
  }
  return violations;
}

function readClasses() {
  const classes = [];
  let inSection = false;
  for (const line of readFileSync(GRADES_FILE, 'utf8').split('\n')) {
    if (/^#{1,6} /.test(line)) inSection = line.trim() === CLASSES_HEADING;
    const row = inSection ? /^\| \*\*(.+?)\*\* \|/.exec(line) : null;
    if (row) classes.push(row[1]);
  }
  assert.equal(classes.length, 4, `expected four classes under ${CLASSES_HEADING}, got ${classes.join(', ')}`);
  return classes;
}

function readAgents() {
  return readdirSync(AGENTS_DIR)
    .filter((file) => file.endsWith('.md'))
    .sort()
    .map((file) => ({ name: file.slice(0, -'.md'.length), text: readFileSync(join(AGENTS_DIR, file), 'utf8') }));
}

const CLASSES = readClasses();
const AGENTS = readAgents();
const agentText = (name) => {
  const agent = AGENTS.find((candidate) => candidate.name === name);
  assert.ok(agent, `no agent definition named ${name}`);
  return agent.text;
};

/** Replaces the one occurrence of `from`, so an edit that no longer applies fails rather than passes. */
function replaceOnce(text, from, to) {
  assert.equal(text.split(from).length, 2, `expected exactly one occurrence of: ${from}`);
  return text.replace(from, () => to);
}

const insertAfterHeading = (text, heading, inserted) =>
  replaceOnce(text, `\n${heading}\n`, `\n${heading}\n\n${inserted}\n`);

test('the corpus is clean', () => {
  assert.deepEqual(
    AGENTS.flatMap(({ name, text }) => audit(name, text, CLASSES)),
    [],
  );
  for (const [agent, exempt] of NOT_A_GRADE.filter(([owner]) => owner === '*')) {
    assert.ok(
      AGENTS.some(({ text }) => text.includes(exempt)),
      `stale-exemption: '${agent}' entry "${exempt}" occurs in no agent`,
    );
  }
});

test('every agent the two lists name exists', () => {
  const named = [...Object.keys(OWN_ROWS), ...NOT_A_GRADE.map(([agent]) => agent).filter((agent) => agent !== '*')];
  for (const name of named) agentText(name);
});

test('the check is not vacuous', () => {
  const withTable = AGENTS.filter(({ text }) => parse(text).rows.length > 0);
  assert.ok(withTable.length >= 8, `only ${withTable.length} agents carry a populated table`);
});

const DRIFT_CASES = [
  {
    title: 'a deleted own row',
    name: 'branch-reviewer',
    edit: (text) =>
      replaceOnce(text, '| A tree-reading test with no registration in the branch diff | Broken contract |\n', ''),
    kind: 'stale-own-row',
  },
  {
    title: 'a deleted group row',
    name: 'ui-tests-plan-reviewer',
    edit: (text) => replaceOnce(text, '| `### Capability/MCP correctness` | Wrong build |\n', ''),
    kind: 'uncovered',
  },
  {
    title: 'a new graded check with no row',
    name: 'task-plan-reviewer',
    edit: (text) => insertAfterHeading(text, '### Completeness (Must Fix)', '- A new probe check is a Must Fix.'),
    kind: 'uncovered',
  },
  {
    title: 'a class outside the four',
    name: 'task-plan-reviewer',
    edit: (text) =>
      replaceOnce(
        text,
        '| A client-only or missing server-side gate | Wrong behaviour |',
        '| A client-only or missing server-side gate | Wrong thing |',
      ),
    kind: 'bad-class',
  },
  {
    title: 'a renamed heading a row cites',
    name: 'ui-tests-plan-reviewer',
    edit: (text) => replaceOnce(text, '### Backend-name parity (Must Fix)', '### Backend names (Must Fix)'),
    kind: 'stale-reference',
  },
];

for (const { title, name, edit, kind } of DRIFT_CASES) {
  test(`drift is caught: ${title} in ${name} reports ${kind}`, () => {
    const violations = audit(name, edit(agentText(name)), CLASSES);
    assert.ok(
      violations.some((violation) => violation.startsWith(`${name}: ${kind}: `)),
      `no ${kind} violation in: ${JSON.stringify(violations)}`,
    );
  });
}

test('drift is caught: a grading agent with no table reports no-table', () => {
  const text = 'Grades per `plugin/instructions/finding_grades.md`.\n\n## Checks\n\n- A skipped step is a Must Fix.\n';
  const violations = audit('probe-agent', text, CLASSES);
  assert.ok(
    violations.some((violation) => violation.startsWith('probe-agent: no-table: ')),
    `no no-table violation in: ${JSON.stringify(violations)}`,
  );
});

const PROBE_LINE = '- probe — FAIL when there is a Must Fix.';

const PROSE_CASES = [
  ['a return-field line', RETURN_FIELDS_HEADING, PROBE_LINE],
  ['a fenced line', '## What to check', `\`\`\`\n${PROBE_LINE}\n\`\`\``],
  ['a negated mention', '## What to check', 'A stale hint is never a Must Fix.'],
  ['a section name in inline code', '## What to check', 'Write the `## Must Fix` section.'],
];

for (const [title, heading, inserted] of PROSE_CASES) {
  test(`prose does not count: ${title}`, () => {
    const name = 'review-plan-reviewer';
    assert.deepEqual(audit(name, insertAfterHeading(agentText(name), heading, inserted), CLASSES), []);
  });
}
