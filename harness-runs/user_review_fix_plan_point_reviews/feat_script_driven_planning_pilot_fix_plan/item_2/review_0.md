# cli review — ### 2. Run analytics sums overlapping node sessions' time into the run's wall, active, idle and host-suspended figures — iteration 0

Verification: the nine affected suites (`run-analytics-node-overlap`, `run-analytics`, `run-analytics-rounds`, `run-analytics-rounds-parse`, `run-analytics-network`, `run-analytics-network-parse`, `run-analytics-report-network`, `run-analytics-report-rounds`, `planning-node-lib`) were run with `node --test` from `cli/`: 106 tests, 106 pass. The exact cluster computation in `run_time` was checked against `lib/run-analytics.jq` → `finalize`. That function's `idle_gaps` is the full list of over-threshold gaps and its `wall_ms` is `tmax - tmin`, so a member's interval minus its gaps is exactly its non-idle time, and the union method is exact as the `RUN TIME` header claims. jq 1.5 compatibility of the new jq was confirmed only by reading: no jq 1.5 binary was run.

## Nice to Have
1. **Header sentence re-wrapped past the block's width** — `cli/templates/scripts/lib/planning-node-lib.sh` (header) — "node-session manifest under `${log_path%.log}.planning/`. The shared flag vector — the binary, the"
   The amended carve-out sentence leaves this comment line much longer than its neighbours in the header block.
   **Fix:** Re-wrap the paragraph from "Every durable write is" to the column width the rest of the header uses.

2. **Header line in mode `rollup` left over-long** — `cli/templates/scripts/lib/run-analytics-report.jq` (header, mode `rollup`) — "and last session's when none parses); span_ms = last_at - first_at. input_tokens, output_tokens,"
   The edited `first_at` / `last_at` sentence was joined onto the following line without re-wrapping.
   **Fix:** Re-wrap that paragraph to the header's column width.
