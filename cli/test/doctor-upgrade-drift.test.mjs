/**
 * `doctor`'s `profile-drift`, `outer-loop-scripts` and `plugin-cli-version` lines, against the
 * compiled CLI on repositories `init` wired.
 *
 * **The rule this suite enforces: a profile or script set that no longer matches this CLI, and a
 * plugin of another version, are reported as warnings naming `init --upgrade`; what this machine can
 * account for is not reported; and `doctor` neither writes anything nor changes its exit status over
 * any of them.**
 *
 * Every repository gets its own agent-runner home, so no plugin installed on the host reaches a case.
 */

import assert from 'node:assert/strict';
import { appendFileSync, mkdirSync, rmSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { describe, it } from 'node:test';

import { requireConfig } from '../dist/config/io.js';
import { formatJson } from '../dist/core/json.js';
import { ownManifestString } from '../dist/core/paths.js';
import { WATCHER_SCRIPT_NAME, outerLoopScriptsDir } from '../dist/generators/outerLoopScripts.js';
import { PROFILE_LOCAL_PATH, PROFILE_PATH } from '../dist/generators/profileEntries.js';
import { PLUGIN_KEY } from '../dist/generators/projectSettings.js';
import { CASE_CONCURRENCY } from './helpers/concurrency.mjs';
import { createFixture, readJson, runCli, runGit, snapshotTree } from './helpers/fixture.mjs';

const PROFILE_CHECK = 'profile-drift';
const SCRIPTS_CHECK = 'outer-loop-scripts';
const VERSION_CHECK = 'plugin-cli-version';
const ALL_CHECKS = [PROFILE_CHECK, SCRIPTS_CHECK, VERSION_CHECK];

const CONFIG_FILE = 'devscene.config.json';
const CLAUDE_HOME_VARIABLE = 'CLAUDE_CONFIG_DIR';
const UPGRADE = ['init', '--upgrade'];
const REMEDY = 'init --upgrade';
const HAND_ENTRY = 'Bash(hand-added-command:*)';
const LOCAL_ENTRY = 'Bash(local-command:*)';
const TOOLCHAIN_COMMAND = 'reference-analyze';
const TOOLCHAIN_ENTRY = `Bash(/opt/reference/${TOOLCHAIN_COMMAND}:*)`;
const STRAY_PLUGIN_ENTRY = 'Bash(bash /tmp/absent-plugin/scripts/helper.sh:*)';
const OTHER_VERSION = '0.0.0-other';

async function temporaryDir(t) {
  const fixture = await createFixture({ git: false });
  t.after(fixture.cleanup);
  return fixture.dir;
}

function assertOk(result, label) {
  assert.equal(result.status, 0, `${label} exited ${result.status}\n${result.stderr}\n${result.stdout}`);
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
  const run = (args, cwd = dir) => runCli(cwd, args, { [CLAUDE_HOME_VARIABLE]: home });
  assertOk(await run(['init']), 'init');
  return { dir, home, run };
}

/** Record `root` as this machine's plugin install root. */
function recordPluginRoot({ home }, root) {
  mkdirSync(join(home, 'plugins'), { recursive: true });
  writeFileSync(
    join(home, 'plugins', 'installed_plugins.json'),
    formatJson({ version: 2, plugins: { [PLUGIN_KEY]: [{ scope: 'user', installPath: root }] } }),
  );
}

function editJson(path, edit) {
  const value = readJson(path);
  edit(value);
  writeFileSync(path, formatJson(value));
}

const editProfile = ({ dir }, edit) => editJson(join(dir, PROFILE_PATH), edit);
const writeLocal = ({ dir }, content) => writeFileSync(join(dir, PROFILE_LOCAL_PATH), formatJson(content));
const scriptKey = ({ dir }) => `${outerLoopScriptsDir(requireConfig(dir))}/${WATCHER_SCRIPT_NAME}`;
const scriptPath = (repo, root = repo.dir) => join(root, ...scriptKey(repo).split('/'));

/** The `id` line in `status`, from the stream the reporter puts it on, or `undefined`. */
function checkLine({ stdout, stderr }, status, id) {
  const [stream, prefix] = status === 'PASS' ? [stdout, ''] : [stderr, '! '];
  return stream.split('\n').find((line) => new RegExp(`^${prefix}${status}\\s+${id}\\s`).test(line));
}

/** Run `doctor`, assert its exit status and that it wrote nothing, and return the result. */
async function doctor(repo, cwd = repo.dir) {
  const before = await snapshotTree(repo.dir);
  const result = await repo.run(['doctor'], cwd);
  assertOk(result, 'doctor');
  assert.deepEqual(await snapshotTree(repo.dir), before, 'doctor wrote to the repository');
  return result;
}

function assertPasses(result, ids = ALL_CHECKS) {
  for (const id of ids) {
    assert.ok(checkLine(result, 'PASS', id), `no PASS ${id} line\n${result.stderr}\n${result.stdout}`);
  }
}

/** The `id` warning, asserted to name the remedy. */
function warning(result, id) {
  const line = checkLine(result, 'WARN', id);
  assert.ok(line, `no WARN ${id} line\n${result.stderr}\n${result.stdout}`);
  assert.ok(line.includes(REMEDY), `the warning does not name ${REMEDY}: ${line}`);
  return line;
}

describe('doctor upgrade drift', { concurrency: CASE_CONCURRENCY }, () => {
  it('passes all three checks after init and again after init --upgrade', async (t) => {
    const repo = await wired(t);
    assertPasses(await doctor(repo));

    assertOk(await repo.run(UPGRADE), 'init --upgrade');
    const result = await doctor(repo);
    assertPasses(result);
    assert.match(checkLine(result, 'PASS', VERSION_CHECK), /nothing was compared/);
  });

  it('warns about a hand-added entry as unaccounted', async (t) => {
    const repo = await wired(t);
    editProfile(repo, (profile) => profile.permissions.allow.push(HAND_ENTRY));

    const line = warning(await doctor(repo), PROFILE_CHECK);
    assert.ok(line.includes(JSON.stringify(HAND_ENTRY)), line);
    assert.match(line, /hand edit or tampering/);
    assert.ok(line.includes(PROFILE_LOCAL_PATH), line);
    assert.doesNotMatch(line, /is stale/);
  });

  it('keeps a line break in a tampered entry on the one report line', async (t) => {
    const repo = await wired(t);
    editProfile(repo, (profile) => profile.permissions.allow.push('Bash(x)\nPASS  forged  line'));

    const result = await doctor(repo);
    assert.ok(warning(result, PROFILE_CHECK).includes('\\n'));
    assert.ok(!`${result.stdout}\n${result.stderr}`.split('\n').some((line) => line.startsWith('PASS  forged')));
  });

  it('warns about a removed generated entry as missing', async (t) => {
    const repo = await wired(t);
    let removed;
    editProfile(repo, (profile) => {
      removed = profile.permissions.deny.pop();
    });

    const line = warning(await doctor(repo), PROFILE_CHECK);
    assert.ok(line.includes(JSON.stringify(removed)), line);
    assert.match(line, /is stale/);
    assert.doesNotMatch(line, /hand edit/);
  });

  it('warns about a setting outside the entry lists, and passes after init --upgrade', async (t) => {
    const repo = await wired(t);
    editProfile(repo, (profile) => {
      profile.hooks = {};
    });

    const line = warning(await doctor(repo), PROFILE_CHECK);
    assert.ok(line.includes(JSON.stringify('hooks')), line);
    assert.match(line, /settings that differ/);
    assert.doesNotMatch(line, /is stale/);

    assertOk(await repo.run(UPGRADE), 'init --upgrade');
    assertPasses(await doctor(repo), [PROFILE_CHECK]);
  });

  it('keeps a line break in a tampered setting key on the one report line', async (t) => {
    const repo = await wired(t);
    editProfile(repo, (profile) => {
      profile['x\nPASS  forged  line'] = true;
    });

    const result = await doctor(repo);
    assert.ok(warning(result, PROFILE_CHECK).includes('\\n'));
    assert.ok(!`${result.stdout}\n${result.stderr}`.split('\n').some((line) => line.startsWith('PASS  forged')));
  });

  it('warns about a local entry not yet rendered, and passes after init --upgrade', async (t) => {
    const repo = await wired(t);
    writeLocal(repo, { permissions: { allow: [LOCAL_ENTRY] } });

    const line = warning(await doctor(repo), PROFILE_CHECK);
    assert.ok(line.includes(JSON.stringify(LOCAL_ENTRY)), line);
    assert.match(line, /is stale/);

    assertOk(await repo.run(UPGRADE), 'init --upgrade');
    assertPasses(await doctor(repo), [PROFILE_CHECK]);
  });

  it('accepts a plugin-root entry under a resolved root and a parity toolchain entry', async (t) => {
    const repo = await wired(t);
    const root = await temporaryDir(t);
    recordPluginRoot(repo, root);
    editJson(join(repo.dir, CONFIG_FILE), (config) => {
      config.phases = { ...config.phases, parity: true };
      config.parity = { ...config.parity, toolchainCommands: [TOOLCHAIN_COMMAND] };
    });
    assertOk(await repo.run(UPGRADE), 'init --upgrade');
    editProfile(repo, (profile) => profile.permissions.allow.push(`Bash(bash ${root}/scripts/helper.sh:*)`, TOOLCHAIN_ENTRY));

    assertPasses(await doctor(repo), [PROFILE_CHECK]);
  });

  it('warns about a plugin-root shape when no root resolves', async (t) => {
    const repo = await wired(t);
    editProfile(repo, (profile) => profile.permissions.allow.push(STRAY_PLUGIN_ENTRY));

    const line = warning(await doctor(repo), PROFILE_CHECK);
    assert.ok(line.includes(JSON.stringify(STRAY_PLUGIN_ENTRY)), line);
    assert.match(line, /hand edit or tampering/);
  });

  it('warns with the refusal when the local file is refused', async (t) => {
    const repo = await wired(t);
    writeLocal(repo, { model: 'not-an-addition' });

    const line = warning(await doctor(repo), PROFILE_CHECK);
    assert.ok(line.includes(`${PROFILE_LOCAL_PATH}: model is not allowed`), line);
  });

  it('warns when an existing local file is not ignored', async (t) => {
    const repo = await wired(t);
    writeLocal(repo, {});
    assertPasses(await doctor(repo), [PROFILE_CHECK]);

    appendFileSync(join(repo.dir, '.gitignore'), `!${PROFILE_LOCAL_PATH}\n`);
    assert.match(warning(await doctor(repo), PROFILE_CHECK), /is not ignored by git/);
  });

  it('names an edited script and a missing one', async (t) => {
    const repo = await wired(t);
    appendFileSync(scriptPath(repo), '\n# edited by hand\n');

    const edited = warning(await doctor(repo), SCRIPTS_CHECK);
    assert.ok(edited.includes(`changed from what this CLI ships: ${scriptKey(repo)}`), edited);
    assert.match(edited, /patched deliberately is replaced/);

    rmSync(scriptPath(repo));
    assert.ok(warning(await doctor(repo), SCRIPTS_CHECK).includes(`missing: ${scriptKey(repo)}`));

    assertOk(await repo.run(UPGRADE), 'init --upgrade');
    assertPasses(await doctor(repo), [SCRIPTS_CHECK]);
  });

  it("grades the main checkout's files from a linked worktree", async (t) => {
    const repo = await wired(t);
    await runGit(repo.dir, ['add', '-A']);
    await runGit(repo.dir, ['commit', '--allow-empty', '-m', 'adopt the harness']);
    const worktree = join(await temporaryDir(t), 'linked');
    await runGit(repo.dir, ['worktree', 'add', '-b', 'feat_linked', worktree]);
    t.after(() => rmSync(worktree, { recursive: true, force: true }));

    // The worktree's own copy is not the one graded.
    appendFileSync(scriptPath(repo, worktree), '\n# edited in the worktree\n');
    assertPasses(await doctor(repo, worktree), [PROFILE_CHECK, SCRIPTS_CHECK]);

    appendFileSync(scriptPath(repo), '\n# edited in the main checkout\n');
    editProfile(repo, (profile) => profile.permissions.allow.push(HAND_ENTRY));
    const result = await doctor(repo, worktree);
    assert.ok(warning(result, PROFILE_CHECK).includes(JSON.stringify(HAND_ENTRY)));
    assert.ok(warning(result, SCRIPTS_CHECK).includes(scriptKey(repo)));
  });

  it('warns about a plugin of another version and passes on a match', async (t) => {
    const repo = await wired(t);
    const root = await temporaryDir(t);
    const manifest = join(root, '.claude-plugin', 'plugin.json');
    mkdirSync(join(root, '.claude-plugin'), { recursive: true });
    recordPluginRoot(repo, root);

    writeFileSync(manifest, formatJson({ name: 'devscene', version: OTHER_VERSION }));
    const line = warning(await doctor(repo), VERSION_CHECK);
    const cliVersion = ownManifestString('version');
    assert.ok(line.includes(OTHER_VERSION) && line.includes(cliVersion), line);
    assert.ok(line.includes(`npx ${ownManifestString('name')}@${OTHER_VERSION} ${REMEDY}`), line);

    writeFileSync(manifest, formatJson({ name: 'devscene', version: cliVersion }));
    assert.ok(checkLine(await doctor(repo), 'PASS', VERSION_CHECK).includes(cliVersion));
  });
});
