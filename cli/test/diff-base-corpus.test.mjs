/**
 * The end-of-branch diff base across the plugin corpus.
 *
 * **The rule this suite exists to enforce: every end-of-branch diff and commit range in
 * `plugin/**\/*.md` is based on `origin/<default_branch>`, and each file that runs `git diff` or
 * `git log` against that base carries the fallback sentence verbatim.**
 *
 * Registered as a tree guard by Task 5 of `fix_default_branch_diff_base`, which adds this file's
 * `treeGuards` entry to `devscene.config.json`.
 *
 * Not covered, deliberately — both are review's: whether a sentence sits in the right row, and
 * `git show <default_branch>:` row reads, which keep `review-sweep.sh`'s local-first rule.
 *
 * RED ONCE (no-bare-base) — 2026-11-21, `origin/` dropped from one `git diff
 * origin/<default_branch>...HEAD` line of `plugin/agents/skeptic-reviewer.md` in the working tree
 * only, then restored: `no-bare-base` failed its `deepEqual`, listing
 * `plugin/agents/skeptic-reviewer.md:90`.
 *
 * RED ONCE (fallback-sentence) — 2026-11-21, the fallback sentence deleted from
 * `plugin/instructions/docs_phase_instructions.md` in the working tree only, then restored:
 * `fallback-sentence` failed its `deepEqual`, listing
 * `plugin/instructions/docs_phase_instructions.md`.
 */

import assert from 'node:assert/strict';
import { readdirSync, readFileSync } from 'node:fs';
import { join, relative, sep } from 'node:path';
import test from 'node:test';

import { WORKSPACE_ROOT } from './helpers/fixture.mjs';

export const FALLBACK_SENTENCE =
  'Where git reports `origin/<default_branch>` unknown — a repository with no `origin` remote — re-issue that command once with `<default_branch>` in its place and say which base you used.';

/** D.2's own no-remote fallback in the two orchestration cores — the one bare range allowed. */
const ALLOWED_LITERAL = 'git rev-list --count <default_branch>..HEAD';

const BARE_PATTERNS = [/(?<!origin\/)<default_branch>\.\.\.?HEAD/g, /diff_base: <default_branch>/g];

const DIFF_SITE = /git (diff|log)\b[^\n`]*(origin\/<default_branch>|<diff_base>)\.\.\.?HEAD/;

function walkMarkdown(dir) {
  const out = [];
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    const path = join(dir, entry.name);
    if (entry.isDirectory()) out.push(...walkMarkdown(path));
    else if (entry.isFile() && entry.name.endsWith('.md')) out.push(path);
  }
  return out;
}

const FILES = walkMarkdown(join(WORKSPACE_ROOT, 'plugin'))
  .map((abs) => ({ rel: relative(WORKSPACE_ROOT, abs).split(sep).join('/'), text: readFileSync(abs, 'utf8') }))
  .sort((a, b) => a.rel.localeCompare(b.rel));

test('no-bare-base', () => {
  const offenders = [];
  for (const { rel, text } of FILES) {
    const lines = text.split(ALLOWED_LITERAL).join('').split('\n');
    lines.forEach((line, i) => {
      for (const pattern of BARE_PATTERNS) {
        for (const _ of line.matchAll(pattern)) offenders.push(`${rel}:${i + 1}`);
      }
    });
  }
  assert.deepEqual(offenders, []);
});

test('fallback-sentence', () => {
  const selected = FILES.filter(({ text }) => text.split('\n').some((line) => DIFF_SITE.test(line)));
  assert.notEqual(selected.length, 0, 'no plugin file runs git diff or git log against the base');
  const lacking = selected.filter(({ text }) => !text.includes(FALLBACK_SENTENCE)).map(({ rel }) => rel);
  assert.deepEqual(lacking, []);
});
