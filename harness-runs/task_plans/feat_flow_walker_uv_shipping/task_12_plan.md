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

- [x] Copy these byte for byte from their templates, so each equals its template as the other self-adopted copies already do:
  - `cli/templates/scripts/flow-host-provision.sh` → `scripts/flow-host-provision.sh`, mode `0755`;
  - `cli/templates/scripts/lib/harness-run-lib.sh` → `scripts/lib/harness-run-lib.sh`;
  - `cli/templates/scripts/setup-worktree.sh` → `scripts/setup-worktree.sh`.
- [x] Create `scripts/python/graphscene` → `../../graphscene` and `scripts/python/devscene-flow-host` → `../../devscene-flow-host` as relative symlinks. Relative targets name no location on the machine, which gate 6a's self-containment rule requires.
- [x] `.gitignore`, the managed block: add the line Task 6's template renders for `scriptsDir` `scripts`, with its comment, in the block's order. The existing `.venv/` rule already covers it. The line is there so that `doctor`'s `ignore-rules` reads this block as `init` would write it.
- [x] `examples/notes-app/.gitignore`: add the same line, because that file is an `init`-rendered fixture kept live (`examples/notes-app/README.md` → *"The capture is frozen; the fixture is live"*), and its `scriptsDir` is `scripts`.
- [x] `devscene.config.json` → `treeGuards`: append two entries, each with `"test": "test/python-packages-staged.test.mjs"`, covering in turn:
  - `cli/src/flowHost/**`
  - `cli/package.json`

  Both globs select only `cli`-layer units, whose `<test_file_cmd>` runs a `cli/test/*.mjs` suite. No entry covers `graphscene/**` or `devscene-flow-host/**`: a unit of those layers runs a guard through `bash scripts/python-service.sh --package <name> test …` (`.claude/context/graphscene.md` → `## Tests`, `.claude/context/devscene-flow-host.md` → `## Tests — what "done" means here`), which cannot run a `.mjs` suite. A change under either Python package reaches this suite at Run gates instead, as Task 1's test header states.

**Verification:**

- `git diff --no-index --stat cli/templates/scripts/flow-host-provision.sh scripts/flow-host-provision.sh` prints nothing. The same holds for `lib/harness-run-lib.sh` and `setup-worktree.sh`.
- `git ls-files -s scripts/python` shows both entries with mode `120000`, and `readlink scripts/python/devscene-flow-host` prints `../../devscene-flow-host`.
- `jq -e '[.treeGuards[] | select(.test == "test/python-packages-staged.test.mjs") | .covers] | sort == ["cli/package.json", "cli/src/flowHost/**"]' devscene.config.json` prints `true`: the entries for this suite are exactly those two globs.
- `git check-ignore -v scripts/python/.venv/pyvenv.cfg` reports an ignore rule.

**Deviations from plan:**

- Blocked on the permission layer, not the sandbox: in this session (don't-ask mode) `cp cli/templates/scripts/{flow-host-provision.sh,lib/harness-run-lib.sh,setup-worktree.sh} scripts/…`, `ln -s ../../graphscene scripts/python/graphscene` and `ln -s ../../devscene-flow-host scripts/python/devscene-flow-host` were each refused with *"Permission to use Bash has been denied because Claude Code is running in don't ask mode"*. The file tools cannot create a symlink, and a byte-for-byte copy of the 352 KB `harness-run-lib.sh` through `Write` is not a faithful copy route, so the three copies and two symlinks are not done. `.claude/settings.json` holds one `Bash(...)` allow entry (`bash scripts/task-offer-check.sh`); the run profile under `~/.local/state/devscene/run-profiles/` could not be read (the same refusal). `scripts/python/` exists as an empty directory (`mkdir -p` was permitted).
- Done: `.gitignore` and `examples/notes-app/.gitignore` carry `scripts/python/.venv/` with the template's comment, placed after the run-control artifacts as `cli/templates/repo/gitignore` orders it; `devscene.config.json` → `treeGuards` carries the two entries (the `jq -e` verification printed `true`). `git check-ignore -v` was refused the same way and is not run.
- Resumed after `harness-runs/clarifications/feat_flow_walker_uv_shipping/answer_1.md`: the operator did the three copies and the two symlinks in this run copy, uncommitted. This iteration only verified them and wrote no work file. Results:
  - `git diff --no-index --stat` printed nothing for `lib/harness-run-lib.sh`. For `flow-host-provision.sh` and `setup-worktree.sh` it printed one `0 insertions(+), 0 deletions(-)` line each. Plain `git diff --no-index` shows only `old mode 100644` / `new mode 100755` for both: the bytes match, and the only difference is the template's tracked mode `100644` against the executable copy (`git ls-files -s` shows `scripts/setup-worktree.sh` already at `100755`). The verification bullet's "prints nothing" is met for content only.
  - Evidence downgrade: `git ls-files -s scripts/python` cannot show mode `120000` until the commit step stages the two untracked symlinks. What this rests on instead: `ls -la scripts/python` lists both as `l` entries, `readlink scripts/python/devscene-flow-host` prints `../../devscene-flow-host`, and `readlink scripts/python/graphscene` prints `../../graphscene`.
  - `jq -e …` printed `true`. `git check-ignore -v scripts/python/.venv/pyvenv.cfg` printed `.gitignore:61:scripts/python/.venv/`.
