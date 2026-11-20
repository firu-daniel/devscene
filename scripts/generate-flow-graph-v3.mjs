#!/usr/bin/env node
// generate-flow-graph-v3.mjs — generate the format-3 planning graph the bash walker reads from its
// format-4 source, and check that both committed format-3 copies equal what it would write.
// Hand-written for this repository, like check-flow-graph.sh; not an `init` output.
//
// THE RULE. Both committed format-3 graphs — cli/templates/scripts/flows/task_plan_writing.graph.json
// and the self-adoption copy scripts/flows/task_plan_writing.graph.json — equal, byte for byte, the
// one generated from cli/templates/scripts/flows/task_plan_writing.v4.graph.json. The format-4 file is
// the one the harness authors until the bash walker reads format 4; neither format-3 copy is edited
// by hand.
//
// WHY THE MAPPING LIVES HERE. Format 4 lets a graph name its own outcomes, bindings and predicates;
// format 3 and cli/templates/scripts/flow-walker.sh know only fixed names with fixed behaviour.
// Mapping one onto the other is knowledge of this harness's walker, so it stays harness-side: the
// GraphScene library is generic and names nothing of the harness, and this script imports nothing
// from it and runs no Python.
//
// Usage: node scripts/generate-flow-graph-v3.mjs [--check]
//          the default: generate, and compare the text with each committed format-3 copy
//        node scripts/generate-flow-graph-v3.mjs --write
//          generate, and only when there are no findings write both format-3 copies
//        node scripts/generate-flow-graph-v3.mjs --check --source <path>
//          generate from another format-4 file, so a refusal can be reproduced against a planted
//          copy; the comparison with the committed copies still runs
// Exit: 0 clean or written · 1 one or more findings, each on stderr as
//       `generate-flow-graph-v3: <file> — <reason>`, all reported · 2 bad usage
import { execFileSync } from 'node:child_process';
import { readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const NAME = 'generate-flow-graph-v3';
const SOURCE = 'cli/templates/scripts/flows/task_plan_writing.v4.graph.json';
const TARGETS = ['cli/templates/scripts/flows/task_plan_writing.graph.json', 'scripts/flows/task_plan_writing.graph.json'];

/**
 * The format-3 outcome names and the vocabulary entry each must carry in format 4. The walker
 * routes a round on `PASS`/`FAIL` and holds a gate's `error`/`blocker` until the round's other
 * gates finish (flow-walker.sh → `round.held.<gate>`).
 */
const V3_OUTCOMES = Object.freeze({
  returned: Object.freeze({}),
  questions: Object.freeze({}),
  no_ui: Object.freeze({}),
  PASS: Object.freeze({ verdict: 'pass' }),
  FAIL: Object.freeze({ verdict: 'fail' }),
  error: Object.freeze({ held: true }),
  blocker: Object.freeze({ held: true }),
});

/**
 * The format-3 binding names and the primitive each must map to. `<ask>` resumes only with
 * `answered` (flow-walker.sh → the refusal *"only 'answered' is"*); `<escalate>` stops with a
 * reason the format-3 graph spells as one of `V3_ESCALATE_REASONS`.
 */
const V3_ESCALATE_REASONS = Object.freeze(['cap', 'error', 'blocker']);
const V3_BINDINGS = Object.freeze({
  '<ask>': Object.freeze({ primitive: 'interrupt', resumeOutcome: 'answered' }),
  '<escalate>': Object.freeze({ primitive: 'stop' }),
  '<terminal_handoff>': Object.freeze({ primitive: 'end' }),
});

/**
 * Predicate name patterns and the format-3 skip construct each becomes. A `skipped` node is left
 * out of a cap escalation's round counts (flow-walker.sh → `add_skipped_node`), so its predicate
 * must declare `inRoundCounts: false`; a `passedByExclusion` node is kept in them.
 */
const V3_PREDICATES = Object.freeze([
  Object.freeze({
    pattern: /^phase_(parity|qa|docs)_off$/,
    construct: 'skipped',
    key: 'phase',
    records: 'skipped',
    inRoundCounts: false,
  }),
  Object.freeze({
    pattern: /^run_mode_skips_([a-z][a-z0-9_-]*)$/,
    construct: 'passedByExclusion',
    key: 'runModeId',
    records: 'passed-by-exclusion',
    inRoundCounts: true,
  }),
]);

/** The format-3 file's own `description`, which describes that file rather than its source. */
const V3_DESCRIPTION =
  "The routing of ${CLAUDE_PLUGIN_ROOT}/instructions/task_plan_writing_instructions_core.md as data: the task-plan loop, whose gates are dispatched together as one set every round and whose round node joins them, the UI-test-plan loop and convergence, with the values the walker resolves (counters, path templates, heartbeats, findings folders, skip gates, cap summaries). The dispatch blocks each agent receives are not here; they stay in that core. Copied verbatim into the adopter's scripts directory, never rendered.";

/**
 * The widest line, trailing comma excluded, on which an all-scalar object is printed inline. The
 * committed format-3 file's widest inline object is 75 columns and its narrowest expanded all-scalar
 * object other than a node is `ui_review`'s `onCap`, far past 80. A node is always expanded, however
 * narrow: `convergence` fits on one line and is not printed on one.
 */
const MAX_INLINE_WIDTH = 80;

const isObject = (v) => v !== null && typeof v === 'object' && !Array.isArray(v);
const isScalar = (v) => v === null || typeof v !== 'object';
const own = (o, k) => Object.prototype.hasOwnProperty.call(o, k);

function sameEntry(actual, expected) {
  if (!isObject(actual)) return false;
  const a = Object.keys(actual);
  const e = Object.keys(expected);
  return a.length === e.length && e.every((k) => own(actual, k) && actual[k] === expected[k]);
}

function predicateRule(name) {
  for (const rule of V3_PREDICATES) {
    const m = rule.pattern.exec(name);
    if (m) return { rule, value: m[1] };
  }
  return undefined;
}

/** Checks the declared vocabulary against the tables; returns the declared name sets. */
function checkVocabulary(vocabulary, fail) {
  const declared = { outcomes: new Set(), bindings: new Set(), predicates: new Set(), reasons: new Map() };
  if (!isObject(vocabulary)) {
    fail('vocabulary', 'missing or not an object');
    return declared;
  }
  for (const section of ['outcomes', 'bindings', 'predicates']) {
    if (!isObject(vocabulary[section])) fail(`vocabulary.${section}`, 'missing or not an object');
  }
  for (const [name, entry] of Object.entries(isObject(vocabulary.outcomes) ? vocabulary.outcomes : {})) {
    declared.outcomes.add(name);
    const path = `vocabulary.outcomes.${name}`;
    if (!own(V3_OUTCOMES, name)) fail(path, 'declares an outcome format 3 has no name for');
    else if (!sameEntry(entry, V3_OUTCOMES[name])) {
      fail(path, `must be ${JSON.stringify(V3_OUTCOMES[name])}, the behaviour format 3 gives '${name}'`);
    }
  }
  for (const [name, entry] of Object.entries(isObject(vocabulary.bindings) ? vocabulary.bindings : {})) {
    declared.bindings.add(name);
    if (isObject(entry) && entry.primitive === 'stop' && Array.isArray(entry.reasons)) {
      declared.reasons.set(name, entry.reasons);
    }
    const path = `vocabulary.bindings.${name}`;
    if (!own(V3_BINDINGS, name)) fail(path, 'declares a binding format 3 has no name for');
    else if (name === '<escalate>') {
      const ok =
        isObject(entry) &&
        Object.keys(entry).length === 2 &&
        entry.primitive === 'stop' &&
        Array.isArray(entry.reasons) &&
        entry.reasons.every((r) => V3_ESCALATE_REASONS.includes(r));
      if (!ok) {
        fail(path, `must be { "primitive": "stop", "reasons": [...] } with reasons drawn from ${V3_ESCALATE_REASONS.join(', ')}`);
      }
    } else if (!sameEntry(entry, V3_BINDINGS[name])) {
      fail(path, `must be ${JSON.stringify(V3_BINDINGS[name])}, the behaviour format 3 gives '${name}'`);
    }
  }
  for (const [name, entry] of Object.entries(isObject(vocabulary.predicates) ? vocabulary.predicates : {})) {
    declared.predicates.add(name);
    const path = `vocabulary.predicates.${name}`;
    const match = predicateRule(name);
    if (match === undefined) {
      fail(path, 'matches neither phase_(parity|qa|docs)_off nor run_mode_skips_<id>, so it has no format-3 skip construct');
      continue;
    }
    const { rule } = match;
    if (!isObject(entry) || entry.records !== rule.records || entry.inRoundCounts !== rule.inRoundCounts) {
      fail(
        path,
        `maps to construct '${rule.construct}', which must declare "records": "${rule.records}" and "inRoundCounts": ${rule.inRoundCounts}`,
      );
    }
  }
  return declared;
}

/** Records every binding the node uses, each with its JSON path and the object carrying it. */
function usedBindings(node, nodePath) {
  const used = [];
  if (own(node, 'binding')) used.push([`${nodePath}.binding`, node.binding, node]);
  for (const [outcome, edge] of Object.entries(isObject(node.outcomes) ? node.outcomes : {})) {
    if (!isObject(edge)) continue;
    const edgePath = `${nodePath}.outcomes.${outcome}`;
    if (own(edge, 'binding')) used.push([`${edgePath}.binding`, edge.binding, edge]);
    if (isObject(edge.onCap) && own(edge.onCap, 'binding')) {
      used.push([`${edgePath}.onCap.binding`, edge.onCap.binding, edge.onCap]);
    }
  }
  return used;
}

function v3Skip(entry, path, declared, fail) {
  if (!isObject(entry)) {
    fail(path, 'a skip entry must be an object');
    return undefined;
  }
  for (const key of Object.keys(entry)) {
    if (!['when', 'to', 'report'].includes(key)) fail(`${path}.${key}`, 'a format-4 skip carries only when, to and report');
  }
  if (!own(entry, 'to')) fail(`${path}.to`, 'missing');
  if (!declared.predicates.has(entry.when)) {
    fail(`${path}.when`, `uses predicate ${JSON.stringify(entry.when)}, which the vocabulary does not declare`);
    return undefined;
  }
  const match = predicateRule(entry.when);
  if (match === undefined) return undefined;
  const out = { construct: match.rule.construct, [match.rule.key]: match.value, to: entry.to };
  if (own(entry, 'report')) out.report = entry.report;
  return out;
}

/** `{ text }` for a format-4 graph that maps cleanly onto format 3, else `{ findings }`. */
function generate(v4) {
  const findings = [];
  const fail = (path, reason) => findings.push(`${path}: ${reason}`);
  if (!isObject(v4)) return { findings: ['(root): not a JSON object'] };
  if (v4.formatVersion !== 4) fail('formatVersion', `is ${JSON.stringify(v4.formatVersion)}, not 4`);
  const declared = checkVocabulary(v4.vocabulary, fail);

  const nodes = isObject(v4.nodes) ? v4.nodes : {};
  if (!isObject(v4.nodes)) fail('nodes', 'missing or not an object');
  const v3Nodes = {};
  for (const [id, node] of Object.entries(nodes)) {
    const nodePath = `nodes.${id}`;
    if (!isObject(node)) {
      fail(nodePath, 'not an object');
      continue;
    }
    for (const outcome of Object.keys(isObject(node.outcomes) ? node.outcomes : {})) {
      if (!declared.outcomes.has(outcome)) {
        fail(`${nodePath}.outcomes.${outcome}`, `uses outcome '${outcome}', which the vocabulary does not declare`);
      }
    }
    for (const [path, binding, carrier] of usedBindings(node, nodePath)) {
      if (!declared.bindings.has(binding)) {
        fail(path, `uses binding ${JSON.stringify(binding)}, which the vocabulary does not declare`);
        continue;
      }
      const reasons = declared.reasons.get(binding);
      if (reasons !== undefined && own(carrier, 'reason') && !reasons.includes(carrier.reason)) {
        fail(
          path.replace(/\.binding$/, '.reason'),
          `uses reason ${JSON.stringify(carrier.reason)}, which binding ${JSON.stringify(binding)} does not declare`,
        );
      }
    }
    const v3Node = {};
    for (const [key, value] of Object.entries(node)) {
      if (key !== 'skip') {
        v3Node[key] = value;
        continue;
      }
      if (!Array.isArray(value)) {
        fail(`${nodePath}.skip`, 'not an array');
        continue;
      }
      v3Node.skip = value.map((entry, i) => v3Skip(entry, `${nodePath}.skip.${i}`, declared, fail));
    }
    v3Nodes[id] = v3Node;
  }
  if (findings.length > 0) return { findings };

  const v3 = {};
  for (const [key, value] of Object.entries(v4)) {
    if (key === 'vocabulary') continue;
    if (key === 'formatVersion') v3.formatVersion = 3;
    else if (key === 'description') v3.description = V3_DESCRIPTION;
    else if (key === 'nodes') v3.nodes = v3Nodes;
    else v3[key] = value;
  }
  return { text: `${print(v3, 0, 0)}\n` };
}

/**
 * Two-space indent; an array of scalars on one line; an object of scalars inline as
 * `{ "k": v, … }` when it is not a node and its line fits MAX_INLINE_WIDTH; everything else
 * expanded. `column` is where the value starts on its line; `path` is its keys from the root.
 */
function print(value, indent, column, path = []) {
  if (isScalar(value)) return JSON.stringify(value);
  const pad = ' '.repeat(indent + 2);
  if (Array.isArray(value)) {
    if (value.length === 0) return '[]';
    if (value.every(isScalar)) return `[${value.map((v) => JSON.stringify(v)).join(', ')}]`;
    const items = value.map((v, i) => `${pad}${print(v, indent + 2, indent + 2, [...path, i])}`);
    return `[\n${items.join(',\n')}\n${' '.repeat(indent)}]`;
  }
  const entries = Object.entries(value);
  if (entries.length === 0) return '{}';
  const isNode = path.length === 2 && path[0] === 'nodes';
  if (!isNode && entries.every(([, v]) => isScalar(v))) {
    const inline = `{ ${entries.map(([k, v]) => `${JSON.stringify(k)}: ${JSON.stringify(v)}`).join(', ')} }`;
    if (column + inline.length <= MAX_INLINE_WIDTH) return inline;
  }
  const lines = entries.map(([k, v]) => {
    const head = `${pad}${JSON.stringify(k)}: `;
    return `${head}${print(v, indent + 2, head.length, [...path, k])}`;
  });
  return `{\n${lines.join(',\n')}\n${' '.repeat(indent)}}`;
}

function main() {
  const repoRoot = execFileSync('git', ['rev-parse', '--show-toplevel'], {
    cwd: dirname(fileURLToPath(import.meta.url)),
    encoding: 'utf8',
  }).trim();

  const usage = (message) => {
    console.error(`${NAME}: ${message}`);
    console.error('  usage: node scripts/generate-flow-graph-v3.mjs [--check] | --write | --check --source <path>');
    process.exit(2);
  };

  const args = process.argv.slice(2);
  let mode = 'check';
  let source;
  if (args.length === 0 || (args.length === 1 && args[0] === '--check')) mode = 'check';
  else if (args.length === 1 && args[0] === '--write') mode = 'write';
  else if (args.length === 3 && args[0] === '--check' && args[1] === '--source' && args[2] !== '') source = args[2];
  else usage(`unrecognised arguments: ${args.join(' ')}`);

  const findings = [];
  const finding = (file, reason) => findings.push(`${NAME}: ${file} — ${reason}`);
  const report = () => {
    for (const line of findings) console.error(line);
    process.exit(findings.length === 0 ? 0 : 1);
  };

  const sourceLabel = source ?? SOURCE;
  const sourcePath = source ?? join(repoRoot, SOURCE);
  let v4;
  try {
    v4 = JSON.parse(readFileSync(sourcePath, 'utf8'));
  } catch (error) {
    finding(sourceLabel, `cannot be read as JSON: ${error.message.split('\n')[0]}`);
    report();
  }
  const result = generate(v4);
  if (result.findings !== undefined) {
    for (const reason of result.findings) finding(sourceLabel, reason);
    report();
  }

  if (mode === 'write') {
    for (const target of TARGETS) writeFileSync(join(repoRoot, target), result.text);
    report();
  }
  for (const target of TARGETS) {
    let bytes;
    try {
      bytes = readFileSync(join(repoRoot, target), 'utf8');
    } catch (error) {
      finding(target, `cannot be read: ${error.message.split('\n')[0]}`);
      continue;
    }
    if (bytes !== result.text) {
      finding(
        target,
        `differs from the graph generated from ${sourceLabel}; this file is generated and never edited by hand — make the change in ${SOURCE}, then run node scripts/generate-flow-graph-v3.mjs --write, which overwrites both format-3 copies`,
      );
    }
  }
  report();
}

main();
