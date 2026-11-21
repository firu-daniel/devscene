/**
 * `scripts/python-service.sh` — the one route to this repository's Python toolchain, driven from a
 * throwaway fixture with a recording `uv` stub first on `PATH`.
 *
 * **The rule this suite enforces: one wrapper reaches the Python packages, every write it causes
 * lands inside the selected package directory or in `uv`'s own temporary cache — never under `HOME`
 * or `XDG_CACHE_HOME` — the package is a row of a closed table, and `provision` lets a host with no
 * `uv` bootstrap (`SKIPPED`, exit 0) while the legs still exit 3 (`BLOCKED`); `probe` runs only a `.py`
 * file inside the state directory's `scratch/` and passes that file's status through, and `check`
 * grades an unprovisioned leg as exit 3, never as a failure.** The table has two rows,
 * and a row with no console script or no compose project refuses `run` / `container-test` with exit 2
 * before calling `uv`; `provision` syncs every row, in table order. That is what makes
 * gate 13 runnable in a run copy, whose sandboxes allow writes to the copy and a temporary
 * directory only. The read-only legs carry `--no-cache`; provisioning does not.
 *
 * Every case runs the fixture's own copy of the script from outside the fixture repository, with
 * `HOME` and `XDG_CACHE_HOME` each a fresh empty directory and an inherited `UV_PROJECT_ENVIRONMENT`
 * pointing at a decoy under `HOME`, so a case proves the wrapper's own value wins. `WORKSPACE_ROOT`
 * is only where the script is read from.
 *
 * Deliberately not covered:
 * - **The real `uv` under the two sandboxes.** That evidence is gate 13 itself, run in a run copy
 *   bootstrapped with `provision`.
 * - **`container-test` against a real Docker daemon.** No case here starts a service
 *   (`.claude/context/cli.md` → `## What "done" means here`); only its no-`docker` exit is pinned.
 * - **The real `uv` running a real probe.** That evidence is a `probe` call against the real
 *   toolchain, made by the change that added the verb and by a reviewer using it.
 * - **The F15 placeholder itself.** Only a bubblewrap host mounts `<scriptsDir>/.git`; here the
 *   probe fixture places the root through `hr_script_root` and the script-only one through the bare
 *   `git rev-parse` fallback, and neither meets the placeholder.
 */

import assert from 'node:assert/strict';
import { existsSync, readFileSync } from 'node:fs';
import { chmod, copyFile, mkdir, mkdtemp, readdir, readFile, realpath, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { delimiter, join } from 'node:path';
import test from 'node:test';

import { runBash, runGit, WORKSPACE_ROOT } from './helpers/fixture.mjs';

const SCRIPT = join(WORKSPACE_ROOT, 'scripts', 'python-service.sh');
const PACKAGE = 'docs-retrieval-service';
const LIBRARY = 'graphscene';
const CONSOLE_SCRIPT = 'devscene-docs-retrieval';
const OTHER_PACKAGE = 'other-package';
const LEG_PREFIX = ['run', '--frozen', '--no-sync', '--no-cache'];
const UNKNOWN_PACKAGE_LINE = (dir) =>
  `python-service: unknown package '${dir}'; the packages are: ${PACKAGE}, ${LIBRARY}`;
const USAGE_PREFIX = 'usage: bash scripts/python-service.sh [--package <dir>] ';

/**
 * The tools the wrapper, the stub and the library's scratch-path test reach on `PATH`; `bash`
 * because `runBash` resolves it there.
 */
const BASE_TOOLS = ['bash', 'git', 'cksum', 'awk', 'dirname', 'mkdir', 'jq', 'basename'];

const LIBRARY_SOURCE = join(WORKSPACE_ROOT, 'scripts', 'lib', 'harness-run-lib.sh');
const STATE_DIR = 'state';
const SCRATCH = `${STATE_DIR}/scratch`;
const PROBE = `${SCRATCH}/probe.py`;

/**
 * The four values the stub records per call. `pwd -P` because the wrapper `cd`s to the physical
 * root `git` answers with.
 */
const UV_STUB = [
  '#!/bin/bash',
  '{',
  "  printf 'cwd\\t%s\\n' \"$(pwd -P)\"",
  '  for name in UV_PROJECT_ENVIRONMENT RUFF_CACHE_DIR MYPY_CACHE_DIR PYTHONDONTWRITEBYTECODE; do',
  "    printf 'env\\t%s\\t%s\\n' \"$name\" \"${!name-<unset>}\"",
  '  done',
  '  for arg in "$@"; do',
  "    printf 'arg\\t%s\\n' \"$arg\"",
  '  done',
  "  printf 'end\\n'",
  '} >> "$FAKE_UV_LOG"',
  'if [ "${1-}" = sync ]; then',
  '  mkdir -p "$UV_PROJECT_ENVIRONMENT" && : > "$UV_PROJECT_ENVIRONMENT/pyvenv.cfg"',
  'fi',
  'exit "${FAKE_UV_STATUS:-0}"',
  '',
].join('\n');

/**
 * `/usr/bin` and `/bin`, plus the directory of any {@link BASE_TOOLS} entry neither holds, resolved
 * on the runner's own `PATH`. A case needing `uv` or `docker` absent checks this with
 * {@link resolveOnBase} and skips when it resolves one.
 */
function basePath() {
  const dirs = ['/usr/bin', '/bin'];
  const hostDirs = (process.env.PATH ?? '').split(delimiter).filter(Boolean);
  for (const tool of BASE_TOOLS) {
    if (dirs.some((dir) => existsSync(join(dir, tool)))) continue;
    const found = hostDirs.find((dir) => existsSync(join(dir, tool)));
    assert.ok(found !== undefined, `fixture setup: ${tool} is on neither /usr/bin, /bin nor PATH`);
    dirs.push(found);
  }
  return dirs.join(delimiter);
}

/** The path `tool` resolves to on `pathValue`, or `undefined`. */
function resolveOnBase(tool, pathValue) {
  const dir = pathValue.split(delimiter).find((entry) => existsSync(join(entry, tool)));
  return dir === undefined ? undefined : join(dir, tool);
}

/**
 * One case's fixture: a git repository holding the script, both table rows' packages and a Python
 * package that is not a row, beside a `bin/uv` stub, an empty `HOME`, an empty `XDG_CACHE_HOME` and
 * the stub's call log — all under one `realpath`-resolved directory under `os.tmpdir()`.
 *
 * `withLibrary` adds what `probe` needs: the library beside the script, a `devscene.config.json`
 * it resolves, and `<stateDir>/scratch/` holding {@link PROBE} and a `.mjs` sibling. Without it the
 * script finds no library, so the root is placed by the bare `git rev-parse` fallback.
 */
async function buildFixture(t, { withLibrary = false } = {}) {
  const root = await realpath(await mkdtemp(join(tmpdir(), 'python-service-')));
  t.after(() => rm(root, { recursive: true, force: true }));
  const repo = join(root, 'repo');
  const bin = join(root, 'bin');
  const home = join(root, 'home');
  const cache = join(root, 'xdg-cache');
  for (const dir of [repo, bin, home, cache, join(repo, 'scripts'), join(repo, PACKAGE), join(repo, LIBRARY), join(repo, OTHER_PACKAGE)]) {
    await mkdir(dir, { recursive: true });
  }
  await runGit(repo, ['init', '-q']);
  const script = join(repo, 'scripts', 'python-service.sh');
  await copyFile(SCRIPT, script);
  await writeFile(join(repo, PACKAGE, 'pyproject.toml'), `[project]\nname = "${PACKAGE}"\n`, 'utf8');
  await writeFile(join(repo, LIBRARY, 'pyproject.toml'), `[project]\nname = "${LIBRARY}"\n`, 'utf8');
  await writeFile(join(repo, OTHER_PACKAGE, 'pyproject.toml'), `[project]\nname = "${OTHER_PACKAGE}"\n`, 'utf8');
  await writeFile(join(repo, OTHER_PACKAGE, 'uv.lock'), 'version = 1\n', 'utf8');
  if (withLibrary) {
    await mkdir(join(repo, 'scripts', 'lib'), { recursive: true });
    await copyFile(LIBRARY_SOURCE, join(repo, 'scripts', 'lib', 'harness-run-lib.sh'));
    const config = { version: 1, defaultBranch: 'main', stateDir: STATE_DIR };
    await writeFile(join(repo, 'devscene.config.json'), `${JSON.stringify(config, null, 2)}\n`, 'utf8');
    await mkdir(join(repo, SCRATCH), { recursive: true });
    await writeFile(join(repo, PROBE), 'print("probe")\n', 'utf8');
    await writeFile(join(repo, SCRATCH, 'probe.mjs'), 'console.log("probe");\n', 'utf8');
    await writeFile(join(repo, 'outside.py'), 'print("outside")\n', 'utf8');
  }
  await writeFile(join(bin, 'uv'), UV_STUB, 'utf8');
  await chmod(join(bin, 'uv'), 0o755);
  const base = basePath();
  const log = join(root, 'uv-calls.log');

  /** Runs the wrapper from `root`, outside the repository, with the stub first unless `noUv`. */
  const runScript = (args, { env = {}, noUv = false } = {}) =>
    runBash(root, [script, ...args], {
      HOME: home,
      XDG_CACHE_HOME: cache,
      UV_PROJECT_ENVIRONMENT: join(home, 'decoy-venv'),
      FAKE_UV_LOG: log,
      PATH: noUv ? base : `${bin}${delimiter}${base}`,
      ...env,
    });

  /** The stub's records since the last call, then an empty log. */
  const takeCalls = async () => {
    if (!existsSync(log)) return [];
    const text = await readFile(log, 'utf8');
    await rm(log, { force: true });
    return text
      .split('end\n')
      .filter((chunk) => chunk !== '')
      .map((chunk) => {
        const call = { cwd: undefined, env: {}, argv: [] };
        for (const line of chunk.split('\n').filter(Boolean)) {
          const [kind, ...rest] = line.split('\t');
          if (kind === 'cwd') call.cwd = rest.join('\t');
          else if (kind === 'env') call.env[rest[0]] = rest.slice(1).join('\t');
          else if (kind === 'arg') call.argv.push(rest.join('\t'));
        }
        return call;
      });
  };

  const plantVenv = async (pkg = PACKAGE) => {
    await mkdir(join(repo, pkg, '.venv'), { recursive: true });
    await writeFile(join(repo, pkg, '.venv', 'pyvenv.cfg'), 'home = /nowhere\n', 'utf8');
  };

  return { root, repo, home, cache, base, runScript, takeCalls, plantVenv };
}

/** The working directory and four environment values every `uv` call for `pkg` must see. */
function expectedSite(repo, pkg = PACKAGE) {
  const dir = join(repo, pkg);
  return {
    cwd: dir,
    env: {
      UV_PROJECT_ENVIRONMENT: join(dir, '.venv'),
      RUFF_CACHE_DIR: join(dir, '.ruff_cache'),
      MYPY_CACHE_DIR: join(dir, '.mypy_cache'),
      PYTHONDONTWRITEBYTECODE: '1',
    },
  };
}

function assertCalls(calls, repo, argvs, context, pkg = PACKAGE) {
  const site = expectedSite(repo, pkg);
  assert.deepEqual(
    calls,
    argvs.map((argv) => ({ ...site, argv })),
    `${context}: recorded uv calls`,
  );
}

/** No recorded value starts with `HOME` or `XDG_CACHE_HOME`, and both are still empty. */
async function assertNothingUnderHome(fixture, calls) {
  for (const call of calls) {
    for (const value of [call.cwd, ...Object.values(call.env), ...call.argv]) {
      for (const forbidden of [fixture.home, fixture.cache]) {
        assert.ok(!value.startsWith(forbidden), `a uv call carries ${JSON.stringify(value)}, under ${forbidden}`);
      }
    }
  }
  assert.deepEqual(await readdir(fixture.home), [], 'HOME was written');
  assert.deepEqual(await readdir(fixture.cache), [], 'XDG_CACHE_HOME was written');
}

const LEGS = [
  { args: ['lint'], argvs: [[...LEG_PREFIX, 'ruff', 'check'], [...LEG_PREFIX, 'ruff', 'format', '--check']] },
  { args: ['typecheck'], argvs: [[...LEG_PREFIX, 'mypy']] },
  { args: ['test', 'tests/a.py', 'tests/b.py'], argvs: [[...LEG_PREFIX, 'pytest', 'tests/a.py', 'tests/b.py']] },
  { args: ['test'], argvs: [[...LEG_PREFIX, 'pytest']] },
  { args: ['run', 'serve', '--port', '1'], argvs: [[...LEG_PREFIX, CONSOLE_SCRIPT, 'serve', '--port', '1']] },
];

const LEG_NAMES = [['lint'], ['typecheck'], ['test'], ['run']];

test('the legs, provisioned: each records its argv, the package directory and the four values, by default and under --package', async (t) => {
  const fixture = await buildFixture(t);
  await fixture.plantVenv();
  const all = [];
  for (const prefix of [[], ['--package', PACKAGE]]) {
    for (const leg of LEGS) {
      const args = [...prefix, ...leg.args];
      const result = await fixture.runScript(args);
      assert.equal(result.status, 0, `${args.join(' ')}: ${result.stderr}`);
      const calls = await fixture.takeCalls();
      assertCalls(calls, fixture.repo, leg.argvs, args.join(' '));
      all.push(...calls);
    }
  }
  await assertNothingUnderHome(fixture, all);
});

test(`the legs under --package ${LIBRARY}: each records its argv, ${LIBRARY}/ and its four values`, async (t) => {
  const fixture = await buildFixture(t);
  await fixture.plantVenv(LIBRARY);
  const all = [];
  for (const leg of LEGS.filter((entry) => entry.args[0] !== 'run').concat([
    { args: ['test', 'tests/a.py'], argvs: [[...LEG_PREFIX, 'pytest', 'tests/a.py']] },
  ])) {
    const args = ['--package', LIBRARY, ...leg.args];
    const result = await fixture.runScript(args);
    assert.equal(result.status, 0, `${args.join(' ')}: ${result.stderr}`);
    const calls = await fixture.takeCalls();
    assertCalls(calls, fixture.repo, leg.argvs, args.join(' '), LIBRARY);
    all.push(...calls);
  }
  await assertNothingUnderHome(fixture, all);
});

test(`run, container-test and sync --with-models under --package ${LIBRARY} exit 2 with the row's refusal line and call no uv`, async (t) => {
  const fixture = await buildFixture(t);
  await fixture.plantVenv(LIBRARY);
  const refusals = [
    [['--package', LIBRARY, 'run', 'serve'], `python-service: package '${LIBRARY}' has no console script`],
    [['--package', LIBRARY, 'container-test'], `python-service: package '${LIBRARY}' has no container tests`],
    [['--package', LIBRARY, 'sync', '--with-models'], `python-service: package '${LIBRARY}' has no models extra`],
  ];
  for (const [args, line] of refusals) {
    const result = await fixture.runScript(args);
    assert.equal(result.status, 2, `${args.join(' ')}: ${result.stderr}`);
    const lines = result.stderr.split('\n').filter(Boolean);
    assert.equal(lines[0], line, result.stderr);
    assert.ok(lines[1]?.startsWith(USAGE_PREFIX), `no usage line: ${result.stderr}`);
    assert.equal(lines.length, 2, result.stderr);
    assert.deepEqual(await fixture.takeCalls(), [], `${args.join(' ')} called uv`);
  }
});

test('a failing tool maps to exit 1, and lint runs both of its calls before failing', async (t) => {
  const fixture = await buildFixture(t);
  await fixture.plantVenv();
  const env = { FAKE_UV_STATUS: '5' };

  const testRun = await fixture.runScript(['test'], { env });
  assert.equal(testRun.status, 1, testRun.stderr);
  assertCalls(await fixture.takeCalls(), fixture.repo, [[...LEG_PREFIX, 'pytest']], 'test, failing');

  const lint = await fixture.runScript(['lint'], { env });
  assert.equal(lint.status, 1, lint.stderr);
  const calls = await fixture.takeCalls();
  assertCalls(calls, fixture.repo, LEGS[0].argvs, 'lint, failing');
  await assertNothingUnderHome(fixture, calls);
});

test('a directory that is not a table row, and a bare --package, exit 2 with the unknown-package line and call no uv', async (t) => {
  const fixture = await buildFixture(t);
  await fixture.plantVenv();
  await fixture.plantVenv(OTHER_PACKAGE);
  for (const [args, dir] of [[['--package', OTHER_PACKAGE, 'lint'], OTHER_PACKAGE], [['--package'], '']]) {
    const result = await fixture.runScript(args);
    assert.equal(result.status, 2, `${args.join(' ')}: ${result.stderr}`);
    const lines = result.stderr.split('\n').filter(Boolean);
    assert.equal(lines[0], UNKNOWN_PACKAGE_LINE(dir), result.stderr);
    assert.ok(lines[1]?.startsWith(USAGE_PREFIX), `no usage line: ${result.stderr}`);
    assert.equal(lines.length, 2, result.stderr);
    assert.deepEqual(await fixture.takeCalls(), [], `${args.join(' ')} called uv`);
  }
});

test('with uv present but no pyvenv.cfg, each leg exits 3 naming provision and calls no uv', async (t) => {
  const fixture = await buildFixture(t);
  for (const args of LEG_NAMES) {
    const result = await fixture.runScript(args);
    assert.equal(result.status, 3, `${args.join(' ')}: ${result.stderr}`);
    assert.match(result.stderr, /provision/, `${args.join(' ')}: ${result.stderr}`);
    assert.deepEqual(await fixture.takeCalls(), [], `${args.join(' ')} called uv`);
  }
});

test('with no uv on PATH, each leg exits 3', async (t) => {
  const fixture = await buildFixture(t);
  const realUv = resolveOnBase('uv', fixture.base);
  if (realUv !== undefined) {
    t.skip(`the base PATH resolves a real uv at ${realUv}`);
    return;
  }
  await fixture.plantVenv();
  for (const args of LEG_NAMES) {
    const result = await fixture.runScript(args, { noUv: true });
    assert.equal(result.status, 3, `${args.join(' ')}: ${result.stderr}`);
    assert.match(result.stderr, /provision/, `${args.join(' ')}: ${result.stderr}`);
  }
});

test('container-test with no docker on PATH exits 4', async (t) => {
  const fixture = await buildFixture(t);
  const realDocker = resolveOnBase('docker', fixture.base);
  if (realDocker !== undefined) {
    t.skip(`the base PATH resolves a real docker at ${realDocker}`);
    return;
  }
  await fixture.plantVenv();
  const result = await fixture.runScript(['container-test']);
  assert.equal(result.status, 4, result.stderr);
  assert.match(result.stderr, /SKIPPED/, result.stderr);
  assert.deepEqual(await fixture.takeCalls(), []);
});

test('provision syncs the rows in table order, each in its own directory, and reports a failure as exit 1', async (t) => {
  const fixture = await buildFixture(t);
  const sync = ['sync', '--frozen', '--group', 'dev'];
  const ok = await fixture.runScript(['provision']);
  assert.equal(ok.status, 0, ok.stderr);
  assert.equal(ok.stdout, `python-service: provisioned ${PACKAGE}\npython-service: provisioned ${LIBRARY}\n`);
  const calls = await fixture.takeCalls();
  assert.equal(calls.length, 2, 'provision: one sync per row');
  assertCalls(calls.slice(0, 1), fixture.repo, [sync], `provision, ${PACKAGE}`);
  assertCalls(calls.slice(1), fixture.repo, [sync], `provision, ${LIBRARY}`, LIBRARY);
  await assertNothingUnderHome(fixture, calls);

  const failed = await fixture.runScript(['provision'], { env: { FAKE_UV_STATUS: '1' } });
  assert.equal(failed.status, 1, failed.stderr);
  const stderrLines = failed.stderr.split('\n');
  for (const row of [PACKAGE, LIBRARY]) {
    assert.ok(stderrLines.includes(`python-service: provision: ${row} failed (exit 1)`), failed.stderr);
  }
});

test('provision with no uv on PATH prints one SKIPPED line, exits 0 and writes nothing in the fixture', async (t) => {
  const fixture = await buildFixture(t);
  const realUv = resolveOnBase('uv', fixture.base);
  if (realUv !== undefined) {
    t.skip(`the base PATH resolves a real uv at ${realUv}`);
    return;
  }
  // `--untracked-files=all` so a file created inside an untracked directory changes the listing.
  const status = ['status', '--porcelain', '--ignored', '--untracked-files=all'];
  const before = (await runGit(fixture.repo, status)).stdout;
  const result = await fixture.runScript(['provision'], { noUv: true });
  assert.equal(result.status, 0, result.stderr);
  const lines = result.stderr.split('\n').filter(Boolean);
  assert.equal(lines.length, 1, result.stderr);
  assert.ok(lines[0].includes('SKIPPED') && lines[0].includes('uv is not on PATH'), result.stderr);
  assert.equal((await runGit(fixture.repo, status)).stdout, before);
});

test('provision takes no argument and no --package', async (t) => {
  const fixture = await buildFixture(t);
  for (const args of [['provision', 'extra'], ['--package', PACKAGE, 'provision'], ['--package', LIBRARY, 'provision']]) {
    const result = await fixture.runScript(args);
    assert.equal(result.status, 2, `${args.join(' ')}: ${result.stderr}`);
    assert.deepEqual(await fixture.takeCalls(), [], `${args.join(' ')} called uv`);
  }
});

test('sync carries no --no-cache, and --with-models appends --extra models', async (t) => {
  const fixture = await buildFixture(t);
  const plain = await fixture.runScript(['sync']);
  assert.equal(plain.status, 0, plain.stderr);
  assertCalls(await fixture.takeCalls(), fixture.repo, [['sync', '--frozen', '--group', 'dev']], 'sync');

  const models = await fixture.runScript(['sync', '--with-models']);
  assert.equal(models.status, 0, models.stderr);
  assertCalls(
    await fixture.takeCalls(),
    fixture.repo,
    [['sync', '--frozen', '--group', 'dev', '--extra', 'models']],
    'sync --with-models',
  );
});

test(`probe, provisioned: one python call on the physical target, from the row's directory, by default and under --package ${LIBRARY}`, async (t) => {
  const fixture = await buildFixture(t, { withLibrary: true });
  await fixture.plantVenv();
  await fixture.plantVenv(LIBRARY);
  const target = join(fixture.repo, PROBE);
  const all = [];
  for (const [args, pkg] of [
    [['probe', PROBE, 'a', 'b'], PACKAGE],
    [['--package', LIBRARY, 'probe', target, 'a', 'b'], LIBRARY],
  ]) {
    const result = await fixture.runScript(args);
    assert.equal(result.status, 0, `${args.join(' ')}: ${result.stderr}`);
    const calls = await fixture.takeCalls();
    assertCalls(calls, fixture.repo, [[...LEG_PREFIX, 'python', target, 'a', 'b']], args.join(' '), pkg);
    all.push(...calls);
  }
  await assertNothingUnderHome(fixture, all);
});

test("probe passes the file's own exit status through", async (t) => {
  const fixture = await buildFixture(t, { withLibrary: true });
  await fixture.plantVenv();
  const result = await fixture.runScript(['probe', PROBE], { env: { FAKE_UV_STATUS: '7' } });
  assert.equal(result.status, 7, result.stderr);
  assert.equal((await fixture.takeCalls()).length, 1, 'probe: one uv call');
});

test('probe refuses a path outside scratch, a `..` path, an option, a non-.py file, an absent file and no argument with exit 2 and no uv call', async (t) => {
  const fixture = await buildFixture(t, { withLibrary: true });
  await fixture.plantVenv();
  const { repo } = fixture;
  const scratch = join(repo, SCRATCH);
  const dotdot = `${SCRATCH}/../scratch/probe.py`;
  const refusals = [
    [['probe', 'outside.py'], `python-service: probe: 'outside.py' resolves to '${repo}', outside '${scratch}' — refusing`],
    [['probe', dotdot], `python-service: probe: '${dotdot}' carries '..' — refusing, a scratch path names no parent`],
    [['probe', '-c'], "python-service: probe: '-c' is an option, not a file — refusing, a probe takes no inline program"],
    [['probe', `${SCRATCH}/probe.mjs`], "python-service: probe: 'probe.mjs' is not a .py file — refusing"],
    [['probe', `${SCRATCH}/absent.py`], `python-service: probe: '${join(scratch, 'absent.py')}' is not a readable regular file`],
    [['probe'], 'python-service: probe: no file argument'],
  ];
  for (const [args, line] of refusals) {
    const result = await fixture.runScript(args);
    assert.equal(result.status, 2, `${args.join(' ')}: ${result.stderr}`);
    assert.equal(result.stderr.split('\n')[0], line, result.stderr);
    assert.deepEqual(await fixture.takeCalls(), [], `${args.join(' ')} called uv`);
  }
});

test('probe with no pyvenv.cfg exits 3 and calls no uv', async (t) => {
  const fixture = await buildFixture(t, { withLibrary: true });
  const result = await fixture.runScript(['probe', PROBE]);
  assert.equal(result.status, 3, result.stderr);
  assert.match(result.stderr, /provision/, result.stderr);
  assert.deepEqual(await fixture.takeCalls(), []);
});

test('probe with no library beside the script exits 1 naming it, and calls no uv', async (t) => {
  const fixture = await buildFixture(t);
  await fixture.plantVenv();
  const result = await fixture.runScript(['probe', PROBE]);
  assert.equal(result.status, 1, result.stderr);
  const lib = join(fixture.repo, 'scripts', 'lib', 'harness-run-lib.sh');
  assert.equal(result.stderr, `python-service: probe: cannot read ${lib} — refusing to run anything\n`);
  assert.deepEqual(await fixture.takeCalls(), []);
});

/** The `check` stdout for `verdicts`, four in table order: each row's `lint`, then its `typecheck`. */
function checkLines(verdicts) {
  const legs = [PACKAGE, LIBRARY].flatMap((row) => ['lint', 'typecheck'].map((leg) => `${row} ${leg}`));
  return legs.map((leg, i) => `python-service: check: ${leg} ${verdicts[i]}\n`).join('');
}

const CHECK_ARGVS = [LEGS[0].argvs[0], LEGS[0].argvs[1], LEGS[1].argvs[0]];

test('check, both rows provisioned: six calls in table order, each at its row, four PASS lines, exit 0', async (t) => {
  const fixture = await buildFixture(t);
  await fixture.plantVenv();
  await fixture.plantVenv(LIBRARY);
  const result = await fixture.runScript(['check']);
  assert.equal(result.status, 0, result.stderr);
  assert.equal(result.stdout, checkLines(['PASS', 'PASS', 'PASS', 'PASS']));
  const calls = await fixture.takeCalls();
  assert.equal(calls.length, 6, 'check: six uv calls');
  assertCalls(calls.slice(0, 3), fixture.repo, CHECK_ARGVS, `check, ${PACKAGE}`);
  assertCalls(calls.slice(3), fixture.repo, CHECK_ARGVS, `check, ${LIBRARY}`, LIBRARY);
  await assertNothingUnderHome(fixture, calls);
});

test(`check with only ${PACKAGE} provisioned grades ${LIBRARY} BLOCKED and exits 3`, async (t) => {
  const fixture = await buildFixture(t);
  await fixture.plantVenv();
  const result = await fixture.runScript(['check']);
  assert.equal(result.status, 3, result.stderr);
  assert.equal(result.stdout, checkLines(['PASS', 'PASS', 'BLOCKED', 'BLOCKED']));
  assertCalls(await fixture.takeCalls(), fixture.repo, CHECK_ARGVS, `check, ${PACKAGE}`);
});

test('check with a failing tool grades FAIL over BLOCKED, exits 1 and still runs every leg', async (t) => {
  const fixture = await buildFixture(t);
  await fixture.plantVenv();
  const result = await fixture.runScript(['check'], { env: { FAKE_UV_STATUS: '1' } });
  assert.equal(result.status, 1, result.stderr);
  assert.equal(result.stdout, checkLines(['FAIL', 'FAIL', 'BLOCKED', 'BLOCKED']));
  assertCalls(await fixture.takeCalls(), fixture.repo, CHECK_ARGVS, `check failing, ${PACKAGE}`);
});

test('check with no uv on PATH prints four BLOCKED lines and exits 3', async (t) => {
  const fixture = await buildFixture(t);
  const realUv = resolveOnBase('uv', fixture.base);
  if (realUv !== undefined) {
    t.skip(`the base PATH resolves a real uv at ${realUv}`);
    return;
  }
  await fixture.plantVenv();
  await fixture.plantVenv(LIBRARY);
  const result = await fixture.runScript(['check'], { noUv: true });
  assert.equal(result.status, 3, result.stderr);
  assert.equal(result.stdout, checkLines(['BLOCKED', 'BLOCKED', 'BLOCKED', 'BLOCKED']));
});

test('check takes no argument and no --package', async (t) => {
  const fixture = await buildFixture(t);
  await fixture.plantVenv();
  await fixture.plantVenv(LIBRARY);
  for (const args of [['check', 'x'], ['--package', LIBRARY, 'check']]) {
    const result = await fixture.runScript(args);
    assert.equal(result.status, 2, `${args.join(' ')}: ${result.stderr}`);
    assert.deepEqual(await fixture.takeCalls(), [], `${args.join(' ')} called uv`);
  }
});

test('the script carries exactly one `# PROVIDES: provision` line', () => {
  const matches = readFileSync(SCRIPT, 'utf8').split('\n').filter((line) => line === '# PROVIDES: provision');
  assert.equal(
    matches.length,
    1,
    "devscene.config.json → commands.depInstall runs provision only after `grep -qx '# PROVIDES: provision'` " +
      'finds this exact line; a respelling silently stops every run copy from provisioning',
  );
});
