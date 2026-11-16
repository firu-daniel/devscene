/**
 * The shipped `commit-on-branch.sh`'s `--unit` and `--artifact` front end, driven as the permission
 * profile runs it from a linked worktree: the MAIN checkout's copy, with the worktree as its `--repo`.
 *
 * **The rule these tests exist to enforce: every unit and artifact commit is ticked, staged, worded
 * and returned by the wrapper alone, and every refusal leaves the target byte-identical** — the
 * index unticked, the worktree's git index unchanged and no new commit on `refs/heads/<branch>`.
 *
 * Not covered here: the plain form, which `cli/test/commit-on-branch-plumbing.test.mjs` and
 * `cli/test/commit-on-branch-target-check.test.mjs` pin, and the library's own functions, which
 * `cli/test/unit-commit-lib.test.mjs` pins. The fixture is built by hand rather than by `init`, the
 * same way the plumbing suite builds its own, and is this file's own.
 */

import assert from 'node:assert/strict';
import { chmod, cp, mkdir, mkdtemp, readFile, realpath, rm, symlink, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import test from 'node:test';

import { PACKAGE_ROOT, runBash, runGit } from './helpers/fixture.mjs';

const TEMPLATE_SCRIPTS = join(PACKAGE_ROOT, 'templates', 'scripts');
const CONFIG = {
  version: 1,
  defaultBranch: 'trunk',
  protectedBranches: ['trunk', 'release/*'],
  stateDir: 'devscene/',
  githooksDir: 'githooks',
  layers: [],
  commands: {},
};
const BRANCH = 'feat_w';
const HEADING = '## Phase 2 Readiness — Ordered Fix List';
const STORY = 'devscene/story_plans/feat_w_story_plan.md';
const CODE_REVIEW = 'devscene/code_reviews/feat_w_review.md';
const USER_REVIEW = 'devscene/user_reviews/feat_w_review.md';
const UI_TEST = 'devscene/ui_test_plans/feat_w_ui_test_plan.md';
const NO_DELAY = { PUSH_RETRY_DELAY_SECS: '0' };

/**
 * `push-branch.sh`'s failure lines, the categories its header's EVERY FAILURE PATH IS NON-FATAL
 * (exit 0) names: each pair is a fragment the push script prints and the `fe_push` pattern in the
 * wrapper that reports it as `pushed: failed`.
 */
const PUSH_FAILURE_LINES = [
  ['push-branch.sh: refusing to push: ', "'push-branch.sh: '*'refusing to push'*"],
  ['— refusing to push"', "'push-branch.sh: '*'refusing to push'*"],
  ["is not a git repository — nothing to push\"", "'push-branch.sh: '*' — nothing to push'"],
  ['push-branch.sh: push failed for $branch: ', "'push-branch.sh: push failed for '*': '*"],
  ['push-branch.sh: push failed for $branch after $PUSH_ATTEMPTS attempts (see output above)"', "'push-branch.sh: push failed for '*' attempts (see output above)'"],
  ['push-branch.sh: $remote no longer has $branch', "'push-branch.sh: '*' no longer has '*"],
];

const output = (result) => `${result.stdout}\n${result.stderr}`;
const quote = (value) => `'${value.replaceAll("'", "'\\''")}'`;

/** A readiness index whose entries are `entries`, numbered from 1. */
function readiness(entries, after = '') {
  return `# Plan\n\n${HEADING}\n\n${entries.map((e, i) => `${i + 1}. ${e}`).join('\n')}\n\n## Scope\n${after}`;
}

/** The `key: value` lines of a return block, as an object. */
function parseReturn(stdout) {
  const out = {};
  for (const line of stdout.split('\n')) {
    const at = line.indexOf(': ');
    if (at > 0) out[line.slice(0, at)] = line.slice(at + 2);
  }
  return out;
}

/**
 * A main checkout on `feat_main` carrying `devscene.config.json`, `githooks/`, the wrappers and
 * their `lib/`, plus `dir/gone.txt`; a bare `origin` the main configuration names; and a linked
 * worktree `wt` on `feat_w`, bootstrapped as `setup-worktree.sh` does.
 *
 * @param {import('node:test').TestContext} t
 */
async function fixture(t) {
  const root = await realpath(await mkdtemp(join(tmpdir(), 'commit-unit-')));
  t.after(() => rm(root, { recursive: true, force: true }));
  const main = join(root, 'main');
  const wt = join(root, 'wt');
  const origin = join(root, 'origin.git');
  await mkdir(main);

  await runGit(main, ['init', '--quiet', '-b', 'trunk']);
  await runGit(main, ['config', 'user.email', 'fixture@example.invalid']);
  await runGit(main, ['config', 'user.name', 'Harness Fixture']);
  await writeFile(join(main, 'devscene.config.json'), `${JSON.stringify(CONFIG)}\n`);
  await mkdir(join(main, 'githooks'));
  await writeFile(join(main, 'githooks', 'README'), 'hooks\n');
  await mkdir(join(main, 'scripts'));
  for (const name of ['commit-on-branch.sh', 'push-branch.sh', 'refresh-branch.sh']) {
    await cp(join(TEMPLATE_SCRIPTS, name), join(main, 'scripts', name));
  }
  await cp(join(TEMPLATE_SCRIPTS, 'lib'), join(main, 'scripts', 'lib'), { recursive: true });
  await mkdir(join(main, 'dir'));
  await writeFile(join(main, 'dir', 'gone.txt'), 'gone\n');
  await runGit(main, ['add', 'devscene.config.json', 'githooks', 'scripts', 'dir']);
  await runGit(main, ['commit', '--quiet', '-m', 'fixture: seed']);
  await runGit(main, ['config', 'core.hooksPath', 'githooks']);
  await runGit(main, ['checkout', '--quiet', '-b', 'feat_main']);
  await runGit(root, ['init', '--quiet', '--bare', origin]);
  await runGit(main, ['remote', 'add', 'origin', origin]);

  const addWorktree = async (path, branch) => {
    await runGit(main, ['worktree', 'add', '--quiet', '-b', branch, path, 'trunk']);
    await runGit(path, ['config', 'extensions.worktreeConfig', 'true']);
    await runGit(path, ['config', '--worktree', 'core.hooksPath', join(path, 'githooks')]);
  };
  await addWorktree(wt, BRANCH);

  const mainGit = async (...args) => (await runGit(main, args)).stdout;
  const f = {
    root,
    main,
    wt,
    origin,
    addWorktree,
    mainGit,
    /** A front-end call of the main checkout's copy against `repo` (default: the worktree). */
    call: (args, { repo = wt, env = {} } = {}) =>
      runBash(root, [join(main, 'scripts', 'commit-on-branch.sh'), '--repo', repo, ...args], { ...NO_DELAY, ...env }),
    tip: async (branch = BRANCH) => (await mainGit('rev-parse', `refs/heads/${branch}`)).trim(),
    message: async () => (await mainGit('log', '-1', '--pretty=%B', `refs/heads/${BRANCH}`)).trimEnd(),
    /** The paths the branch's tip commit changed, as `<status>\t<path>` lines. */
    changed: async () =>
      (await mainGit('show', '--name-status', '--no-renames', '--pretty=format:', `refs/heads/${BRANCH}`)).trim(),
    write: async (rel, content, base = wt) => {
      await mkdir(dirname(join(base, rel)), { recursive: true });
      await writeFile(join(base, rel), content);
    },
    read: (rel, base = wt) => readFile(join(base, rel), 'utf8'),
    /** Write and commit `files` on the worktree's branch, so the call starts from a clean tree. */
    seed: async (files, base = wt) => {
      for (const [rel, content] of Object.entries(files)) await f.write(rel, content, base);
      await runGit(base, ['add', '--', ...Object.keys(files)]);
      await runGit(base, ['commit', '--quiet', '--no-verify', '-m', 'fixture: seed index']);
    },
    status: async () => (await runGit(wt, ['status', '--porcelain', '--untracked-files=all'])).stdout,
    gitIndex: () => readFile(join(main, '.git', 'worktrees', 'wt', 'index')),
  };
  return f;
}

/** Assert a refusal left the index file, the worktree's git index and the branch untouched. */
async function assertUntouched(f, run, { code = 1, plan = STORY, error } = {}) {
  const planBefore = await f.read(plan);
  const indexBefore = await f.gitIndex();
  const tipBefore = await f.tip();
  const result = await run();
  assert.equal(result.status, code, output(result));
  assert.match(result.stdout, /^error: .+\n$/, output(result));
  if (error) assert.match(result.stdout.trimEnd(), error, output(result));
  assert.equal(await f.read(plan), planBefore, `the index changed\n${output(result)}`);
  assert.deepEqual(await f.gitIndex(), indexBefore, `the git index changed\n${output(result)}`);
  assert.equal(await f.tip(), tipBefore, `a commit landed\n${output(result)}`);
  return result;
}

test('task with a work file: ticked, staged, worded and returned', async (t) => {
  const f = await fixture(t);
  await f.seed({ [STORY]: readiness(['[ ] **Task 1** — Add `x` widget _(layer: cli)_ _(points: 5)_', '[ ] **Task 2** — Other']) });
  await f.write('src.txt', 'work\n');
  const before = await f.tip();

  const result = await f.call(['--unit', 'task', '--plan', STORY, '--id', '1']);
  assert.equal(result.status, 0, output(result));
  const after = await f.tip();
  assert.equal((await f.mainGit('rev-parse', `${after}^`)).trim(), before);
  assert.equal(
    result.stdout,
    [
      `commit_sha: ${after}`,
      'subject: feat: Task 1 — Add x widget',
      'files_committed: 2',
      'plan_flipped: 1. [x] **Task 1** — Add `x` widget _(layer: cli)_ _(points: 5)_',
      'pushed: no',
      '',
    ].join('\n'),
  );
  assert.equal(await f.message(), 'feat: Task 1 — Add x widget');
  assert.equal(await f.changed(), `M\t${STORY}\nA\tsrc.txt`);
  assert.equal(
    await f.read(STORY),
    readiness(['[x] **Task 1** — Add `x` widget _(layer: cli)_ _(points: 5)_', '[ ] **Task 2** — Other']),
  );
  assert.equal(await f.status(), '');
});

test('task index-only: the staged line and the mark-done body line', async (t) => {
  const f = await fixture(t);
  await f.seed({ [STORY]: readiness(['[ ] **Task 1** — Add x']) });

  const result = await f.call(['--unit', 'task', '--plan', STORY, '--id', '1']);
  assert.equal(result.status, 0, output(result));
  const ret = parseReturn(result.stdout);
  assert.equal(ret.subject, 'feat: Task 1 — Add x');
  assert.equal(ret.files_committed, '1');
  assert.equal(ret.staged, `index-only — ${STORY} was the whole diff; no work file was staged`);
  assert.equal(await f.message(), `feat: Task 1 — Add x\n\nmark Task 1 done — ${STORY}`);
  assert.equal(await f.changed(), `M\t${STORY}`);
});

test('a dispositioned task: the record body line, and the subject is still the title', async (t) => {
  const f = await fixture(t);
  await f.seed({ [STORY]: readiness(['[ ] **Task 1** — Add x']) });
  const detail = 'devscene/task_plans/feat_w/task_1_plan.md';
  await f.write(detail, '### Task 1\n\n## Disposition\n\n- **Cause:** tool-layer guard refused the write\n- (a) tried\n');

  const result = await f.call(['--unit', 'task', '--plan', STORY, '--id', '1']);
  assert.equal(result.status, 0, output(result));
  assert.equal(parseReturn(result.stdout).subject, 'feat: Task 1 — Add x');
  assert.equal(
    await f.message(),
    'feat: Task 1 — Add x\n\nrecord disposition of Task 1 — tool-layer guard refused the write',
  );
  assert.equal(await f.changed(), `M\t${STORY}\nA\t${detail}`);
});

test('review_item on a code-review index: the Code review finding label and the fix prefix', async (t) => {
  const f = await fixture(t);
  await f.seed({ [CODE_REVIEW]: readiness(['[ ] **Finding 1** — Fix the y _(layer: cli)_']) });
  await f.write('src.txt', 'fix\n');

  const result = await f.call(['--unit', 'review_item', '--plan', CODE_REVIEW, '--id', '1']);
  assert.equal(result.status, 0, output(result));
  assert.equal(parseReturn(result.stdout).subject, 'fix: Code review finding 1 — Fix the y');
  assert.equal(parseReturn(result.stdout).plan_flipped, '1. [x] **Finding 1** — Fix the y _(layer: cli)_');
  assert.equal(await f.message(), 'fix: Code review finding 1 — Fix the y');
  assert.equal(await f.changed(), `M\t${CODE_REVIEW}\nA\tsrc.txt`);
});

test('a user_reviews Should Fix entry: refused without --prefix, worded by it with one', async (t) => {
  const f = await fixture(t);
  await f.seed({
    [USER_REVIEW]: readiness(['[ ] **Finding 1** — Restructure z'], '\n## Should Fix\n\n### 1. Restructure z\n\nbody\n'),
  });
  await f.write('src.txt', 'z\n');

  await assertUntouched(f, () => f.call(['--unit', 'review_item', '--plan', USER_REVIEW, '--id', '1']), {
    plan: USER_REVIEW,
    error: /^error: refusing to commit: a Should Fix user-review finding needs --prefix refactor or chore$/m,
  });

  const result = await f.call(['--unit', 'review_item', '--plan', USER_REVIEW, '--id', '1', '--prefix', 'refactor']);
  assert.equal(result.status, 0, output(result));
  assert.equal(parseReturn(result.stdout).subject, 'refactor: User review finding 1 — Restructure z');
  assert.equal(await f.message(), 'refactor: User review finding 1 — Restructure z');
});

test('an already-[x] entry: committed on a dirty tree, exit 3 on a clean one', async (t) => {
  const f = await fixture(t);
  await f.seed({ [STORY]: readiness(['[x] **Task 1** — Add x']) });
  await f.write('src.txt', 'late\n');
  const planBefore = await f.read(STORY);

  const dirty = await f.call(['--unit', 'task', '--plan', STORY, '--id', '1']);
  assert.equal(dirty.status, 0, output(dirty));
  assert.equal(parseReturn(dirty.stdout).plan_flipped, 'already-[x]: 1. [x] **Task 1** — Add x — not flipped by this call');
  assert.equal(await f.changed(), 'A\tsrc.txt');
  assert.equal(await f.read(STORY), planBefore);

  const tip = await f.tip();
  const clean = await f.call(['--unit', 'task', '--plan', STORY, '--id', '1']);
  assert.equal(clean.status, 3, output(clean));
  assert.equal(clean.stdout, 'error: nothing to commit\n');
  assert.equal(await f.tip(), tip);
});

test('review_plan_file with --extra: the plan, its findings folder and the extra folder', async (t) => {
  const f = await fixture(t);
  await f.write(CODE_REVIEW, readiness(['[ ] **Finding 1** — Fix the y']));
  await f.write('devscene/code_reviews/feat_w_review/finding_1.md', 'finding\n');
  await f.write('devscene/review_extras/feat_w/notes.md', 'extra\n');
  await f.write('src.txt', 'not staged\n');

  const result = await f.call(['--unit', 'review_plan_file', '--plan', CODE_REVIEW, '--extra', 'devscene/review_extras/feat_w/']);
  assert.equal(result.status, 0, output(result));
  const ret = parseReturn(result.stdout);
  assert.equal(ret.subject, 'chore: add code review for feat_w');
  assert.equal(ret.plan_flipped, 'none');
  assert.equal(ret.files_committed, '3');
  assert.equal(
    await f.changed(),
    `A\t${CODE_REVIEW}\nA\tdevscene/code_reviews/feat_w_review/finding_1.md\nA\tdevscene/review_extras/feat_w/notes.md`,
  );
  assert.match(await f.read(CODE_REVIEW), /1\. \[ \] \*\*Finding 1\*\*/);
});

test('ui_test_pass: the plan alone, then the noop line', async (t) => {
  const f = await fixture(t);
  await f.seed({ [UI_TEST]: readiness(['[ ] **Test 1** — Log in']) });
  await f.write('src.txt', 'not staged\n');

  const result = await f.call(['--unit', 'ui_test_pass', '--plan', UI_TEST, '--id', '1']);
  assert.equal(result.status, 0, output(result));
  assert.equal(parseReturn(result.stdout).subject, 'chore: Mark UI test 1 passing for feat_w');
  assert.equal(await f.message(), 'chore: Mark UI test 1 passing for feat_w');
  assert.equal(await f.changed(), `M\t${UI_TEST}`);

  const tip = await f.tip();
  const again = await f.call(['--unit', 'ui_test_pass', '--plan', UI_TEST, '--id', '1']);
  assert.equal(again.status, 0, output(again));
  assert.equal(again.stdout, 'noop: UI test 1 already marked\n');
  assert.equal(await f.tip(), tip);
});

test('each artifact kind commits its table path under its table subject', async (t) => {
  const f = await fixture(t);
  const cases = [
    ['task-plan', [], 'devscene/task_plans/feat_w/task_1_plan.md', 'chore: Add task plan for feat_w'],
    ['plan-round', ['--round', '2'], 'devscene/plan_revisions/feat_w/r2.md', 'chore: Plan round 2 for feat_w'],
    ['plan-round-partial', ['--round', '1'], 'devscene/plan_revisions/feat_w/p1.md', 'chore: Plan round 1 partial for feat_w'],
    ['ui-test-plan', [], UI_TEST, 'chore: Add UI-test plan for feat_w'],
    ['ledger', [], 'devscene/flow_progress/feat_w_progress.md', 'chore: Add flow-progress ledger for feat_w'],
    ['ledger-flip', ['--entry', 'P1'], 'devscene/flow_progress/feat_w_progress.md', 'chore: Flow progress P1 for feat_w'],
    ['statistics', [], 'devscene/branch_statistics/feat_w/statistics.md', 'chore: Add branch statistics for feat_w'],
    ['statistics-update', [], 'devscene/branch_statistics/feat_w/statistics.md', 'chore: Update branch statistics for feat_w'],
    ['observations', [], 'devscene/improvement_observations/feat_w.md', 'chore: Log improvement observations for feat_w'],
    ['dispatch-additions', [], 'devscene/dispatch_additions/feat_w.md', 'chore: Log dispatch additions for feat_w'],
    ['clarification-digest', [], 'devscene/clarification_digests/feat_w.md', 'chore: Record clarification digest for feat_w'],
    ['lessons', [], 'devscene/lessons.md', 'chore: Record lessons for feat_w'],
    ['fix-plan', ['--round', '1'], 'devscene/user_reviews/feat_w_fix_plan.md', 'chore: Add user-review fix plan for feat_w'],
    ['fix-plan-round', ['--round', '2', '--iteration', '3'], 'devscene/user_reviews/feat_w_fix_plan_2.md', 'chore: Fix plan 2 round 3 for feat_w'],
    ['fix-plan-round-partial', ['--round', '1', '--iteration', '1'], 'devscene/plan_revisions/feat_w/fp.md', 'chore: Fix plan 1 round 1 partial for feat_w'],
    ['rescreened-input', ['--path', 'devscene/task_prompts/feat_w.md'], 'devscene/task_prompts/feat_w.md', 'chore: Commit re-screened input edit for feat_w'],
  ];
  for (const [kind, args, file, subject] of cases) {
    await f.write(file, `${kind}\n`);
    await f.write('src.txt', `${kind}: never staged by an artifact\n`);
    const result = await f.call(['--artifact', kind, ...args]);
    assert.equal(result.status, 0, `${kind}\n${output(result)}`);
    const ret = parseReturn(result.stdout);
    assert.equal(ret.subject, subject, kind);
    assert.equal(ret.plan_flipped, 'none', kind);
    assert.equal(await f.message(), subject, kind);
    assert.match(await f.changed(), new RegExp(`^[AM]\t${file.replaceAll('.', '\\.')}$`), kind);
  }
});

test('--push: pushed yes against the bare origin, and an exit 3 still pushes an earlier commit', async (t) => {
  const f = await fixture(t);
  await f.seed({ [STORY]: readiness(['[ ] **Task 1** — Add x', '[x] **Task 2** — Done']) });
  await f.write('src.txt', 'work\n');
  const originTip = async () =>
    (await runBash(f.root, ['-c', `git --git-dir=${quote(f.origin)} rev-parse --verify --quiet refs/heads/${BRANCH}`])).stdout.trim();

  const pushed = await f.call(['--unit', 'task', '--plan', STORY, '--id', '1', '--push']);
  assert.equal(pushed.status, 0, output(pushed));
  assert.equal(parseReturn(pushed.stdout).pushed, 'yes', output(pushed));
  assert.equal(await originTip(), await f.tip());

  await f.write('more.txt', 'more\n');
  const unpushed = await f.call(['--unit', 'task', '--plan', STORY, '--id', '2']);
  assert.equal(unpushed.status, 0, output(unpushed));
  assert.equal(parseReturn(unpushed.stdout).pushed, 'no');
  assert.notEqual(await originTip(), await f.tip());

  const resumed = await f.call(['--unit', 'task', '--plan', STORY, '--id', '2', '--push']);
  assert.equal(resumed.status, 3, output(resumed));
  assert.equal(resumed.stdout, 'error: nothing to commit\n');
  assert.equal(await originTip(), await f.tip());
});

test('--push reports failed on push-branch.sh failure lines', async (t) => {
  const f = await fixture(t);
  await runGit(f.main, ['remote', 'remove', 'origin']);
  await f.seed({ [STORY]: readiness(['[ ] **Task 1** — Add x']) });
  const result = await f.call(['--unit', 'task', '--plan', STORY, '--id', '1', '--push']);
  assert.equal(result.status, 0, output(result));
  assert.equal(parseReturn(result.stdout).pushed, 'failed', output(result));
  assert.match(result.stderr, /^push-branch\.sh: refusing to push: /m, output(result));
  const push = await readFile(join(TEMPLATE_SCRIPTS, 'push-branch.sh'), 'utf8');
  const wrapper = await readFile(join(TEMPLATE_SCRIPTS, 'commit-on-branch.sh'), 'utf8');
  for (const [printed, matched] of PUSH_FAILURE_LINES) {
    assert.ok(push.includes(printed), `push-branch.sh no longer prints: ${printed}`);
    assert.ok(wrapper.includes(matched), `commit-on-branch.sh no longer matches: ${matched}`);
  }
});

test('a deletion is staged as the deleted path', async (t) => {
  const f = await fixture(t);
  await f.seed({ [STORY]: readiness(['[ ] **Task 1** — Remove gone']) });
  await rm(join(f.wt, 'dir', 'gone.txt'));
  await f.write('dir/kept.txt', 'kept\n');

  const result = await f.call(['--unit', 'task', '--plan', STORY, '--id', '1']);
  assert.equal(result.status, 0, output(result));
  assert.equal(await f.changed(), `M\t${STORY}\nD\tdir/gone.txt\nA\tdir/kept.txt`);
  assert.equal(await f.status(), '');
});

/**
 * An unrelated filter-attributed file. The driver is named `marker`, not `lfs`: the wrapper drops
 * `GIT_CONFIG_GLOBAL`, so a host `~/.gitconfig` defining `filter.lfs` would run during the listing.
 */
const FILTERED = { '.gitattributes': 'kept/lfs.bin filter=marker\n', 'kept/lfs.bin': 'blob\n' };

/** Seed `top.txt`, the readiness index and `extra`, then delete `top.txt` and run `--unit task`. */
async function deleteTopLevel(t, extra = {}) {
  const f = await fixture(t);
  await f.seed({ [STORY]: readiness(['[ ] **Task 1** — Remove top']), 'top.txt': 'top\n', ...extra });
  const before = await f.tip();
  await rm(join(f.wt, 'top.txt'));
  const result = await f.call(['--unit', 'task', '--plan', STORY, '--id', '1']);
  return { f, before, result };
}

/** Seed the readiness index and `extra`, then delete the whole `dir/` and run `--unit task`. */
async function deleteDirectory(t, extra = {}) {
  const f = await fixture(t);
  await f.seed({ [STORY]: readiness(['[ ] **Task 1** — Remove dir']), ...extra });
  const before = await f.tip();
  await rm(join(f.wt, 'dir'), { recursive: true });
  const result = await f.call(['--unit', 'task', '--plan', STORY, '--id', '1']);
  return { f, before, result };
}

test('a deletion at the repository top is committed', async (t) => {
  const { f, result } = await deleteTopLevel(t);
  assert.equal(result.status, 0, output(result));
  assert.equal((await runGit(f.wt, ['ls-files', 'top.txt'])).stdout, '');
  assert.equal(await f.changed(), `M\t${STORY}\nD\ttop.txt`);
});

test('a whole-directory deletion is committed', async (t) => {
  const { f, result } = await deleteDirectory(t);
  assert.equal(result.status, 0, output(result));
  assert.equal(await f.mainGit('ls-tree', '-r', await f.tip(), '--', 'dir'), '');
  assert.equal(await f.changed(), `M\t${STORY}\nD\tdir/gone.txt`);
});

test('a top-level deletion commits beside an unrelated filtered file without touching it', async (t) => {
  const { f, before, result } = await deleteTopLevel(t, FILTERED);
  assert.equal(result.status, 0, output(result));
  assert.equal((await runGit(f.wt, ['ls-files', 'top.txt'])).stdout, '');
  const names = await f.mainGit('diff', '--name-only', before, await f.tip());
  assert.equal(names.trim(), `${STORY}\ntop.txt`);
  assert.doesNotMatch(names, /kept\/lfs\.bin|\.gitattributes/);
});

test('a whole-directory deletion commits beside an unrelated filtered file without touching it', async (t) => {
  const { f, before, result } = await deleteDirectory(t, FILTERED);
  assert.equal(result.status, 0, output(result));
  assert.equal(await f.mainGit('ls-tree', '-r', await f.tip(), '--', 'dir'), '');
  const names = await f.mainGit('diff', '--name-only', before, await f.tip());
  assert.equal(names.trim(), `${STORY}\ndir/gone.txt`);
  assert.doesNotMatch(names, /kept\/lfs\.bin|\.gitattributes/);
});

test('a findings folder is staged whole and counted as index, not work', async (t) => {
  const f = await fixture(t);
  await f.seed({ [CODE_REVIEW]: readiness(['[ ] **Finding 1** — Fix the y']) });
  const folder = 'devscene/code_reviews/feat_w_review/';
  await f.write(`${folder}finding_1.md`, 'finding\n');
  await f.write(`${folder}finding_2.md`, 'another\n');

  const result = await f.call(['--unit', 'review_item', '--plan', CODE_REVIEW, '--id', '1', '--findings', folder]);
  assert.equal(result.status, 0, output(result));
  assert.match(parseReturn(result.stdout).staged, /^index-only — devscene\/code_reviews\/feat_w_review\.md, devscene\/code_reviews\/feat_w_review was the whole diff; no work file was staged$/);
  assert.equal(
    await f.changed(),
    `M\t${CODE_REVIEW}\nA\t${folder}finding_1.md\nA\t${folder}finding_2.md`,
  );
});

test('every new refusal leaves the index, the git index and the branch byte-identical', async (t) => {
  const f = await fixture(t);
  await f.seed({
    [STORY]: readiness(['[ ] **Task 1** — Add x']),
    [CODE_REVIEW]: readiness(['[ ] **Finding 1** — Fix the y']),
    'notes/plan.md': readiness(['[ ] **Task 1** — Add x']),
    'devscene/other/feat_w.md': readiness(['[ ] **Task 1** — Add x']),
  });
  await f.write('src.txt', 'work\n');
  await mkdir(join(f.wt, 'devscene', 'story_plans', 'dir.md'));
  await f.write('elsewhere/feat_w_story_plan.md', readiness(['[ ] **Task 1** — Add x']));
  await symlink(join(f.wt, 'elsewhere'), join(f.wt, 'devscene', 'linked'));

  const task = ['--unit', 'task', '--plan', STORY, '--id', '1'];
  const usage = [
    [[...task, '--', 'feat: x'], /^error: a front-end flag cannot be combined with '--' and a message$/],
    [[...task, '--artifact', 'ledger'], /^error: --unit and --artifact cannot be combined$/],
    [[...task, '--extra', 'devscene/x/'], /^error: --extra is not taken by --unit task$/],
    [['--unit', 'task', '--plan', STORY], /^error: --unit task needs --id <K>$/],
    [['--unit', 'task', '--plan', STORY, '--id', 'one'], /^error: --id 'one' is not a number$/],
    [['--artifact', 'ledger', '--path', 'x.md'], /^error: --path is not taken by --artifact ledger$/],
    [['--artifact', 'rescreened-input'], /^error: --artifact rescreened-input needs at least one --path$/],
    [['--plan', STORY], /^error: a front-end flag needs --unit or --artifact$/],
  ];
  for (const [args, error] of usage) {
    const result = await assertUntouched(f, () => f.call(args), { error });
    assert.match(result.stderr, /usage: commit-on-branch\.sh/, output(result));
  }

  const refused = [
    [['--unit', 'task', '--plan', join(f.wt, STORY), '--id', '1'], /^error: refusing to commit: --plan '.*' is not a path relative to /],
    [['--unit', 'task', '--plan', 'devscene/../devscene/story_plans/feat_w_story_plan.md', '--id', '1'], /^error: refusing to commit: --plan '.*' has a '\.\.' segment$/],
    [['--unit', 'task', '--plan', 'notes/plan.md', '--id', '1'], /^error: refusing to commit: --plan 'notes\/plan\.md' is not under 'devscene\/'$/],
    [['--unit', 'task', '--plan', 'devscene/linked/feat_w_story_plan.md', '--id', '1'], /^error: refusing to commit: --plan '.*' is reached through the symbolic link 'devscene\/linked'$/],
    [['--unit', 'task', '--plan', 'devscene/story_plans/dir.md', '--id', '1'], /^error: refusing to commit: --plan '.*' is not a regular file$/],
    [[...task, '--findings', '/tmp'], /^error: refusing to commit: --findings '\/tmp' is not a path relative to /],
    [[...task, '--findings', 'notes/'], /^error: refusing to commit: --findings 'notes' is not under 'devscene\/'$/],
    [['--unit', 'review_plan_file', '--plan', CODE_REVIEW, '--extra', 'devscene/../x'], /^error: refusing to commit: --extra '.*' has a '\.\.' segment$/],
    [['--artifact', 'rescreened-input', '--path', '/etc/hosts'], /^error: refusing to commit: --path '\/etc\/hosts' is not a path relative to /],
    [['--unit', 'task', '--plan', 'devscene/other/feat_w.md', '--id', '1'], /^error: refusing to commit: --plan 'devscene\/other\/feat_w\.md' is not a readiness index this wrapper can classify$/],
    [['--unit', 'task', '--plan', CODE_REVIEW, '--id', '1'], /^error: refusing to commit: --plan '.*' is a code_review index, which --unit task does not take$/],
    [['--unit', 'ui_test_pass', '--plan', STORY, '--id', '1'], /^error: refusing to commit: --plan '.*' is a story index, which --unit ui_test_pass does not take$/],
    [['--unit', 'task', '--plan', STORY, '--id', '9'], /^error: --id 9 matched no readiness entry in devscene\/story_plans\/feat_w_story_plan\.md$/],
    [['--artifact', 'no-such-kind'], /^error: refusing to commit: 'no-such-kind' is not an artifact kind$/],
  ];
  for (const [args, error] of refused) {
    await assertUntouched(f, () => f.call(args), { error });
  }
});

test('a commit refused after the tick restores the index', async (t) => {
  const f = await fixture(t);
  await f.seed({ [STORY]: readiness(['[ ] **Task 1** — Add x']), '.gitattributes': 'src.txt filter=marker\n' });
  await f.write('src.txt', 'work\n');
  await assertUntouched(f, () => f.call(['--unit', 'task', '--plan', STORY, '--id', '1']), {
    error: /^error: refusing to commit: 'src\.txt' selects a filter driver, which this wrapper never runs$/,
  });
});

test('a protected branch exits 2 with the index unticked', async (t) => {
  const f = await fixture(t);
  const rel = join(f.root, 'rel');
  await f.addWorktree(rel, 'release/x');
  await f.seed({ [STORY]: readiness(['[ ] **Task 1** — Add x']) }, rel);
  const plan = await f.read(STORY, rel);
  const tip = await f.tip('release/x');

  const result = await f.call(['--unit', 'task', '--plan', STORY, '--id', '1', '--push'], { repo: rel });
  assert.equal(result.status, 2, output(result));
  assert.equal(result.stdout, "error: branch 'release/x' is protected — refusing to commit\n");
  assert.equal(await f.read(STORY, rel), plan);
  assert.equal(await f.tip('release/x'), tip);
  assert.equal((await runBash(f.root, ['-c', `git --git-dir=${quote(f.origin)} for-each-ref`])).stdout, '');
});

test('a landed commit whose index sync fails still returns, exit 0', async (t) => {
  const f = await fixture(t);
  await f.seed({ [STORY]: readiness(['[ ] **Task 1** — Add x']) });
  await f.write('src.txt', 'work\n');
  // The record's index lock appears just before the ref moves, so the commit lands and the sync fails.
  const realGit = (await runBash(f.root, ['-c', 'command -v git'])).stdout.trim();
  const bin = join(f.root, 'shim-bin');
  await mkdir(bin);
  const lock = join(f.main, '.git', 'worktrees', 'wt', 'index.lock');
  const done = join(f.root, 'flip-done');
  await writeFile(
    join(bin, 'git'),
    `#!/bin/sh\nif [ ! -e ${quote(done)} ]; then case " $* " in *" update-ref "*) : > ${quote(done)}; : > ${quote(lock)} ;; esac; fi\nexec ${quote(realGit)} "$@"\n`,
  );
  await chmod(join(bin, 'git'), 0o755);
  const before = await f.tip();

  const result = await f.call(['--unit', 'task', '--plan', STORY, '--id', '1'], { env: { PATH: `${bin}:${process.env.PATH}` } });
  assert.equal(result.status, 0, output(result));
  const after = await f.tip();
  assert.notEqual(after, before);
  const ret = parseReturn(result.stdout);
  assert.equal(ret.commit_sha, after);
  assert.equal(ret.subject, 'feat: Task 1 — Add x');
  assert.match(ret.index_sync, /^failed — exit [0-9]+, /, output(result));
  assert.match(result.stderr, /^commit-on-branch\.sh: committed [0-9a-f]+ on feat_w, but the index of /m);
});
