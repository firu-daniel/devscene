"""The planning driver's node-session records: `NodeSessions`, the `UsageSink` and `LaunchSink` in
one class, writing each node's stream, the run stream, the `node-sessions.jsonl` manifest and the
formatted log, and pairing each usage record with its `Launch` row into the session table.

The rule:
- The numbering is the retired `pd_seq_init`'s (`cli/templates/scripts/lib/planning-driver-lib.sh`,
  read in its history before the bash driver's retirement): the first `seq` is one past the largest
  all-digit `<n>` of a `<n>-*.stream.jsonl` already in `${log%.log}.planning/`, else `1`, so a
  second drive never overwrites the first drive's files. `Launch.seq` is not used: the dispatch
  counter resets per drive.
- `record(usage)` is the retired `pnl_launch` / `pnl_reap` (`planning-node-lib.sh`, same history),
  in order: `usage.stream` to `<seq>-<node>.stream.jsonl`; the same bytes appended to
  `${log%.log}.stream.jsonl`; when `session_id` is set, one compact
  `{"session_id", "seq", "node"}` line appended to `MANIFEST_NAME`, `seq` a string; the formatter
  run as one argv word with the stream on stdin, its stdout appended to the log; a non-empty
  `stderr_tail` appended to the log. A formatter's exit status is ignored, as the bash pipeline
  ignored it, and a formatter that cannot be started is narrated, never raised. Any other
  `OSError` propagates. A usage whose `withheld_tools` is non-empty is then narrated as
  `WITHHELD_LINE`, the retired `pnl_reap`'s text; the session is never refused for it.
- `record(launch)` pairs the `Launch` with the oldest pending usage of `launch.node` whose
  `result` equals `launch.result`; failing that, a `Launch` whose result is `Failed("infra", …)`
  pairs with the oldest pending usage of that node whose result is a `Completed`, the one
  transformation `host/planning_executor.py` → `PlanningExecutor` makes after the usage was
  recorded. It then appends one row `<seq> <node> <agent>
  <attempt>/<max_attempts> <outcome, else the result kind> <duration>s <cost>`.
  A `Launch` with no such usage — a GraphScene total-run timeout, whose cancelled run reports
  none — is no fault: its row carries `-` for seq, duration and cost, and it is narrated.
- The per-session observations are the retired `pd_reap_one`'s: permission denials are
  `tooling-gap`; a `Failed("infra", …)` with attempts left is `flow-efficiency`; a final `Failed`
  — `agent`, or `infra` on the last attempt, which the walk records as error — is
  `silent-failure`. A `Failed("undelivered", …)` is the retired `pd_undelivered`'s
  `flow-efficiency` observation, one per undelivered `Launch`, narrated as an immediate
  re-dispatch or, with a backoff above 0, as backing off first; its consecutive-set count is
  `Launch.undelivered_strikes + 1`, and the strike that reaches the undelivered limit adds
  neither, since the set halts and `host/run_exits.py` records the self-pause.
- The last return document each node's usage carried is kept for `return_document(node)`, and the
  result of each node's last `Launch` for `launch_result(node)`. Each node's `Failed("infra", …)`
  launches are logged as `attempt <k> of <max> (#<seq>): <reason>`, as the retired `pd_reap_one`
  logged them; a launch that ends the node's attempts keeps the log for `exhausted_attempts(node)`
  when it was the last `infra` attempt and clears it otherwise, and an undelivered launch touches
  neither.

Deliberately not covered:
- What the run does with a `Failed`: GraphScene's `AttemptBook` and the driver's exits.
- Deciding an outcome or running a hook: this module writes and pairs only.
"""

import json
import re
import subprocess
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Final

from graphscene import Completed, Failed, Launch, NodeResult

from devscene_flow_host.host.claude_executor import SessionUsage
from devscene_flow_host.host.observations import Observations

PLANNING_DIRECTORY_SUFFIX: Final = ".planning"
MANIFEST_NAME: Final = "node-sessions.jsonl"
RUN_STREAM_SUFFIX: Final = ".stream.jsonl"
UNKNOWN: Final = "-"
WITHHELD_LINE: Final = (
    "#{seq} {node} ({agent}): the init event lacks declared tools [{tools}] "
    "(a lacking tool is never refused)"
)
_SEQ_PATTERN: Final = re.compile(r"([0-9]+)-.*\.stream\.jsonl")


def _log_stem(log_path: Path) -> str:
    return str(log_path).removesuffix(".log")


def planning_directory(log_path: Path) -> Path:
    return Path(_log_stem(log_path) + PLANNING_DIRECTORY_SUFFIX)


def run_stream_path(log_path: Path) -> Path:
    return Path(_log_stem(log_path) + RUN_STREAM_SUFFIX)


def _first_seq(directory: Path) -> int:
    seq = 1
    if not directory.is_dir():
        return seq
    for entry in directory.iterdir():
        match = _SEQ_PATTERN.fullmatch(entry.name)
        if match is not None:
            seq = max(seq, int(match.group(1)) + 1)
    return seq


def _append(path: Path, data: bytes) -> None:
    with path.open("ab") as handle:
        handle.write(data)


class NodeSessions:
    def __init__(
        self,
        *,
        log_path: Path,
        formatter: str,
        observations: Observations,
        narrate: Callable[[str], None],
        backoff_seconds: float,
        undelivered_limit: int,
    ) -> None:
        self._log_path = log_path
        self._formatter = formatter
        self._observations = observations
        self._narrate = narrate
        self._backoff_seconds = backoff_seconds
        self._undelivered_limit = undelivered_limit
        self._directory = planning_directory(log_path)
        self._next_seq = _first_seq(self._directory)
        self._pending: dict[str, list[tuple[int, SessionUsage]]] = {}
        self._returns: dict[str, Mapping[str, object]] = {}
        self._results: dict[str, NodeResult] = {}
        self._rows: list[str] = []
        self._attempt_log: dict[str, list[str]] = {}
        self._exhausted: dict[str, tuple[int, tuple[str, ...]]] = {}

    @property
    def rows(self) -> tuple[str, ...]:
        return tuple(self._rows)

    def return_document(self, node: str) -> Mapping[str, object] | None:
        return self._returns.get(node)

    def launch_result(self, node: str) -> NodeResult | None:
        return self._results.get(node)

    def exhausted_attempts(self, node: str) -> tuple[int, tuple[str, ...]] | None:
        return self._exhausted.get(node)

    def record(self, item: SessionUsage | Launch) -> None:
        if isinstance(item, Launch):
            self._record_launch(item)
        else:
            self._record_usage(item)

    def _record_usage(self, usage: SessionUsage) -> None:
        seq = self._next_seq
        self._next_seq += 1
        data = usage.stream.encode("utf-8")
        self._directory.mkdir(parents=True, exist_ok=True)
        (self._directory / f"{seq}-{usage.node}{RUN_STREAM_SUFFIX}").write_bytes(data)
        _append(run_stream_path(self._log_path), data)
        if usage.session_id:
            line = json.dumps(
                {"session_id": usage.session_id, "seq": str(seq), "node": usage.node},
                separators=(",", ":"),
                ensure_ascii=False,
            )
            _append(self._directory / MANIFEST_NAME, (line + "\n").encode("utf-8"))
        self._format(data)
        tail = usage.stderr_tail
        if tail:
            _append(self._log_path, (tail if tail.endswith("\n") else tail + "\n").encode("utf-8"))
        if usage.withheld_tools:
            self._narrate(
                WITHHELD_LINE.format(
                    seq=seq,
                    node=usage.node,
                    agent=usage.agent,
                    tools=", ".join(usage.withheld_tools),
                )
            )
        self._pending.setdefault(usage.node, []).append((seq, usage))
        if usage.return_document is not None:
            self._returns[usage.node] = usage.return_document

    def _format(self, data: bytes) -> None:
        with self._log_path.open("ab") as log:
            try:
                subprocess.run([self._formatter], input=data, stdout=log, check=False)
            except OSError as error:
                self._narrate(f"the formatter '{self._formatter}' could not run: {error}")

    def _pair(self, launch: Launch) -> tuple[int, SessionUsage] | None:
        pending = self._pending.get(launch.node, [])
        for index, (_, usage) in enumerate(pending):
            if usage.result == launch.result:
                return pending.pop(index)
        if isinstance(launch.result, Failed) and launch.result.failure == "infra":
            for index, (_, usage) in enumerate(pending):
                if isinstance(usage.result, Completed):
                    return pending.pop(index)
        return None

    def _record_launch(self, launch: Launch) -> None:
        paired = self._pair(launch)
        result = launch.result
        self._results[launch.node] = result
        shown = result.outcome if isinstance(result, Completed) else result.kind
        attempts = f"{launch.attempt}/{launch.max_attempts}"
        if paired is None:
            seq_text, duration, cost = UNKNOWN, UNKNOWN, UNKNOWN
            self._narrate(f"no usage record for {launch.node} (total-run timeout)")
        else:
            seq, usage = paired
            seq_text = str(seq)
            duration = f"{round(usage.duration_seconds)}s"
            cost = UNKNOWN if usage.total_cost_usd is None else str(usage.total_cost_usd)
        self._track_attempts(launch, seq_text)
        self._rows.append(
            f"{seq_text} {launch.node} {launch.agent} {attempts} {shown} {duration} {cost}"
        )
        self._observe(launch, seq_text, paired)

    def _track_attempts(self, launch: Launch, seq_text: str) -> None:
        result = launch.result
        if isinstance(result, Failed) and result.failure == "undelivered":
            return
        log = self._attempt_log.setdefault(launch.node, [])
        if isinstance(result, Failed) and result.failure == "infra":
            log.append(
                f"attempt {launch.attempt} of {launch.max_attempts} (#{seq_text}): {result.reason}"
            )
            if launch.attempt < launch.max_attempts:
                return
            self._exhausted[launch.node] = (launch.max_attempts, tuple(log))
        else:
            self._exhausted.pop(launch.node, None)
        self._attempt_log[launch.node] = []

    def _observe(
        self, launch: Launch, seq_text: str, paired: tuple[int, SessionUsage] | None
    ) -> None:
        who = f"#{seq_text} {launch.node} ({launch.agent})"
        denials = 0 if paired is None else paired[1].permission_denials
        if denials > 0:
            self._observations.add(
                "tooling-gap",
                "A planning node session met permission denials",
                f"{who}: {denials} denial(s)",
                f"{denials} refused tool call(s)",
            )
        result = launch.result
        if not isinstance(result, Failed):
            return
        if result.failure == "undelivered":
            count = launch.undelivered_strikes + 1
            if count >= self._undelivered_limit:
                return
            self._observations.add(
                "flow-efficiency",
                "An undelivered planning dispatch was re-dispatched",
                f"nodes: {launch.node}; consecutive undelivered sets: {count}; "
                f"reason: {result.reason}",
                "one re-dispatch per node",
            )
            if self._backoff_seconds > 0:
                self._narrate(
                    f"undelivered: backing off {self._backoff_seconds:g}s "
                    f"before re-dispatching {launch.node}"
                )
            else:
                self._narrate(f"undelivered: re-dispatching {launch.node} at once")
            return
        attempts = f"attempt {launch.attempt} of {launch.max_attempts}"
        if result.failure == "infra" and launch.attempt < launch.max_attempts:
            self._observations.add(
                "flow-efficiency",
                "A planning node session failed for an infrastructure reason and was re-dispatched",
                f"{who}: {attempts}: {result.reason}",
                f"one re-dispatch of {launch.node}",
            )
            return
        self._observations.add(
            "silent-failure",
            "A planning node session ended in error",
            f"{who}: {result.reason or 'no reason'}",
            "one dispatch recorded as error",
        )
