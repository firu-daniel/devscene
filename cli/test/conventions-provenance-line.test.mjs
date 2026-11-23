/**
 * The document-level provenance line of a conventions document, as three plugin files state it.
 *
 * **The rule this test exists to enforce: the conventions writer, the conventions reviewer and the
 * analyze command state the document-level provenance line's bound in the same words, so a
 * rewording in one of them fails here.** `analyze.md`'s (4b) reaches the bound by pointer to (4a),
 * so a copy of the bound written there fails too.
 *
 * Not covered, deliberately:
 * - whether the prose around a phrase still means what it did;
 * - whether any real conventions document's footer meets the bound — that is the reviewer's
 *   check (1) at run time, and the existing footers are trimmed by hand.
 *
 * Not a tree guard: it reads three fixed files rather than a tree, so it owes no `treeGuards` entry
 * (`plugin/instructions/unit_loop_core.md` → `## The test-run rule`, point 8's boundary).
 */

import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import test from 'node:test';

import { WORKSPACE_ROOT } from './helpers/fixture.mjs';

const WRITER = 'plugin/agents/conventions-writer.md';
const REVIEWER = 'plugin/agents/conventions-reviewer.md';
const ANALYZE = 'plugin/commands/analyze.md';

const PASS_ONLY = 'describing this pass only';
const AREA_LEVEL = 'at directory or area level';
const NO_PER_FILE = 'never a per-file list';
const NO_CARRY = 'carries no earlier pass forward';
const NO_CARRY_ANALYZE = 'carrying no earlier pass forward';

const MARKER_4A = '**(4a) The conventions documents**';
const MARKER_4B = '**(4b) The `project` target';
const MARKER_4C = '**(4c) The review';

const read = (rel) => readFileSync(join(WORKSPACE_ROOT, rel), 'utf8');
const collapse = (text) => text.replace(/\s+/g, ' ');

/** From the line equal to `heading` up to the next `## ` heading. */
function section(rel, heading) {
  const lines = read(rel).split('\n');
  const start = lines.indexOf(heading);
  assert.notEqual(start, -1, `${rel}: heading ${JSON.stringify(heading)} not found`);
  const rest = lines.slice(start + 1);
  const end = rest.findIndex((line) => line.startsWith('## '));
  return collapse([lines[start], ...(end === -1 ? rest : rest.slice(0, end))].join('\n'));
}

/** From the line opening `from` up to, not including, the line opening `to`. */
function slice(rel, from, to) {
  const lines = read(rel).split('\n');
  const find = (marker) => {
    const at = lines.findIndex((line) => line.trimStart().startsWith(marker));
    assert.notEqual(at, -1, `${rel}: marker ${JSON.stringify(marker)} not found`);
    return at;
  };
  return collapse(lines.slice(find(from), find(to)).join('\n'));
}

function check(where, text, present, absent = []) {
  for (const phrase of present) {
    assert.ok(text.includes(phrase), `${where}: missing ${JSON.stringify(phrase)}`);
  }
  for (const phrase of absent) {
    assert.ok(!text.includes(phrase), `${where}: must not carry ${JSON.stringify(phrase)}`);
  }
}

test('conventions-writer.md states the bound and the fix-pass rule', () => {
  check(
    `${WRITER} → ## The document`,
    section(WRITER, '## The document'),
    [
      PASS_ONLY,
      "it replaces the skeleton's footer",
      'it replaces the previous provenance line',
      AREA_LEVEL,
      NO_PER_FILE,
      NO_CARRY,
      'edited by hand after #<number>',
    ],
  );
  check(`${WRITER} → ## The fix dispatch`, section(WRITER, '## The fix dispatch'), [
    'A fix adds nothing to the provenance line',
  ]);
  check(WRITER, collapse(read(WRITER)), [], ["Replace the skeleton's footer with a document-level provenance line"]);
});

test('conventions-reviewer.md check (1) grades the same bound', () => {
  check(`${REVIEWER} → ## What to verify`, section(REVIEWER, '## What to verify'), [
    PASS_ONLY,
    AREA_LEVEL,
    'Concrete correction: cut the line down to this pass',
  ]);
});

test('analyze.md (4a) restates the bound', () => {
  check(`${ANALYZE} → (4a)`, slice(ANALYZE, MARKER_4A, MARKER_4B), [PASS_ONLY, AREA_LEVEL, NO_CARRY_ANALYZE]);
  check(ANALYZE, collapse(read(ANALYZE)), [], ['skeleton-footer replacement']);
});

test('analyze.md (4b) points at the bound rather than copying it', () => {
  check(
    `${ANALYZE} → (4b)`,
    slice(ANALYZE, MARKER_4B, MARKER_4C),
    [
      "the note replaces that section's previous note",
      "bounded as (4a)'s provenance line is",
      'whose per-section counterpart is the provenance note above',
      "adds nothing to that section's provenance note",
    ],
    [PASS_ONLY, AREA_LEVEL, NO_PER_FILE, NO_CARRY, NO_CARRY_ANALYZE],
  );
});
