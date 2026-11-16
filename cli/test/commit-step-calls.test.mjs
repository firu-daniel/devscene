import { readdirSync, readFileSync } from 'node:fs';
import { join, relative, sep } from 'node:path';
import { test } from 'node:test';
import assert from 'node:assert/strict';

import { WORKSPACE_ROOT } from './helpers/fixture.mjs';

/**
 * The rule this suite enforces: every commit step is one literal call of the main checkout's
 * `commit-on-branch.sh`, issued once, alone, with no `$` in it, and the four forks' `<commit_call>`
 * values differ only by `--push` — the two autonomous forks carry it, the two semi-autonomous forks
 * do not.
 *
 * This is a source guard, the last resort `.claude/context/conventions.md` → `## The testing bar`
 * permits: the rule is orchestrator prose, and no behavioural test starts an orchestrator session.
 *
 * Deliberately not covered: whether a live session actually issues one Bash call per commit. That
 * needs a live session, which no test in this package starts.
 *
 * Each section assertion reads one section, sliced from its heading to the next heading of the same
 * or a higher level, so a match elsewhere in the file cannot satisfy it; a heading that is not found
 * fails its case by name. `DEFINITION` and the two `<commit_call>` values are literals here, never
 * read from a plugin file, so an edit made to every prose copy at once still fails. Case (e) reads
 * every file under `plugin/` as text.
 *
 * Red once, 2026-11-16: with `--push` deleted from
 * `plan_orchestration_instructions_autonomous.md`'s `<commit_call>` row, case (c) failed with
 * "plugin/instructions/plan_orchestration_instructions_autonomous.md → ## Mode contract — bindings:
 * <commit_call> row does not carry the value
 * `bash <MAIN_REPO>/<scripts_dir>/commit-on-branch.sh --repo <repo_root> --push`". The file was then
 * restored byte-identical.
 */

const read = (rel) => ({ rel, text: readFileSync(join(WORKSPACE_ROOT, rel), 'utf8') });

const UNIT_LOOP = read('plugin/instructions/unit_loop_core.md');
const LEDGER = read('plugin/instructions/autonomous_pause_and_ledger.md');
const AUTONOMOUS_FORKS = [
  read('plugin/instructions/plan_orchestration_instructions_autonomous.md'),
  read('plugin/instructions/user_review_fixes_instructions_autonomous.md'),
];
const SEMI_AUTONOMOUS_FORKS = [
  read('plugin/instructions/plan_orchestration_instructions_semi_autonomous.md'),
  read('plugin/instructions/user_review_fixes_instructions_semi_autonomous.md'),
];

const DEFINITION =
  '**Once, alone** means its own Bash call holding that one command and nothing else — no `cd`, `;`, `&&`, `||`, pipe, `echo "exit $?"`, `$(…)` or shell variable before or after it.';
const UNPUSHED = 'bash <MAIN_REPO>/<scripts_dir>/commit-on-branch.sh --repo <repo_root>';
const PUSHED = `${UNPUSHED} --push`;
const BINDINGS = '## Mode contract — bindings';

const collapse = (s) => s.replace(/\s+/g, ' ');

function section(file, heading) {
  const lines = file.text.split('\n');
  const start = lines.findIndex((line) => line === heading);
  assert.notEqual(start, -1, `${file.rel}: heading not found: ${heading}`);
  const level = heading.match(/^#+/)[0].length;
  const end = lines.findIndex(
    (line, i) => i > start && /^#+ /.test(line) && line.match(/^#+/)[0].length <= level,
  );
  return { where: `${file.rel} → ${heading}`, text: lines.slice(start, end === -1 ? undefined : end).join('\n') };
}

function commitCallRow(file) {
  const sec = section(file, BINDINGS);
  const row = sec.text.split('\n').find((l) => l.startsWith('| `<commit_call>` |'));
  assert.ok(row, `${sec.where}: no <commit_call> row`);
  return { where: sec.where, row };
}

test('(a) the unit loop step 5 issues the commit call once, alone', () => {
  const loop = section(UNIT_LOOP, '## The unit loop');
  const call = '<commit_call> --unit <the row\'s commit unit> --plan <the row\'s readiness index> --id <K> <the row\'s commit extra args>';
  assert.ok(loop.text.includes(call), `${loop.where}: step 5 does not carry "${call}"`);
  assert.ok(collapse(loop.text).includes(DEFINITION), `${loop.where}: the "Once, alone" definition not found`);
});

test('(b) the ledger §1.6 states the once, alone rule for its ledger-flip call', () => {
  const s16 = section(LEDGER, '### 1.6 How to flip / create — direct `commit-on-branch.sh`, NEVER a committer dispatch');
  assert.ok(s16.text.includes('Call each wrapper once, alone.'), `${s16.where}: "Call each wrapper once, alone." not found`);
  assert.ok(collapse(s16.text).includes(DEFINITION), `${s16.where}: the "Once, alone" definition not found`);
  assert.ok(!s16.text.includes('newline-separated'), `${s16.where}: still carries "newline-separated"`);
  assert.ok(s16.text.includes('--artifact ledger-flip --entry'), `${s16.where}: does not name "--artifact ledger-flip --entry"`);
});

test('(c) each autonomous fork binds <commit_call> to the main checkout\'s wrapper with --push', () => {
  for (const fork of AUTONOMOUS_FORKS) {
    const { where, row } = commitCallRow(fork);
    assert.ok(row.includes(`\`${PUSHED}\``), `${where}: <commit_call> row does not carry the value \`${PUSHED}\``);
  }
});

test('(d) each semi-autonomous fork binds <commit_call> to the same wrapper without --push', () => {
  for (const fork of SEMI_AUTONOMOUS_FORKS) {
    const { where, row } = commitCallRow(fork);
    assert.ok(row.includes(`\`${UNPUSHED}\``), `${where}: <commit_call> row does not carry the value \`${UNPUSHED}\``);
    assert.ok(!row.includes(`\`${PUSHED}\``), `${where}: <commit_call> row carries the --push value`);
  }
});

test('(e) no file under plugin/ names agents/committer.md or carries <committer_push>', () => {
  const files = readdirSync(join(WORKSPACE_ROOT, 'plugin'), { recursive: true, withFileTypes: true })
    .filter((entry) => entry.isFile())
    .map((entry) => relative(WORKSPACE_ROOT, join(entry.parentPath ?? entry.path, entry.name)).split(sep).join('/'));
  assert.ok(files.length > 0, 'plugin/: no files found');
  const offenders = [];
  for (const rel of files) {
    const { text } = read(rel);
    for (const needle of ['agents/committer.md', '<committer_push>']) {
      if (text.includes(needle)) offenders.push(`${rel}: ${needle}`);
    }
  }
  assert.deepEqual(offenders, [], `plugin/ still references the committer agent:\n${offenders.join('\n')}`);
});
