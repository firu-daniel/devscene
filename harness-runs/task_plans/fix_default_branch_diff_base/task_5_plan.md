### Task 5 — Register the diff-base corpus test as a tree guard

**Goal:** Add the `treeGuards` entry that makes every later unit touching `plugin/**/*.md` run the diff-base corpus test, so a bare `<default_branch>` diff base cannot come back unnoticed.

**Depends on:** Task 4, which creates `cli/test/diff-base-corpus.test.mjs` and names this task as its registering task (`${CLAUDE_PLUGIN_ROOT}/instructions/unit_loop_core.md` → `## The test-run rule`, point 8). The test reads every `*.md` under `plugin/`. This task adds the configuration entry only and changes nothing in the test.

**How this task's implementer reads the conventions.** This is the catch-all task, so its implementer reads every configured layer's conventions document. The rules that bind this edit are `.claude/context/conventions.md` → `## Configuration is the source of truth, and it is read at run time` and the existing `treeGuards` entry shape.

### Targets

- `devscene.config.json` (repository root)

**Work:**

- [ ] `devscene.config.json` → `treeGuards`: append `{ "test": "test/diff-base-corpus.test.mjs", "covers": "plugin/**/*.md" }` after the last existing entry. Use the existing entries' shape: `test` is relative to the `cli` workspace, as in `test/untrusted-input-corpus.test.mjs`. Keep every other key and entry byte-identical, with the file's two-space indentation.

**Verification:**

- `git diff devscene.config.json` shows exactly one added array element, and no other line changed apart from the comma the preceding element gains.
- The file still parses: `node -e "JSON.parse(require('fs').readFileSync('devscene.config.json','utf8'))"` exits 0, run from the repository root.
