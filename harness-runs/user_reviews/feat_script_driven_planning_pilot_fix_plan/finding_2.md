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
   - **Owner: `pnl_reap`** in `cli/templates/scripts/lib/planning-node-lib.sh`, and no other library. It already appends the node's stream to the run's `${log_path%.log}.stream.jsonl` ("`cat "$stream" >>"${log_path%.log}.stream.jsonl"`"), and in the same reap it records the node session's `session_id`, read from its `init` event, against `<seq>` and `<node>` in one small manifest beside those streams, under `${log_path%.log}.planning/`. `planning-record-lib.sh` is not the owner: its header's rule is *"each write is the one the autonomous planning fork makes today, by the same two wrapper calls"*, the fork makes no node-session manifest, and that header is left unchanged.
     - In the same edit, amend `planning-node-lib.sh`'s header sentence *"Every durable write is `lib/planning-record-lib.sh`'s."* so that it carves out this library's run-log-side writes: for example *"Every durable write is `lib/planning-record-lib.sh`'s, except the two run-log-side writes `pnl_reap` makes — the node's stream appended to the run's `.stream.jsonl` and the node-session manifest under `${log_path%.log}.planning/`."* Update `pnl_reap`'s own comment block ("pnl_reap <handle> — after the session's pid has exited. Appends the node's stream …") to name the manifest write too.
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
6. **Docs (`general` layer).**
   - Update `docs/watcher.md` → `### Run analytics`. Its sentence "is `schema: 3` when it carries gate-log entries, `schema: 2` when it carries rounds but none, and `schema: 1` otherwise" becomes the schema-4 rule, and "one entry per session" is restated to cover the engine/planning-node session split (each session's `kind` and `node`). Describe the run-perspective (union) wall, idle, active and host-suspended figures beside the separately named summed-session-time figure, and name the node-session manifest under `${log_path%.log}.planning/` as a new input `run-analytics.sh` reads when present, owned by `pnl_reap`.
   - Grep `docs/` and `ARCHITECTURE.md` for the record's schema wording (`schema: 3`, `schema: 2`, `schema: 1`) and its session-count wording (`one entry per session`, `sessions`) in a run-analytics context, and update every hit the change makes inaccurate. `ARCHITECTURE.md`'s run-analytics reader row (the `stream-json` binding that names `lib/run-analytics.jq`) is checked against the new manifest input.
7. **Floors.** jq 1.5 (no regex, every `if` has an `else`), as the header of `run-analytics-report.jq` states, and bash 3.2 for any shell change.
8. **Tests.**
   - Add a new suite, for example `cli/test/run-analytics-node-overlap.test.mjs`. Over a fixture stream holding one engine session and three node sessions overlapping in time, plus the node manifest, assert:
     - the hand-computed union `wall_ms`, the run idle and active figures, and the summed-session figure;
     - the engine/node session counts;
     - that cost and tokens are sums;
     - that each node's own figures appear in the record and in `run-analytics.md`.
   - Add one case asserting that a schema-3 document is read and extended.
   - Add one case asserting that a run with sequential, non-overlapping sessions produces the same `wall_ms`, `active_ms`, `idle_ms` and `host_suspended_ms` as before.
   - Edit the existing suites only where their expected bytes change because of the schema bump or the new fields.

**Deviations from plan:**

- `cli` layer dispatch only. Fix items 5 (`plugin/commands/branch-status.md` → the `Time:` bullet, and every `plugin/` file quoting `Time: wall` / `wall_ms`) and 6 (`docs/watcher.md` → `### Run analytics`, the `docs/` and `ARCHITECTURE.md` schema / session-count wording) are outside `cli/` and were not touched here; they belong to the `plugin` and `general` layer dispatches of this unit. The fields they must read are `.run.wall_ms`, `.run.active_ms`, `.run.host_suspended_ms`, `.run.idle_ms` (now the run's own, union-based), `.run.engine_sessions` and `.run.node_sessions` (`.run.sessions` stays the total), `.run.session_wall_sum_ms`, `.run.planning_nodes`; the manifest is `${log_path%.log}.planning/node-sessions.jsonl`, one `{"session_id","seq","node"}` line per reaped node session, written by `pnl_reap`.
- Schema 4 shape: every document written is schema 4 and always carries a `rounds` and a `gate_logs` array (possibly empty), rather than keeping schema 1/2/3's presence rules beside a kind bump. The existing suites' `schema` / `'rounds' in doc` / `'gate_logs' in doc` assertions on written documents changed to `4` / `[]` accordingly; `run-analytics-rounds.test.mjs`'s "schema 1 extended" case now plants a real schema-1 document (the writer no longer writes one), and its refusal case moved from schema 4 to schema 5. `check_doc`'s two messages changed to "expected 1, 2, 3 or 4" and "only schema 3 and 4 may"; the two report suites' regexes follow.
- The manifest reaches mode `sessions` as a new jq variable `$nodes` (`--slurpfile nodes`), so per the program's EVERY MODE TAKES EVERY VARIABLE rule every other call — the five others in `run-analytics.sh` and the three direct calls in `run-analytics-network-parse.test.mjs` and `run-analytics-rounds-parse.test.mjs` — now passes `--argjson nodes '[]'`.
- Host-suspended over a cluster of overlapping sessions is the largest member's figure, stated as an approximation in `run-analytics-report.jq` → `RUN TIME`: the records' `host_asleep` class marks a gap overlapping a suspend, not the suspend's bounds, so no exact intersection is available from them. A cluster of one session (every non-overlapping session) keeps its own four figures verbatim, which is what keeps the orchestrated path's figures unchanged.
- `.run.first_at` / `.run.last_at` are now the earliest / latest by time (falling back to the first / last session's when none parses), since with overlapping sessions the last-recorded session need not end last; identical for sequential sessions.
- Run duration_ms and duration_api_ms stay summed over sessions (the header says so); only wall / active / idle / host-suspended moved to the run perspective.
- `general` layer dispatch (item 6): `docs/watcher.md` → `### Run analytics` now states the schema-4 rule, the per-session `kind` / `node`, and a new **Node sessions, and the run's time.** paragraph (the manifest as `run-analytics.sh`'s input owned by `pnl_reap`, the union-based figures, `session_wall_sum_ms`, the split counts, `planning_nodes`). `grep -rn "schema: [123]\|one entry per session\|Time: wall"` over `docs/`, `ARCHITECTURE.md` and `README.md` found no other hit. `ARCHITECTURE.md`'s run-analytics reader row (the `stream-json` binding naming `lib/run-analytics.jq`) was checked and left unchanged: the manifest is a harness-written file, not an engine format, and the reader reads no new stream field. The row that did become inaccurate is the `planning-node-lib.sh` → `pnl_reap` row, which enumerates what is read off a node's stream; it now names the `init` event's `session_id` and the manifest it is recorded in. Item 5 was already present in the working tree (`plugin/commands/branch-status.md`) and was not touched by this dispatch.
- `run-analytics.test.mjs` gained three assertions beside its changed `schema` line (each session's `kind` / `node`, `engine_sessions` / `node_sessions`, `session_wall_sum_ms`), and `planning-node-lib.test.mjs`'s reap helper reads the manifest so two existing cases assert it is written (and not written without an `init` event).
