/**
 * The shipped Python layout: the GraphScene packages this package carries under `dist/python/`, and
 * where they land in an adopting repository, under `<scriptsDir>/python/`.
 *
 * **The rule this module exists to enforce: this is the one owner of every name the shipped Python
 * layout is reached by.** No other module spells the layout's directory, its package names, its
 * project, its environment directory or the shipped-file set; each reads the export here, so the
 * staging step, the writer that copies the tree into an adopting repository and the step that syncs
 * its environment cannot disagree about a path.
 *
 * MIRRORS. `hr_flow_host_provision` in `cli/templates/scripts/lib/harness-run-lib.sh` spells
 * {@link FLOW_HOST_DIRNAME}, {@link FLOW_HOST_PROJECT} and {@link FLOW_HOST_ENV_DIRNAME} as shell
 * literals, because a shipped script cannot import this module; a rename here is an edit there,
 * and `cli/test/flow-host-provision.test.mjs` holds the two equal.
 */

import { join, posix } from 'node:path';

import type { HarnessConfig } from '../config/model.js';
import { packageRoot } from '../core/paths.js';
import { outerLoopScriptsDir } from '../generators/outerLoopScripts.js';

/** The directory, under `scriptsDir` in an adopting repository and under `dist/` here, holding the packages. */
export const FLOW_HOST_DIRNAME = 'python';

/** The shipped packages, in order: `devscene-flow-host` sources `graphscene` from `../graphscene`. */
export const FLOW_HOST_PACKAGES: readonly string[] = ['graphscene', 'devscene-flow-host'];

/** The package whose project the environment is synced from. */
export const FLOW_HOST_PROJECT = 'devscene-flow-host';

/** The environment directory, inside {@link FLOW_HOST_PROJECT}'s directory. */
export const FLOW_HOST_ENV_DIRNAME = '.venv';

/** The staged tree inside this package: `<packageRoot>/dist/python`. */
export function stagedPythonDir(): string {
  return join(packageRoot(), 'dist', FLOW_HOST_DIRNAME);
}

/** The repo-relative directory the packages land in: `<scriptsDir>/python`. */
export function flowHostDir(config: HarnessConfig): string {
  return posix.join(outerLoopScriptsDir(config), FLOW_HOST_DIRNAME);
}

/** The repo-relative directory of {@link FLOW_HOST_PROJECT}: `<scriptsDir>/python/devscene-flow-host`. */
export function flowHostProjectDir(config: HarnessConfig): string {
  return posix.join(flowHostDir(config), FLOW_HOST_PROJECT);
}

/** The repo-relative environment directory: `<scriptsDir>/python/devscene-flow-host/.venv`. */
export function flowHostEnvDir(config: HarnessConfig): string {
  return posix.join(flowHostProjectDir(config), FLOW_HOST_ENV_DIRNAME);
}

/**
 * Whether a file, given by its forward-slashed path relative to its package's root, is shipped:
 * `pyproject.toml`, `uv.lock`, and every file under `src/` except a `__pycache__` directory's
 * contents and a `*.pyc`.
 */
export function isShippedPythonFile(relativePath: string): boolean {
  if (relativePath === 'pyproject.toml' || relativePath === 'uv.lock') return true;
  const segments = relativePath.split('/');
  if (segments[0] !== 'src' || segments.length < 2) return false;
  if (segments.includes('__pycache__')) return false;
  return !relativePath.endsWith('.pyc');
}
