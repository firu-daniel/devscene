/**
 * The build-time staging of the shipped Python packages into this package's `dist/python/`.
 *
 * **The rule this module exists to enforce: it is the one producer of `dist/python/`, and it runs
 * only from a source checkout.** For each of `FLOW_HOST_PACKAGES` it removes the staged copy and
 * copies, byte for byte, every file `isShippedPythonFile` admits from the workspace root's package of
 * that name. A package missing its `pyproject.toml`, `uv.lock` or `src/` throws, naming the path.
 *
 * **It writes outside `cli/src/core/writer.ts`** because what it writes is this package's own build
 * output, never an adopting repository; the write engine's monopoly covers only adopting
 * repositories. **Its uncaught throw ends the build** and it never calls `process.exit()`: it is the
 * one exception `cli/src/core/errors.ts` rule 1 names.
 *
 * **The compiled `dist/flowHost/stage.js` ships in the tarball**, because `files` carries all of
 * `dist`, and it never runs there: its main-module guard is reached only through
 * `cli/package.json` → `build`, in a source checkout, where the workspace root is the parent of
 * `packageRoot()`.
 */

import { copyFileSync, lstatSync, mkdirSync, readdirSync, rmSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

import { internal } from '../core/errors.js';
import { lstatOrUndefined, packageRoot } from '../core/paths.js';
import { FLOW_HOST_PACKAGES, isShippedPythonFile, stagedPythonDir } from './layout.js';

/** The paths, relative to a package's root, that must exist for it to be staged. */
const REQUIRED_PATHS = ['pyproject.toml', 'uv.lock', 'src'] as const;

/** Every regular file under `relativeDir`, forward-slashed and relative to `base`, in sorted order. */
function listFiles(base: string, relativeDir: string): string[] {
  const files: string[] = [];
  const entries = readdirSync(join(base, ...relativeDir.split('/'))).sort();
  for (const name of entries) {
    const relativePath = `${relativeDir}/${name}`;
    const stat = lstatSync(join(base, ...relativePath.split('/')));
    if (stat.isDirectory()) files.push(...listFiles(base, relativePath));
    else if (stat.isFile()) files.push(relativePath);
    else throw internal(`${join(base, ...relativePath.split('/'))} is neither a regular file nor a directory, so it cannot be staged`);
  }
  return files;
}

/**
 * Stage every package of `FLOW_HOST_PACKAGES` from `workspaceRoot` into `outDir`, returning the
 * staged files as forward-slashed paths relative to `outDir`, in staging order.
 */
export function stagePythonPackages({ workspaceRoot, outDir }: { workspaceRoot: string; outDir: string }): string[] {
  const staged: string[] = [];
  for (const pkg of FLOW_HOST_PACKAGES) {
    const source = join(workspaceRoot, pkg);
    for (const required of REQUIRED_PATHS) {
      const path = join(source, required);
      if (lstatOrUndefined(path) === undefined) throw internal(`${path} is missing, so ${pkg} cannot be staged`);
    }

    const target = join(outDir, pkg);
    rmSync(target, { recursive: true, force: true });

    const candidates = ['pyproject.toml', 'uv.lock', ...listFiles(source, 'src')].sort();
    for (const relativePath of candidates.filter(isShippedPythonFile)) {
      const destination = join(target, ...relativePath.split('/'));
      mkdirSync(dirname(destination), { recursive: true });
      copyFileSync(join(source, ...relativePath.split('/')), destination);
      staged.push(`${pkg}/${relativePath}`);
    }
  }
  return staged;
}

const invokedAs = process.argv[1];
if (invokedAs !== undefined && resolve(invokedAs) === fileURLToPath(import.meta.url)) {
  stagePythonPackages({ workspaceRoot: dirname(packageRoot()), outDir: stagedPythonDir() });
}
