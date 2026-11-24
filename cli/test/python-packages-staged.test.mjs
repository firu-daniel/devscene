/**
 * The shipped Python packages staged under `dist/python/`.
 *
 * **The rule this test exists to enforce: the tarball carries exactly the tracked shipped files,
 * byte for byte.** For each of `FLOW_HOST_PACKAGES`, the files under `cli/dist/python/<package>/`
 * equal the files `git ls-files <package>` lists that `isShippedPythonFile` admits; the exclusion is
 * also asserted against a planted tree under the system temp directory, and `npm pack --dry-run`,
 * run with a cache of its own under that directory, must list the staged files.
 *
 * The staged tree read here is the one `pretest`'s build produced from the tracked files. This
 * suite's tree guard covers `cli/src/flowHost/**` and `cli/package.json` only, because a guard
 * covering either Python package would be run by that layer's pytest command; so a change under
 * `graphscene/` or `devscene-flow-host/` reaches this suite at Run gates, where `pretest` re-stages
 * the tree before it is compared.
 */

import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { mkdirSync, mkdtempSync, readdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import test from 'node:test';

import { MAIN_REPO_ANCHOR_VARIABLE } from '../dist/core/mainRepoAnchor.js';
import { FLOW_HOST_PACKAGES, isShippedPythonFile, stagedPythonDir } from '../dist/flowHost/layout.js';
import { stagePythonPackages } from '../dist/flowHost/stage.js';

const CLI_ROOT = join(import.meta.dirname, '..');
const WORKSPACE_ROOT = join(CLI_ROOT, '..');

/** Every file under `root`, forward-slashed and relative to it, sorted. */
function filesUnder(root) {
  return readdirSync(root, { recursive: true, withFileTypes: true })
    .filter((entry) => entry.isFile())
    .map((entry) => join(entry.parentPath ?? entry.path, entry.name).slice(root.length + 1).split('\\').join('/'))
    .sort();
}

/** The tracked files of `pkg` the shipped-file rule admits, relative to the package root, sorted. */
function trackedShipped(pkg) {
  const listed = execFileSync('git', ['ls-files', '-z', '--', pkg], { cwd: WORKSPACE_ROOT, encoding: 'utf8' });
  return listed
    .split('\0')
    .filter((path) => path !== '')
    .map((path) => path.slice(pkg.length + 1))
    .filter(isShippedPythonFile)
    .sort();
}

for (const pkg of FLOW_HOST_PACKAGES) {
  test(`dist/python/${pkg} holds exactly the tracked shipped files, byte for byte`, () => {
    const stagedRoot = join(stagedPythonDir(), pkg);
    const staged = filesUnder(stagedRoot);
    const expected = trackedShipped(pkg);

    assert.ok(expected.includes('pyproject.toml'));
    assert.ok(expected.includes('uv.lock'));
    assert.deepEqual(staged, expected);
    for (const relative of expected) {
      assert.ok(
        readFileSync(join(WORKSPACE_ROOT, pkg, relative)).equals(readFileSync(join(stagedRoot, relative))),
        `${pkg}/${relative} differs from its staged copy`,
      );
    }

    const excluded = staged.filter((path) => {
      const segments = path.split('/');
      return (
        segments.includes('__pycache__') ||
        segments.includes('.venv') ||
        segments[0] === 'tests' ||
        segments.at(-1) === 'README.md'
      );
    });
    assert.deepEqual(excluded, []);
  });
}

test('staging a planted tree copies only pyproject.toml, uv.lock and the source files', () => {
  const workspaceRoot = mkdtempSync(join(tmpdir(), 'harness-stage-src-'));
  const outDir = mkdtempSync(join(tmpdir(), 'harness-stage-out-'));
  try {
    const planted = {
      'pyproject.toml': '[project]\n',
      'uv.lock': 'version = 1\n',
      'src/pkg/mod.py': 'X = 1\n',
      'src/pkg/__pycache__/x.pyc': 'cache',
      'src/pkg/other.pyc': 'cache',
      'tests/test_x.py': 'def test_x(): pass\n',
      'README.md': '# pkg\n',
    };
    for (const pkg of FLOW_HOST_PACKAGES) {
      for (const [relative, content] of Object.entries(planted)) {
        const path = join(workspaceRoot, pkg, ...relative.split('/'));
        mkdirSync(dirname(path), { recursive: true });
        writeFileSync(path, content);
      }
    }

    stagePythonPackages({ workspaceRoot, outDir });

    for (const pkg of FLOW_HOST_PACKAGES) {
      assert.deepEqual(filesUnder(join(outDir, pkg)), ['pyproject.toml', 'src/pkg/mod.py', 'uv.lock']);
    }
  } finally {
    rmSync(workspaceRoot, { recursive: true, force: true });
    rmSync(outDir, { recursive: true, force: true });
  }
});

// npm gets a cache of its own under the system temp directory: a sandboxed run may write only
// `~/.npm/_logs`, so the default cache's `_cacache/tmp` write is refused with EPERM before the
// file list is printed.
test('npm pack lists the staged Python files', () => {
  const cache = mkdtempSync(join(tmpdir(), 'harness-npm-cache-'));
  try {
    const output = execFileSync('npm', ['pack', '--dry-run', '--json'], {
      cwd: CLI_ROOT,
      encoding: 'utf8',
      env: { ...process.env, [MAIN_REPO_ANCHOR_VARIABLE]: '', npm_config_cache: cache },
    });
    const [pack] = JSON.parse(output);
    const paths = new Set(pack.files.map((file) => file.path));
    for (const expected of [
      'dist/python/devscene-flow-host/pyproject.toml',
      'dist/python/devscene-flow-host/uv.lock',
      'dist/python/graphscene/src/graphscene/schemas/flow-graph.schema.json',
    ]) {
      assert.ok(paths.has(expected), `${expected} is not in the packed file list`);
    }
  } finally {
    rmSync(cache, { recursive: true, force: true });
  }
});
