/**
 * The `Set up uv` step of the `devscene-run.yml` template's `run` job.
 *
 * **The rule these tests enforce: the `run` job puts a commit-pinned `uv` on the runner, uncached and
 * skipped under DEVSCENE_REMOTE_STOP, after the job-surfaces refusal and before the checkout is
 * bootstrapped, so `setup-worktree.sh` provisions the walker's environment there.** Its place is
 * directly after `Generate the job's permission profile` and directly before `Install the sandbox
 * prerequisites`, which keeps that step adjacent to `Preflight with doctor`
 * (`workflow-sandbox-install.test.mjs`).
 *
 * It reads one fixed file, `cli/templates/` + `WORKFLOW_TEMPLATE_DIR` + `WORKFLOW_RUN_FILE`, parsed with
 * js-yaml (a cli/package.json devDependency) for the step order and read as lines for the comments
 * YAML drops. No step runs here.
 */

import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import test from 'node:test';

import { load } from 'js-yaml';

import { PACKAGE_ROOT } from './helpers/fixture.mjs';
import { WORKFLOW_RUN_FILE, WORKFLOW_TEMPLATE_DIR } from '../dist/remote/githubActions.js';

const TEXT = readFileSync(join(PACKAGE_ROOT, 'templates', WORKFLOW_TEMPLATE_DIR, WORKFLOW_RUN_FILE), 'utf8');
const LINES = TEXT.split('\n');
const STEPS = load(TEXT).jobs.run.steps;
const NAMES = STEPS.map((s) => s.name);

const STEP = 'Set up uv';
const ACTION = 'astral-sh/setup-uv';
const PIN = new RegExp(`^${ACTION}@[0-9a-f]{40}$`);
const VERSION_COMMENT = new RegExp(`^\\s*# ${ACTION} (v\\d+\\.\\d+\\.\\d+)$`);

/** The index of the `run` job step named `name`. */
function at(name) {
  const i = NAMES.indexOf(name);
  assert.notEqual(i, -1, `the run job carries the step ${name}`);
  return i;
}

test('the run job carries exactly one commit-pinned setup-uv step, its version on the line above', () => {
  const steps = STEPS.filter((s) => typeof s.uses === 'string' && s.uses.startsWith(`${ACTION}@`));
  assert.equal(steps.length, 1, 'one setup-uv step in the run job');
  assert.equal(steps[0].name, STEP);
  assert.match(steps[0].uses, PIN);

  const usesAt = LINES.findIndex((l) => l.trim() === `uses: ${steps[0].uses}`);
  assert.notEqual(usesAt, -1, 'the uses: line is found in the text');
  assert.match(LINES[usesAt - 1], VERSION_COMMENT);
});

test('the setup-uv step is uncached and skipped under DEVSCENE_REMOTE_STOP', () => {
  const step = STEPS[at(STEP)];
  assert.equal(step.if, "env.HARNESS_STOPPED != '1'");
  assert.equal(step.with?.['enable-cache'], false);
});

test('the setup-uv step sits after the refusal, between the profile and the sandbox install, before the bootstrap', () => {
  const uv = at(STEP);
  assert.ok(at("Refuse a branch that changed the job's own files") < uv, 'after the job-surfaces refusal');
  assert.equal(at("Generate the job's permission profile"), uv - 1, "directly after Generate the job's permission profile");
  assert.equal(at('Install the sandbox prerequisites'), uv + 1, 'directly before Install the sandbox prerequisites');
  assert.ok(uv < at('Preflight with doctor'), 'before Preflight with doctor');
  assert.ok(uv < at('Bootstrap the checkout'), 'before Bootstrap the checkout');
});

test('the ACTION PINS header names setup-uv at the version its step carries', () => {
  const usesAt = LINES.findIndex((l) => new RegExp(`^\\s*uses: ${ACTION}@`).test(l));
  const [, version] = VERSION_COMMENT.exec(LINES[usesAt - 1]);
  const start = LINES.indexOf('# ACTION PINS.');
  assert.notEqual(start, -1, 'the header carries an ACTION PINS block');
  const pins = [];
  for (let i = start + 1; /^# {3}\S+ +v\d/.test(LINES[i]); i++) pins.push(LINES[i].slice(1).trim().split(/ +/).join(' '));
  assert.ok(pins.includes(`${ACTION} ${version}`), `ACTION PINS lists ${ACTION} ${version}: ${pins.join(', ')}`);
});
