/**
 * The agent return schemas, held to their contract.
 *
 * **The rule this suite exists to enforce: every agent under `plugin/agents/` has a
 * `plugin/schemas/<agent>.return.json`, declares its return there in the closed dialect — an array's object items included — describes
 * exactly that schema — names and non-string types, an object item's properties as bullets indented
 * under its `(array of objects)` field — in its `### Return fields`, carries the canonical
 * return-block sentence, never re-inlines the schema in its definition, and is cited — by the
 * planning graph, by every `` `<agent>.<field>` `` and `` `<agent>.<field>.<property>` `` across the
 * plugin's Markdown and the outer-loop scripts under `cli/templates/scripts/` — only for outcomes,
 * fields and item properties it declares.**
 * The sentence is read from `docs/structured-agent-returns.md`
 * → `### The return block` and the roster from `plugin/instructions/agent_return_contract.md` →
 * `## Who may cite this`, never restated here.
 *
 * An agent definition with no schema file fails, as does a schema file with no agent definition
 * beside it, so a new agent lands with its schema. The suite reads this checkout's files and
 * creates nothing in it.
 *
 * Every check is a function over text, and each is also run once on an inline bad sample it must
 * reject, so none can pass vacuously on the real tree.
 *
 * Section scans skip `#` lines inside fences: several `## Output contract` sections carry a fenced
 * findings-file template whose `## Must Fix` lines are not headings.
 *
 * Registered as a tree guard in `devscene.config.json` → `treeGuards`, once per covered glob — the
 * plugin's Markdown, `plugin/schemas/`, `cli/templates/scripts/` and the sentence's home
 * `docs/structured-agent-returns.md` — so a schema-only or docs-only edit still runs it.
 */

import assert from 'node:assert/strict';
import { readdirSync, readFileSync } from 'node:fs';
import { join, relative, sep } from 'node:path';
import test from 'node:test';

import { WORKSPACE_ROOT } from './helpers/fixture.mjs';

const MODULE = 'plugin/instructions/agent_return_contract.md';
const AUTHORING_DOC = 'docs/structured-agent-returns.md';
const AGENTS_DIR = 'plugin/agents';
const SCHEMAS_DIR = 'plugin/schemas';
const SCHEMA_SUFFIX = '.return.json';
const SCRIPTS_DIR = 'cli/templates/scripts';
const GRAPH = 'cli/templates/scripts/flows/task_plan_writing.graph.json';
const PLUGIN_ROOT_TOKEN = '${CLAUDE_PLUGIN_ROOT}/';

const DRAFT_07 = 'http://json-schema.org/draft-07/schema#';
const TOP_KEYS = ['$schema', 'title', 'description', 'type', 'oneOf'];
const VARIANT_KEYS = ['type', 'description', 'properties', 'required', 'additionalProperties'];
const OUTCOME_KEYS = ['const', 'description'];
const PROPERTY_KEYS = ['type', 'description', 'const', 'enum', 'minLength', 'minimum', 'minItems', 'items'];
const PROPERTY_TYPES = ['string', 'integer', 'boolean', 'array'];
const ITEM_KEYS = ['type', 'description', 'properties', 'required', 'additionalProperties'];
const ITEM_PROPERTY_KEYS = ['type', 'description', 'const', 'enum', 'minLength', 'minimum'];
const ITEM_PROPERTY_TYPES = ['string', 'integer', 'boolean'];
/** A `### Return fields` type annotation, as written after the backticked name, to its schema `type` and, for an array, its `items.type`. */
const ANNOTATIONS = new Map([
  ['string', { type: 'string' }],
  ['integer', { type: 'integer' }],
  ['boolean', { type: 'boolean' }],
  ['array of strings', { type: 'array', items: 'string' }],
  ['array of objects', { type: 'array', items: 'object' }],
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

/** The canonical sentence: the first fenced block of the authoring document's `### The return block`. */
function canonicalSentence(docText) {
  const body = section(docText, '### The return block');
  assert.ok(body !== null, `${AUTHORING_DOC} has no ### The return block`);
  const [first] = fencedBlocks(body);
  assert.ok(first, `${AUTHORING_DOC} → ### The return block carries no fenced block`);
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

/** Every agent definition has a schema file. */
export function checkSchemaCoverage(agentNames, schemaNames) {
  return agentNames
    .filter((n) => !schemaNames.includes(n))
    .map((n) => `${AGENTS_DIR}/${n}.md has no ${SCHEMAS_DIR}/${n}${SCHEMA_SUFFIX}`);
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

/** An array's `{ "type": "object", … }` items, at `at`, in the closed dialect. */
function checkObjectItems(items, at) {
  const problems = [];
  for (const k of unknownKeys(items, ITEM_KEYS)) problems.push(`${at}: keyword "${k}" is not in the dialect`);
  if (typeof items.description !== 'string' || items.description === '') problems.push(`${at}: description is missing`);
  if (!isPlainObject(items.properties)) problems.push(`${at}: properties is missing`);
  if (!Array.isArray(items.required)) problems.push(`${at}: required is missing`);
  if (items.additionalProperties !== false) problems.push(`${at}: additionalProperties is not false`);
  const props = isPlainObject(items.properties) ? items.properties : {};
  for (const r of Array.isArray(items.required) ? items.required : []) {
    if (!Object.hasOwn(props, r)) problems.push(`${at}: required "${r}" is not an item property`);
  }
  for (const [name, prop] of Object.entries(props)) {
    const q = `${at}.properties.${name}`;
    if (!isPlainObject(prop)) {
      problems.push(`${q}: not an object`);
      continue;
    }
    for (const k of unknownKeys(prop, ITEM_PROPERTY_KEYS)) problems.push(`${q}: keyword "${k}" is not in the dialect`);
    if (!ITEM_PROPERTY_TYPES.includes(prop.type)) problems.push(`${q}: type "${prop.type}" is not in the dialect`);
    if (typeof prop.description !== 'string' || prop.description === '') problems.push(`${q}: description is missing`);
    if ('minLength' in prop && prop.type !== 'string') problems.push(`${q}: minLength on a non-string`);
    if ('minimum' in prop && prop.type !== 'integer') problems.push(`${q}: minimum on a non-integer`);
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
        if (isPlainObject(items) && items.type === 'object') {
          problems.push(...checkObjectItems(items, `${p}.items`));
        } else if (!isPlainObject(items) || items.type !== 'string') {
          problems.push(`${p}.items: is neither { "type": "string" } nor { "type": "object", … }`);
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

/** Each non-`outcome` property name to the distinct `{ type, items }` its variants declare it with, `items` being `items.type`. */
function propertyShapes(schema) {
  const shapes = new Map();
  for (const v of schema.oneOf) {
    if (!isPlainObject(v.properties)) continue;
    for (const [name, prop] of Object.entries(v.properties)) {
      if (name === 'outcome' || !isPlainObject(prop)) continue;
      const items = isPlainObject(prop.items) ? prop.items.type : undefined;
      if (!shapes.has(name)) shapes.set(name, new Map());
      shapes.get(name).set(`${prop.type}|${items}`, { type: prop.type, items });
    }
  }
  return new Map([...shapes].map(([name, byKey]) => [name, [...byKey.values()]]));
}

/** Each property whose items are objects, in any variant, to the union of its item properties' `type`s. */
function itemProperties(schema) {
  const fields = new Map();
  for (const v of schema.oneOf) {
    if (!isPlainObject(v.properties)) continue;
    for (const [name, prop] of Object.entries(v.properties)) {
      if (!isPlainObject(prop) || !isPlainObject(prop.items) || prop.items.type !== 'object') continue;
      if (!fields.has(name)) fields.set(name, new Map());
      const props = fields.get(name);
      for (const [k, p] of Object.entries(isPlainObject(prop.items.properties) ? prop.items.properties : {})) {
        if (!props.has(k)) props.set(k, new Set());
        if (isPlainObject(p)) props.get(k).add(p.type);
      }
    }
  }
  return fields;
}

/** A bullet's annotation against every `{ type, items }` the schema declares its name with. */
function annotationProblems(label, annotation, shapes) {
  const annotated = ANNOTATIONS.get(annotation);
  const problems = [];
  for (const { type, items } of shapes) {
    if (annotated === undefined && type !== 'string') {
      problems.push(`### Return fields: "${label}" is a schema ${type} but its bullet carries no type annotation`);
    } else if (annotated !== undefined && annotated.type !== type) {
      problems.push(`### Return fields: "${label}" is annotated (${annotation}) but the schema types it ${type}`);
    } else if (annotated?.items !== undefined && annotated.items !== items) {
      problems.push(`### Return fields: "${label}" is annotated (${annotation}) but the schema's items are ${items ?? 'undeclared'}`);
    }
  }
  return problems;
}

const FIELD_BULLET = /^- `([^`]+)`(?: \(([^)]*)\))?/;
const ITEM_BULLET = /^ {2}- `([^`]+)`(?: \(([^)]*)\))?/;

/** `### Return fields`' top-level field bullets, each with the run of nested item bullets directly under it. */
function fieldBullets(fields) {
  const bullets = [];
  let current = null;
  for (const e of scanLines(fields)) {
    if (e.fenced) continue;
    const top = FIELD_BULLET.exec(e.line);
    if (top) {
      current = { name: top[1], annotation: top[2], nested: [] };
      bullets.push(current);
      continue;
    }
    if (/^- /.test(e.line)) {
      current = null;
      continue;
    }
    const sub = ITEM_BULLET.exec(e.line);
    if (sub && current !== null) current.nested.push({ name: sub[1], annotation: sub[2] });
  }
  return bullets;
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
    const bullets = fieldBullets(fields);
    const declared = sorted(propertyNames(schema));
    const named = sorted(new Set(bullets.map((b) => b.name)));
    for (const n of declared) if (!named.includes(n)) problems.push(`### Return fields lists no bullet for "${n}"`);
    for (const n of named) if (!declared.includes(n)) problems.push(`### Return fields lists "${n}", which the schema does not declare`);
    const shapes = propertyShapes(schema);
    const items = itemProperties(schema);
    for (const { name, annotation, nested } of bullets) {
      if (!shapes.has(name)) continue;
      problems.push(...annotationProblems(name, annotation, shapes.get(name)));
      const itemProps = items.get(name);
      if (itemProps === undefined) {
        for (const n of nested) {
          problems.push(`### Return fields: "${name}" carries a nested bullet "${n.name}" but its items are not objects`);
        }
        continue;
      }
      const declaredItems = sorted(itemProps.keys());
      const namedItems = sorted(new Set(nested.map((n) => n.name)));
      for (const n of declaredItems) {
        if (!namedItems.includes(n)) problems.push(`### Return fields: "${name}" lists no nested bullet for item property "${n}"`);
      }
      for (const n of namedItems) {
        if (!declaredItems.includes(n)) problems.push(`### Return fields: "${name}" lists item property "${n}", which its items do not declare`);
      }
      for (const n of nested) {
        if (!itemProps.has(n.name)) continue;
        const itemShapes = [...itemProps.get(n.name)].map((type) => ({ type, items: undefined }));
        problems.push(...annotationProblems(`${name}.${n.name}`, n.annotation, itemShapes));
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

/**
 * Every `` `<agent>.<field>` `` naming a schema-carrying agent names one of its properties, and every
 * `` `<agent>.<field>.<property>` `` one of that field's object-item properties. A file name — one
 * ending `.md`, or the agent's own `<agent>.return.json` — is not a citation.
 */
export function checkCitations(files, schemas) {
  const problems = [];
  let seen = 0;
  for (const { path, text } of files) {
    for (const [, agent, field, property] of text.matchAll(/`([a-z0-9-]+)\.([A-Za-z0-9_]+)(?:\.([A-Za-z0-9_]+))?`/g)) {
      if (!schemas.has(agent) || (property ?? field) === 'md') continue;
      if (property !== undefined && `.${field}.${property}` === SCHEMA_SUFFIX) continue;
      seen += 1;
      const schema = schemas.get(agent);
      const cited = property === undefined ? `${agent}.${field}` : `${agent}.${field}.${property}`;
      if (!propertyNames(schema).has(field)) {
        problems.push(`${path}: \`${cited}\` is not declared`);
      } else if (property !== undefined) {
        const itemProps = itemProperties(schema).get(field);
        if (itemProps === undefined) problems.push(`${path}: \`${cited}\` cites an item property, but the items of ${field} are not objects`);
        else if (!itemProps.has(property)) problems.push(`${path}: \`${cited}\` is not declared`);
      }
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
const SENTENCE = canonicalSentence(read(AUTHORING_DOC));
const pluginFiles = walk('plugin').map((path) => ({ path, text: read(path) }));
const pluginMarkdown = pluginFiles.filter((f) => f.path.endsWith('.md'));
const agentName = (path) => path.slice(AGENTS_DIR.length + 1, -'.md'.length);
const schemaName = (path) => path.slice(SCHEMAS_DIR.length + 1, -SCHEMA_SUFFIX.length);
const allAgentFiles = pluginFiles.filter((f) => f.path.startsWith(`${AGENTS_DIR}/`) && f.path.endsWith('.md'));
const schemaFiles = pluginFiles.filter((f) => f.path.startsWith(`${SCHEMAS_DIR}/`) && f.path.endsWith(SCHEMA_SUFFIX));
const schemaTexts = new Map(schemaFiles.map((f) => [schemaName(f.path), f.text]));
const agentFiles = allAgentFiles.filter((f) => schemaTexts.has(agentName(f.path)));
const scriptFiles = walk(SCRIPTS_DIR).map((path) => ({ path, text: read(path) }));
const graph = JSON.parse(read(GRAPH));

const SCHEMAS = new Map();
for (const [name, text] of schemaTexts) {
  const { schema } = checkSchemaBlock(text);
  if (schema) SCHEMAS.set(name, schema);
}

test('the authoring document yields a canonical sentence and the module a roster', () => {
  assert.match(SENTENCE, /^End your reply with your return object: /);
  assert.ok(roster(moduleText).length > 0, 'the roster is empty');
});

test(`every agent definition has a ${SCHEMAS_DIR}/<agent>${SCHEMA_SUFFIX}`, () => {
  assert.ok(allAgentFiles.length > 0, `${AGENTS_DIR} holds no agent definition`);
  assert.deepEqual(checkSchemaCoverage(allAgentFiles.map((f) => agentName(f.path)), [...schemaTexts.keys()]), []);
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

test('every `<agent>.<field>` citation across plugin/**/*.md names a declared field', () => {
  const { seen, problems } = checkCitations(pluginMarkdown, SCHEMAS);
  assert.ok(seen > 0, 'no citation of a schema-carrying agent was found');
  assert.deepEqual(problems, []);
});

test(`every \`<agent>.<field>\` citation across ${SCRIPTS_DIR}/** names a declared field`, () => {
  assert.ok(scriptFiles.length > 0, `${SCRIPTS_DIR} holds no file`);
  const { seen, problems } = checkCitations(scriptFiles, SCHEMAS);
  assert.ok(seen > 0, `no citation of a schema-carrying agent was found under ${SCRIPTS_DIR}`);
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
  nested = {},
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
    ...fields.flatMap((f) => [
      `- \`${f}\`${annotations[f] ? ` (${annotations[f]})` : ''} — described.`,
      ...(nested[f] ?? []).map(([n, a]) => (n.startsWith('**') ? `  - ${n} — not a field.` : `  - \`${n}\`${a ? ` (${a})` : ''} — described.`)),
    ]),
    '',
  ].join('\n');

/** `goodSchema()` with an `items_list` array of object items on its `FAIL` variant. */
const objectItemSchema = () => {
  const s = goodSchema();
  s.oneOf[1].properties.items_list = {
    type: 'array',
    description: 'Object items.',
    items: {
      type: 'object',
      description: 'One item.',
      properties: {
        check_id: { type: 'string', minLength: 1, description: 'The id.' },
        line: { type: 'integer', minimum: 1, description: 'The line.' },
        blocking: { type: 'boolean', description: 'Whether it blocks.' },
        severity: { type: 'string', enum: ['high', 'low'], description: 'The severity.' },
      },
      required: ['check_id', 'line'],
      additionalProperties: false,
    },
  };
  return s;
};

const OBJECT_ITEM_BULLETS = [['check_id'], ['line', 'integer'], ['blocking', 'boolean'], ['severity'], ['**`stale-rule`**']];

/** The sample agent for `objectItemSchema()`, its item bullets overridable. */
const objectItemAgent = (items = OBJECT_ITEM_BULLETS, annotation = 'array of objects') =>
  sampleAgent({
    fields: ['outcome', 'findings_file', 'questions', 'items_list'],
    annotations: { questions: 'array of strings', items_list: annotation },
    nested: { items_list: items },
  });

const itemsAt = 'oneOf\\[1\\]\\.properties\\.items_list\\.items';

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

test('bad samples: an agent definition with no schema file is rejected', () => {
  assert.deepEqual(checkSchemaCoverage(['sample-agent'], ['sample-agent']), []);
  assert.deepEqual(checkSchemaCoverage(['sample-agent', 'unschemaed-agent'], ['sample-agent']), [
    `${AGENTS_DIR}/unschemaed-agent.md has no ${SCHEMAS_DIR}/unschemaed-agent${SCHEMA_SUFFIX}`,
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

test('bad samples: the good object-item sample passes every per-agent check', () => {
  const text = objectItemAgent();
  const { schema, problems } = checkSchemaBlock(JSON.stringify(objectItemSchema(), null, 2));
  assert.deepEqual(problems, []);
  assert.deepEqual(checkDialect(schema), []);
  assert.deepEqual(checkNotInlined(text), []);
  assert.deepEqual(checkOutputContract(text, schema, SENTENCE), []);
});

test('bad samples: object items missing a required keyword are rejected', () => {
  for (const key of ['description', 'properties', 'required']) {
    const s = objectItemSchema();
    delete s.oneOf[1].properties.items_list.items[key];
    assert.match(checkDialect(s).join('\n'), new RegExp(`${itemsAt}: ${key} is missing`));
  }
  const s = objectItemSchema();
  delete s.oneOf[1].properties.items_list.items.additionalProperties;
  assert.match(checkDialect(s).join('\n'), new RegExp(`${itemsAt}: additionalProperties is not false`));
});

test('bad samples: object items outside the dialect are rejected', () => {
  const s = objectItemSchema();
  const items = s.oneOf[1].properties.items_list.items;
  items.minProperties = 1;
  items.properties.check_id.pattern = '^C';
  items.properties.blocking.type = 'array';
  items.properties.line.minLength = 1;
  items.properties.check_id.minimum = 0;
  items.required.push('nope');
  const problems = checkDialect(s).join('\n');
  assert.match(problems, new RegExp(`${itemsAt}: keyword "minProperties" is not in the dialect`));
  assert.match(problems, new RegExp(`${itemsAt}\\.properties\\.check_id: keyword "pattern" is not in the dialect`));
  assert.match(problems, new RegExp(`${itemsAt}\\.properties\\.blocking: type "array" is not in the dialect`));
  assert.match(problems, new RegExp(`${itemsAt}\\.properties\\.line: minLength on a non-string`));
  assert.match(problems, new RegExp(`${itemsAt}\\.properties\\.check_id: minimum on a non-integer`));
  assert.match(problems, new RegExp(`${itemsAt}: required "nope" is not an item property`));
});

test('bad samples: nested item bullets that differ from the object items are rejected', () => {
  const schema = objectItemSchema();
  const missing = objectItemAgent(OBJECT_ITEM_BULLETS.filter(([n]) => n !== 'blocking'));
  assert.match(
    checkOutputContract(missing, schema, SENTENCE).join('\n'),
    /"items_list" lists no nested bullet for item property "blocking"/,
  );
  const extra = objectItemAgent([...OBJECT_ITEM_BULLETS, ['nope']]);
  assert.match(
    checkOutputContract(extra, schema, SENTENCE).join('\n'),
    /"items_list" lists item property "nope", which its items do not declare/,
  );
  const unannotated = objectItemAgent(OBJECT_ITEM_BULLETS.map(([n, a]) => (n === 'line' ? [n] : [n, a])));
  assert.match(
    checkOutputContract(unannotated, schema, SENTENCE).join('\n'),
    /"items_list\.line" is a schema integer but its bullet carries no type annotation/,
  );
});

test('bad samples: an (array of strings) annotation on object items, and nested bullets under string items, are rejected', () => {
  const schema = objectItemSchema();
  const wrong = objectItemAgent(OBJECT_ITEM_BULLETS, 'array of strings');
  assert.match(
    checkOutputContract(wrong, schema, SENTENCE).join('\n'),
    /"items_list" is annotated \(array of strings\) but the schema's items are object/,
  );
  const stringItems = sampleAgent({ nested: { questions: [['check_id']] } });
  assert.match(
    checkOutputContract(stringItems, goodSchema(), SENTENCE).join('\n'),
    /"questions" carries a nested bullet "check_id" but its items are not objects/,
  );
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

test('bad samples: a citation of an undeclared field is rejected; a .md file name is not a citation', () => {
  const schemas = new Map([['sample-reviewer', goodSchema()]]);
  const files = [{ path: 'x.md', text: 'Read `sample-reviewer.md`, then `sample-reviewer.review_file`.' }];
  const { seen, problems } = checkCitations(files, schemas);
  assert.equal(seen, 1);
  assert.deepEqual(problems, ['x.md: `sample-reviewer.review_file` is not declared']);
});

test('bad samples: a citation of an undeclared item property is rejected; the schema file name is not a citation', () => {
  const schemas = new Map([['sample-reviewer', objectItemSchema()]]);
  const files = [
    {
      path: 'x.md',
      text: 'See `sample-reviewer.return.json`, `sample-reviewer.items_list.check_id`, `sample-reviewer.items_list.nope` and `sample-reviewer.questions.x`.',
    },
  ];
  const { seen, problems } = checkCitations(files, schemas);
  assert.equal(seen, 3);
  assert.deepEqual(problems, [
    'x.md: `sample-reviewer.items_list.nope` is not declared',
    'x.md: `sample-reviewer.questions.x` cites an item property, but the items of questions are not objects',
  ]);
});

test('bad samples: a citation inside an outer-loop script is checked like a Markdown one', () => {
  const schemas = new Map([['sample-reviewer', objectItemSchema()]]);
  const files = [
    {
      path: `${SCRIPTS_DIR}/x.sh`,
      text: '# reads `sample-reviewer.items_list.check_id` and `sample-reviewer.verdict`\n',
    },
  ];
  const { seen, problems } = checkCitations(files, schemas);
  assert.equal(seen, 2);
  assert.deepEqual(problems, [`${SCRIPTS_DIR}/x.sh: \`sample-reviewer.verdict\` is not declared`]);
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
