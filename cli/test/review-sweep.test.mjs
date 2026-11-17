/**
 * `review-sweep.sh` — the end-of-branch review's grep sweep, run against repositories the test builds
 * and throws away.
 *
 * **The rule these tests exist to enforce: the sweep applies each row of `.claude/review-sweep.md`,
 * as the default branch commits it, to the lines the branch adds inside that row's `Covers` minus
 * its `Exempts` and outside the state directory, and answers `0` with nothing printed, `1` with one
 * `<path>:<line>: <escape class>` per hit, the line being the branch file's, or `2` with one stderr
 * line naming the configuration error.** A branch's own edit to the document, committed or not,
 * changes nothing.
 *
 * Each fixture copies the template and `lib/harness-run-lib.sh` into its `scriptsDir`, so the
 * script places its configuration from its own location. `jq` must be on `PATH`: the library reads
 * the configuration with it.
 */

import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { mkdir, writeFile } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import test from 'node:test';

import { WORKSPACE_ROOT, createFixture, runBash, runGit } from './helpers/fixture.mjs';

const TEMPLATES = join(WORKSPACE_ROOT, 'cli', 'templates');
const SCRIPT_SOURCE = readFileSync(join(TEMPLATES, 'scripts', 'review-sweep.sh'), 'utf8');
const LIB_SOURCE = readFileSync(join(TEMPLATES, 'scripts', 'lib', 'harness-run-lib.sh'), 'utf8');
const SKELETON = readFileSync(join(TEMPLATES, 'claude', 'review-sweep.md'), 'utf8');

const SCRIPTS_DIR = 'scripts';
const STATE_DIR = 'devscene';
const DEFAULT_BRANCH = 'main';
const SWEEP = '.claude/review-sweep.md';
const HEADER_ROW = '| Escape class | Regex | Covers | Exempts | A hit is a candidate for |';

/** A sweep document whose table holds `rows`, each one already-formatted Markdown row. */
function sweepDoc(rows) {
  return ['# The review sweep', '', '## Sweep rows', '', HEADER_ROW, '|---|---|---|---|---|', ...rows, '', 'Trailing prose.', ''].join('\n');
}

const CONSOLE_ROW = '| Raw console | `console\\.log` | `.` | — | the logger |';

async function write(dir, relativePath, content) {
  const target = join(dir, relativePath);
  await mkdir(dirname(target), { recursive: true });
  await writeFile(target, content, 'utf8');
}

async function commitAll(dir, message) {
  await runGit(dir, ['add', '-A']);
  await runGit(dir, ['commit', '--quiet', '--allow-empty', '-m', message]);
}

/**
 * A repository whose `main` commits `base` (path → content, the sweep document included when given)
 * and is then left on branch `feat`.
 */
async function sweepFixture(t, base = {}) {
  const fixture = await createFixture({
    remote: false,
    files: {
      'devscene.config.json': {
        version: 1,
        defaultBranch: DEFAULT_BRANCH,
        stateDir: `${STATE_DIR}/`,
        scriptsDir: SCRIPTS_DIR,
        layers: [{ name: 'general', path: '.', conventions: '.claude/context/conventions.md' }],
      },
      [`${SCRIPTS_DIR}/review-sweep.sh`]: SCRIPT_SOURCE,
      [`${SCRIPTS_DIR}/lib/harness-run-lib.sh`]: LIB_SOURCE,
      ...base,
    },
  });
  t.after(() => fixture.cleanup());
  const { dir } = fixture;
  await runGit(dir, ['symbolic-ref', 'HEAD', `refs/heads/${DEFAULT_BRANCH}`]);
  await commitAll(dir, 'base');
  await runGit(dir, ['checkout', '--quiet', '-b', 'feat']);
  return dir;
}

function sweep(dir, args = ['--repo', dir]) {
  return runBash(dir, [join(dir, SCRIPTS_DIR, 'review-sweep.sh'), ...args]);
}

const show = (r) => `status ${r.status}\nstdout: ${r.stdout}\nstderr: ${r.stderr}`;

function assertHits(result, lines) {
  assert.equal(result.status, 1, show(result));
  assert.equal(result.stdout, lines.map((line) => `${line}\n`).join(''), show(result));
  assert.equal(result.stderr, '', show(result));
}

function assertClean(result) {
  assert.equal(result.status, 0, show(result));
  assert.equal(result.stdout, '', show(result));
  assert.equal(result.stderr, '', show(result));
}

function assertConfigError(result, pattern) {
  assert.equal(result.status, 2, show(result));
  assert.equal(result.stdout, '', show(result));
  const lines = result.stderr.split('\n').filter((line) => line !== '');
  assert.equal(lines.length, 1, show(result));
  assert.match(lines[0], pattern, show(result));
}

test('a branch adding no matching line exits 0 and prints nothing', async (t) => {
  const dir = await sweepFixture(t, { [SWEEP]: sweepDoc([CONSOLE_ROW]) });
  await write(dir, 'src/a.js', 'logger.info(1);\n');
  await commitAll(dir, 'clean');
  assertClean(await sweep(dir));
});

test('each matching added line is one hit carrying the branch file\'s line number', async (t) => {
  const dir = await sweepFixture(t, {
    [SWEEP]: sweepDoc([CONSOLE_ROW]),
    'src/a.js': 'one\ntwo\nthree\n',
  });
  await write(dir, 'src/a.js', 'one\nconsole.log(1);\ntwo\nthree\nconsole.log(2);\n');
  await write(dir, 'src/name with space.js', 'console.log(3);\n');
  await commitAll(dir, 'hits');

  const expected = ['src/a.js:2: Raw console', 'src/a.js:5: Raw console', 'src/name with space.js:1: Raw console'];
  assertHits(await sweep(dir), expected);
  assertHits(await sweep(dir, []), expected);
});

test('a match on an unchanged or removed line is not a hit', async (t) => {
  const dir = await sweepFixture(t, {
    [SWEEP]: sweepDoc([CONSOLE_ROW]),
    'src/a.js': 'console.log(kept);\nconsole.log(removed);\nplain\n',
  });
  await write(dir, 'src/a.js', 'console.log(kept);\nplain\nadded\n');
  await commitAll(dir, 'edit');
  assertClean(await sweep(dir));
});

test('a row sweeps its Covers and skips its Exempts, paths and globs alike', async (t) => {
  const row = '| Raw console | `console\\.log` | `src`, `lib` | `src/owner.js`, `src/gen/*.js` | the logger |';
  const dir = await sweepFixture(t, { [SWEEP]: sweepDoc([row]) });
  for (const path of ['src/a.js', 'lib/b.js', 'src/owner.js', 'src/gen/c.js', 'other/d.js']) {
    await write(dir, path, 'console.log(1);\n');
  }
  await commitAll(dir, 'scoped');
  assertHits(await sweep(dir), ['lib/b.js:1: Raw console', 'src/a.js:1: Raw console']);
});

test('nothing under the state directory is ever a hit', async (t) => {
  const dir = await sweepFixture(t, { [SWEEP]: sweepDoc([CONSOLE_ROW]) });
  await write(dir, `${STATE_DIR}/notes.md`, 'console.log(1);\n');
  await write(dir, 'a.js', 'console.log(2);\n');
  await commitAll(dir, 'state');
  assertHits(await sweep(dir), ['a.js:1: Raw console']);
});

test('an escaped \\| in a Regex cell is alternation, and both arms match', async (t) => {
  const row = '| Timing literal | `setTimeout\\|setInterval` | `.` | — | the timing owner |';
  const dir = await sweepFixture(t, { [SWEEP]: sweepDoc([CONSOLE_ROW, row]) });
  await write(dir, 'a.js', 'setTimeout(f, 5);\nsetInterval(f, 5);\nconsole.log(1);\n');
  await commitAll(dir, 'timers');
  assertHits(await sweep(dir), ['a.js:3: Raw console', 'a.js:1: Timing literal', 'a.js:2: Timing literal']);
});

test('a branch edit to the sweep document, committed or not, changes nothing', async (t) => {
  const dir = await sweepFixture(t, { [SWEEP]: sweepDoc([CONSOLE_ROW]) });
  await write(dir, 'src/a.js', 'console.log(1);\n');
  await write(dir, SWEEP, sweepDoc(['| Nothing | `^never-matches$` | `src` | — | nothing |']));
  await commitAll(dir, 'disarm on the branch');
  await write(dir, SWEEP, '# emptied in the working tree\n');
  assertHits(await sweep(dir), ['src/a.js:1: Raw console']);
});

test('a document absent from the default branch is a configuration error', async (t) => {
  const dir = await sweepFixture(t);
  await write(dir, SWEEP, sweepDoc([CONSOLE_ROW]));
  await commitAll(dir, 'only on the branch');
  assertConfigError(await sweep(dir), /not committed on main/);
});

test('the untouched skeleton is a configuration error', async (t) => {
  const dir = await sweepFixture(t, { [SWEEP]: SKELETON });
  assertConfigError(await sweep(dir), /untouched skeleton/);
});

test('a malformed document or row is a configuration error naming its cause', async (t) => {
  const cases = [
    ['no heading', sweepDoc([CONSOLE_ROW]).replace('## Sweep rows', '## Rows'), /no '## Sweep rows' heading/],
    ['another header row', sweepDoc([CONSOLE_ROW]).replace(HEADER_ROW, '| Class | Regex | Covers | Exempts | Note |'), /exact header row/],
    ['no data row', sweepDoc([]), /no data row/],
    ['four cells', sweepDoc(['| Raw console | `console` | `.` | — |']), /4 cells, not 5/],
    ['regex not one code span', sweepDoc(['| Raw console | console\\.log | `.` | — | x |']), /'Raw console'.*not exactly one code span/],
    ['empty Covers', sweepDoc(['| Raw console | `console` |  | — | x |']), /'Raw console': empty Covers/],
    ['invalid regex', sweepDoc([CONSOLE_ROW, '| Broken class | `(unclosed` | `.` | — | x |']), /invalid regex in row 'Broken class'/],
  ];
  for (const [name, doc, pattern] of cases) {
    await t.test(name, async (st) => {
      const dir = await sweepFixture(st, { [SWEEP]: doc });
      await write(dir, 'a.js', 'console.log(1);\n');
      await commitAll(dir, 'a hit that must not be printed');
      assertConfigError(await sweep(dir), pattern);
    });
  }
});

test('bad usage, a --repo that is not a work tree and an unresolvable default branch are configuration errors', async (t) => {
  const dir = await sweepFixture(t, { [SWEEP]: sweepDoc([CONSOLE_ROW]) });
  assertConfigError(await sweep(dir, ['--bogus']), /^usage: review-sweep\.sh/);
  assertConfigError(await sweep(dir, ['--repo']), /^usage: review-sweep\.sh/);

  assertConfigError(await sweep(dir, ['--repo', `${dir}-missing`]), /is not a git work tree/);

  await runGit(dir, ['branch', '--quiet', '-m', DEFAULT_BRANCH, 'renamed']);
  assertConfigError(await sweep(dir), /default branch main does not resolve/);
});
