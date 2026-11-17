### 1. The watcher planning-driver fixture's plugin copy carries no `schemas/` directory

**Site:** `cli/test/watcher-planning-driver.test.mjs` → `pilotFixture`, the plugin-copy block that begins `const source = join(WORKSPACE_ROOT, 'plugin');` and holds `await mkdir(join(plugin, 'agents'));` and the loop `for (const agent of graphAgents(f.dir)) {` (around line 212, navigation hint only).

**Failing test:** `cli/test/watcher-planning-driver.test.mjs`:
- `key on: the setup session, then node sessions on its vector, then one engine session`
- `key on, and the driver parks: no engine session follows, and the record is parked`
- `key on, and every node dispatch is undelivered: the run pauses and its one paused notification names the overload`
- `a job with the key on: the setup session, node sessions pinned to the installed runtime root, then the engine session`
- `the hand-off archives only what the driver consumed`

**Failure, from the log** (the same line appears in four of the five diagnostics; the job case's diagnostic is truncated but shows the same `pd_drive exit 2` on every launch):

```
2026-11-16T20:46:11 [watcher] planning driver failed for 'feat_x' (pd_drive exit 2) — see /private/tmp/claude-501/harness-fixture-EZIzV4/devscene/autonomous_logs/feat_x.log
--- run log, plan-drive and planning-driver lines
planning-driver: the return schema file '/private/tmp/claude-501/watcher-planning-driver-H4GLTn/plugin/schemas/task-plan-writer.return.json' cannot be read
```

```
2026-11-16T20:47:30 [watcher] planning driver failed for 'feat_x' (pd_drive exit 2) — see /private/tmp/claude-501/harness-fixture-23DrPb/devscene/autonomous_logs/feat_x.log
2026-11-16T20:47:30 [watcher] run 'feat_x' failed — rc=2
```

The assertions then fail on that outcome — `'failed' !== 'paused'`, `0 !== 1`, and `expected: true, actual: false` at `cli/test/watcher-planning-driver.test.mjs:370:10` / `:404:10`.

**Class:** first round — no earlier log was named for this gate run.

**Diagnosis.** This branch's Finding 1 commit moved every planning agent's return schema out of the agent file's `## Return schema` section into `plugin/schemas/<agent>.return.json`, and `pnl_load_schemas` in `cli/templates/scripts/lib/planning-node-lib.sh` now reads `"$PNL_PLUGIN_DIR/schemas/$agent.return.json"` and fails with `the return schema file '$f' cannot be read` (exit 2) when it is absent. The shared driver fixture, `cli/test/helpers/planning-driver.mjs` → `driverFixture`, was updated in the same commit to `mkdir` a `schemas` directory and copy each agent's `<agent>.return.json` beside its agent file. `pilotFixture` in `cli/test/watcher-planning-driver.test.mjs` builds its own plugin copy independently and was not updated: it creates `agents/` and `instructions/` only, and copies each `graphAgents(f.dir)` agent's `.md` file but no schema. So the watcher launches `pd_drive` against a plugin directory with no `schemas/` folder, the first dispatch node (`task-plan-writer`) faults in `pnl_load_schemas`, the driver exits 2 and the watcher records the run as failed — which is exactly what every one of the five cases logs. A grep of `cli/test` for files that copy `'agents'` without `'schemas'` returns this file (and `cli/test/prompt-injection-verdict.test.mjs`, which does not drive the planning driver).

The product code is correct; the test fixture is out of date with the relocated schemas.

**Fix.** In `pilotFixture`, mirror `driverFixture`'s plugin copy:

- [ ] After `await mkdir(join(plugin, 'agents'));`, add `await mkdir(join(plugin, 'schemas'));`.
- [ ] Inside the `for (const agent of graphAgents(f.dir)) {` loop, after the agent `.md` copy, copy `join(source, 'schemas', `${agent}.return.json`)` to `join(plugin, 'schemas', `${agent}.return.json`)`.
- [ ] Update the `pilotFixture` doc comment ("A watcher fixture on `feat_x`, a plugin directory under the system temp directory, …") so it states the plugin copy holds each graph agent's `schemas/<agent>.return.json` as well as its agent file, matching the fixture description `cli/templates/scripts/autonomous-watcher.sh` already gives.

Do not touch `pnl_load_schemas` or the schema files: the fault message is the intended behaviour for a plugin with no schema. The stub in this file still reads the agent's `tools:` line from `agents/<agent>.md` and needs no change.
