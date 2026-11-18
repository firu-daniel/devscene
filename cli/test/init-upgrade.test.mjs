/**
 * `init --upgrade` end to end, through the compiled CLI against wired fixture repositories.
 *
 * **The rule this suite exists to enforce: one run brings the outer-loop scripts and the permission
 * profile up to this CLI, reports what changed, and leaves every other file alone; a refused run and
 * a dry run leave the tree byte-identical.**
 *
 * Every run gets its own agent-runner home, so no plugin installed on the host reaches a profile or
 * the report. Expected script bytes come from the shipped template because "copied verbatim" is the
 * contract, as `outer-loop-scripts.test.mjs` argues in its header.
 */

import assert from 'node:assert/strict';
import { appendFileSync, existsSync, mkdirSync, readdirSync, readFileSync, rmSync, statSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { test } from 'node:test';
import { setTimeout as delay } from 'node:timers/promises';

import { requireConfig } from '../dist/config/io.js';
import { formatJson } from '../dist/core/json.js';
import {
  OUTER_LOOP_SCRIPTS,
  RESTART_WATCHER_SCRIPT_NAME,
  WATCHER_SCRIPT_NAME,
  outerLoopRelativePath,
  outerLoopScriptsDir,
} from '../dist/generators/outerLoopScripts.js';
import { PROFILE_LOCAL_PATH, PROFILE_PATH } from '../dist/generators/profileEntries.js';
import { PLUGIN_KEY } from '../dist/generators/projectSettings.js';
import { WRAPPER_SCRIPTS, scriptInvocation } from '../dist/generators/scripts.js';
import { PACKAGE_ROOT, createFixture, readJson, runBash, runCli, runGit, snapshotTree } from './helpers/fixture.mjs';

const UPGRADE = ['init', '--upgrade'];
const DRY_RUN = [...UPGRADE, '--dry-run'];
const BACKUP_ROOT = ['.git', 'devscene', 'upgrade-backups'];
const SELF_ADOPT_ENV = 'HARNESS_SELF_ADOPT';
const CLAUDE_HOME_VARIABLE = 'CLAUDE_CONFIG_DIR';

const EDIT = '\n# This line was added by hand.\n';
const RETIRED_ENTRY = 'Bash(retired-command:*)';
const LOCAL_ENTRY = 'Bash(local-command:*)';
const WOULD_REFUSE = /a real --upgrade run would refuse: runs are active on feat_live/;
const RUNNING_SCRIPT_LIMIT_MS = 30_000;

const rowNamed = (file) => {
  const row = OUTER_LOOP_SCRIPTS.find((script) => script.file === file);
  assert.ok(row, `${file} has no row`);
  return row;
};
const SCRATCH_RUN = rowNamed('scratch-run.sh');
const WATCHER = rowNamed(WATCHER_SCRIPT_NAME);

const shipped = (script) =>
  readFileSync(join(import.meta.dirname, '..', 'templates', 'scripts', ...outerLoopRelativePath(script).split('/')));

async function temporaryDir(t) {
  const fixture = await createFixture({ git: false });
  t.after(fixture.cleanup);
  return fixture.dir;
}

/** A repository wired by the compiled `init`, with its own agent-runner home. */
async function wired(t) {
  const home = await temporaryDir(t);
  const fixture = await createFixture({
    files: {
      'package.json': {
        name: 'fixture-project',
        private: true,
        version: '0.0.0',
        scripts: { typecheck: 'echo typecheck', test: 'echo test', build: 'echo build', dev: 'echo dev' },
      },
      'README.md': '# fixture project\n',
    },
  });
  t.after(fixture.cleanup);
  const { dir } = fixture;
  const repo = {
    dir,
    home,
    run: (args, env = {}) => runCli(dir, args, { [CLAUDE_HOME_VARIABLE]: home, ...env }),
  };
  assertOk(await repo.run(['init']), 'init');
  const scriptsDir = outerLoopScriptsDir(requireConfig(dir));
  return {
    ...repo,
    scriptsDir,
    scriptKey: (script) => `${scriptsDir}/${outerLoopRelativePath(script)}`,
    scriptPath: (script) => join(dir, scriptsDir, ...outerLoopRelativePath(script).split('/')),
  };
}

function assertOk(result, what) {
  assert.equal(result.status, 0, `${what} exited ${result.status}\n${result.stdout}\n${result.stderr}`);
  return result;
}

const upgrade = async (repo, args = UPGRADE, env = {}) => assertOk(await repo.run(args, env), args.join(' '));

const profilePath = (repo) => join(repo.dir, PROFILE_PATH);
const profileOf = (repo) => readJson(profilePath(repo));

function editProfile(repo, edit) {
  const profile = profileOf(repo);
  edit(profile);
  writeFileSync(profilePath(repo), formatJson(profile));
}

const backupRoot = (repo) => join(repo.dir, ...BACKUP_ROOT);
const backupRuns = (repo) => (existsSync(backupRoot(repo)) ? readdirSync(backupRoot(repo)) : []);

/** The keys of `after` that are new or differ from `before`, and the keys it lost. */
function changedKeys(before, after) {
  const keys = new Set([...Object.keys(before), ...Object.keys(after)]);
  return [...keys].filter((key) => before[key] !== after[key]).sort();
}

const statusLines = async (dir) =>
  (await runGit(dir, ['status', '--porcelain'])).stdout.split('\n').filter((line) => line !== '');

/**
 * A wired repository holding everything an upgrade must leave alone, committed, plus one edited
 * outer-loop script and a profile that has lost one generated entry and gained a retired one.
 */
async function filled(t) {
  const repo = await wired(t);
  const wrapper = `${repo.scriptsDir}/${WRAPPER_SCRIPTS[0].file}`;
  const owned = [
    '.claude/CLAUDE.md',
    '.claude/context/conventions.md',
    '.claude/review-sweep.md',
    '.claude/devscene-task-offer.md',
    wrapper,
    'devscene/lessons.md',
    'devscene/improvement_suggestions.md',
    'devscene/README.md',
    'devscene/task_plans/README.md',
  ];
  for (const path of owned) {
    assert.ok(existsSync(join(repo.dir, path)), `${path} was not wired`);
    appendFileSync(join(repo.dir, path), EDIT);
  }
  appendFileSync(repo.scriptPath(SCRATCH_RUN), EDIT);
  await runGit(repo.dir, ['add', '--', ...owned, repo.scriptKey(SCRATCH_RUN)]);
  await runGit(repo.dir, ['commit', '--quiet', '-m', 'fill the repository']);

  const lost = profileOf(repo).permissions.allow[0];
  editProfile(repo, (profile) => {
    profile.permissions.allow = [...profile.permissions.allow.slice(1), RETIRED_ENTRY];
  });
  return { ...repo, owned, lost };
}

test('init --help lists --upgrade', async (t) => {
  const repo = await wired(t);
  assert.match(assertOk(await repo.run(['init', '--help']), 'init --help').stdout, /^\s+--upgrade\s+\S/m);
});

test('an upgrade changes only the outer-loop scripts and the profile', async (t) => {
  const repo = await filled(t);
  const before = await snapshotTree(repo.dir);

  const { stdout } = await upgrade(repo);

  assert.deepEqual(
    changedKeys(before, await snapshotTree(repo.dir)),
    [repo.scriptKey(SCRATCH_RUN), PROFILE_PATH].sort(),
  );
  assert.deepEqual(await statusLines(repo.dir), [` M ${repo.scriptKey(SCRATCH_RUN)}`]);
  assert.deepEqual(readFileSync(repo.scriptPath(SCRATCH_RUN)), shipped(SCRATCH_RUN));
  assert.ok(profileOf(repo).permissions.allow.includes(repo.lost));
  assert.match(stdout, /^Upgrade complete: 2 files changed\.$/m);
});

test('a second upgrade changes nothing and adds no backup', async (t) => {
  const repo = await filled(t);
  await upgrade(repo);
  const before = await snapshotTree(repo.dir);
  const backups = await snapshotTree(backupRoot(repo));

  const { stdout } = await upgrade(repo);

  assert.deepEqual(await snapshotTree(repo.dir), before);
  assert.deepEqual(await snapshotTree(backupRoot(repo)), backups);
  assert.match(stdout, /^Already current: no file changed\.$/m);
});

test("a changed file's old bytes are kept under the common directory's backup tree", async (t) => {
  const repo = await filled(t);
  const oldScript = readFileSync(repo.scriptPath(SCRATCH_RUN));
  const oldProfile = readFileSync(profilePath(repo));

  const { stdout } = await upgrade(repo);

  const runs = backupRuns(repo);
  assert.equal(runs.length, 1);
  assert.match(runs[0], /^\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}-\d{3}Z$/);
  const backup = join(backupRoot(repo), runs[0]);
  assert.deepEqual(readFileSync(join(backup, repo.scriptKey(SCRATCH_RUN))), oldScript);
  assert.deepEqual(readFileSync(join(backup, PROFILE_PATH)), oldProfile);
  assert.ok(stdout.includes(`Backed up 2 replaced files under ${backup}.`), stdout);
});

test('--dry-run leaves the tree byte-identical and names the entries it would change', async (t) => {
  const repo = await filled(t);
  const before = await snapshotTree(repo.dir);

  const { stdout } = await upgrade(repo, DRY_RUN);

  assert.deepEqual(await snapshotTree(repo.dir), before);
  assert.deepEqual(backupRuns(repo), []);
  assert.ok(stdout.includes(`Profile permissions.allow: would add ${repo.lost}`), stdout);
  assert.ok(stdout.includes(`Profile permissions.allow: would remove ${RETIRED_ENTRY}`), stdout);
  assert.match(stdout, /^Dry run: 2 files would change\.$/m);
});

for (const [name, args, flag] of [
  ['--force', [...UPGRADE, '--force'], '--force'],
  ['a switch of init', [...UPGRADE, '--qa'], '--qa'],
  ['a value flag of init', [...UPGRADE, '--project-name', 'other'], '--project-name'],
  ['--force on a dry run', [...DRY_RUN, '--force'], '--force'],
]) {
  test(`--upgrade with ${name} is refused and writes nothing`, async (t) => {
    const repo = await filled(t);
    const before = await snapshotTree(repo.dir);

    const result = await repo.run(args);

    assert.equal(result.status, 1, result.stdout);
    assert.ok(result.stderr.includes(`--upgrade cannot be combined with ${flag}`), result.stderr);
    assert.deepEqual(await snapshotTree(repo.dir), before);
    assert.deepEqual(backupRuns(repo), []);
  });
}

test('the flag refusal comes before any repository is looked for', async (t) => {
  const outside = await temporaryDir(t);
  const before = await snapshotTree(outside);

  const result = await runCli(outside, [...UPGRADE, '--git-init']);

  assert.equal(result.status, 1);
  assert.match(result.stderr, /--upgrade cannot be combined with --git-init/);
  assert.deepEqual(await snapshotTree(outside), before);
});

test('an active run refuses the upgrade, and a dry run reports that it would', async (t) => {
  const repo = await filled(t);
  writeFileSync(
    join(repo.dir, 'devscene', 'autonomous_logs', 'registry.json'),
    JSON.stringify({ runs: { feat_live: { status: 'running', pid: String(process.pid) } } }),
  );
  const before = await snapshotTree(repo.dir);

  const refused = await repo.run(UPGRADE);
  assert.equal(refused.status, 1, refused.stdout);
  assert.match(refused.stderr, /refusing to upgrade: runs are active on feat_live/);
  assert.deepEqual(await snapshotTree(repo.dir), before);
  assert.deepEqual(backupRuns(repo), []);

  const { stdout } = await upgrade(repo, DRY_RUN);
  assert.match(stdout, WOULD_REFUSE);
  assert.deepEqual(await snapshotTree(repo.dir), before);
  assert.deepEqual(backupRuns(repo), []);
});

test("the harness's own repository is refused unless self-adoption is asked for", async (t) => {
  const repo = await wired(t);
  const { name } = readJson(join(PACKAGE_ROOT, 'package.json'));
  mkdirSync(join(repo.dir, '.claude-plugin'));
  writeFileSync(join(repo.dir, '.claude-plugin', 'marketplace.json'), '{}\n');
  mkdirSync(join(repo.dir, 'cli'));
  writeFileSync(join(repo.dir, 'cli', 'package.json'), formatJson({ name }));
  const before = await snapshotTree(repo.dir);

  const refused = await repo.run(UPGRADE);
  assert.equal(refused.status, 1, refused.stdout);
  assert.match(refused.stderr, /refusing to wire the harness's own repository/);
  assert.deepEqual(await snapshotTree(repo.dir), before);

  await upgrade(repo, UPGRADE, { [SELF_ADOPT_ENV]: '1' });
});

test('a plain init still keeps an edited script and the existing profile', async (t) => {
  const repo = await filled(t);
  const script = readFileSync(repo.scriptPath(SCRATCH_RUN));
  const profile = readFileSync(profilePath(repo));

  assertOk(await repo.run(['init']), 'init');

  assert.deepEqual(readFileSync(repo.scriptPath(SCRATCH_RUN)), script);
  assert.deepEqual(readFileSync(profilePath(repo)), profile);
});

test('a deleted agent-invocable script and its stripped entries come back', async (t) => {
  const repo = await wired(t);
  assert.equal(SCRATCH_RUN.agentInvocable, true);
  const intact = profileOf(repo);
  const names = (entry) => entry.includes(SCRATCH_RUN.file);
  const lists = (profile) => ({
    allow: profile.permissions.allow,
    deny: profile.permissions.deny,
    denyWrite: profile.sandbox.filesystem.denyWrite,
  });
  for (const [list, entries] of Object.entries(lists(intact))) {
    assert.ok(entries.some(names), `${list} never named the script`);
  }

  rmSync(repo.scriptPath(SCRATCH_RUN));
  editProfile(repo, (profile) => {
    profile.permissions.allow = profile.permissions.allow.filter((entry) => !names(entry));
    profile.permissions.deny = profile.permissions.deny.filter((entry) => !names(entry));
    profile.sandbox.filesystem.denyWrite = profile.sandbox.filesystem.denyWrite.filter((entry) => !names(entry));
  });

  await upgrade(repo);

  assert.deepEqual(readFileSync(repo.scriptPath(SCRATCH_RUN)), shipped(SCRATCH_RUN));
  assert.equal(statSync(repo.scriptPath(SCRATCH_RUN)).mode & 0o777, SCRATCH_RUN.mode);
  assert.deepEqual(lists(profileOf(repo)), lists(intact));
});

test('a local entry appears and survives a further upgrade', async (t) => {
  const repo = await wired(t);
  writeFileSync(join(repo.dir, PROFILE_LOCAL_PATH), formatJson({ permissions: { allow: [LOCAL_ENTRY] } }));

  const first = await upgrade(repo);
  assert.ok(profileOf(repo).permissions.allow.includes(LOCAL_ENTRY));
  assert.ok(first.stdout.includes(`Profile permissions.allow: added ${LOCAL_ENTRY}`), first.stdout);
  assert.ok(first.stdout.includes(`Profile includes 1 local addition from ${PROFILE_LOCAL_PATH}.`), first.stdout);
  assert.ok(!first.stderr.includes('is not ignored by git'), first.stderr);

  const second = await upgrade(repo);
  assert.ok(profileOf(repo).permissions.allow.includes(LOCAL_ENTRY));
  assert.match(second.stdout, /^Already current: no file changed\.$/m);
});

test('a local file setting another key refuses the run with scripts and profile untouched', async (t) => {
  const repo = await filled(t);
  writeFileSync(join(repo.dir, PROFILE_LOCAL_PATH), formatJson({ model: 'other' }));
  const before = await snapshotTree(repo.dir);

  const result = await repo.run(UPGRADE);

  assert.equal(result.status, 1, result.stdout);
  assert.match(result.stderr, /model/);
  assert.deepEqual(await snapshotTree(repo.dir), before);
  assert.deepEqual(backupRuns(repo), []);
});

test('a retired generated entry disappears and is reported', async (t) => {
  const repo = await wired(t);
  editProfile(repo, (profile) => profile.permissions.allow.push(RETIRED_ENTRY));

  const { stdout, stderr } = await upgrade(repo);

  assert.ok(!profileOf(repo).permissions.allow.includes(RETIRED_ENTRY));
  assert.ok(stdout.includes(`Profile permissions.allow: removed ${RETIRED_ENTRY}`), stdout);
  assert.ok(stderr.includes(RETIRED_ENTRY), stderr);
});

test('a retired entry for a server the profile does not start is not sent to the local file', async (t) => {
  const repo = await wired(t);
  const entry = 'mcp__retired-server__click';
  editProfile(repo, (profile) => profile.permissions.allow.push(entry));
  const refusal = `cannot be moved to ${PROFILE_LOCAL_PATH}, because this profile does not start its MCP server: ${entry}.`;

  const dry = await upgrade(repo, DRY_RUN);
  assert.ok(dry.stderr.includes(`1 permissions.allow entry would be removed and ${refusal}`), dry.stderr);

  const real = await upgrade(repo);
  assert.ok(real.stderr.includes(`1 permissions.allow entry was removed and ${refusal}`), real.stderr);
  assert.ok(!real.stderr.includes('still wanted'), real.stderr);
});

test('retired entries the local file would refuse for their shape are not sent to it', async (t) => {
  const repo = await wired(t);
  const bare = 'mcp__retired-server';
  const browserDeny = 'mcp__playwright__browser_click';
  editProfile(repo, (profile) => {
    profile.permissions.allow.push(bare);
    profile.permissions.deny.push(browserDeny);
  });
  const bareRefusal = `cannot be moved to ${PROFILE_LOCAL_PATH}, because it names an MCP server and no tool: ${bare}.`;
  const denyRefusal = `cannot be moved to ${PROFILE_LOCAL_PATH}, because a deny naming a browser tool would revoke the interactive-test agent's own grant: ${browserDeny}.`;

  const dry = await upgrade(repo, DRY_RUN);
  assert.ok(dry.stderr.includes(`1 permissions.allow entry would be removed and ${bareRefusal}`), dry.stderr);
  assert.ok(dry.stderr.includes(`1 permissions.deny entry would be removed and ${denyRefusal}`), dry.stderr);
  assert.ok(!dry.stderr.includes('still wanted'), dry.stderr);

  const real = await upgrade(repo);
  assert.ok(real.stderr.includes(`1 permissions.allow entry was removed and ${bareRefusal}`), real.stderr);
  assert.ok(real.stderr.includes(`1 permissions.deny entry was removed and ${denyRefusal}`), real.stderr);
  assert.ok(!real.stderr.includes('still wanted'), real.stderr);
});

test('a setting outside the entry lists is reset and named, and a dry run names it first', async (t) => {
  const repo = await wired(t);
  editProfile(repo, (profile) => {
    profile.env = { HAND_ADDED: '1' };
  });

  const dry = await upgrade(repo, DRY_RUN);
  assert.match(dry.stderr, /1 profile setting outside the entry lists would be reset to what this CLI renders: env\./);
  assert.deepEqual(profileOf(repo).env, { HAND_ADDED: '1' });

  const real = await upgrade(repo);
  assert.match(real.stderr, /1 profile setting outside the entry lists was reset to what this CLI renders: env\./);
  assert.equal(profileOf(repo).env, undefined);
});

for (const [mode, extra] of [
  ['a real run', []],
  ['a dry run', ['--dry-run']],
]) {
  test(`a warning the profile render emits is printed on ${mode}`, async (t) => {
    const repo = await wired(t);
    const { stderr } = await upgrade(repo, [...UPGRADE, ...extra, '--reference-toolchain-path', '/opt/reference']);
    assert.match(stderr, /--reference-toolchain-path was given but phases\.parity is off/);
  });

  test(`a note the profile render emits is printed on ${mode}`, async (t) => {
    const repo = await wired(t);
    const root = await temporaryDir(t);
    mkdirSync(join(repo.home, 'plugins'), { recursive: true });
    writeFileSync(
      join(repo.home, 'plugins', 'installed_plugins.json'),
      formatJson({ version: 2, plugins: { [PLUGIN_KEY]: [{ scope: 'user', installPath: root }] } }),
    );
    const entry = `Bash(bash ${root}/scripts/helper.sh:*)`;
    editProfile(repo, (profile) => profile.permissions.allow.push(entry));

    const { stdout } = await upgrade(repo, [...UPGRADE, ...extra]);

    assert.match(stdout, /1 `permissions\.allow` entry naming this machine's plugin roots (were|would be) carried/);
    assert.ok(profileOf(repo).permissions.allow.includes(entry));
  });
}

test('a script running during the upgrade finishes on its original contents', async (t) => {
  const repo = await wired(t);
  const markers = await temporaryDir(t);
  const started = join(markers, 'started');
  const release = join(markers, 'release');
  const original = 'finished on the original contents';
  // Bash re-reads a script from its file offset after each child it forks, so an in-place rewrite
  // would make this one continue into the replacement's bytes instead of reaching its last line.
  writeFileSync(
    repo.scriptPath(SCRATCH_RUN),
    `#!/usr/bin/env bash\n: > "$1"\nwhile [ ! -e "$2" ]; do sleep 0.05; done\necho '${original}'\n`,
  );

  const running = runBash(repo.dir, [repo.scriptPath(SCRATCH_RUN), started, release], {}, {
    timeoutMs: RUNNING_SCRIPT_LIMIT_MS,
  });
  const deadline = Date.now() + RUNNING_SCRIPT_LIMIT_MS;
  while (!existsSync(started)) {
    assert.ok(Date.now() < deadline, 'the script never started');
    await delay(20);
  }

  try {
    await upgrade(repo);
    assert.deepEqual(readFileSync(repo.scriptPath(SCRATCH_RUN)), shipped(SCRATCH_RUN));
  } finally {
    writeFileSync(release, '');
  }

  const result = await running;
  assert.equal(result.status, 0, result.stderr);
  assert.equal(result.stdout, `${original}\n`);
});

test('the restart line appears when the watcher changes, and not otherwise', async (t) => {
  const repo = await wired(t);
  const restart = scriptInvocation(repo.scriptsDir, RESTART_WATCHER_SCRIPT_NAME);
  const { name, version } = readJson(join(PACKAGE_ROOT, 'package.json'));
  const pinned = `DEVSCENE_CLI="npx ${name}@${version}" ${restart}`;
  const quiet = await upgrade(repo);
  assert.ok(!quiet.stderr.includes(restart), quiet.stderr);

  appendFileSync(repo.scriptPath(WATCHER), EDIT);

  const preview = await upgrade(repo, DRY_RUN);
  assert.ok(preview.stdout.includes(`restart the daemon afterwards with ${pinned}`), preview.stdout);
  const applied = await upgrade(repo);
  assert.ok(applied.stderr.includes(`restart it with ${pinned}`), applied.stderr);
});
