/**
 * Generator: the shipped Python packages — every file `cli/src/flowHost/layout.ts` →
 * `FLOW_HOST_PACKAGES` names, staged at build under this package's `dist/python/` — written into an
 * adopting repository at `<scriptsDir>/python/<package>/`.
 *
 * **The rule this module exists to enforce: the files written are the staged tree's, byte for byte,
 * and the staged tree is the only source of them.** The set is read off `stagedPythonDir()` and
 * filtered through `isShippedPythonFile`; nothing here lists a package file or re-derives the layout.
 *
 * It copies verbatim and renders nothing, so it has no `assertNoneSurvive` setting to argue: no
 * file passes through `cli/src/core/templating.ts`, and a `{{…}}` in a Python source is content.
 * Verbatim copies make both re-run contracts a byte test, as `generators/outerLoopScripts.ts` →
 * choice 1 argues for its own set: `create-if-absent` under `init`, `replace-if-changed` under
 * `init --upgrade`.
 *
 * A staged tree that is absent or empty, or that holds a file that does not survive a UTF-8 round
 * trip (the write plan carries text), is a packaging fault and throws through `internal()`.
 *
 * **Deliberately not covered:** a file a later release stops shipping stays on disk, because nothing
 * here removes.
 */

import { lstatSync, readdirSync, readFileSync } from 'node:fs';
import { join, posix } from 'node:path';

import type { HarnessConfig } from '../config/model.js';
import { internal } from '../core/errors.js';
import { lstatOrUndefined } from '../core/paths.js';
import type { WritePlan, WritePolicy } from '../core/writer.js';
import { FLOW_HOST_PACKAGES, flowHostDir, isShippedPythonFile, stagedPythonDir } from '../flowHost/layout.js';

/** Every shipped file is data or a module imported by an interpreter; none is executed directly. */
const SHIPPED_FILE_MODE = 0o644;

/** The one bit {@link flowHostPackageDrift} compares, for the reason `outerLoopScripts.ts` gives for its own. */
const OWNER_EXECUTE_BIT = 0o100;

/** `ENOTDIR` counts as absent: a regular file where a package directory belongs leaves its files missing. */
const ABSENT_CODES: readonly string[] = ['ENOENT', 'ENOTDIR'];

/** Everything {@link writeFlowHostPackages} and {@link planFlowHostPackageUpgrade} need. */
export interface FlowHostPackagesOptions {
  readonly repoRoot: string;
  readonly config: HarnessConfig;
  /** The command's write plan; this generator enqueues into it and never touches `fs` to write. */
  readonly plan: WritePlan;
}

/** What the generator enqueued. */
export interface FlowHostPackagesResult {
  /** Repo-relative, forward-slashed paths of the files enqueued, in shipped order. */
  readonly written: readonly string[];
}

/** How the copies on disk differ from the staged tree. Repo-relative, in shipped order. */
export interface FlowHostPackageDrift {
  readonly missing: readonly string[];
  readonly changed: readonly string[];
}

/** One shipped file: its path relative to `stagedPythonDir()`, forward-slashed, and its staged bytes. */
interface ShippedFile {
  readonly relativePath: string;
  readonly bytes: Buffer;
}

/** Every regular file under `root/relativeDir`, forward-slashed and relative to `root`. */
function filesUnder(root: string, relativeDir: string): string[] {
  const files: string[] = [];
  for (const name of readdirSync(join(root, ...relativeDir.split('/')))) {
    const relativePath = `${relativeDir}/${name}`;
    const stats = lstatSync(join(root, ...relativePath.split('/')));
    if (stats.isDirectory()) files.push(...filesUnder(root, relativePath));
    else if (stats.isFile()) files.push(relativePath);
    else throw internal(`${join(root, ...relativePath.split('/'))} in the staged Python tree is neither a regular file nor a directory`);
  }
  return files;
}

/** The staged files, package by package in `FLOW_HOST_PACKAGES` order, each package's files sorted. */
function shippedFiles(): ShippedFile[] {
  const staged = stagedPythonDir();
  const shipped: ShippedFile[] = [];
  for (const pkg of FLOW_HOST_PACKAGES) {
    const stats = lstatOrUndefined(join(staged, pkg), ABSENT_CODES);
    if (stats === undefined || !stats.isDirectory()) {
      throw internal(`the staged Python package ${join(staged, pkg)} is missing from the installed package`);
    }
    const files = filesUnder(staged, pkg)
      .filter((path) => isShippedPythonFile(path.slice(pkg.length + 1)))
      .sort();
    if (files.length === 0) throw internal(`the staged Python package ${join(staged, pkg)} holds no shipped file`);
    for (const relativePath of files) {
      shipped.push({ relativePath, bytes: readFileSync(join(staged, ...relativePath.split('/'))) });
    }
  }
  return shipped;
}

/** The staged bytes as the text the write plan carries, refusing any file the round trip would alter. */
function shippedText({ relativePath, bytes }: ShippedFile): string {
  const text = bytes.toString('utf8');
  if (!Buffer.from(text, 'utf8').equals(bytes)) {
    throw internal(`the staged Python file ${relativePath} is not valid UTF-8, so it cannot be copied as text`);
  }
  return text;
}

/** Enqueue one `ensure-dir` per directory, then one write per shipped file under `policy`. */
function enqueueFlowHostPackages({ repoRoot, config, plan }: FlowHostPackagesOptions, policy: WritePolicy): FlowHostPackagesResult {
  const base = flowHostDir(config);
  const files = shippedFiles();
  const ensured = new Set<string>();
  const ensure = (dir: string): void => {
    if (ensured.has(dir)) return;
    const parent = posix.dirname(dir);
    if (parent !== '.') ensure(parent);
    ensured.add(dir);
    plan.add({ path: join(repoRoot, base, ...dir.split('/')), policy: 'ensure-dir', label: `shipped Python directory ${dir}` });
  };

  plan.add({ path: join(repoRoot, ...base.split('/')), policy: 'ensure-dir', label: 'shipped Python packages directory' });
  const written: string[] = [];
  for (const file of files) {
    ensure(posix.dirname(file.relativePath));
    plan.add({
      path: join(repoRoot, ...base.split('/'), ...file.relativePath.split('/')),
      policy,
      content: shippedText(file),
      label: `shipped Python file ${file.relativePath}`,
      mode: SHIPPED_FILE_MODE,
    });
    written.push(posix.join(base, file.relativePath));
  }
  return { written };
}

/**
 * Enqueue the shipped packages under `create-if-absent`: a re-run keeps an edited copy, and `--force`
 * replaces it after the write engine's `.bak`.
 */
export function writeFlowHostPackages(options: FlowHostPackagesOptions): FlowHostPackagesResult {
  return enqueueFlowHostPackages(options, 'create-if-absent');
}

/** Enqueue the same set under `replace-if-changed`, `init --upgrade`'s contract. */
export function planFlowHostPackageUpgrade(options: FlowHostPackagesOptions): FlowHostPackagesResult {
  return enqueueFlowHostPackages(options, 'replace-if-changed');
}

/**
 * Which shipped files differ from the staged tree. Bytes are compared as buffers, so an invalid
 * UTF-8 sequence cannot decode into a match. Reads only.
 */
export function flowHostPackageDrift(repoRoot: string, config: HarnessConfig): FlowHostPackageDrift {
  const base = flowHostDir(config);
  const missing: string[] = [];
  const changed: string[] = [];
  for (const { relativePath, bytes } of shippedFiles()) {
    const repoRelative = posix.join(base, relativePath);
    const path = join(repoRoot, ...repoRelative.split('/'));
    const stats = lstatOrUndefined(path, ABSENT_CODES);
    if (stats === undefined) {
      missing.push(repoRelative);
      continue;
    }
    const current =
      stats.isFile() &&
      (Number(stats.mode) & OWNER_EXECUTE_BIT) === (SHIPPED_FILE_MODE & OWNER_EXECUTE_BIT) &&
      readFileSync(path).equals(bytes);
    if (!current) changed.push(repoRelative);
  }
  return { missing, changed };
}
