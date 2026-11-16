### Task 12 — Bring the watcher planning-driver suite's stub and the watcher's REPRO note to the return block

**Goal:** Make the end-to-end suite that drives the script-driven planning pilot through `autonomous-watcher.sh` stand in for a node session the way a real one answers — a `result` whose text ends in a return block valid against the agent's schema, with no `structured_output` — and make the watcher's own reproduce-by-hand note describe that stub.

**Depends on:** Task 11, after which the driver reads the validated object `pnl_reap` prints (Task 10) and takes a writer's questions from its `questions` array. The return objects this stub must emit, per Tasks 2–5 and the story index `## Context` field table: `ui-tests-plan-writer` → `{"outcome":"no_ui","reason":"…"}`; a gate → `{"outcome":"PASS","findings_file":"<the round file it wrote>"}` (`task-plan-reviewer`, `architecture-reviewer` and `business-parity-reviewer` all carry `findings_file` on a plan-review `PASS`); `task-plan-writer` → `{"outcome":"returned","story_file":…,"task_files_dir":…,"tasks_count":1,"story_points_total":…}`, or, in the park mode, `{"outcome":"questions","questions":["Which storage key does the feature use?"]}`.

**Where this task stops.** The suite header states that its stub imports nothing from `cli/test/helpers/planning-driver.mjs` and spells every literal it asserts on in its own file — keep that: the objects are written out here, not built from a schema at run time. The watcher's behaviour is unchanged; its only edit is the REPRO comment.

### Targets

- `cli/test/watcher-planning-driver.test.mjs`
- `cli/templates/scripts/autonomous-watcher.sh` → the header's `REPRO` block, the `planning pilot` entry

**Work:**

- [ ] `watcher-planning-driver.test.mjs` → `STUB_SOURCE`: replace the `decision` object and the `structured_output` field with the four return objects above, emitted as the `result` event's `result` text — one prose line, a blank line, then the object in a ```` ```json ```` block, nothing after it — and no `structured_output` key (`<state_dir>/lessons.md` → *"When a check moves to reading a field one producer writes, the same change makes every path that stands in for that producer … write the field too."*). The writer's `story_points_total` is any non-negative integer; keep every file the stub writes as it is.
- [ ] `watcher-planning-driver.test.mjs`: bring any assertion on the park's question file to the body Task 11's `pd_ask_park` writes — one `## Q1 — Which storage key does the feature use?` section — and restate the suite header where it describes what a node session prints.
- [ ] `autonomous-watcher.sh` → the `REPRO` block's `planning pilot` entry: "a success result whose structured_output names an outcome its node declares" becomes a success result whose text ends in a return block valid against its agent's `## Return schema`, naming an outcome its node declares. Comment text only; no code line changes.

**Verification:**

- `cli/test/watcher-planning-driver.test.mjs` passes.
- `git grep -nE 'structured_output|harness_friction' -- cli/test/watcher-planning-driver.test.mjs cli/templates/scripts/autonomous-watcher.sh` prints only `autonomous-watcher.sh` lines that belong to the remote mention control, if any, and none about a planning node.
- `git diff -- cli/templates/scripts/autonomous-watcher.sh` changes comment lines only.
