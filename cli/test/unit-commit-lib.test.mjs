/**
 * The unit and artifact commit library, `cli/templates/scripts/lib/unit-commit-lib.sh`.
 *
 * **The rule this suite enforces: every unit and artifact commit subject is built from the
 * readiness index or the library's artifact table, never from a caller's text.** Each case
 * sources the template library in one `bash` process and drives one function against index,
 * detail and listing files written under the system temp directory and removed in process; the
 * artifact rows are asserted byte-for-byte against the table the story plan fixes.
 */

import assert from 'node:assert/strict';
import { mkdtemp, readFile, realpath, rm, stat, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import test from 'node:test';

import { PACKAGE_ROOT, runBash } from './helpers/fixture.mjs';

const LIB = join(PACKAGE_ROOT, 'templates', 'scripts', 'lib', 'unit-commit-lib.sh');
const READINESS = '## Phase 2 Readiness — Ordered Fix List';

async function scratch(t) {
  const dir = await realpath(await mkdtemp(join(tmpdir(), 'unit-commit-lib-')));
  t.after(() => rm(dir, { recursive: true, force: true }));
  return dir;
}

/** Source the library, then run `script`; `env` carries every value the script reads. */
function ucl(dir, script, env = {}) {
  return runBash(dir, ['-c', `. "$UCL_LIB" || exit 99\n${script}`], { UCL_LIB: LIB, ...env });
}

function lines(stdout) {
  return stdout.split('\n').slice(0, -1);
}

const STORY_INDEX = [
  '# Story',
  '',
  '- [ ] **Task 3** — a sub-step bullet outside the readiness section',
  '',
  READINESS,
  '',
  '1. [ ] **Task 3** — Add `ucl_tick`, the $tick | <helper> _(layer: cli)_ _(points: 5)_',
  '   - [ ] **Task 3** — a sub-step inside the section',
  '2. [x] **Task 1** — Already done _(layer: cli)_',
  '3. [ ] **Task 31** — A longer token _(layer: plugin)_',
  '',
  '## Notes',
  '',
  '1. [ ] **Task 5** — Outside the section',
].join('\n');

test('ucl_entry_find resolves a token by K, never by walk position or outside the section', async (t) => {
  const dir = await scratch(t);
  const index = join(dir, 'index.md');
  await writeFile(index, STORY_INDEX);
  const probe = (word, k) =>
    ucl(dir, `ucl_entry_find "$I" ${word} ${k}; rc=$?; printf '%s\\n%s\\n%s\\n%s\\n' "$rc" "$UCL_ENTRY_LINENO" "$UCL_ENTRY_STATE" "$UCL_ENTRY_LINE"`, { I: index });

  const three = await probe('Task', '3');
  assert.deepEqual(lines(three.stdout).slice(0, 3), ['0', '7', 'open']);
  assert.match(lines(three.stdout)[3], /^1\. \[ \] \*\*Task 3\*\* — Add/);

  assert.deepEqual(lines((await probe('Task', '1')).stdout).slice(0, 3), ['0', '9', 'done']);
  assert.deepEqual(lines((await probe('Task', '31')).stdout).slice(0, 3), ['0', '10', 'open']);
  assert.equal(lines((await probe('Task', '5')).stdout)[0], '1');
  assert.equal(lines((await probe('Finding', '3')).stdout)[0], '1');

  const bad = await probe('Story', '3');
  assert.equal(lines(bad.stdout)[0], '2');
  assert.match(bad.stderr, /^unit-commit-lib: /);
});

test('ucl_tick changes exactly one line and leaves the file mode 644', async (t) => {
  const dir = await scratch(t);
  const index = join(dir, 'index.md');
  const before = `${STORY_INDEX}\r\n- [ ] trailing line with no newline`;
  await writeFile(index, before, { mode: 0o600 });

  const r = await ucl(dir, 'ucl_tick "$I" 7; echo "$?"', { I: index });
  assert.equal(r.stdout, '0\n', r.stderr);
  const after = await readFile(index, 'utf8');
  assert.equal(after, before.replace('1. [ ] **Task 3**', '1. [x] **Task 3**'));
  assert.equal((await stat(index)).mode & 0o777, 0o644);

  assert.equal((await ucl(dir, 'ucl_tick "$I" 7; echo "$?"', { I: index })).stdout, '1\n');
  assert.equal((await ucl(dir, 'ucl_tick "$I" 8 2>/dev/null; echo "$?"', { I: index })).stdout, '2\n');
  assert.equal(await readFile(index, 'utf8'), after);
});

test('ucl_short_title strips the tags and normalises the title', async (t) => {
  const dir = await scratch(t);
  const entry = '1. [ ] **Task 3** — Add `ucl_tick`, the $tick | <helper> _(layer: cli)_ _(points: 5)_';
  const r = await ucl(dir, 'ucl_short_title "$E"; printf "%s\\n" "$UCL_OUT"', { E: entry });
  assert.equal(r.stdout, 'Add ucl_tick, the tick helper\n');
});

test('ucl_normalise drops each of the five marks and turns control characters into spaces', async (t) => {
  const dir = await scratch(t);
  for (const [input, expected] of [
    ['a`b', 'ab'],
    ['a$b', 'ab'],
    ['a|b', 'ab'],
    ['a<b', 'ab'],
    ['a>b', 'ab'],
    ['  one\ttwo\nthree\r\nfour   five  ', 'one two three four five'],
  ]) {
    const r = await ucl(dir, 'ucl_normalise "$T"; printf "%s\\n" "$UCL_OUT"', { T: input });
    assert.equal(r.stdout, `${expected}\n`, JSON.stringify(input));
  }
});

test('ucl_subject cuts at a word boundary within 72 bytes and drops a title whose first word cannot fit', async (t) => {
  const dir = await scratch(t);
  const subject = async (title) =>
    (await ucl(dir, 'ucl_subject fix "Code review finding 12" "$T"; printf "%s\\n" "$UCL_SUBJECT"', { T: title })).stdout.slice(0, -1);

  const cut = await subject('alpha bravo charlie delta echo foxtrot golf hotel india');
  assert.equal(cut, 'fix: Code review finding 12 — alpha bravo charlie delta echo foxtrot');
  assert.equal(Buffer.byteLength(cut), 70);
  assert.equal(await subject('Short title'), 'fix: Code review finding 12 — Short title');
  assert.equal(await subject('x'.repeat(50)), 'fix: Code review finding 12');
});

test('ucl_unit_label labels every kind and keeps the body token', async (t) => {
  const dir = await scratch(t);
  const expected = {
    story: ['Task 4', 'Task 4'],
    code_review: ['Code review finding 4', 'Finding 4'],
    parity_review: ['Parity review finding 4', 'Finding 4'],
    arch_review: ['Architecture review finding 4', 'Finding 4'],
    skeptic_review: ['Skeptic review finding 4', 'Finding 4'],
    qa_review: ['QA finding 4', 'Finding 4'],
    test_fix: ['Test fix 4', 'Finding 4'],
    user_review: ['User review finding 4', 'Finding 4'],
  };
  for (const [kind, pair] of Object.entries(expected)) {
    const r = await ucl(dir, `ucl_unit_label ${kind} 4; printf '%s\\n%s\\n%s\\n' "$?" "$UCL_LABEL" "$UCL_TOKEN"`);
    assert.deepEqual(lines(r.stdout), ['0', ...pair], kind);
  }
  assert.equal(lines((await ucl(dir, 'ucl_unit_label ui_test 4; echo "$?"')).stdout)[0], '1');
  assert.equal(lines((await ucl(dir, 'ucl_unit_label nope 4 2>/dev/null; echo "$?"')).stdout)[0], '2');
});

test('ucl_unit_prefix maps the three user-review severities and refuses a misplaced or illegal --prefix', async (t) => {
  const dir = await scratch(t);
  const prefix = async (kind, branch, sev, arg) => {
    const r = await ucl(dir, 'ucl_unit_prefix "$K" "$B" "$S" "$P"; printf "%s\\n%s\\n" "$?" "$UCL_OUT"', { K: kind, B: branch, S: sev, P: arg });
    return { out: lines(r.stdout), stderr: r.stderr };
  };
  assert.deepEqual((await prefix('user_review', 'feat_x', 'must', '')).out, ['0', 'fix']);
  assert.deepEqual((await prefix('user_review', 'feat_x', 'nice', '')).out, ['0', 'chore']);
  assert.deepEqual((await prefix('user_review', 'feat_x', 'should', 'refactor')).out, ['0', 'refactor']);
  assert.deepEqual((await prefix('user_review', 'feat_x', 'should', 'chore')).out, ['0', 'chore']);
  assert.equal((await prefix('user_review', 'feat_x', 'should', '')).out[0], '2');
  assert.equal((await prefix('user_review', 'feat_x', 'should', 'feat')).out[0], '2');
  const misplaced = await prefix('user_review', 'feat_x', 'must', 'chore');
  assert.equal(misplaced.out[0], '2');
  assert.match(misplaced.stderr, /^unit-commit-lib: /);
  assert.equal((await prefix('code_review', 'feat_x', '', 'refactor')).out[0], '2');
  assert.deepEqual((await prefix('code_review', 'feat_x', '', '')).out, ['0', 'fix']);
  assert.deepEqual((await prefix('story', 'feat_x', '', '')).out, ['0', 'feat']);
  assert.deepEqual((await prefix('story', 'refactor_x', '', '')).out, ['0', 'refactor']);
  assert.deepEqual((await prefix('story', 'docs_x', '', '')).out, ['0', 'chore']);
});

test('ucl_severity reads the section a pointer heading sits under', async (t) => {
  const dir = await scratch(t);
  const index = join(dir, 'review.md');
  await writeFile(index, ['## Must Fix', '', '### 1. One', '', '## Should Fix', '', '### 2. Two', '', '## Nice to Have', '', '### 3. Three', '', '## Out of scope', '', '### 4. Four'].join('\n'));
  for (const [k, sev] of [['1', 'must'], ['2', 'should'], ['3', 'nice'], ['4', '']]) {
    const r = await ucl(dir, `ucl_severity "$I" ${k}; printf '%s\\n%s\\n' "$?" "$UCL_OUT"`, { I: index });
    assert.deepEqual(lines(r.stdout), ['0', sev], k);
  }
  assert.equal(lines((await ucl(dir, 'ucl_severity "$I" 9; echo "$?"', { I: index })).stdout)[0], '1');
});

test('ucl_index_kind classifies by the directory under the state dir and names the per-finding folder', async (t) => {
  const dir = await scratch(t);
  const kind = async (plan) =>
    lines((await ucl(dir, 'ucl_index_kind devscene/ "$P"; printf "%s\\n%s\\n%s\\n" "$?" "$UCL_KIND" "$UCL_FINDINGS_DIR"', { P: plan })).stdout);
  assert.deepEqual(await kind('devscene/story_plans/b_story_plan.md'), ['0', 'story', 'devscene/story_plans/b_story_plan/']);
  assert.deepEqual(await kind('devscene/code_reviews/b_code_review_2.md'), ['0', 'code_review', 'devscene/code_reviews/b_code_review_2/']);
  assert.deepEqual(await kind('devscene/business_parity_branch_reviews/b.md'), ['0', 'parity_review', 'devscene/business_parity_branch_reviews/b/']);
  assert.deepEqual(await kind('devscene/architecture_branch_reviews/b.md'), ['0', 'arch_review', 'devscene/architecture_branch_reviews/b/']);
  assert.deepEqual(await kind('devscene/skeptic_reviews/b.md'), ['0', 'skeptic_review', 'devscene/skeptic_reviews/b/']);
  assert.deepEqual(await kind('devscene/qa_reviews/b/qa_review_2.md'), ['0', 'qa_review', 'devscene/qa_reviews/b/']);
  assert.deepEqual(await kind('devscene/test_fix_plans/b_task_round_1.md'), ['0', 'test_fix', 'devscene/test_fix_plans/b_task_round_1/']);
  assert.deepEqual(await kind('devscene/user_reviews/b_fix_plan_2.md'), ['0', 'user_review', 'devscene/user_reviews/b_fix_plan_2/']);
  assert.deepEqual(await kind('devscene/ui_test_plans/b_ui_test_plan.md'), ['0', 'ui_test', 'devscene/ui_test_plans/b_ui_test_plan/']);
  assert.equal((await kind('devscene/task_plans/b/task_1_plan.md'))[0], '1');
  assert.equal((await kind('elsewhere/story_plans/b_story_plan.md'))[0], '1');
});

test('ucl_detail_file reads the pointer section, else falls back to finding_<K>.md', async (t) => {
  const dir = await scratch(t);
  const index = join(dir, 'b_code_review.md');
  await writeFile(index, ['## Must Fix', '', '### 1. One', '→ [finding_1.md](b_code_review/finding_one.md)', '', '### 2. Two', 'no pointer', ''].join('\n'));
  const detail = async (kind, k) =>
    lines((await ucl(dir, `ucl_index_kind devscene devscene/code_reviews/b_code_review.md; ucl_detail_file ${kind} devscene feat_x ${k} "$I"; printf '%s\\n%s\\n' "$?" "$UCL_OUT"`, { I: index })).stdout);
  assert.deepEqual(await detail('code_review', 1), ['0', 'devscene/code_reviews/b_code_review/finding_one.md']);
  assert.deepEqual(await detail('code_review', 2), ['0', 'devscene/code_reviews/b_code_review/finding_2.md']);
  assert.deepEqual(await detail('story', 3), ['0', 'devscene/task_plans/feat_x/task_3_plan.md']);
});

test('ucl_record_cause reads the **Cause:** line, with its absent-line fallback', async (t) => {
  const dir = await scratch(t);
  const file = join(dir, 'task_3_plan.md');
  await writeFile(file, [
    '# Task 3',
    '- **Cause:** not this one, it is outside the section',
    '## Disposition',
    '- (a) attempted',
    '- **Cause:** tool-layer guard refused the write to `.claude/x` | twice',
    '## Already passing',
    '- (a) the test',
    '## After',
    '- **Cause:** not this one either',
  ].join('\n'));
  const cause = async (section) =>
    lines((await ucl(dir, 'ucl_record_cause "$F" "$S" devscene/task_plans/b/task_3_plan.md; printf "%s\\n%s\\n" "$?" "$UCL_OUT"', { F: file, S: section })).stdout);
  assert.deepEqual(await cause('Disposition'), ['0', 'tool-layer guard refused the write to .claude/x twice']);
  assert.deepEqual(await cause('Already passing'), ['0', 'cause not recorded — see devscene/task_plans/b/task_3_plan.md']);
  await writeFile(file, '# Task 3\n');
  assert.equal((await cause('Disposition'))[0], '1');
});

test('ucl_body_record writes each record and keeps their precedence', async (t) => {
  const dir = await scratch(t);
  const record = async (disp, ap, work, set) =>
    lines((await ucl(dir, 'ucl_body_record "Task 3" "$D" "$A" "$W" "$S"; printf "%s\\n%s\\n" "$?" "$UCL_OUT"', { D: disp, A: ap, W: work, S: set })).stdout);
  const set = 'devscene/story_plans/b_story_plan.md, devscene/task_plans/b/task_3_plan.md';
  assert.deepEqual(await record('refused', 'passing', '0', set), ['0', 'record disposition of Task 3 — refused']);
  assert.deepEqual(await record('', 'passing', '0', set), ['0', 'mark Task 3 already passing — passing']);
  assert.deepEqual(await record('', '', '0', set), ['0', `mark Task 3 done — ${set}`]);
  assert.deepEqual(await record('', '', '2', set), ['1', '']);
  assert.deepEqual(await record('refused', '', '2', set), ['0', 'record disposition of Task 3 — refused']);
});

/** The listing `commit-on-branch.sh` writes: name-status records, `--others`, untracked paths. */
function listing(diff, others) {
  return `${[...diff, '--others', ...others].join('\0')}\0`;
}

async function stageSet(t, records, others, args) {
  const dir = await scratch(t);
  const file = join(dir, 'listing');
  const out = join(dir, 'stage');
  await writeFile(file, listing(records, others));
  const r = await ucl(dir, 'UCL_STAGE_FILE="$O"; ucl_stage_set "$L" "$P" "$F" "$D" "$X"; printf "%s\\n%s\\n%s\\n" "$?" "$UCL_WORK_COUNT" "$UCL_INDEX_ONLY_SET"', {
    O: out,
    L: file,
    ...args,
  });
  const [status, work, set] = lines(r.stdout);
  const staged = status === '0' ? (await readFile(out, 'utf8')).split('\0').slice(0, -1) : [];
  return { status, work: Number(work), set, staged, stderr: r.stderr };
}

const PLAN = 'devscene/story_plans/b_story_plan.md';
const DETAIL = 'devscene/task_plans/b/task_3_plan.md';
const FINDINGS = 'devscene/task_plan_point_reviews/b_task_plan/task_3/';

test('ucl_stage_set stages a deletion as its parent directory and excludes the findings folder from the work count', async (t) => {
  const r = await stageSet(
    t,
    ['M', PLAN, 'D', 'src/a/old.ts', 'D', 'src/a/older.ts', 'M', 'src/b.ts'],
    [`${FINDINGS}review_1.md`, 'src/c.ts'],
    { P: PLAN, F: FINDINGS, D: DETAIL, X: '' },
  );
  assert.equal(r.status, '0', r.stderr);
  assert.deepEqual(r.staged, [PLAN, FINDINGS, 'src/a/', 'src/b.ts', 'src/c.ts']);
  assert.equal(r.work, 3);
  assert.equal(r.set, `${PLAN}, ${FINDINGS}`);
});

test('ucl_stage_set reports an index-only set', async (t) => {
  const fdir = 'devscene/code_reviews/b_code_review/';
  const r = await stageSet(t, ['M', 'devscene/code_reviews/b_code_review.md', 'M', `${fdir}finding_2.md`], [], {
    P: 'devscene/code_reviews/b_code_review.md',
    F: '',
    D: `${fdir}finding_2.md`,
    X: fdir,
  });
  assert.equal(r.status, '0', r.stderr);
  assert.deepEqual(r.staged, ['devscene/code_reviews/b_code_review.md', `${fdir}finding_2.md`]);
  assert.equal(r.work, 0);
  assert.equal(r.set, `devscene/code_reviews/b_code_review.md, ${fdir}finding_2.md`);
});

test('ucl_stage_set refuses a deletion at the repository top', async (t) => {
  const r = await stageSet(t, ['D', 'README.md'], [], { P: PLAN, F: '', D: DETAIL, X: '' });
  assert.equal(r.status, '2');
  assert.match(r.stderr, /^unit-commit-lib: /);
});

const S = 'devscene';
const B = 'feat_x';
const PLAN_ROUND_PATHS = [
  `${S}/story_plans/${B}_story_plan.md`,
  `${S}/task_plans/${B}/`,
  `${S}/task_plan_reviews/${B}/`,
  `${S}/business_parity_reviews/${B}/`,
  `${S}/architecture_reviews/${B}/`,
  `${S}/plan_revisions/${B}/`,
];
const fixPlanRoundPaths = (round, sfx) => [
  `${S}/user_reviews/${B}_fix_plan${sfx}.md`,
  `${S}/user_reviews/${B}_fix_plan${sfx}/`,
  `${S}/business_parity_user_review_reviews/${B}/user_review_${round}/`,
  `${S}/architecture_user_review_reviews/${B}/user_review_${round}/`,
  `${S}/plan_revisions/${B}/`,
];

/** Each row: kind, round, iteration, entry → subject and paths, as the story plan's table fixes them. */
const ARTIFACT_ROWS = [
  ['task-plan', '', '', '', `chore: Add task plan for ${B}`, [...PLAN_ROUND_PATHS, `${S}/ui_test_plan_reviews/${B}/`]],
  ['plan-round', '2', '', '', `chore: Plan round 2 for ${B}`, PLAN_ROUND_PATHS],
  ['plan-round-partial', '2', '', '', `chore: Plan round 2 partial for ${B}`, PLAN_ROUND_PATHS],
  ['ui-test-plan', '', '', '', `chore: Add UI-test plan for ${B}`, [`${S}/ui_test_plans/${B}_ui_test_plan.md`, `${S}/ui_test_plans/${B}/`]],
  ['ledger', '', '', '', `chore: Add flow-progress ledger for ${B}`, [`${S}/flow_progress/${B}_progress.md`]],
  ['ledger-flip', '', '', 'A1.5f', `chore: Flow progress A1.5f for ${B}`, [`${S}/flow_progress/${B}_progress.md`]],
  ['statistics', '', '', '', `chore: Add branch statistics for ${B}`, [`${S}/branch_statistics/${B}/statistics.md`]],
  ['statistics-update', '', '', '', `chore: Update branch statistics for ${B}`, [`${S}/branch_statistics/${B}/statistics.md`]],
  ['observations', '', '', '', `chore: Log improvement observations for ${B}`, [`${S}/improvement_observations/${B}.md`]],
  ['dispatch-additions', '', '', '', `chore: Log dispatch additions for ${B}`, [`${S}/dispatch_additions/${B}.md`]],
  ['clarification-digest', '', '', '', `chore: Record clarification digest for ${B}`, [`${S}/clarification_digests/${B}.md`]],
  ['lessons', '', '', '', `chore: Record lessons for ${B}`, [`${S}/lessons.md`]],
  [
    'fix-plan',
    '1',
    '',
    '',
    `chore: Add user-review fix plan for ${B}`,
    [
      `${S}/user_reviews/${B}_fix_plan.md`,
      `${S}/user_reviews/${B}_review.md`,
      `${S}/user_reviews/${B}_fix_plan/`,
      `${S}/business_parity_user_review_reviews/${B}/`,
      `${S}/architecture_user_review_reviews/${B}/`,
      `${S}/plan_revisions/${B}/`,
    ],
  ],
  [
    'fix-plan',
    '3',
    '',
    '',
    `chore: Add user-review fix plan for ${B}`,
    [
      `${S}/user_reviews/${B}_fix_plan_3.md`,
      `${S}/user_reviews/${B}_review_3.md`,
      `${S}/user_reviews/${B}_fix_plan_3/`,
      `${S}/business_parity_user_review_reviews/${B}/`,
      `${S}/architecture_user_review_reviews/${B}/`,
      `${S}/plan_revisions/${B}/`,
    ],
  ],
  ['fix-plan-round', '2', '4', '', `chore: Fix plan 2 round 4 for ${B}`, fixPlanRoundPaths('2', '_2')],
  ['fix-plan-round-partial', '1', '3', '', `chore: Fix plan 1 round 3 partial for ${B}`, fixPlanRoundPaths('1', '')],
  ['rescreened-input', '', '', '', `chore: Commit re-screened input edit for ${B}`, []],
];

async function artifact(dir, kind, round, iteration, entry) {
  const r = await ucl(dir, 'ucl_artifact "$K" devscene/ feat_x "$R" "$N" "$E"; rc=$?; printf "%s\\n%s\\n" "$rc" "$UCL_SUBJECT"; [ "${#UCL_PATHS[@]}" -eq 0 ] || printf "%s\\n" "${UCL_PATHS[@]}"', {
    K: kind,
    R: round,
    N: iteration,
    E: entry,
  });
  const [status, subject, ...paths] = lines(r.stdout);
  return { status, subject, paths, stderr: r.stderr };
}

test('ucl_artifact returns every row of the artifact table byte-for-byte', async (t) => {
  const dir = await scratch(t);
  for (const [kind, round, iteration, entry, subject, paths] of ARTIFACT_ROWS) {
    const r = await artifact(dir, kind, round, iteration, entry);
    assert.equal(r.status, '0', `${kind}: ${r.stderr}`);
    assert.equal(r.subject, subject, kind);
    assert.deepEqual(r.paths, paths, kind);
  }
});

test('each partial row carries its round row’s paths and a subject differing only by " partial"', async (t) => {
  const dir = await scratch(t);
  for (const [whole, partial, round, iteration] of [
    ['plan-round', 'plan-round-partial', '3', ''],
    ['fix-plan-round', 'fix-plan-round-partial', '2', '4'],
  ]) {
    const a = await artifact(dir, whole, round, iteration, '');
    const b = await artifact(dir, partial, round, iteration, '');
    assert.equal(a.status, '0', a.stderr);
    assert.equal(b.status, '0', b.stderr);
    assert.deepEqual(b.paths, a.paths, partial);
    assert.equal(b.subject, a.subject.replace(` for ${B}`, ` partial for ${B}`), partial);
    assert.notEqual(b.subject, a.subject);
  }
  const first = await artifact(dir, 'fix-plan-round-partial', '1', '4', '');
  assert.deepEqual(first.paths, fixPlanRoundPaths('1', ''));
});

test('ucl_artifact refuses an unknown kind, a missing round and an illegal entry id', async (t) => {
  const dir = await scratch(t);
  for (const [kind, round, iteration, entry] of [
    ['nope', '', '', ''],
    ['plan-round', '', '', ''],
    ['plan-round-partial', 'x', '', ''],
    ['fix-plan-round', '2', '', ''],
    ['ledger-flip', '', '', 'P1;x'],
    ['ledger-flip', '', '', ''],
  ]) {
    const r = await artifact(dir, kind, round, iteration, entry);
    assert.equal(r.status, '2', `${kind} ${round} ${iteration} ${entry}`);
    assert.match(r.stderr, /^unit-commit-lib: /);
  }
});

test('the two fixed --unit subjects', async (t) => {
  const dir = await scratch(t);
  const r = await ucl(dir, 'ucl_review_kind_subject feat_x; printf "%s\\n" "$UCL_SUBJECT"; ucl_ui_pass_subject 4 feat_x; printf "%s\\n" "$UCL_SUBJECT"');
  assert.deepEqual(lines(r.stdout), ['chore: add code review for feat_x', 'chore: Mark UI test 4 passing for feat_x']);
});
