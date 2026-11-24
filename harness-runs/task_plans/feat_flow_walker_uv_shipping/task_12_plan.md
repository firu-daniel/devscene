### Task 12 — Carry the change into this self-adopted repository and register Task 1's tree guard

**Goal:** Apply to this repository, which has adopted its own harness (`.claude/context/conventions.md` → `## Documents of record`), what `init --upgrade` would apply to an adopter. Then register the tree-reading test Task 1 added.

**Depends on:**

- **Task 3:** `cli/templates/scripts/flow-host-provision.sh` and the edited `cli/templates/scripts/lib/harness-run-lib.sh`.
- **Task 4:** the edited `cli/templates/scripts/setup-worktree.sh`.
- **Task 6:** the rendered rule `<scriptsDir>/python/.venv/`, which is `scripts/python/.venv/` for this repository's `scriptsDir`.
- **Task 1:** `cli/test/python-packages-staged.test.mjs`, which names this task as its registering task.

**Why the packages are linked here, not copied.** Task 2's generator skips this repository, because its packages already live at the root. So the layout `flow-walker.sh` will use after #419, `<scriptsDir>/python/devscene-flow-host`, is made to resolve here through two committed relative symlinks rather than a second copy of the sources. The walker's environment `scripts/python/.venv` stays apart from the dev environments `scripts/python-service.sh` keeps in each package's own `.venv`.

### Targets

- `scripts/flow-host-provision.sh` (new).
- `scripts/lib/harness-run-lib.sh`.
- `scripts/setup-worktree.sh`.
- `scripts/python/graphscene` (new symlink).
- `scripts/python/devscene-flow-host` (new symlink).
- `.gitignore`.
- `examples/notes-app/.gitignore`.
- `devscene.config.json`: `treeGuards` only.

**Work:**

- [ ] Copy these byte for byte from their templates, so each equals its template as the other self-adopted copies already do:
  - `cli/templates/scripts/flow-host-provision.sh` → `scripts/flow-host-provision.sh`, mode `0755`;
  - `cli/templates/scripts/lib/harness-run-lib.sh` → `scripts/lib/harness-run-lib.sh`;
  - `cli/templates/scripts/setup-worktree.sh` → `scripts/setup-worktree.sh`.
- [ ] Create `scripts/python/graphscene` → `../../graphscene` and `scripts/python/devscene-flow-host` → `../../devscene-flow-host` as relative symlinks. Relative targets name no location on the machine, which gate 6a's self-containment rule requires.
- [ ] `.gitignore`, the managed block: add the line Task 6's template renders for `scriptsDir` `scripts`, with its comment, in the block's order. The existing `.venv/` rule already covers it. The line is there so that `doctor`'s `ignore-rules` reads this block as `init` would write it.
- [ ] `examples/notes-app/.gitignore`: add the same line, because that file is an `init`-rendered fixture kept live (`examples/notes-app/README.md` → *"The capture is frozen; the fixture is live"*), and its `scriptsDir` is `scripts`.
- [ ] `devscene.config.json` → `treeGuards`: append six entries, each with `"test": "test/python-packages-staged.test.mjs"`, covering in turn:
  - `graphscene/src/**`
  - `graphscene/pyproject.toml`
  - `graphscene/uv.lock`
  - `devscene-flow-host/src/**`
  - `devscene-flow-host/pyproject.toml`
  - `devscene-flow-host/uv.lock`

**Verification:**

- `git diff --no-index --stat cli/templates/scripts/flow-host-provision.sh scripts/flow-host-provision.sh` prints nothing. The same holds for `lib/harness-run-lib.sh` and `setup-worktree.sh`.
- `git ls-files -s scripts/python` shows both entries with mode `120000`, and `readlink scripts/python/devscene-flow-host` prints `../../devscene-flow-host`.
- `jq -e '.treeGuards | map(select(.test == "test/python-packages-staged.test.mjs")) | length == 6' devscene.config.json` prints `true`.
- `git check-ignore -v scripts/python/.venv/pyvenv.cfg` reports an ignore rule.
