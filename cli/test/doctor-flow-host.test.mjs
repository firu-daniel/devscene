/**
 * `doctor`'s `uv` and `flow-host` lines, against the compiled CLI on repositories `init` wired.
 *
 * **The rule this suite enforces: a host without `uv`, shipped Python packages that are missing or
 * changed, and an unprovisioned walker environment are each reported as a warning naming its
 * remedy, and none of them moves `doctor`'s exit status until #419 makes the walker needed.**
 *
 * `uv` is given to the command as a machine rather than mocked: a stub first on `PATH`, or a `PATH`
 * built from links to only the binaries the run needs, so the host's own `uv` cannot reach a case.
 */

import assert from 'node:assert/strict';
import { accessSync, appendFileSync, constants as fsConstants, mkdirSync, rmSync, symlinkSync, writeFileSync } from 'node:fs';
import { mkdtemp, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { delimiter, join } from 'node:path';
import { describe, it } from 'node:test';

import { requireConfig } from '../dist/config/io.js';
import { flowHostEnvDir, flowHostProjectDir } from '../dist/flowHost/layout.js';
import { flowHostProvisionInvocation } from '../dist/flowHost/provision.js';
import { CASE_CONCURRENCY } from './helpers/concurrency.mjs';
import { createFixture, runCli } from './helpers/fixture.mjs';

const UV_CHECK = 'uv';
const FLOW_HOST_CHECK = 'flow-host';
const REMEDY = 'init --upgrade';
const STUB_VERSION = 'uv 0.9.0';
const ENV_MARKER_FILE = 'pyvenv.cfg';

/**
 * The binaries a wired fixture's `doctor` run needs to pass every other check, linked into the
 * `PATH` that leaves `uv` out. Built from links rather than by filtering the host's `PATH`, because
 * `uv` and `jq` commonly share a directory.
 */
const NEEDED_BINARIES = ['git', 'jq', 'bash', 'sh', 'node', 'npm', 'echo', 'env'];

/** A repository whose stack detection resolves every command — the seed `doctor.test.mjs` uses. */
function nodeProjectFiles() {
  return {
    'package.json': {
      name: 'fixture-project',
      private: true,
      version: '0.0.0',
      scripts: { typecheck: 'echo typecheck', test: 'echo test', build: 'echo build', dev: 'echo dev' },
    },
    'README.md': '# fixture project\n',
  };
}

/** A repository wired by the compiled `init`. */
async function wired(t) {
  const fixture = await createFixture({ files: nodeProjectFiles() });
  t.after(fixture.cleanup);
  const result = await runCli(fixture.dir, ['init']);
  assert.equal(result.status, 0, `init exited ${result.status}\n${result.stdout}\n${result.stderr}`);
  return fixture.dir;
}

async function tempDir(t, prefix) {
  const dir = await mkdtemp(join(tmpdir(), prefix));
  t.after(() => rm(dir, { recursive: true, force: true }));
  return dir;
}

/** Where a name resolves on this machine's `PATH`, or `undefined`. */
function resolveOnPath(name) {
  for (const entry of (process.env.PATH ?? '').split(delimiter)) {
    if (entry === '') continue;
    const candidate = join(entry, name);
    try {
      accessSync(candidate, fsConstants.X_OK);
      return candidate;
    } catch {
      // Not here; keep looking.
    }
  }
  return undefined;
}

/** A `PATH` with a stub `uv` printing `line` ahead of the host's own. */
async function uvStubPath(t, line) {
  const dir = await tempDir(t, 'harness-uv-stub-');
  writeFileSync(join(dir, 'uv'), `#!/bin/sh\nprintf '%s\\n' ${JSON.stringify(line)}\n`, { mode: 0o755 });
  return `${dir}${delimiter}${process.env.PATH ?? ''}`;
}

/** A `PATH` of links to {@link NEEDED_BINARIES} only, so no `uv` resolves. */
async function pathWithoutUv(t) {
  const dir = await tempDir(t, 'harness-nouv-');
  for (const name of NEEDED_BINARIES) {
    const target = resolveOnPath(name);
    assert.ok(target, `${name} does not resolve on PATH, so an environment without uv cannot be built for this test`);
    symlinkSync(target, join(dir, name));
  }
  return dir;
}

/** The `id` line in `status` from the stream the reporter puts it on, or `undefined`. */
function checkLine({ stdout, stderr }, status, id) {
  const [stream, prefix] = status === 'PASS' ? [stdout, ''] : [stderr, '! '];
  return stream.split('\n').find((line) => new RegExp(`^${prefix}${status}\\s+${id}\\s`).test(line));
}

function line(result, status, id) {
  const found = checkLine(result, status, id);
  assert.ok(found, `no ${status} ${id} line\n${result.stderr}\n${result.stdout}`);
  return found;
}

async function doctor(dir, env = {}) {
  const result = await runCli(dir, ['doctor'], env);
  assert.equal(result.status, 0, `doctor exited ${result.status}\n${result.stdout}\n${result.stderr}`);
  return result;
}

/** Plant the marker `uv` writes into every environment, as a provisioned repository has. */
function plantEnvironment(dir) {
  const envDir = join(dir, ...flowHostEnvDir(requireConfig(dir)).split('/'));
  mkdirSync(envDir, { recursive: true });
  writeFileSync(join(envDir, ENV_MARKER_FILE), 'home = /usr/bin\n');
}

/** One shipped file's repo-relative path: the walker project's own `pyproject.toml`. */
function shippedFile(dir) {
  return `${flowHostProjectDir(requireConfig(dir))}/pyproject.toml`;
}

describe('doctor uv and flow-host', { concurrency: CASE_CONCURRENCY }, () => {
  it('passes uv with a stub that answers, quoting the printed version', async (t) => {
    const dir = await wired(t);
    const result = await doctor(dir, { PATH: await uvStubPath(t, STUB_VERSION) });
    const pass = line(result, 'PASS', UV_CHECK);
    assert.ok(pass.includes(JSON.stringify(STUB_VERSION)), pass);
  });

  it('warns on uv with no uv reachable, and doctor still exits 0', async (t) => {
    const dir = await wired(t);
    const result = await doctor(dir, { PATH: await pathWithoutUv(t) });
    assert.match(line(result, 'WARN', UV_CHECK), /DevScene requires uv/);
    const flowHost = line(result, 'WARN', FLOW_HOST_CHECK);
    assert.match(flowHost, /install uv first/);
    assert.match(result.stdout, /^Summary: \d+ pass, [1-9]\d* warn, 0 fail — exit 0/m);
  });

  it('warns on uv when the stub prints no version', async (t) => {
    const dir = await wired(t);
    const result = await doctor(dir, { PATH: await uvStubPath(t, 'not a version') });
    assert.match(line(result, 'WARN', UV_CHECK), /carries no version/);
  });

  it('warns on flow-host naming the provisioning command, then passes once provisioned', async (t) => {
    const dir = await wired(t);
    const env = { PATH: await uvStubPath(t, STUB_VERSION) };
    const command = flowHostProvisionInvocation(requireConfig(dir));

    const unprovisioned = line(await doctor(dir, env), 'WARN', FLOW_HOST_CHECK);
    assert.ok(unprovisioned.includes(command), unprovisioned);
    assert.match(unprovisioned, /outside the sandbox/);
    assert.doesNotMatch(unprovisioned, /install uv first/);

    plantEnvironment(dir);
    line(await doctor(dir, env), 'PASS', FLOW_HOST_CHECK);
  });

  it('warns on flow-host naming an edited shipped file and init --upgrade', async (t) => {
    const dir = await wired(t);
    plantEnvironment(dir);
    const file = shippedFile(dir);
    appendFileSync(join(dir, ...file.split('/')), '# edited\n');

    const warning = line(await doctor(dir), 'WARN', FLOW_HOST_CHECK);
    assert.ok(warning.includes(`changed from what this CLI ships: ${file}`), warning);
    assert.ok(warning.includes(REMEDY), warning);
  });

  it('warns on flow-host naming a deleted shipped file as missing', async (t) => {
    const dir = await wired(t);
    plantEnvironment(dir);
    const file = shippedFile(dir);
    rmSync(join(dir, ...file.split('/')));

    const warning = line(await doctor(dir), 'WARN', FLOW_HOST_CHECK);
    assert.ok(warning.includes(`missing: ${file}`), warning);
    assert.ok(warning.includes(REMEDY), warning);
  });

  it('lists uv after jq and flow-host after outer-loop-scripts', async () => {
    const { CHECKS } = await import('../dist/doctor/checks.js');
    const ids = CHECKS.map((check) => check.id);
    assert.equal(ids.indexOf(UV_CHECK), ids.indexOf('jq') + 1);
    assert.equal(ids.indexOf(FLOW_HOST_CHECK), ids.indexOf('outer-loop-scripts') + 1);
  });
});
