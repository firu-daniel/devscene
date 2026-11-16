/**
 * The agent return schemas, held to their contract.
 *
 * **The rule this suite exists to enforce: every agent with a `plugin/schemas/<agent>.return.json`
 * declares its return there in the closed dialect, describes exactly that schema — names and
 * non-string types — in its `### Return fields`, carries the canonical return-block sentence, never
 * re-inlines the schema in its definition, and is cited — by the planning graph, by every
 * `` `<agent>.<field>` `` in the plugin and by every `pd_ret_field` call in the driver — only for
 * outcomes and fields it declares.** The sentence and the roster are read from
 * `plugin/instructions/agent_return_contract.md`, never restated here.
 *
 * An agent with no schema file is skipped by design, so agents adopt the mechanism one at a time
 * (#380); a schema file with no agent definition beside it fails. The suite reads this checkout's
 * files and creates nothing in it.
 *
 * Every check is a function over text, and each is also run once on an inline bad sample it must
 * reject, so none can pass vacuously on the real tree.
 *
 * Section scans skip `#` lines inside fences: several `## Output contract` sections carry a fenced
 * findings-file template whose `## Must Fix` lines are not headings.
 *
 * Registered as a tree guard in `devscene.config.json` → `treeGuards`, once per covered glob — the
 * plugin's Markdown, `plugin/schemas/` and `cli/templates/scripts/` — so a schema-only edit still
 * runs it.
 */

import assert from 'node:assert/strict';
import { readdirSync, readFileSync } from 'node:fs';
import { join, relative, sep } from 'node:path';
import test from 'node:test';

import { WORKSPACE_ROOT } from './helpers/fixture.mjs';

const MODULE = 'plugin/instructions/agent_return_contract.md';
const AGENTS_DIR = 'plugin/agents';
const SCHEMAS_DIR = 'plugin/schemas';
const SCHEMA_SUFFIX = '.return.json';
const GRAPH = 'cli/templates/scripts/flows/task_plan_writing.graph.json';
const DRIVER = 'cli/templates/scripts/lib/planning-driver-lib.sh';
const PLUGIN_ROOT_TOKEN = '${CLAUDE_PLUGIN_ROOT}/';

const DRAFT_07 = 'http://json-schema.org/draft-07/schema#';
const TOP_KEYS = ['$schema', 'title', 'description', 'type', 'oneOf'];
const VARIANT_KEYS = ['type', 'description', 'properties', 'required', 'additionalProperties'];
const OUTCOME_KEYS = ['const', 'description'];
const PROPERTY_KEYS = ['type', 'description', 'const', 'enum', 'minLength', 'minimum', 'minItems', 'items'];
const PROPERTY_TYPES = ['string', 'integer', 'boolean', 'array'];
/** A `### Return fields` type annotation, as written after the backticked name, to its schema `type`. */
const ANNOTATIONS = new Map([
  ['string', 'string'],
  ['integer', 'integer'],
  ['boolean', 'boolean'],
  ['array of strings', 'array'],
]);

const read = (rel) => readFileSync(join(WORKSPACE_ROOT, rel), 'utf8');
const toPosix = (p) => p.split(sep).join('/');

function walk(relDir) {
  const out = [];
  for (const entry of readdirSync(join(WORKSPACE_ROOT, relDir), { withFileTypes: true })) {
    const rel = `${relDir}/${entry.name}`;
    if (entry.isDirectory()) out.push(...walk(rel));
    else if (entry.isFile()) out.push(toPosix(relative(WORKSPACE_ROOT, join(WORKSPACE_ROOT, rel))));
  }
  return out;
}

// ---------------------------------------------------------------------------------------------
// Markdown reading — fence-aware.
// ---------------------------------------------------------------------------------------------

/** Each line with `fenced` set for the fence lines themselves and everything between them. */
function scanLines(text) {
  const out = [];
  let open = null;
  for (const line of text.split('\n')) {
    const m = /^ {0,3}(`{3,}|~{3,})(.*)$/.exec(line);
    if (open === null) {
      if (m) {
        open = { char: m[1][0], len: m[1].length };
        out.push({ line, fenced: true, opener: m[2].trim() });
      } else {
        out.push({ line, fenced: false });
      }
    } else {
      const closes =
        m && m[1][0] === open.char && m[1].length >= open.len && m[2].trim() === '';
      out.push({ line, fenced: true, closer: Boolean(closes) });
      if (closes) open = null;
    }
  }
  return out;
}

const headingLevel = (entry) => {
  if (entry.fenced) return 0;
  const m = /^(#{1,6})\s+\S/.exec(entry.line);
  return m ? m[1].length : 0;
};

/** The body under the first unfenced heading line equal to `heading`, or `null`. */
function section(text, heading) {
  const lines = scanLines(text);
  const level = /^#+/.exec(heading)[0].length;
  const start = lines.findIndex((e) => !e.fenced && e.line.trimEnd() === heading);
  if (start === -1) return null;
  let end = start + 1;
  while (end < lines.length) {
    const l = headingLevel(lines[end]);
    if (l > 0 && l <= level) break;
    end += 1;
  }
  return lines
    .slice(start + 1, end)
    .map((e) => e.line)
    .join('\n');
}

/** Every fenced block: `{ info, body }`. */
function fencedBlocks(text) {
  const blocks = [];
  let current = null;
  for (const e of scanLines(text)) {
    if (current === null) {
      if (e.fenced && e.opener !== undefined) current = { info: e.opener, body: [] };
    } else if (e.closer) {
      blocks.push({ info: current.info, body: current.body.join('\n') });
      current = null;
    } else {
      current.body.push(e.line);
    }
  }
  return blocks;
}

// ---------------------------------------------------------------------------------------------
// Reading the module.
// ---------------------------------------------------------------------------------------------

/** The canonical sentence: the first fenced block of `## The return block`. */
function canonicalSentence(moduleText) {
  const body = section(moduleText, '## The return block');
  assert.ok(body !== null, `${MODULE} has no ## The return block`);
  const [first] = fencedBlocks(body);
  assert.ok(first, `${MODULE} → ## The return block carries no fenced block`);
  return first.body.trim();
}

/** The `## Who may cite this` roster as repo-relative paths. */
function roster(moduleText) {
  const body = section(moduleText, '## Who may cite this');
  assert.ok(body !== null, `${MODULE} has no ## Who may cite this`);
  return [...body.matchAll(/^- `\$\{CLAUDE_PLUGIN_ROOT\}\/([^`]+)`/gm)].map((m) => `plugin/${m[1]}`);
}

// ---------------------------------------------------------------------------------------------
// The checks. Each returns a list of problems; empty means it holds.
// ---------------------------------------------------------------------------------------------

const unknownKeys = (obj, allowed) => Object.keys(obj).filter((k) => !allowed.includes(k));
const isPlainObject = (v) => typeof v === 'object' && v !== null && !Array.isArray(v);

/** A schema file's text holds one JSON object. */
export function checkSchemaBlock(schemaText) {
  let value;
  try {
    value = JSON.parse(schemaText);
  } catch (error) {
    return { schema: null, problems: [`the schema file does not parse: ${error.message}`] };
  }
  if (!isPlainObject(value)) return { schema: null, problems: ['the schema file is not one JSON object'] };
  return { schema: value, problems: [] };
}

/** Every schema file names an agent that has a definition. */
export function checkSchemaOwners(schemaNames, agentNames) {
  return schemaNames
    .filter((n) => !agentNames.includes(n))
    .map((n) => `${SCHEMAS_DIR}/${n}${SCHEMA_SUFFIX} has no ${AGENTS_DIR}/${n}.md`);
}

/** The definition carries no `## Return schema` section and no fenced `json` block in `## Output contract`. */
export function checkNotInlined(agentText) {
  const problems = [];
  if (section(agentText, '## Return schema') !== null) problems.push('the definition carries a ## Return schema section');
  const contract = section(agentText, '## Output contract');
  if (contract !== null && fencedBlocks(contract).some((b) => b.info === 'json')) {
    problems.push('## Output contract carries a fenced json block');
  }
  return problems;
}

/** Every keyword at every level is in the closed dialect. */
export function checkDialect(schema) {
  const problems = [];
  if (!isPlainObject(schema)) return ['the schema is not an object'];
  for (const k of unknownKeys(schema, TOP_KEYS)) problems.push(`top level: keyword "${k}" is not in the dialect`);
  for (const k of TOP_KEYS) if (!(k in schema)) problems.push(`top level: "${k}" is missing`);
  if (schema.$schema !== DRAFT_07) problems.push(`top level: $schema is not ${DRAFT_07}`);
  if (schema.type !== 'object') problems.push('top level: type is not "object"');
  if (typeof schema.title !== 'string' || schema.title === '') problems.push('top level: title is not a non-empty string');
  if (typeof schema.description !== 'string' || schema.description === '') {
    problems.push('top level: description is not a non-empty string');
  }
  if (!Array.isArray(schema.oneOf) || schema.oneOf.length === 0) {
    problems.push('top level: oneOf is not a non-empty array');
    return problems;
  }
  const consts = [];
  schema.oneOf.forEach((variant, i) => {
    const at = `oneOf[${i}]`;
    if (!isPlainObject(variant)) {
      problems.push(`${at}: not an object`);
      return;
    }
    for (const k of unknownKeys(variant, VARIANT_KEYS)) problems.push(`${at}: keyword "${k}" is not in the dialect`);
    for (const k of VARIANT_KEYS) if (!(k in variant)) problems.push(`${at}: "${k}" is missing`);
    if (variant.type !== 'object') problems.push(`${at}: type is not "object"`);
    if (variant.additionalProperties !== false) problems.push(`${at}: additionalProperties is not false`);
    const props = isPlainObject(variant.properties) ? variant.properties : {};
    if (!Array.isArray(variant.required) || !variant.required.includes('outcome')) {
      problems.push(`${at}: required does not include "outcome"`);
    } else {
      for (const r of variant.required) if (!(r in props)) problems.push(`${at}: required "${r}" is not a property`);
    }
    for (const [name, prop] of Object.entries(props)) {
      const p = `${at}.properties.${name}`;
      if (!isPlainObject(prop)) {
        problems.push(`${p}: not an object`);
        continue;
      }
      if (name === 'outcome') {
        for (const k of unknownKeys(prop, OUTCOME_KEYS)) problems.push(`${p}: keyword "${k}" is not in the dialect`);
        if (typeof prop.const !== 'string' || prop.const === '') problems.push(`${p}: const is not a non-empty string`);
        else consts.push(prop.const);
        continue;
      }
      for (const k of unknownKeys(prop, PROPERTY_KEYS)) problems.push(`${p}: keyword "${k}" is not in the dialect`);
      if (!PROPERTY_TYPES.includes(prop.type)) problems.push(`${p}: type "${prop.type}" is not in the dialect`);
      if (typeof prop.description !== 'string' || prop.description === '') problems.push(`${p}: description is missing`);
      if ('minLength' in prop && prop.type !== 'string') problems.push(`${p}: minLength on a non-string`);
      if ('minimum' in prop && prop.type !== 'integer') problems.push(`${p}: minimum on a non-integer`);
      if ('minItems' in prop && prop.type !== 'array') problems.push(`${p}: minItems on a non-array`);
      if ('items' in prop) {
        if (prop.type !== 'array') problems.push(`${p}: items on a non-array`);
        const items = prop.items;
        if (!isPlainObject(items) || items.type !== 'string') {
          problems.push(`${p}.items: is not { "type": "string" }`);
        } else {
          for (const k of unknownKeys(items, ['type', 'minLength'])) {
            problems.push(`${p}.items: keyword "${k}" is not in the dialect`);
          }
        }
      }
    }
    if (!('outcome' in props)) problems.push(`${at}: no outcome property`);
  });
  const dupes = consts.filter((c, i) => consts.indexOf(c) !== i);
  for (const d of new Set(dupes)) problems.push(`outcome const "${d}" is not distinct across variants`);
  return problems;
}

/** The outcome consts, in variant order. */
const outcomeConsts = (schema) => schema.oneOf.map((v) => v.properties?.outcome?.const).filter(Boolean);

/** The union of every variant's property names. */
const propertyNames = (schema) =>
  new Set(schema.oneOf.flatMap((v) => (isPlainObject(v.properties) ? Object.keys(v.properties) : [])));

/** Each non-`outcome` property name to the set of `type`s its variants declare it with. */
function propertyTypes(schema) {
  const types = new Map();
  for (const v of schema.oneOf) {
    if (!isPlainObject(v.properties)) continue;
    for (const [name, prop] of Object.entries(v.properties)) {
      if (name === 'outcome' || !isPlainObject(prop)) continue;
      if (!types.has(name)) types.set(name, new Set());
      types.get(name).add(prop.type);
    }
  }
  return types;
}

const sorted = (iterable) => [...iterable].sort();

/** A block whose every non-blank line is `key: value` — the retired return form. */
const isKeyValueBlock = (body) => {
  const lines = body.split('\n').filter((l) => l.trim() !== '');
  return lines.length > 0 && lines.every((l) => /^\s*[A-Za-z_][A-Za-z0-9_]*:(\s|$)/.test(l));
};

/** `## Output contract` against the schema and the canonical sentence. */
export function checkOutputContract(agentText, schema, sentence) {
  const problems = [];
  const contract = section(agentText, '## Output contract');
  if (contract === null) return ['no ## Output contract section'];
  if (!contract.includes(sentence)) problems.push('## Output contract does not carry the canonical sentence verbatim');
  const fields = section(contract, '### Return fields');
  if (fields === null) {
    problems.push('## Output contract has no ### Return fields');
  } else {
    const bullets = scanLines(fields)
      .filter((e) => !e.fenced)
      .map((e) => /^- `([^`]+)`(?: \(([^)]*)\))?/.exec(e.line))
      .filter(Boolean)
      .map((m) => ({ name: m[1], annotation: m[2] }));
    const declared = sorted(propertyNames(schema));
    const named = sorted(new Set(bullets.map((b) => b.name)));
    for (const n of declared) if (!named.includes(n)) problems.push(`### Return fields lists no bullet for "${n}"`);
    for (const n of named) if (!declared.includes(n)) problems.push(`### Return fields lists "${n}", which the schema does not declare`);
    const types = propertyTypes(schema);
    for (const { name, annotation } of bullets) {
      if (!types.has(name)) continue;
      const annotated = ANNOTATIONS.get(annotation);
      for (const type of types.get(name)) {
        if (annotated === undefined && type !== 'string') {
          problems.push(`### Return fields: "${name}" is a schema ${type} but its bullet carries no type annotation`);
        } else if (annotated !== undefined && annotated !== type) {
          problems.push(`### Return fields: "${name}" is annotated (${annotation}) but the schema types it ${type}`);
        }
      }
    }
  }
  for (const c of outcomeConsts(schema)) {
    if (!contract.includes(`\`${c}\``)) problems.push(`outcome "${c}" does not appear backticked in ## Output contract`);
  }
  for (const block of fencedBlocks(contract)) {
    if (isKeyValueBlock(block.body)) problems.push('## Output contract carries a fenced key: value block (the retired return form)');
  }
  return problems;
}

/** Every dispatch node's agent against its outcomes; every round gate's PASS and FAIL against `findings_file`. */
export function checkGraph(graph, schemas) {
  const problems = [];
  for (const [id, node] of Object.entries(graph.nodes)) {
    if (node.kind !== 'dispatch') continue;
    const schema = schemas.get(node.agent);
    if (!schema) {
      problems.push(`node ${id}: agent ${node.agent} has no ${SCHEMAS_DIR}/${node.agent}${SCHEMA_SUFFIX}`);
      continue;
    }
    const expected = sorted(Object.keys(node.outcomes).filter((k) => k !== 'error'));
    const actual = sorted(outcomeConsts(schema));
    if (JSON.stringify(expected) !== JSON.stringify(actual)) {
      problems.push(`node ${id}: outcomes [${expected}] differ from ${node.agent}'s consts [${actual}]`);
    }
  }
  for (const [id, node] of Object.entries(graph.nodes)) {
    if (node.kind !== 'round') continue;
    for (const gate of node.gates) {
      const agent = graph.nodes[gate]?.agent;
      const schema = schemas.get(agent);
      if (!schema) {
        problems.push(`round ${id}: gate ${gate} has no schema-carrying agent`);
        continue;
      }
      for (const outcome of ['PASS', 'FAIL']) {
        const variant = schema.oneOf.find((v) => v.properties?.outcome?.const === outcome);
        if (!variant || !('findings_file' in variant.properties)) {
          problems.push(`round ${id}: gate ${gate}'s agent ${agent} declares no findings_file on ${outcome}`);
        }
      }
    }
  }
  return problems;
}

/** Every literal `pd_ret_field <node> <field>` call names a property of that node's agent's schema. */
export function checkDriverCalls(driverText, graph, schemas) {
  const problems = [];
  const calls = [...driverText.matchAll(/\bpd_ret_field[ \t]+([a-z_][a-z0-9_]*)[ \t]+([a-z_][a-z0-9_]*)/g)];
  for (const [, node, field] of calls) {
    const agent = graph.nodes[node]?.kind === 'dispatch' ? graph.nodes[node].agent : undefined;
    const schema = schemas.get(agent);
    if (!schema) problems.push(`pd_ret_field ${node} ${field}: ${node} is no dispatch node of a schema-carrying agent`);
    else if (!propertyNames(schema).has(field)) problems.push(`pd_ret_field ${node} ${field}: ${agent} declares no ${field}`);
  }
  return { calls: calls.length, problems };
}

/** Every `` `<agent>.<field>` `` naming a schema-carrying agent names one of its properties. */
export function checkCitations(files, schemas) {
  const problems = [];
  let seen = 0;
  for (const { path, text } of files) {
    for (const [, agent, field] of text.matchAll(/`([a-z0-9-]+)\.([A-Za-z0-9_]+)`/g)) {
      if (!schemas.has(agent) || field === 'md') continue;
      seen += 1;
      if (!propertyNames(schemas.get(agent)).has(field)) problems.push(`${path}: \`${agent}.${field}\` is not declared`);
    }
  }
  return { seen, problems };
}

/** The plugin files naming the module, the module excluded, equal its roster. */
export function checkRoster(moduleText, files) {
  const citers = sorted(
    files.filter((f) => f.path !== MODULE && f.text.includes('agent_return_contract.md')).map((f) => f.path),
  );
  const listed = sorted(roster(moduleText));
  const problems = [];
  for (const c of citers) if (!listed.includes(c)) problems.push(`${c} names the module but is not on its roster`);
  for (const l of listed) if (!citers.includes(l)) problems.push(`${l} is on the roster but does not name the module`);
  return problems;
}

// ---------------------------------------------------------------------------------------------
// The real tree.
// ---------------------------------------------------------------------------------------------

const moduleText = read(MODULE);
const SENTENCE = canonicalSentence(moduleText);
const pluginFiles = walk('plugin').map((path) => ({ path, text: read(path) }));
const pluginMarkdown = pluginFiles.filter((f) => f.path.endsWith('.md'));
const agentName = (path) => path.slice(AGENTS_DIR.length + 1, -'.md'.length);
const schemaName = (path) => path.slice(SCHEMAS_DIR.length + 1, -SCHEMA_SUFFIX.length);
const allAgentFiles = pluginFiles.filter((f) => f.path.startsWith(`${AGENTS_DIR}/`) && f.path.endsWith('.md'));
const schemaFiles = pluginFiles.filter((f) => f.path.startsWith(`${SCHEMAS_DIR}/`) && f.path.endsWith(SCHEMA_SUFFIX));
const schemaTexts = new Map(schemaFiles.map((f) => [schemaName(f.path), f.text]));
const agentFiles = allAgentFiles.filter((f) => schemaTexts.has(agentName(f.path)));
const graph = JSON.parse(read(GRAPH));
const driverText = read(DRIVER);

const SCHEMAS = new Map();
for (const [name, text] of schemaTexts) {
  const { schema } = checkSchemaBlock(text);
  if (schema) SCHEMAS.set(name, schema);
}

test('the module yields a canonical sentence and a roster', () => {
  assert.match(SENTENCE, /^End your reply with your return object: /);
  assert.ok(roster(moduleText).length > 0, 'the roster is empty');
});

test(`at least one agent has a ${SCHEMAS_DIR}/<agent>${SCHEMA_SUFFIX}`, () => {
  assert.ok(agentFiles.length > 0, `no agent under ${AGENTS_DIR} has a schema file under ${SCHEMAS_DIR}`);
});

test('every schema file belongs to an agent definition', () => {
  assert.deepEqual(checkSchemaOwners([...schemaTexts.keys()], allAgentFiles.map((f) => agentName(f.path))), []);
});

test('no agent definition re-inlines a return schema', () => {
  const problems = allAgentFiles.flatMap((f) => checkNotInlined(f.text).map((p) => `${f.path}: ${p}`));
  assert.deepEqual(problems, []);
});

for (const file of agentFiles) {
  const name = agentName(file.path);
  test(`${file.path}: ${SCHEMAS_DIR}/${name}${SCHEMA_SUFFIX}, dialect and Output contract`, () => {
    const { schema, problems } = checkSchemaBlock(schemaTexts.get(name));
    assert.deepEqual(problems, []);
    assert.deepEqual(checkDialect(schema), []);
    assert.deepEqual(checkOutputContract(file.text, schema, SENTENCE), []);
  });
}

test('the planning graph dispatches only schema-carrying agents, for outcomes they declare', () => {
  assert.deepEqual(checkGraph(graph, SCHEMAS), []);
});

test('every pd_ret_field call in the driver names a declared field', () => {
  const { calls, problems } = checkDriverCalls(driverText, graph, SCHEMAS);
  assert.ok(calls > 0, `${DRIVER} carries no literal pd_ret_field call`);
  assert.deepEqual(problems, []);
});

test('every `<agent>.<field>` citation across plugin/**/*.md names a declared field', () => {
  const { seen, problems } = checkCitations(pluginMarkdown, SCHEMAS);
  assert.ok(seen > 0, 'no citation of a schema-carrying agent was found');
  assert.deepEqual(problems, []);
});

test('the plugin files naming the module equal its ## Who may cite this roster', () => {
  assert.deepEqual(checkRoster(moduleText, pluginMarkdown), []);
});

// ---------------------------------------------------------------------------------------------
// Bad samples — each check must reject one.
// ---------------------------------------------------------------------------------------------

const goodSchema = () => ({
  $schema: DRAFT_07,
  title: 'sample return',
  description: 'A sample.',
  type: 'object',
  oneOf: [
    {
      type: 'object',
      description: 'Passed.',
      properties: {
        outcome: { const: 'PASS', description: 'Passed.' },
        findings_file: { type: 'string', minLength: 1, description: 'The file.' },
      },
      required: ['outcome', 'findings_file'],
      additionalProperties: false,
    },
    {
      type: 'object',
      description: 'Failed.',
      properties: {
        outcome: { const: 'FAIL', description: 'Failed.' },
        findings_file: { type: 'string', minLength: 1, description: 'The file.' },
        questions: { type: 'array', minItems: 1, items: { type: 'string', minLength: 1 }, description: 'Items.' },
      },
      required: ['outcome', 'findings_file'],
      additionalProperties: false,
    },
  ],
});

/** The sample agent's definition; its schema is `goodSchema()`, passed alongside. */
const sampleAgent = ({
  sentence = SENTENCE,
  fields = ['outcome', 'findings_file', 'questions'],
  annotations = { questions: 'array of strings' },
  extra = '',
} = {}) =>
  [
    '# sample',
    '',
    '## Output contract',
    '',
    sentence,
    '',
    'Return `PASS` or `FAIL`.',
    '',
    '```markdown',
    '## Must Fix',
    '```',
    extra,
    '### Return fields',
    '',
    ...fields.map((f) => `- \`${f}\`${annotations[f] ? ` (${annotations[f]})` : ''} — described.`),
    '',
  ].join('\n');

test('bad samples: the good sample passes every per-agent check', () => {
  const text = sampleAgent();
  const { schema, problems } = checkSchemaBlock(JSON.stringify(goodSchema(), null, 2));
  assert.deepEqual(problems, []);
  assert.deepEqual(checkDialect(schema), []);
  assert.deepEqual(checkNotInlined(text), []);
  assert.deepEqual(checkOutputContract(text, schema, SENTENCE), []);
});

test('bad samples: a schema file that is not one JSON object is rejected', () => {
  assert.match(checkSchemaBlock('{"oneOf":[]} {}').problems.join('\n'), /does not parse/);
  assert.match(checkSchemaBlock('[1]').problems.join('\n'), /not one JSON object/);
});

test('bad samples: a schema file with no agent definition is rejected', () => {
  assert.deepEqual(checkSchemaOwners(['sample'], ['sample']), []);
  assert.deepEqual(checkSchemaOwners(['orphan'], ['sample']), [
    `${SCHEMAS_DIR}/orphan${SCHEMA_SUFFIX} has no ${AGENTS_DIR}/orphan.md`,
  ]);
});

test('bad samples: a re-inlined schema is rejected', () => {
  const inline = `${sampleAgent()}\n## Return schema\n\n\`\`\`json\n${JSON.stringify(goodSchema())}\n\`\`\`\n`;
  assert.match(checkNotInlined(inline).join('\n'), /carries a ## Return schema section/);
  const fenced = sampleAgent({ extra: `\`\`\`json\n${JSON.stringify(goodSchema())}\n\`\`\`\n` });
  assert.match(checkNotInlined(fenced).join('\n'), /## Output contract carries a fenced json block/);
});

test('bad samples: a missing or wrong type annotation is rejected', () => {
  const missing = sampleAgent({ annotations: {} });
  assert.match(
    checkOutputContract(missing, goodSchema(), SENTENCE).join('\n'),
    /"questions" is a schema array but its bullet carries no type annotation/,
  );
  const wrong = sampleAgent({ annotations: { questions: 'integer', findings_file: 'boolean' } });
  const problems = checkOutputContract(wrong, goodSchema(), SENTENCE).join('\n');
  assert.match(problems, /"questions" is annotated \(integer\) but the schema types it array/);
  assert.match(problems, /"findings_file" is annotated \(boolean\) but the schema types it string/);
});

test('bad samples: a schema with an unknown keyword is rejected', () => {
  const s = goodSchema();
  s.oneOf[0].properties.findings_file.pattern = '^/';
  assert.match(checkDialect(s).join('\n'), /keyword "pattern" is not in the dialect/);
  const t = goodSchema();
  t.definitions = {};
  assert.match(checkDialect(t).join('\n'), /top level: keyword "definitions"/);
});

test('bad samples: a variant without additionalProperties: false is rejected', () => {
  const s = goodSchema();
  delete s.oneOf[1].additionalProperties;
  assert.match(checkDialect(s).join('\n'), /oneOf\[1\]: additionalProperties is not false/);
});

test('bad samples: required without outcome, and duplicate consts, are rejected', () => {
  const s = goodSchema();
  s.oneOf[0].required = ['findings_file'];
  s.oneOf[1].properties.outcome.const = 'PASS';
  const problems = checkDialect(s).join('\n');
  assert.match(problems, /oneOf\[0\]: required does not include "outcome"/);
  assert.match(problems, /outcome const "PASS" is not distinct/);
});

test('bad samples: a ### Return fields list missing one property is rejected', () => {
  const text = sampleAgent({ fields: ['outcome', 'findings_file'] });
  assert.match(checkOutputContract(text, goodSchema(), SENTENCE).join('\n'), /lists no bullet for "questions"/);
});

test('bad samples: an Output contract without the canonical sentence is rejected', () => {
  const text = sampleAgent({ sentence: 'End your reply with a summary.' });
  assert.match(checkOutputContract(text, goodSchema(), SENTENCE).join('\n'), /canonical sentence/);
});

test('bad samples: an outcome not backticked in the Output contract is rejected', () => {
  const text = sampleAgent().replace('Return `PASS` or `FAIL`.', 'Return a verdict.');
  assert.match(checkOutputContract(text, goodSchema(), SENTENCE).join('\n'), /outcome "PASS" does not appear/);
});

test('bad samples: a fenced key: value block in the Output contract is rejected', () => {
  const text = sampleAgent({ extra: '```\noutcome: PASS\nfindings_file: <path>\n```\n' });
  assert.match(checkOutputContract(text, goodSchema(), SENTENCE).join('\n'), /retired return form/);
});

const sampleGraph = () => ({
  nodes: {
    review: {
      kind: 'dispatch',
      agent: 'sample-reviewer',
      outcomes: { PASS: {}, FAIL: {}, error: {} },
    },
    round: { kind: 'round', gates: ['review'] },
  },
});

test('bad samples: a graph node whose outcomes differ from its agent\'s consts is rejected', () => {
  const schemas = new Map([['sample-reviewer', goodSchema()]]);
  assert.deepEqual(checkGraph(sampleGraph(), schemas), []);
  const g = sampleGraph();
  g.nodes.review.outcomes.blocker = {};
  assert.match(checkGraph(g, schemas).join('\n'), /node review: outcomes \[FAIL,PASS,blocker\] differ/);
  assert.match(checkGraph(sampleGraph(), new Map()).join('\n'), /has no plugin\/schemas\/sample-reviewer\.return\.json/);
});

test('bad samples: a round gate whose agent declares no findings_file on PASS is rejected', () => {
  const s = goodSchema();
  delete s.oneOf[0].properties.findings_file;
  s.oneOf[0].required = ['outcome'];
  const problems = checkGraph(sampleGraph(), new Map([['sample-reviewer', s]])).join('\n');
  assert.match(problems, /declares no findings_file on PASS/);
});

test('bad samples: a pd_ret_field call naming an undeclared field is rejected', () => {
  const schemas = new Map([['sample-reviewer', goodSchema()]]);
  const ok = checkDriverCalls('pd_ret_field review findings_file\n', sampleGraph(), schemas);
  assert.deepEqual(ok, { calls: 1, problems: [] });
  const bad = checkDriverCalls('if pd_ret_field review review_file; then :; fi\n', sampleGraph(), schemas);
  assert.match(bad.problems.join('\n'), /sample-reviewer declares no review_file/);
});

test('bad samples: a citation of an undeclared field is rejected; a .md file name is not a citation', () => {
  const schemas = new Map([['sample-reviewer', goodSchema()]]);
  const files = [{ path: 'x.md', text: 'Read `sample-reviewer.md`, then `sample-reviewer.review_file`.' }];
  const { seen, problems } = checkCitations(files, schemas);
  assert.equal(seen, 1);
  assert.deepEqual(problems, ['x.md: `sample-reviewer.review_file` is not declared']);
});

test('bad samples: a roster that differs from the citing files is rejected', () => {
  const extra = [...pluginMarkdown, { path: 'plugin/instructions/new_citer.md', text: 'see agent_return_contract.md' }];
  assert.match(checkRoster(moduleText, extra).join('\n'), /new_citer\.md names the module but is not on its roster/);
  const fewer = pluginMarkdown.filter((f) => f.path !== roster(moduleText)[0]);
  assert.match(checkRoster(moduleText, fewer).join('\n'), /is on the roster but does not name the module/);
});

test('a real agent with findings_file renamed in its schema only fails the property and citation checks', () => {
  const real = agentFiles.find((f) => propertyNames(SCHEMAS.get(agentName(f.path))).has('findings_file'));
  assert.ok(real, 'no schema-carrying agent declares findings_file');
  const schema = structuredClone(SCHEMAS.get(agentName(real.path)));
  for (const variant of schema.oneOf) {
    if (!('findings_file' in variant.properties)) continue;
    variant.properties.review_file = variant.properties.findings_file;
    delete variant.properties.findings_file;
    variant.required = variant.required.map((r) => (r === 'findings_file' ? 'review_file' : r));
  }
  assert.deepEqual(checkDialect(schema), []);
  const contractProblems = checkOutputContract(real.text, schema, SENTENCE).join('\n');
  assert.match(contractProblems, /lists no bullet for "review_file"/);
  assert.match(contractProblems, /lists "findings_file", which the schema does not declare/);
  const name = agentName(real.path);
  const schemas = new Map(SCHEMAS).set(name, schema);
  const { problems } = checkCitations(pluginMarkdown, schemas);
  assert.ok(
    problems.some((p) => p.includes(`\`${name}.findings_file\``)),
    `no citation of ${name}.findings_file was reported`,
  );
});
