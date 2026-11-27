/**
 * The run library's two readers behind the script-driven planning pilot —
 * `hr_script_driven_planning` and `hr_plugin_runtime_root_var` in
 * `cli/templates/scripts/lib/harness-run-lib.sh`.
 *
 * **The rule this suite enforces: `hr_script_driven_planning` answers `execution.scriptDrivenPlanning`
 * through its status alone, with an absent key off; and `hr_plugin_runtime_root_var` derives the
 * plugin's runtime root from the agent runner's records as `cli/src/machine/plugins.ts` →
 * `pluginRuntimeRoot` does, falling back to its install-row order, and answers 1 rather than
 * guessing.** The runtime-root cases are held against the compiled `pluginRuntimeRoot` over the same
 * records, so the mirror and its source cannot drift unseen.
 *
 * The library is sourced from the package's template tree, one `bash` process per case because
 * `hr_config_load` memoises per `$$`. Every record lives under a `CLAUDE_CONFIG_DIR` the case creates
 * under the system temp directory, never the real account home, and is removed in process.
 */

import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { test } from 'node:test';

import { PACKAGE_ROOT, runBash } from './helpers/fixture.mjs';

const LIB_PATH = join(PACKAGE_ROOT, 'templates', 'scripts', 'lib', 'harness-run-lib.sh');
const PLUGINS_MODULE = join(PACKAGE_ROOT, 'dist', 'machine', 'plugins.js');
const KEY = 'devscene@devscene';

const JQ_RESOLVES = (await runBash(PACKAGE_ROOT, ['-c', 'command -v jq >/dev/null 2>&1'])).status === 0;
const NO_JQ = JQ_RESOLVES ? false : "jq does not resolve on this process's PATH, so the library cannot read a record here";

/** Source the library, then run `script` with the remaining values as `$1`, `$2`, …. */
function libCall(script, args = [], env = {}) {
  return runBash(PACKAGE_ROOT, ['-c', `. "$1"; shift; ${script}`, '_', LIB_PATH, ...args], { GITHUB_ACTIONS: '', ...env });
}

test('hr_script_driven_planning reads the key as true 0, false or absent 1, unresolvable or non-boolean 2', { skip: NO_JQ }, async () => {
  const cases = [
    ['absent', { defaultBranch: 'main' }, 1],
    ['true', { defaultBranch: 'main', execution: { scriptDrivenPlanning: true } }, 0],
    ['false', { defaultBranch: 'main', execution: { scriptDrivenPlanning: false } }, 1],
    ['"true"', { defaultBranch: 'main', execution: { scriptDrivenPlanning: 'true' } }, 2],
    ['no file', undefined, 2],
  ];
  for (const [label, config, expected] of cases) {
    const dir = mkdtempSync(join(tmpdir(), 'script-driven-planning-config-'));
    try {
      if (config !== undefined) writeFileSync(join(dir, 'devscene.config.json'), JSON.stringify(config));
      const result = await libCall('hr_script_driven_planning "$1"', [dir]);
      assert.equal(result.status, expected, label);
      assert.equal(result.stdout, '', `${label}: printed something`);
    } finally {
      rmSync(dir, { recursive: true, force: true });
    }
  }
});

/** The TypeScript answer for the same records, from the compiled module, in a child with `CLAUDE_CONFIG_DIR` set. */
function typescriptRoot(home, repo) {
  const script = `import(${JSON.stringify(PLUGINS_MODULE)}).then((m) => process.stdout.write(m.pluginRuntimeRoot(process.argv[1]) ?? ''))`;
  return execFileSync(process.execPath, ['--input-type=module', '-e', script, repo], {
    env: { PATH: process.env.PATH ?? '', CLAUDE_CONFIG_DIR: home },
    encoding: 'utf8',
  });
}

test('hr_plugin_runtime_root_var derives the root pluginRuntimeRoot derives, and answers 1 when none resolves', { skip: NO_JQ }, async (t) => {
  const root = mkdtempSync(join(tmpdir(), 'plugin-runtime-root-'));
  t.after(() => rmSync(root, { recursive: true, force: true }));
  const repo = join(root, 'repo');
  const market = join(root, 'market');

  const rows = (list) => JSON.stringify({ version: 2, plugins: { [KEY]: list } });
  const directoryMarket = (source) =>
    JSON.stringify({ devscene: { source: { source: 'directory', path: market }, installLocation: `${market}/` } }) +
    `\n${source}`;
  const cases = [
    { label: 'no records', expected: '' },
    {
      label: 'the project row for this repository wins over the user row',
      installed: rows([
        { scope: 'user', installPath: join(root, 'user') },
        { scope: 'project', projectPath: join(root, 'other'), installPath: join(root, 'other-project') },
        { scope: 'project', projectPath: repo, installPath: join(root, 'project') },
      ]),
      expected: join(root, 'project'),
    },
    {
      label: 'no project row for this repository: the user row',
      installed: rows([
        { scope: 'project', projectPath: join(root, 'other'), installPath: join(root, 'other-project') },
        { scope: 'user', installPath: join(root, 'user') },
      ]),
      expected: join(root, 'user'),
    },
    {
      label: 'no scope this mirror knows: the first usable row',
      installed: rows([{ scope: 'local', installPath: '' }, { scope: 'local', installPath: join(root, 'first') }]),
      expected: join(root, 'first'),
    },
    {
      label: 'a directory-sourced marketplace: <installLocation>/<source>, over the install row',
      installed: rows([{ scope: 'user', installPath: join(root, 'cache') }]),
      marketplaces: directoryMarket('./plugin'),
      expected: join(market, 'plugin'),
    },
    {
      label: 'a git-sourced marketplace: the install row',
      installed: rows([{ scope: 'user', installPath: join(root, 'cache') }]),
      marketplaces: JSON.stringify({ devscene: { source: { source: 'github', repo: 'o/r' }, installLocation: market } }),
      expected: join(root, 'cache'),
    },
    { label: 'an unparsable install record', installed: '{', expected: '' },
  ];

  let n = 0;
  for (const { label, installed, marketplaces, expected } of cases) {
    const home = join(root, `home-${n++}`);
    mkdirSync(join(home, 'plugins'), { recursive: true });
    if (installed !== undefined) writeFileSync(join(home, 'plugins', 'installed_plugins.json'), installed);
    if (marketplaces !== undefined) {
      const [register, source] = marketplaces.split('\n');
      writeFileSync(join(home, 'plugins', 'known_marketplaces.json'), register);
      mkdirSync(join(market, '.claude-plugin'), { recursive: true });
      writeFileSync(
        join(market, '.claude-plugin', 'marketplace.json'),
        JSON.stringify({ name: 'devscene', plugins: [{ name: 'devscene', source: source ?? './plugin' }] }),
      );
    }
    const result = await libCall(
      'hr_plugin_runtime_root_var "$1"; rc=$?; printf "%s|%s" "$rc" "$HR_PLUGIN_RUNTIME_ROOT"',
      [repo],
      { CLAUDE_CONFIG_DIR: home, HOME: join(root, 'no-home') },
    );
    assert.equal(result.stdout, `${expected === '' ? 1 : 0}|${expected}`, `${label}\n${result.stderr}`);
    assert.equal(typescriptRoot(home, repo), expected, `${label}: pluginRuntimeRoot disagrees`);
  }
});
