/**
 * The planning driver's durable writes, `cli/templates/scripts/lib/planning-record-lib.sh`: the
 * round, partial and convergence commits, the `## Planning` ledger flips, the park and pause files
 * and the improvement-observation flush.
 *
 * **The rule this suite enforces: every write is the autonomous planning fork's own — the main
 * checkout's `commit-on-branch.sh` over the override's exact path set under its fixed subject, then
 * its `push-branch.sh` — and a repeated write commits nothing.** Each case is graded on the bytes on
 * disk, on `git log` and on the bare `origin`'s ref.
 *
 * Each case builds its own main checkout, bare `origin` and linked worktree on `feat_x` under the
 * system temp directory, with the isolated git configuration `runBash` and `runGit` apply and a
 * fake `HOME`. It copies `lib/harness-run-lib.sh`, `commit-on-branch.sh`, `push-branch.sh` and the
 * library from `cli/templates/scripts/`, and seeds a task-engine ledger.
 *
 * Not covered: that the run copy's index matches `HEAD` after a real landed exit 1. The real
 * wrapper reaches that exit only when the working copy's index cannot take the paths after the ref
 * has moved, which this fixture cannot produce without racing the wrapper; the stubbed case covers
 * `prl_commit`'s side of `plugin/instructions/autonomous_pause_and_ledger.md` → `### 1.6`, and the
 * wrapper's own re-sync is its own contract.
 */

import assert from 'node:assert/strict';
import { existsSync } from 'node:fs';
import { appendFile, copyFile, mkdir, mkdtemp, readFile, realpath, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import test from 'node:test';

import { PACKAGE_ROOT, runBash, runGit } from './helpers/fixture.mjs';

const TEMPLATES = join(PACKAGE_ROOT, 'templates', 'scripts');
const BRANCH = 'feat_x';
const S = 'devscene';
const LEDGER = `${S}/flow_progress/${BRANCH}_progress.md`;
const LEDGER_TEXT = [
  `# Flow progress — ${BRANCH}   (engine: task)`,
  '',
  '## Planning',
  '- [x] P0. Untrusted input screened (prompt-injection-reviewer SAFE)',
  '- [ ] P1. Task plan converged (business_parity + architecture + task-plan-reviewer all PASS)',
  '- [-] P2. UI-test plan converged (ui-tests-plan-reviewer PASS) — or no_ui',
  '- [ ] P3. Plans committed & pushed (story index + per-task dir + UI-test plan)',
  '',
  '## Implementation',
  '- [ ] A.      Tasks implemented (story-index readiness all [x])',
  '',
].join('\n');
const CONFIG = {
  version: 1,
  defaultBranch: 'trunk',
  protectedBranches: ['trunk'],
  stateDir: `${S}/`,
  scriptsDir: 's',
  layers: [],
  commands: {},
};
const CLOSING = '# Task run (Phase D)';

const PRELUDE = [
  '. "$M/s/lib/harness-run-lib.sh" || exit 99',
  '. "$M/s/lib/planning-record-lib.sh" || exit 98',
  `prl_init ${BRANCH} "$W" "$M" "$LOG" || exit 97`,
].join('\n');

async function fixture(t) {
  const root = await realpath(await mkdtemp(join(tmpdir(), 'planning-record-lib-')));
  t.after(() => rm(root, { recursive: true, force: true }));
  const main = join(root, 'main');
  const wt = join(root, 'wt');
  const origin = join(root, 'origin.git');
  const home = join(root, 'home');
  await mkdir(main);
  await mkdir(origin);
  await mkdir(home);
  await runGit(origin, ['init', '--quiet', '--bare']);
  await runGit(main, ['init', '--quiet', '-b', 'trunk']);
  await runGit(main, ['config', 'user.email', 'fixture@example.invalid']);
  await runGit(main, ['config', 'user.name', 'Harness Fixture']);
  await runGit(main, ['remote', 'add', 'origin', origin]);
  await writeFile(join(main, 'devscene.config.json'), `${JSON.stringify(CONFIG)}\n`);
  await mkdir(join(main, 's', 'lib'), { recursive: true });
  for (const name of ['commit-on-branch.sh', 'push-branch.sh', 'lib/harness-run-lib.sh', 'lib/planning-record-lib.sh']) {
    await copyFile(join(TEMPLATES, name), join(main, 's', name));
  }
  await mkdir(join(main, S, 'flow_progress'), { recursive: true });
  await writeFile(join(main, LEDGER), LEDGER_TEXT);
  await runGit(main, ['add', 'devscene.config.json', 's', S]);
  await runGit(main, ['commit', '--quiet', '-m', 'fixture: seed']);
  await runGit(main, ['worktree', 'add', '--quiet', '-b', BRANCH, wt, 'trunk']);

  const log = join(root, 'run.log');
  const env = {
    M: main,
    W: wt,
    LOG: log,
    HOME: home,
    XDG_CONFIG_HOME: join(home, '.config'),
    GH_TOKEN: '',
    GITHUB_TOKEN: '',
    HARNESS_PR_TOKEN: '',
    DEVSCENE_GIT_TOKEN: '',
    GITHUB_ACTIONS: '',
    PUSH_RETRY_DELAY_SECS: '0',
  };
  const git = async (...args) => (await runGit(main, args)).stdout;
  return {
    root,
    main,
    wt,
    origin,
    home,
    log,
    env,
    bash: (body, extra = {}) => runBash(root, ['-c', `${PRELUDE}\n${body}`], { ...env, ...extra }),
    write: async (rel, text) => {
      await mkdir(dirname(join(wt, rel)), { recursive: true });
      await writeFile(join(wt, rel), text);
    },
    read: (rel) => readFile(join(wt, rel), 'utf8'),
    tip: async () => (await git('rev-parse', `refs/heads/${BRANCH}`)).trim(),
    originTip: async () => (await runGit(origin, ['rev-parse', `refs/heads/${BRANCH}`])).stdout.trim(),
    /** The raw message and the changed files of a commit on the branch. */
    commit: async (rev = `refs/heads/${BRANCH}`) => {
      const raw = await git('cat-file', 'commit', rev);
      const message = raw.slice(raw.indexOf('\n\n') + 2);
      const files = (await git('show', '--name-only', '--format=', rev)).split('\n').filter(Boolean).sort();
      return { message, files };
    },
  };
}

const ROUND_FILES = (b) => [
  `${S}/story_plans/${b}_story_plan.md`,
  `${S}/task_plans/${b}/task_1_plan.md`,
  `${S}/task_plan_reviews/${b}/review_1.md`,
  `${S}/business_parity_reviews/${b}/review_1.md`,
  `${S}/architecture_reviews/${b}/review_1.md`,
  `${S}/plan_revisions/${b}/task_plan_revision_1.md`,
];

test('prl_round_commit and prl_partial_commit commit exactly the round path set, then push; a repeat commits nothing', async (t) => {
  const f = await fixture(t);
  for (const rel of ROUND_FILES(BRANCH)) await f.write(rel, `${rel}\n`);
  await f.write(`${S}/ui_test_plans/${BRANCH}_ui_test_plan.md`, 'ui\n');
  await f.write(`${S}/notes.md`, 'not planning\n');
  const before = await f.tip();

  const first = await f.bash('prl_round_commit 1');
  assert.equal(first.status, 0, first.stderr);
  const round = await f.commit();
  assert.equal(round.message, `chore: Plan round 1 for ${BRANCH}\n`, 'subject only, no trailer');
  assert.deepEqual(round.files, ROUND_FILES(BRANCH).sort());
  assert.equal(await f.originTip(), await f.tip());

  const tip = await f.tip();
  assert.notEqual(tip, before);
  const again = await f.bash('prl_round_commit 1');
  assert.equal(again.status, 0, again.stderr);
  assert.equal(await f.tip(), tip, 'exit 3: nothing committed');

  await f.write(`${S}/task_plans/${BRANCH}/task_1_plan.md`, 'revised\n');
  const partial = await f.bash('prl_partial_commit 2');
  assert.equal(partial.status, 0, partial.stderr);
  const p = await f.commit();
  assert.equal(p.message, `chore: Plan round 2 partial for ${BRANCH}\n`);
  assert.deepEqual(p.files, [`${S}/task_plans/${BRANCH}/task_1_plan.md`]);
  assert.equal(await f.originTip(), await f.tip());

  const bad = await f.bash('prl_round_commit x');
  assert.equal(bad.status, 2);
  assert.match(bad.stderr, /^planning-driver: 'x' is not a round number$/m);

  const log = await readFile(f.log, 'utf8');
  assert.ok(log.includes(`[plan-drive] commit: chore: Plan round 1 for ${BRANCH}\n`), log);
  assert.ok(log.split('\n').filter(Boolean).every((line) => line.startsWith('[plan-drive] ')), log);
});

test('prl_convergence_commits: the UI-test plan first with yes, then always the task plan', async (t) => {
  const f = await fixture(t);
  await f.write(`${S}/ui_test_plans/${BRANCH}_ui_test_plan.md`, 'ui index\n');
  await f.write(`${S}/ui_test_plans/${BRANCH}/ui_test_1.md`, 'ui 1\n');
  await f.write(`${S}/story_plans/${BRANCH}_story_plan.md`, 'story\n');
  await f.write(`${S}/task_plans/${BRANCH}/task_1_plan.md`, 'task\n');
  await f.write(`${S}/ui_test_plan_reviews/${BRANCH}/review_0.md`, 'ui review\n');

  const r = await f.bash('prl_convergence_commits yes');
  assert.equal(r.status, 0, r.stderr);
  const ui = await f.commit(`refs/heads/${BRANCH}~1`);
  assert.equal(ui.message, `chore: Add UI-test plan for ${BRANCH}\n`);
  assert.deepEqual(ui.files, [`${S}/ui_test_plans/${BRANCH}/ui_test_1.md`, `${S}/ui_test_plans/${BRANCH}_ui_test_plan.md`]);
  const plan = await f.commit();
  assert.equal(plan.message, `chore: Add task plan for ${BRANCH}\n`);
  assert.deepEqual(plan.files, [
    `${S}/story_plans/${BRANCH}_story_plan.md`,
    `${S}/task_plans/${BRANCH}/task_1_plan.md`,
    `${S}/ui_test_plan_reviews/${BRANCH}/review_0.md`,
  ]);
  assert.equal(await f.originTip(), await f.tip());

  const tip = await f.tip();
  await f.write(`${S}/ui_test_plans/${BRANCH}_ui_test_plan.md`, 'ui index, edited\n');
  const no = await f.bash('prl_convergence_commits no');
  assert.equal(no.status, 0, no.stderr);
  assert.equal(await f.tip(), tip, 'with no, the UI-test plan is not committed and the task plan is unchanged');

  const bad = await f.bash('prl_convergence_commits maybe');
  assert.equal(bad.status, 2);
});

test('prl_ledger_flip flips one [ ] line, leaves [x] and [-] untouched, and refuses a missing line', async (t) => {
  const f = await fixture(t);
  const r = await f.bash('prl_ledger_flip P1');
  assert.equal(r.status, 0, r.stderr);
  assert.equal(await f.read(LEDGER), LEDGER_TEXT.replace('- [ ] P1.', '- [x] P1.'));
  const flip = await f.commit();
  assert.equal(flip.message, `chore: Flow progress P1 for ${BRANCH}\n`);
  assert.deepEqual(flip.files, [LEDGER]);
  assert.equal(await f.originTip(), await f.tip());

  const tip = await f.tip();
  const flipped = await f.read(LEDGER);
  for (const id of ['P1', 'P2']) {
    const again = await f.bash(`prl_ledger_flip ${id}`);
    assert.equal(again.status, 0, again.stderr);
    assert.equal(await f.read(LEDGER), flipped, `${id} unchanged`);
    assert.equal(await f.tip(), tip, `${id}: nothing committed`);
  }

  await f.write(LEDGER, flipped.replace(/^- \[ \] P3\..*\n/m, ''));
  const missing = await f.bash('prl_ledger_flip P3');
  assert.equal(missing.status, 2);
  assert.match(missing.stderr, /^planning-driver: the ledger '.*' carries no P3 line$/m);
  assert.equal(await f.tip(), tip);

  const other = await f.bash('prl_ledger_flip P0');
  assert.equal(other.status, 2);
});

test('prl_park takes the index above hr_max_question_index, answered/ and zero padding included', async (t) => {
  const f = await fixture(t);
  const clar = `${S}/clarifications/${BRANCH}`;
  await f.write(`${clar}/answered/question_3.md`, 'old\n');
  await f.write(`${clar}/question_08.md`, 'padded\n');
  await writeFile(join(f.root, 'plain.md'), 'Which storage key?\n');
  await writeFile(join(f.root, 'labelled.md'), '## Q1 — One\nA?\n\n## Q2 — Two\nB?\n');

  const r = await f.bash(`
prl_park task-plan-writer 'Questions from task-plan-writer' "${join(f.root, 'plain.md')}" || exit 1
prl_park task-plan-writer 'More questions' "${join(f.root, 'labelled.md')}" || exit 1
`);
  assert.equal(r.status, 0, r.stderr);
  assert.equal(
    await f.read(`${clar}/question_9.md`),
    '# Questions from task-plan-writer\n\nRaised by: task-plan-writer (script-driven planning)\n\n' +
      '## Q1 — Questions from task-plan-writer\n\nWhich storage key?\n',
  );
  assert.equal(
    await f.read(`${clar}/question_10.md`),
    '# More questions\n\nRaised by: task-plan-writer (script-driven planning)\n\n## Q1 — One\nA?\n\n## Q2 — Two\nB?\n',
  );
  assert.equal(await f.read(`${clar}/question_08.md`), 'padded\n');
  const log = await readFile(f.log, 'utf8');
  assert.ok(log.includes(`[plan-drive] PARKED: ${BRANCH} — 1 question(s) at ${clar}/\n`), log);
});

test('prl_pause appends to PAUSE_PROGRESS.md and writes PAUSE_ACK', async (t) => {
  const f = await fixture(t);
  await f.write(`${S}/PAUSE_PROGRESS.md`, 'earlier entry\n');
  const r = await f.bash(`prl_pause planning 'dispatch plan_review for round 2'`);
  assert.equal(r.status, 0, r.stderr);
  const progress = await f.read(`${S}/PAUSE_PROGRESS.md`);
  assert.ok(progress.startsWith('earlier entry\n'), progress);
  assert.match(progress, /\n## \d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ — feat_x paused \(script-driven planning\)\n- phase: planning\n- next step: dispatch plan_review for round 2\n$/);
  assert.ok((await f.read(`${S}/PAUSE_ACK`)).length > 0);
  assert.ok((await readFile(f.log, 'utf8')).includes(`[plan-drive] PAUSED: ${BRANCH} — planning\n`));
});

test('prl_observe_flush rewrites every machine path and commits the intake file alone', async (t) => {
  const f = await fixture(t);
  const before = await f.tip();
  const r = await f.bash(`
prl_observe nonsense p e c; [ $? -eq 2 ] || exit 1
prl_observe tooling-gap 'A wrapper call was
refused' "the call named $W/${S}/x.md and $M/s/push-branch.sh, then $HOME/.claude/settings.json
on two lines" 'one round lost' || exit 1
prl_observe_flush
`);
  assert.equal(r.status, 0, r.stderr);
  const rel = `${S}/improvement_observations/${BRANCH}.md`;
  const text = await f.read(rel);
  assert.ok(!text.includes(f.root), text);
  assert.match(text, /^# Script-driven planning — \d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ\n\n/);
  assert.ok(
    text.endsWith(
      '## A wrapper call was refused\n' +
        '- **category:** tooling-gap\n' +
        `- **evidence:** the call named ${S}/x.md and s/push-branch.sh (main checkout), then ~/.claude/settings.json on two lines\n` +
        '- **cost this run:** one round lost\n\n' +
        `${CLOSING}\n`,
    ),
    text,
  );
  const c = await f.commit();
  assert.equal(c.message, `chore: Log improvement observations for ${BRANCH}\n`);
  assert.deepEqual(c.files, [rel]);
  assert.notEqual(await f.tip(), before);
  assert.equal(await f.originTip(), await f.tip());
});

test('a flush ends on the closing label; Phase D lands under it; a resumed flush keeps one closing label, last', async (t) => {
  const f = await fixture(t);
  const rel = `${S}/improvement_observations/${BRANCH}.md`;
  const count = (text, line) => text.split('\n').filter((l) => l === line).length;
  const openings = (text) => text.split('\n').filter((l) => l.startsWith('# Script-driven planning — ')).length;

  const one = await f.bash(`prl_observe convention 'first' 'e1' 'c1' && prl_observe_flush`);
  assert.equal(one.status, 0, one.stderr);
  const first = await f.read(rel);
  assert.ok(first.endsWith(`${CLOSING}\n`), first);

  const two = await f.bash(`prl_observe convention 'second' 'e2' 'c2' && prl_observe_flush`);
  assert.equal(two.status, 0, two.stderr);
  const second = await f.read(rel);
  assert.equal(openings(second), 2);
  assert.equal(count(second, CLOSING), 1);
  assert.ok(second.endsWith(`${CLOSING}\n`), second);
  assert.ok(second.indexOf('## first') < second.indexOf('## second'));

  await appendFile(join(f.wt, rel), '\n## Phase D entry\n- **category:** convention\n- **evidence:** e\n- **cost this run:** c\n');
  const withD = await f.read(rel);
  const labels = withD.split('\n').filter((l) => l.startsWith('# '));
  assert.equal(labels.at(-1), CLOSING);
  assert.ok(withD.lastIndexOf(CLOSING) < withD.indexOf('## Phase D entry'));

  const three = await f.bash(`prl_observe convention 'third' 'e3' 'c3' && prl_observe_flush`);
  assert.equal(three.status, 0, three.stderr);
  const third = await f.read(rel);
  assert.equal(count(third, CLOSING), 2, 'a closing label with an entry under it is never touched');
  assert.ok(third.startsWith(withD.trimEnd()), 'earlier content is kept');
  assert.ok(third.endsWith(`${CLOSING}\n`));
});

test('an empty flush writes no file and commits nothing', async (t) => {
  const f = await fixture(t);
  const tip = await f.tip();
  const r = await f.bash('prl_observe_flush');
  assert.equal(r.status, 0, r.stderr);
  assert.equal(existsSync(join(f.wt, S, 'improvement_observations')), false);
  assert.equal(await f.tip(), tip);
});

/** Swap the main checkout's wrappers for stubs that record their calls. */
async function stubWrappers(f) {
  const calls = join(f.root, 'calls');
  await writeFile(
    join(f.main, 's', 'commit-on-branch.sh'),
    [
      '#!/usr/bin/env bash',
      `n=$(cat '${calls}/count' 2>/dev/null || echo 0); n=$((n + 1)); echo "$n" > '${calls}/count'`,
      `printf '%s\\037' "$@" >> '${calls}/commits'; echo >> '${calls}/commits'`,
      `if [ "$n" -eq 1 ]; then echo 'commit-on-branch.sh: committed abc1234 on feat_x, but the index could not be synced' >&2; exit 1; fi`,
      'exit "$STUB_SECOND"',
      '',
    ].join('\n'),
  );
  await writeFile(join(f.main, 's', 'push-branch.sh'), `#!/usr/bin/env bash\nprintf '%s\\n' "$*" >> '${calls}/pushes'\n`);
  await mkdir(calls);
  return {
    commits: async () => (await readFile(join(calls, 'commits'), 'utf8')).trimEnd().split('\n'),
    pushes: () => (existsSync(join(calls, 'pushes')) ? readFile(join(calls, 'pushes'), 'utf8') : ''),
  };
}

test('a landed exit 1 re-issues the identical call; exit 3 then pushes and returns 0', async (t) => {
  const f = await fixture(t);
  const stub = await stubWrappers(f);
  const r = await f.bash('prl_round_commit 4', { STUB_SECOND: '3' });
  assert.equal(r.status, 0, r.stderr);
  const commits = await stub.commits();
  assert.equal(commits.length, 2);
  assert.equal(commits[0], commits[1]);
  assert.ok(commits[0].startsWith(`--repo\x1f${f.wt}\x1f${S}/story_plans/${BRANCH}_story_plan.md\x1f`), commits[0]);
  assert.ok(commits[0].endsWith(`--\x1fchore: Plan round 4 for ${BRANCH}\x1f`), commits[0]);
  assert.equal(await stub.pushes(), `${f.wt}\n`);
});

test('a landed exit 1 whose re-sync does not exit 3 returns 2 with the re-sync cause and never pushes', async (t) => {
  const f = await fixture(t);
  const stub = await stubWrappers(f);
  const r = await f.bash('prl_round_commit 4', { STUB_SECOND: '1' });
  assert.equal(r.status, 2);
  assert.match(r.stderr, /^planning-driver: index re-sync after a landed commit exited 1$/m);
  assert.equal((await stub.commits()).length, 2);
  assert.equal(await stub.pushes(), '');
});
