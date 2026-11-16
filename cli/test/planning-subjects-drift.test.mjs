/**
 * The planning driver's fixed commit subjects against the artifact table,
 * `cli/templates/scripts/lib/planning-record-lib.sh` against `cli/templates/scripts/lib/unit-commit-lib.sh`.
 *
 * **The rule this suite enforces: each fixed subject and path set the planning driver hardcodes
 * equals the library's artifact-table row byte-for-byte.** The driver keeps its own plain wrapper
 * calls while the autonomous fork issues `commit-on-branch.sh --artifact <kind>`, so the two must
 * name the same commit or the same commit point lands under two subjects.
 *
 * Each case runs one `bash` subprocess that sources `lib/harness-run-lib.sh`,
 * `lib/planning-record-lib.sh` and `lib/unit-commit-lib.sh` from the templates, sets the `PRL_*`
 * globals to a throwaway worktree under the system temp directory, and redefines `prl_commit` to
 * print its subject and paths NUL-separated, each commit closed by an empty record. A second
 * subprocess prints the matching `ucl_artifact` rows the same way, and the two outputs are compared.
 *
 * It reads two fixed files, not a tree, so it is not a tree guard.
 */

import assert from 'node:assert/strict';
import { mkdir, mkdtemp, realpath, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import test from 'node:test';

import { PACKAGE_ROOT, runBash } from './helpers/fixture.mjs';

const LIB = join(PACKAGE_ROOT, 'templates', 'scripts', 'lib');
const BRANCH = 'feat_x';
const S = 'devscene';

const PRELUDE = [
  `. '${join(LIB, 'harness-run-lib.sh')}' || exit 99`,
  `. '${join(LIB, 'planning-record-lib.sh')}' || exit 98`,
  `. '${join(LIB, 'unit-commit-lib.sh')}' || exit 97`,
  `PRL_BRANCH=${BRANCH}`,
  `PRL_STATE_DIR=${S}`,
  'PRL_WORKTREE="$W"',
  'PRL_MAIN_REPO="$M"',
  'PRL_LOG=""',
  'PRL_COMMIT_LANDED=no',
  "prl_commit() { printf '%s\\0' \"$@\"; printf '\\0'; PRL_COMMIT_LANDED=yes; return 0; }",
  "ucl_print() { ucl_artifact \"$@\" || exit 96; printf '%s\\0' \"$UCL_SUBJECT\" \"${UCL_PATHS[@]}\"; printf '\\0'; }",
].join('\n');

/** Each case's name, the driver calls and the `ucl_artifact` rows each must equal, in commit order. */
const CASES = [
  ['prl_round_commit 3', 'prl_round_commit 3', [`plan-round ${S} ${BRANCH} 3 '' ''`]],
  ['prl_partial_commit 3', 'prl_partial_commit 3', [`plan-round-partial ${S} ${BRANCH} 3 '' ''`]],
  ['prl_convergence_commits yes', 'prl_convergence_commits yes', [`ui-test-plan ${S} ${BRANCH} '' '' ''`, `task-plan ${S} ${BRANCH} '' '' ''`]],
  ['prl_ledger_flip P1', 'prl_ledger_flip P1', [`ledger-flip ${S} ${BRANCH} '' '' P1`]],
  ['prl_observe_flush', "prl_observe convention 'p' 'e' 'c' || exit 95; prl_observe_flush", [`observations ${S} ${BRANCH} '' '' ''`]],
];

async function workspace(t) {
  const root = await realpath(await mkdtemp(join(tmpdir(), 'planning-subjects-drift-')));
  t.after(() => rm(root, { recursive: true, force: true }));
  const wt = join(root, 'wt');
  const main = join(root, 'main');
  await mkdir(join(wt, S, 'flow_progress'), { recursive: true });
  await mkdir(main);
  await writeFile(join(wt, S, 'flow_progress', `${BRANCH}_progress.md`), '## Planning\n- [ ] P1. Task plan converged\n');
  return { W: wt, M: main, HOME: join(root, 'home'), TMPDIR: root };
}

/** The NUL-separated records of one run, split into commits. */
function commits(stdout) {
  const out = [];
  let current = [];
  for (const record of stdout.split('\0').slice(0, -1)) {
    if (record === '') {
      out.push(current);
      current = [];
    } else {
      current.push(record);
    }
  }
  assert.deepEqual(current, [], 'output ended mid-commit');
  return out;
}

for (const [name, call, rows] of CASES) {
  test(`${name} commits the artifact table's subject and path set`, async (t) => {
    const env = await workspace(t);
    const driver = await runBash(env.W, ['-c', `${PRELUDE}\n${call}`], env);
    assert.equal(driver.status, 0, `the driver call exited ${driver.status}: ${driver.stderr}`);
    const table = await runBash(env.W, ['-c', `${PRELUDE}\n${rows.map((r) => `ucl_print ${r}`).join('\n')}`], env);
    assert.equal(table.status, 0, `ucl_artifact exited ${table.status}: ${table.stderr}`);

    const expected = commits(table.stdout);
    assert.equal(expected.length, rows.length);
    assert.deepEqual(commits(driver.stdout), expected);
  });
}
