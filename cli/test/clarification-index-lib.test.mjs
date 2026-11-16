/**
 * The run library's clarification-channel index answers — `hr_max_question_index` and
 * `hr_top_level_answered_pairs` in `cli/templates/scripts/lib/harness-run-lib.sh`.
 *
 * **The rule this suite enforces: one definition of each clarification-index answer, in the run
 * library.** The watcher, the planning record library and the planning driver all take them from
 * there, so a second copy could drift on numeric-only names, zero padding or base-10 handling with
 * no failing test. The last case guards the source: it reads two fixed files only — the watcher
 * template and the run library — never a directory.
 *
 * Each case copies the library into its own throwaway directory under `os.tmpdir()`, sources it
 * from there in one `bash` process under `set -u`, and removes the directory in process.
 */

import assert from 'node:assert/strict';
import { copyFile, mkdir, mkdtemp, readFile, realpath, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import test from 'node:test';

import { PACKAGE_ROOT, runBash } from './helpers/fixture.mjs';

const LIB_TEMPLATE = join(PACKAGE_ROOT, 'templates', 'scripts', 'lib', 'harness-run-lib.sh');
const WATCHER_TEMPLATE = join(PACKAGE_ROOT, 'templates', 'scripts', 'autonomous-watcher.sh');

/** A fresh directory holding a copy of the library and a clarification channel directory path. */
async function fixture(t) {
  const root = await realpath(await mkdtemp(join(tmpdir(), 'clarification-index-')));
  t.after(() => rm(root, { recursive: true, force: true }));
  const lib = join(root, 'harness-run-lib.sh');
  await copyFile(LIB_TEMPLATE, lib);
  const clar = join(root, 'clarifications');
  /** Source the copied library, then run `fn <clar>` under `set -u`. */
  const call = (fn) => runBash(root, ['-c', `. "$1" || exit 99; set -u; ${fn} "$2"`, '_', lib, clar]);
  /** Create each named file (relative to the channel), with its parent directory. */
  const touch = async (...names) => {
    for (const name of names) {
      const path = join(clar, name);
      await mkdir(join(path, '..'), { recursive: true });
      await writeFile(path, 'x\n');
    }
  };
  return { clar, call, touch };
}

/** The call's exit status, stderr and stdout, asserted whole. */
function assertOut(r, stdout, label) {
  assert.equal(r.stderr, '', `${label}: ${r.stderr}`);
  assert.equal(r.status, 0, label);
  assert.equal(r.stdout, stdout, label);
}

test('an absent or empty channel: the maximum is 0 and there are no pairs', async (t) => {
  const f = await fixture(t);
  assertOut(await f.call('hr_max_question_index'), '0\n', 'absent: max');
  assertOut(await f.call('hr_top_level_answered_pairs'), '', 'absent: pairs');
  await mkdir(join(f.clar, 'answered'), { recursive: true });
  assertOut(await f.call('hr_max_question_index'), '0\n', 'empty: max');
  assertOut(await f.call('hr_top_level_answered_pairs'), '', 'empty: pairs');
});

test('the maximum counts answered/ as well as the top level', async (t) => {
  const f = await fixture(t);
  await f.touch('question_2.md', 'answered/question_5.md', 'answered/answer_5.md');
  assertOut(await f.call('hr_max_question_index'), '5\n', 'answered/ holds the maximum');
  await f.touch('question_7.md');
  assertOut(await f.call('hr_max_question_index'), '7\n', 'the top level holds the maximum');
});

test('a non-numeric name is ignored by both', async (t) => {
  const f = await fixture(t);
  await f.touch('question_x.md', 'answer_x.md', 'answered/question_y.md');
  assertOut(await f.call('hr_max_question_index'), '0\n', 'max');
  assertOut(await f.call('hr_top_level_answered_pairs'), '', 'pairs');
  await f.touch('question_3.md', 'answer_3.md');
  assertOut(await f.call('hr_max_question_index'), '3\n', 'max beside a numeric one');
  assertOut(await f.call('hr_top_level_answered_pairs'), '3\n', 'pairs beside a numeric one');
});

test('a zero-padded index reads in base 10 and is printed as its file name spells it', async (t) => {
  const f = await fixture(t);
  await f.touch('question_08.md', 'answer_08.md');
  assertOut(await f.call('hr_max_question_index'), '8\n', 'max');
  assertOut(await f.call('hr_top_level_answered_pairs'), '08\n', 'pairs');
});

test('an unanswered question is left out, and the pairs are numerically sorted', async (t) => {
  const f = await fixture(t);
  await f.touch(
    'question_10.md',
    'answer_10.md',
    'question_2.md',
    'answer_2.md',
    'question_9.md',
    'question_1.md',
    'answer_1.md',
    'answered/question_4.md',
    'answered/answer_4.md',
  );
  assertOut(await f.call('hr_top_level_answered_pairs'), '1 2 10\n', 'pairs');
});

test('the watcher defines neither answer, and the run library defines both', async () => {
  const watcher = await readFile(WATCHER_TEMPLATE, 'utf8');
  const lib = await readFile(LIB_TEMPLATE, 'utf8');
  const defines = (text, name) => new RegExp(`^${name}\\(\\)`, 'm').test(text);
  for (const name of ['max_question_index', 'top_level_answered_pairs', 'hr_max_question_index', 'hr_top_level_answered_pairs']) {
    assert.equal(defines(watcher, name), false, `autonomous-watcher.sh defines ${name}()`);
  }
  for (const name of ['hr_max_question_index', 'hr_top_level_answered_pairs']) {
    assert.equal(defines(lib, name), true, `harness-run-lib.sh does not define ${name}()`);
  }
});
