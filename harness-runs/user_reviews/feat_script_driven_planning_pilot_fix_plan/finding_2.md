### 2. Run analytics sums overlapping node sessions' time into the run's wall, active, idle and host-suspended figures

**File:** `cli/templates/scripts/lib/run-analytics-report.jq` (`run_of`) — "wall_ms: ($ss | num_sum(.time.wall_ms))"

**Problem.** `run_of` builds the run figures by summing each session record: `wall_ms`, `active_ms`, `idle_ms` and `host_suspended_ms` (also `duration_ms`) are all `num_sum` over `.sessions`, and `sessions` is `$ss | length`. Each planning node session's stream is appended to the run's `<branch>.stream.jsonl` when it is reaped (`cli/templates/scripts/lib/planning-node-lib.sh` → `pnl_reap`: `cat "$stream" >>"${log_path%.log}.stream.jsonl"`), so `run-analytics.sh` records every node session as one more session record.

With the driver on, the gates of a set run at the same time. Three 10-minute gates therefore add 30 minutes of "wall" time, and the `sessions` count mixes the engine sessions with every node session. `/devscene:branch-status` prints these sums on its `Time:` line (`plugin/commands/branch-status.md`, the `Time: wall … (<sessions> sessions)` bullet). This branch introduced the overlap, so the analytics must handle it on this branch.

**Required shape** (the user's, verbatim in the index's `## Source observations`):

- **Run perspective, the headline figures.**
  - `wall_ms` is the length of the **union** of all session intervals `[first_at, last_at]`: elapsed time, which is what an adopter's runner minutes bill.
  - `idle_ms` counts only gaps longer than the idle threshold in which **no** session emitted an event.
  - `active_ms` is wall minus idle.
  - `host_suspended_ms` is computed over the same union.
- **Per node.** Each node session's own wall, active, idle, duration and cost, listed individually in the record and in `run-analytics.md`.
- **Summed figures stay summed.** Cost and tokens are summed across all sessions. A separately named summed-session-time figure (for example `session_wall_sum_ms`) may sit beside wall time, never in its place.
- **Session counts split.** Engine sessions (setup and engine) are counted apart from planning node sessions.
- `/devscene:branch-status` prints the run-perspective figures on its `Time:` line. The orchestrated path's figures do not change: its sessions never overlap, so the union of their intervals is their sum and its idle gaps are each session's own.
- Bump the record's `schema` if its shape changes, and keep reading the older schemas.

**Fix.**

1. **Identify each session's kind.**
   - A session record needs to say whether it is an engine session or a planning node session, and for a node, which node (`<seq>-<node>`). The node's identity is known only to the driver: its stream file is `${log_path%.log}.planning/<seq>-<node>.stream.jsonl`.
   - Suggested route: have `pnl_reap` (or `planning-record-lib.sh`, which owns every durable write) record the node session's `session_id`, read from its `init` event, against `<seq>` and `<node>` in one small manifest beside those streams.
   - `run-analytics.sh` already takes the run's stream file. It reads that manifest from `${stream%.stream.jsonl}.planning/` when present and passes it to `lib/run-analytics.jq` mode `sessions` through `--slurpfile`, as `known` is passed today.
   - The mode then tags each new record, for example `kind: "engine" | "planning_node"` and `node: "<seq>-<node>"` or `null`.
   - Any route works if a session is classed from a record the driver wrote and never guessed from its timing. A record from an older schema carries no kind and counts as an engine session.
2. **Run-perspective time in `run_of`.**
   - Wall: compute the union of the `[first_at, last_at]` intervals with `ts_ms`, and take its length as `wall_ms`. A session without both timestamps keeps its own `time.wall_ms` as a fallback, which the header states.
   - Idle: build the run-level idle from each session's `time.idle_gaps` (`start_at`, `length_ms`). A gap, or the part of it, that another session's active span covers is not run idle. Prefer an exact computation over the sessions' gap lists, intersecting each gap with the complement of every other session's non-idle stretches. If the records lack what an exact computation needs, add the needed field to the session record in `lib/run-analytics.jq` (for example the session's event-time extent per gap is already `start_at` + `length_ms`), and state the method in `run-analytics-report.jq`'s header.
   - Active: `active_ms = wall_ms - idle_ms`.
   - Host-suspended: compute it over the union. A host suspend stalls every session at once, so suspended time that overlapping sessions share counts once. Where the session records' suspend classification (`idle_gaps[].class`, re-classed by mode `overlay`) gives intervals, intersect them with the union. Otherwise state the approximation in the header.
   - Keep the old summed figure under a new name beside `wall_ms`, never in its place.
   - Split `sessions` into, for example, `engine_sessions` and `node_sessions`. Keep `sessions` as the total only if the header names it as such.
   - `total_cost_usd`, every token figure, `requests`, `api_retries`, `permission_denials` and the sub-agent figures stay summed or pooled exactly as today.
3. **Markdown (`--arg mode markdown`).**
   - `## Whole run`: show the run-perspective Wall / Active / Host-suspended / Idle rows, the summed-session-time row labelled as a sum, and the split session counts.
   - Per node: list each node session with its own wall, active, idle, duration and cost. The existing `## Session <k>` sections already carry per-session figures, so title a node's section with its node name, or add a compact `## Planning node sessions` table. The user asked for both the record and `run-analytics.md`.
   - Update the header block of `run-analytics-report.jq` (mode `rollup` field list, the `branch-status reads …` fixed names) and of `run-analytics.jq` (session record shape) in the same edit.
4. **Schema.**
   - The record's shape changes (a session `kind`/`node`, new run fields), so bump `schema` to 4 in `run-analytics.sh`'s writer and in both jq files' schema checks.
   - Keep accepting schema 1, 2 and 3 documents. Extend one in place by appending new sessions; its old records carry no kind and count as engine sessions.
   - Update `run-analytics.sh`'s header paragraph that enumerates the accepted schemas and refuses others.
   - Update `cli/templates/state-dir/run_analytics/README.md` where it describes the record.
5. **`/devscene:branch-status`.** In `plugin/commands/branch-status.md`, have the `Time:` bullet read the run-perspective fields and the split session counts, for example `(<engine> engine sessions, <nodes> planning node sessions)`. Keep the line unchanged for a record with no node sessions. Grep `plugin/` for the `Time: wall` literal and for `wall_ms` and update every file that quotes it.
6. **Floors.** jq 1.5 (no regex, every `if` has an `else`), as the header of `run-analytics-report.jq` states, and bash 3.2 for any shell change.
7. **Tests.**
   - Add a new suite, for example `cli/test/run-analytics-node-overlap.test.mjs`. Over a fixture stream holding one engine session and three node sessions overlapping in time, plus the node manifest, assert:
     - the hand-computed union `wall_ms`, the run idle and active figures, and the summed-session figure;
     - the engine/node session counts;
     - that cost and tokens are sums;
     - that each node's own figures appear in the record and in `run-analytics.md`.
   - Add one case asserting that a schema-3 document is read and extended.
   - Add one case asserting that a run with sequential, non-overlapping sessions produces the same `wall_ms`, `active_ms`, `idle_ms` and `host_suspended_ms` as before.
   - Edit the existing suites only where their expected bytes change because of the schema bump or the new fields.
