### Task 8 — Read a prompt source's fenced blocks from a plugin document in `records/prompt_blocks.py`

**Goal:** Give the flow host a record reader that parses a graph node's `promptSource` and returns the fenced blocks under that heading of a plugin document. It reads as `cli/templates/scripts/lib/planning-node-lib.sh` → `pnl_core_scan` and `pnl_init` do, so the builder (Task 11) and the core-agreement check (Task 15) cut prompts exactly as the bash driver does.

**Where this layer stops.** This task reads and decides nothing (`.claude/context/devscene-flow-host.md` → `## Records, and which one is the truth`):

- **It returns a heading's blocks, whatever their number.** Whether that number matches the node's `prompts` is the caller's: Task 11 refuses at construction, and Task 15 reports a violation.
- **Filling a block's tokens** is Task 11's.

The `promptSource` string is GraphScene's opaque `DispatchNode.prompt_source` (Task 2). Its harness spelling, which Task 1 wrote into the planning graph, is:

`<document> → <section> → <heading>`

for example ``instructions/task_plan_writing_instructions_core.md → ## Loop → ### 1. Spawn `task-plan-writer` ``. The separator is `" → "` (U+2192 with one space each side). `<document>` is relative to the plugin directory.

### Targets

- `devscene-flow-host/src/devscene_flow_host/records/prompt_blocks.py` (new)
- `devscene-flow-host/tests/test_prompt_blocks.py` (new)

**The contract this task produces.** Tasks 11 and 15 call it.

```python
SOURCE_SEPARATOR: Final = " → "

@dataclass(frozen=True)
class PromptSource:
    document: str   # relative to the plugin directory
    section: str    # a "## " line
    heading: str    # a "### " line

def parse_prompt_source(value: str) -> PromptSource: ...
def read_prompt_blocks(plugin_dir: Path, source: PromptSource) -> tuple[str, ...]: ...
```

- **`parse_prompt_source`.** It raises `ValueError(f"prompt source '{value}' is not '<document> → ## <section> → ### <heading>'")` unless all of these hold:
  - the value splits on `SOURCE_SEPARATOR` into exactly three parts;
  - the section starts with `## ` and the heading with `### `;
  - the document is neither empty nor absolute, and has no `..` segment.
- **`read_prompt_blocks` scopes the heading as `pnl_core_scan` does:**
  - a `##` line opens a section;
  - the heading is the `###` line equal to `source.heading` inside the section equal to `source.section`, and it ends at the next `##` or `###` line;
  - a line opening with three backticks toggles a fence, and nothing inside a fence is read as a heading;
  - a trailing CR is stripped from every line.
- **What it returns.** Each block is its lines joined by `\n`, with trailing newlines stripped, as bash's `$(…)` strips them, returned in document order.
- **Its `RecordError` messages**, after `pnl_init`'s wording:
  - a missing document: `the prompt document '<path>' cannot be read`. This is `FileNotFoundError` only; any other `OSError` propagates (`.claude/context/devscene-flow-host.md` → `## Errors`);
  - a document that is not UTF-8: `<path>: not UTF-8 text`;
  - a missing section: `the heading '<section>' is not in '<path>'`;
  - a section without the heading: `the heading '<heading>' is not under '<section>' in '<path>'`;
  - an odd number of fence lines under the heading: `the heading '<heading>' carries <n> fence lines in '<path>', an unclosed block`.

  `<path>` is `plugin_dir / document`.

**Work:**

- [ ] **`records/prompt_blocks.py`.**
  - **The docstring.** Its *"The rule:"* names `pnl_core_scan` and `pnl_init` as the bash readers it reads as, and states the scoping and the strip. Its *"Deliberately not covered"* list names two things: the block-count check (the caller's), and token filling (`host/agent_prompts.py`'s).
  - **The code.** Declare `SOURCE_SEPARATOR` and the heading prefixes as `Final` constants. Implement both functions exactly as the contract spells them.
- [ ] **`tests/test_prompt_blocks.py` — the readers.** Open with the header *"The rule this file exists to enforce"*. Plant documents under `tmp_path` and cover:
  - two blocks under one heading, returned in order;
  - a heading of the same name under another section, which is not matched;
  - a `###` line inside a fence, which is not read as a heading;
  - a CRLF document;
  - a block with trailing blank lines inside its fence, stripped;
  - one case per `RecordError` above, each asserting the exact message;
  - one case per `parse_prompt_source` refusal clause, each asserting the exact message.
- [ ] **`tests/test_prompt_blocks.py` — the real core.** Add one case that reads this checkout's real `plugin/instructions/task_plan_writing_instructions_core.md` as read-only input, with `plugin_dir` the checkout's `plugin/`. It asserts that ``## Loop → ### 1. Spawn `task-plan-writer` `` yields two blocks, the first opening `Write the task plan.` and the second opening `Revise the task plan per findings at`. Those literals are hand-written from the core.

**Verification:**

- `bash scripts/python-service.sh --package devscene-flow-host test tests/test_prompt_blocks.py` passes.
- `records/prompt_blocks.py` imports neither `graphscene` nor any `host` module. The `records` layer rule (`.claude/context/devscene-flow-host.md` → `## The internal layers`) forbids both.
