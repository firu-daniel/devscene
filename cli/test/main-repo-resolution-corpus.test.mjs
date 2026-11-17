/**
 * The `<MAIN_REPO>` resolution clause across the plugin corpus.
 *
 * **The rule this suite exists to enforce: the `<MAIN_REPO>` resolution clause is wire text carried
 * byte-identical at every plugin site that resolves `<MAIN_REPO>`, and its single home's roster
 * (`plugin/instructions/main_repo_resolution.md` → `## Who may cite this`) names exactly those
 * sites.** The expected carrier set is that roster's `${CLAUDE_PLUGIN_ROOT}/` entries (`ROSTER`),
 * each carrying the clause once unless `CLAUSE_COUNT_OVERRIDES` says otherwise, and every entry must
 * name an existing file; so a plugin change moves a carrier and its roster entry together, in one
 * unit, with no edit here. Every roster entry not in `EXEMPT` is an autonomous binder and carries the
 * byte-identical `<MAIN_REPO>` `## Resolved values` row (`MAIN_REPO_ROW`); every `EXEMPT` entry
 * carries its reason for needing none;
 * every file with a `<MAIN_REPO>` table row carries the literal-spelling sentence, except
 * `plugin/instructions/main_repo_resolution.md`; and no plugin file spells the push path as `<scripts_dir>/push-branch.sh` under any prefix but
 * `<MAIN_REPO>/`, passes it a `$` argument, or resolves `<MAIN_REPO>` through "watcher-supplied" or
 * a pipeline. A mention of the bare name `push-branch.sh` with no `<scripts_dir>/` in front is not
 * policed: wrapper-property and inventory sentences ("`push-branch.sh` is non-fatal") use that name
 * legitimately.
 *
 * Registered as a tree guard by Task 11 of `fix_clone_main_repo_resolution`, which adds this
 * file's `treeGuards` entry to `devscene.config.json`.
 *
 * A later suite adds a corpus case as a row in `CASES`, with no new runner code. A `forbidden` entry
 * is either a string, matched by `includes`, or a `RegExp` without the `g` flag, matched by `test`.
 *
 * RED ONCE (first row) — 2026-10-29, `plugin/commands/branch-status.md` reverted to the old clause
 * in the working tree only, then restored: `main-repo-resolution-clause` failed its `deepEqual`,
 * the file missing from `needle` and listed under `forbidden`; the roster check stayed green.
 *
 * RED ONCE (roster check) — 2026-10-29, the `${CLAUDE_PLUGIN_ROOT}/commands/branch-status.md`
 * entry deleted from `## Who may cite this` in the working tree only, then restored: the roster
 * check failed its `deepEqual`, `plugin/commands/branch-status.md` missing from the roster.
 *
 * RED ONCE (row, missing sentence) — 2026-11-10, the literal-spelling sentence deleted from
 * `plugin/commands/branch-start-docs-autonomous.md`'s `<MAIN_REPO>` row in the working tree only,
 * then restored: `main-repo-resolved-values-row` and `main-repo-literal-spelling` failed, the file
 * missing from each `needle`.
 *
 * RED ONCE (bare push) — 2026-11-10, the hard boundary's push in
 * `plugin/commands/branch-start-docs-autonomous.md` rewritten as "via `<scripts_dir>/push-branch.sh`"
 * in the working tree only, then restored: `main-repo-resolved-values-row` failed, a `forbidden` hit
 * on the bare-spelling pattern.
 *
 * RED ONCE (prefixed push) — 2026-11-10, the hard boundary's push in
 * `plugin/commands/branch-start-docs-autonomous.md` rewritten as
 * "via `bash <repo_root>/<scripts_dir>/push-branch.sh`" in the working tree only, then restored:
 * `main-repo-resolved-values-row` failed, a `forbidden` hit on the `<MAIN_REPO>/` lookbehind pattern.
 *
 * RED ONCE (`$` argument) — 2026-11-10, `"$REPO_ROOT"` put as the argument of the Override D push
 * fence in `plugin/instructions/plan_orchestration_instructions_autonomous.md` in the working tree
 * only, then restored: `main-repo-resolved-values-row` failed, a `forbidden` hit on the `$`-argument
 * pattern.
 *
 * RED ONCE (`$REPO_ROOT` prose) — 2026-11-10, "It uses the `$REPO_ROOT` the calling command"
 * restored in `plugin/instructions/task_plan_writing_instructions_autonomous.md` in the working tree
 * only, then restored: `main-repo-resolved-values-row` failed, a `forbidden` hit on that string.
 *
 * RED ONCE (watcher-supplied) — 2026-11-10, "watcher-supplied" inserted into
 * `plugin/instructions/prompt_injection_screen.md`'s `<MAIN_REPO>` row in the working tree only,
 * then restored: `main-repo-resolved-values-row` failed, a `forbidden` hit on that string.
 *
 * RED ONCE (pipeline) — 2026-11-10, "`git worktree list --porcelain | head -1`" inserted into
 * `plugin/instructions/prompt_injection_screen.md`'s `<MAIN_REPO>` row in the working tree only,
 * then restored: `main-repo-resolved-values-row` failed, a `forbidden` hit on the pipeline pattern.
 *
 * RED ONCE (sentence alone) — 2026-11-10, the literal-spelling sentence deleted from
 * `plugin/instructions/prompt_injection_screen.md`'s `<MAIN_REPO>` row in the working tree only,
 * then restored: `main-repo-literal-spelling` failed, the file missing from its `needle`.
 *
 * RED ONCE (classification) — 2026-11-10, `plugin/agents/qa-tester.md` removed from `EXEMPT` in
 * this file only, then restored: the binder-classification test failed, the file a clause-carrier
 * in neither the row binders nor `EXEMPT`.
 *
 * RED ONCE (inherited row) — 2026-11-10, the line "| `<MAIN_REPO>` | derived at runtime | The main
 * checkout the citing engine command resolved. |" appended to `plugin/instructions/mode_contract.md`
 * in the working tree only, then restored: only the inherited-row test failed, with
 * `plugin/instructions/mode_contract.md` in the actual set and absent from the expected set.
 *
 * RED ONCE (roster-derived expected set) — 2026-11-16, the
 * `${CLAUDE_PLUGIN_ROOT}/commands/branch-status.md` entry deleted from `## Who may cite this` in the
 * working tree only, then restored byte-identical: `main-repo-resolution-clause` failed its
 * `deepEqual` with `plugin/commands/branch-status.md: 1` in `needle`'s actual and absent from its
 * expected; the roster check failed with that file in the tree's carriers and absent from `ROSTER`;
 * the binder-classification test failed with it in the binders-plus-`EXEMPT` set and absent from
 * the carriers.
 */

import assert from 'node:assert/strict';
import { existsSync, readdirSync, readFileSync } from 'node:fs';
import { join, relative, sep } from 'node:path';
import test from 'node:test';

import { MAIN_REPO_ANCHOR_READ } from '../dist/core/mainRepoAnchor.js';
import { WORKSPACE_ROOT } from './helpers/fixture.mjs';

// Concatenation, not a template literal: `NEW_CLAUSE` carries the literal text `${CLAUDE_PLUGIN_ROOT}`.
const NEW_CLAUSE =
  'the path a bare `' +
  MAIN_REPO_ANCHOR_READ +
  '` prints, else the path `${CLAUDE_PLUGIN_ROOT}/instructions/main_repo_resolution.md` → `## The fallback` resolves, and a stop with its sentence when it resolves none';

const OLD_CLAUSE =
  'the path a bare `' +
  MAIN_REPO_ANCHOR_READ +
  '` prints, else the first `worktree ` line of a bare `git worktree list --porcelain`';

const LITERAL_SPELLING =
  'Spell it as a literal absolute path in the command, never through a substitution or a variable.';

const MAIN_REPO_ROW =
  '| `<MAIN_REPO>` | derived at runtime | The main checkout — ' + NEW_CLAUSE + '. ' + LITERAL_SPELLING + ' |';

const MODULE = 'plugin/instructions/main_repo_resolution.md';

const MODULE_LINES = readFileSync(join(WORKSPACE_ROOT, MODULE), 'utf8').split('\n');

/**
 * The module's `## Who may cite this` plugin entries, as sorted repo-relative paths: the expected
 * clause-carrier set every case below derives from. Only `${CLAUDE_PLUGIN_ROOT}/` entries are read:
 * the repo-relative entries (`cli/…`, `docs/…`) lie outside the cases' `plugin` root.
 */
function readRoster(lines) {
  const start = lines.indexOf('## Who may cite this');
  if (start === -1) return [];
  const end = lines.findIndex((line, i) => i > start && line.startsWith('## '));
  return lines
    .slice(start + 1, end === -1 ? undefined : end)
    .map((line) => line.match(/^- `\$\{CLAUDE_PLUGIN_ROOT\}\/([^`]+)`/))
    .filter(Boolean)
    .map((match) => `plugin/${match[1]}`)
    .sort();
}

const ROSTER = readRoster(MODULE_LINES);

/** Roster members carrying the clause more than once, with the count each carries. */
export const CLAUSE_COUNT_OVERRIDES = {
  // Its `## Resolved values` row and its global kill-switch step each spell the clause.
  'plugin/commands/branch-start-user-review-fix-autonomous.md': 2,
};

/** Carriers of the resolution clause without `MAIN_REPO_ROW`, each with the reason it needs none. */
const SUPERVISED_NO_PUSH =
  'user-invoked in a supervised session, where an unmatched command prompts rather than being refused, and none issues a push';

export const EXEMPT = {
  'plugin/agents/qa-tester.md': 'it resolves a Read-tool path and spells no command with `<MAIN_REPO>`',
  'plugin/commands/branch-answer.md': SUPERVISED_NO_PUSH,
  'plugin/commands/branch-pause.md': SUPERVISED_NO_PUSH,
  'plugin/commands/branch-prompt.md': SUPERVISED_NO_PUSH,
  'plugin/commands/branch-resume.md': SUPERVISED_NO_PUSH,
  'plugin/commands/branch-status.md': SUPERVISED_NO_PUSH,
  'plugin/commands/branch-user-review.md': SUPERVISED_NO_PUSH,
};

/** The autonomous binders, each carrying `MAIN_REPO_ROW` once: the roster minus `EXEMPT`. */
const ROW_BINDERS = ROSTER.filter((file) => !Object.hasOwn(EXEMPT, file));

/** `{ id, root, glob, needle, expected, forbidden }` — `root` repo-relative, `glob` a file-name suffix. */
export const CASES = [
  {
    id: 'main-repo-resolution-clause',
    root: 'plugin',
    glob: '.md',
    needle: NEW_CLAUSE,
    expected: Object.fromEntries(ROSTER.map((f) => [f, CLAUSE_COUNT_OVERRIDES[f] ?? 1])),
        forbidden: [OLD_CLAUSE],
  },
  {
    id: 'main-repo-resolved-values-row',
    root: 'plugin',
    glob: '.md',
    needle: MAIN_REPO_ROW,
    expected: Object.fromEntries(ROW_BINDERS.map((file) => [file, 1])),
    forbidden: [
      /(?<!<MAIN_REPO>\/)<scripts_dir>\/push-branch\.sh/,
      /push-branch\.sh\s+"?\$/,
      'It uses the `$REPO_ROOT` the calling command',
      'watcher-supplied',
      /git worktree list --porcelain`?\s*\|/,
    ],
  },
  {
    id: 'main-repo-literal-spelling',
    root: 'plugin',
    glob: '.md',
    needle: LITERAL_SPELLING,
    expected: Object.fromEntries(
      [...ROW_BINDERS, 'plugin/instructions/prompt_injection_screen.md'].map((file) => [file, 1]),
    ),
    forbidden: [],
  },
];


/** Repo-relative, `/`-separated paths of every file under `root` whose name ends in `glob`. */
function filesUnder(root, glob) {
  return readdirSync(join(WORKSPACE_ROOT, root), { recursive: true, withFileTypes: true })
    .filter((entry) => entry.isFile() && entry.name.endsWith(glob))
    .map((entry) => relative(WORKSPACE_ROOT, join(entry.parentPath ?? entry.path, entry.name)).split(sep).join('/'));
}

const occurrences = (text, needle) => text.split(needle).length - 1;

const sorted = (record) => Object.fromEntries(Object.entries(record).sort(([a], [b]) => a.localeCompare(b)));

test('corpus cases', async (t) => {
  for (const row of CASES) {
    await t.test(row.id, () => {
      const found = {};
      const forbiddenHits = [];
      for (const file of filesUnder(row.root, row.glob)) {
        const text = readFileSync(join(WORKSPACE_ROOT, file), 'utf8');
        const count = occurrences(text, row.needle);
        if (count > 0) found[file] = count;
        for (const entry of row.forbidden) {
          const hit = entry instanceof RegExp ? entry.test(text) : text.includes(entry);
          if (hit) forbiddenHits.push(`${file}: ${entry}`);
        }
      }
      // One assertion, so a site reverted to a forbidden string reports both its halves.
      assert.deepEqual(
        { needle: sorted(found), forbidden: forbiddenHits },
        { needle: sorted(row.expected), forbidden: [] },
      );
    });
  }
});

test('main_repo_resolution.md — one `## The fallback`, and a plugin roster equal to the clause carriers in the tree', () => {
  assert.equal(MODULE_LINES.filter((line) => line === '## The fallback').length, 1);
  assert.notEqual(MODULE_LINES.indexOf('## Who may cite this'), -1, `${MODULE} has no \`## Who may cite this\``);

  const missing = ROSTER.filter((file) => !existsSync(join(WORKSPACE_ROOT, file)));
  assert.deepEqual(missing, [], `roster entries naming no file: ${missing.join(', ')}`);

  // The tree, not `CASES`, is the other side: the clause case's `expected` is the roster itself.
  const carriers = filesUnder('plugin', '.md')
    .filter((file) => readFileSync(join(WORKSPACE_ROOT, file), 'utf8').includes(NEW_CLAUSE))
    .sort();
  assert.deepEqual(ROSTER, carriers);
});

test('every clause-carrier is a row binder or listed in EXEMPT, never both', () => {
  const clause = Object.keys(CASES.find((c) => c.id === 'main-repo-resolution-clause').expected);
  const binders = Object.keys(CASES.find((c) => c.id === 'main-repo-resolved-values-row').expected);
  const exempt = Object.keys(EXEMPT);
  assert.deepEqual(
    { carriers: [...clause].sort(), overlap: exempt.filter((file) => binders.includes(file)) },
    { carriers: [...new Set([...binders, ...exempt])].sort(), overlap: [] },
  );
});

test('every `<MAIN_REPO>` table row carries the literal-spelling sentence, the resolution module excepted', () => {
  const spellers = Object.keys(CASES.find((c) => c.id === 'main-repo-literal-spelling').expected);
  const rowFiles = filesUnder('plugin', '.md').filter((file) =>
    readFileSync(join(WORKSPACE_ROOT, file), 'utf8')
      .split('\n')
      .some((line) => line.startsWith('| `<MAIN_REPO>` |')),
  );
  // `MODULE` produces the value and spells no command with it, so it carries no sentence.
  assert.deepEqual(rowFiles.sort(), [...spellers, MODULE].sort());
});
