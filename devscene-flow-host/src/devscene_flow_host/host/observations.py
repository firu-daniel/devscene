"""The planning driver's improvement observations: collected during a drive, flushed into
`<state_dir>/improvement_observations/<branch>.md` with every machine path rewritten, and committed
as the `observations` artifact.

The rule:
- `Observations.add` is `prl_observe` (`cli/templates/scripts/lib/planning-record-lib.sh`, read in
  its history before the bash driver's retirement): the category must be one of `CATEGORIES`, each
  text is flattened to one line (`\\r` and `\\n` become spaces), an empty problem is refused, and
  the block `## <problem>` / `- **category:**` / `- **evidence:**` / `- **cost this run:**` is held
  in memory.
- `Observations.flush` is `prl_observe_flush`: best-effort, every failure one `observations: `
  log line and never an exception. With no blocks it does nothing. The existing file is kept up
  to its last non-blank line, less that line when it is exactly `CLOSING_LABEL`, less trailing
  blank lines, then a blank line; then `# Script-driven planning — <UTC ts>`, a blank line, the
  blocks and `CLOSING_LABEL`. The file is replaced atomically with mode `0o644`.
- The machine-path rewrite is `PRL_REWRITE_AWK` over the needles `prl_needle` admits: the
  worktree, the main checkout (dropped when it equals the worktree) and the home directory, each
  less one trailing `/`; a needle that is empty, `/`, one path segment or carries `'` is dropped
  with a log line. The longer needle is rewritten first, line by line, and a match counts only
  where the line ends or the needle is followed by `/` or a `_DELIMITERS` character. The worktree
  becomes its repo-relative remainder or `.`; the main checkout that remainder and
  `MAIN_CHECKOUT_SUFFIX`; the home directory `~`.
- When a needle still occurs after the rewrite, or the commit raises, the previous file is
  restored — removed when there was none — and nothing is committed.

Deliberately not covered:
- Which events are observed: the driver's, which calls `Observations.add`.
- Pushing: the wrapper's `--push`, which `commit_artifact` passes.
"""

import contextlib
import os
import tempfile
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Final, Literal

from devscene_flow_host.host.commit_points import CommitPointError, commit_artifact

CATEGORIES: Final = (
    "tooling-gap",
    "silent-failure",
    "flow-efficiency",
    "optimization",
    "agent-contract",
    "shared-state",
    "convention",
)
CLOSING_LABEL: Final = "# Task run (Phase D)"
OBSERVATIONS_DIRECTORY: Final = "improvement_observations"
OBSERVATIONS_ARTIFACT: Final = "observations"
SECTION_HEADING: Final = "# Script-driven planning — "
MAIN_CHECKOUT_SUFFIX: Final = " (main checkout)"
HOME_REPLACEMENT: Final = "~"
_TIMESTAMP_FORMAT: Final = "%Y-%m-%dT%H:%M:%SZ"
_DELIMITERS: Final = "` \t'\"),;]>"
_BLANK_CHARACTERS: Final = " \t\r"
_FILE_MODE: Final = 0o644

NeedleKind = Literal["worktree", "main", "home"]


@dataclass(frozen=True)
class Needle:
    path: str
    kind: NeedleKind


def observations_path(repo_root: Path, state_dir: str, branch: str) -> Path:
    return repo_root / state_dir / OBSERVATIONS_DIRECTORY / f"{branch}.md"


def _one_line(text: str) -> str:
    return text.replace("\r", " ").replace("\n", " ")


class Observations:
    def __init__(self) -> None:
        self._blocks: list[str] = []

    def add(self, category: str, problem: str, evidence: str, cost: str) -> None:
        if category not in CATEGORIES:
            raise ValueError(f"'{category}' is not an observation category")
        problem = _one_line(problem)
        if not problem:
            raise ValueError("an observation needs a problem statement")
        self._blocks.append(
            f"## {problem}\n"
            f"- **category:** {category}\n"
            f"- **evidence:** {_one_line(evidence)}\n"
            f"- **cost this run:** {_one_line(cost)}\n\n"
        )

    async def flush(
        self,
        *,
        repo_root: Path,
        main_repo: Path,
        state_dir: str,
        branch: str,
        wrapper: Path,
        home: str | None,
        now: datetime,
        log: Callable[[str], None],
    ) -> None:
        if not self._blocks:
            return
        blocks = "".join(self._blocks)
        self._blocks.clear()
        rel = f"{state_dir}/{OBSERVATIONS_DIRECTORY}/{branch}.md"
        try:
            await _flush(
                blocks,
                path=observations_path(repo_root, state_dir, branch),
                rel=rel,
                repo_root=repo_root,
                main_repo=main_repo,
                wrapper=wrapper,
                home=home,
                now=now,
                log=log,
            )
        except Exception as error:
            log(f"observations: '{rel}' not flushed: {type(error).__name__}: {error}")


async def _flush(
    blocks: str,
    *,
    path: Path,
    rel: str,
    repo_root: Path,
    main_repo: Path,
    wrapper: Path,
    home: str | None,
    now: datetime,
    log: Callable[[str], None],
) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
    except OSError:
        log(f"observations: cannot write in '{Path(rel).parent.as_posix()}'; not flushed")
        return
    previous: bytes | None
    try:
        previous = path.read_bytes()
    except FileNotFoundError:
        previous = None
    except OSError:
        log(f"observations: cannot back up '{rel}'; not flushed")
        return
    stamp = (now.astimezone(UTC) if now.tzinfo is not None else now).strftime(_TIMESTAMP_FORMAT)
    kept = "" if previous is None else _kept(previous.decode("utf-8", errors="surrogateescape"))
    text = f"{kept}{SECTION_HEADING}{stamp}\n\n{blocks}{CLOSING_LABEL}\n"
    needles = machine_needles(worktree=str(repo_root), main_repo=str(main_repo), home=home, log=log)
    rewritten = rewrite_machine_paths(text, needles)
    try:
        _replace(path, rewritten.encode("utf-8", errors="surrogateescape"))
    except OSError:
        log(f"observations: cannot write '{rel}'; not flushed")
        return
    if any(needle.path in rewritten for needle in needles):
        log(f"observations: '{rel}' still carries a machine path after the rewrite; not committed")
        _restore(path, previous, rel, log)
        return
    try:
        await commit_artifact(wrapper, repo_root, OBSERVATIONS_ARTIFACT)
    except (CommitPointError, OSError) as error:
        log(f"observations: the commit of '{rel}' failed: {error}")
        _restore(path, previous, rel, log)


def _is_blank(line: str) -> bool:
    return not line.strip(_BLANK_CHARACTERS)


def _kept(text: str) -> str:
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    last = len(lines)
    while last > 0 and _is_blank(lines[last - 1]):
        last -= 1
    if last > 0 and lines[last - 1] == CLOSING_LABEL:
        last -= 1
    while last > 0 and _is_blank(lines[last - 1]):
        last -= 1
    if last == 0:
        return ""
    return "".join(line + "\n" for line in lines[:last]) + "\n"


def _replace(path: Path, data: bytes) -> None:
    descriptor, temporary = tempfile.mkstemp(dir=path.parent, prefix=".observations.")
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
        os.chmod(temporary, _FILE_MODE)
        os.replace(temporary, path)
    except BaseException:
        with contextlib.suppress(FileNotFoundError):
            os.unlink(temporary)
        raise


def _restore(path: Path, previous: bytes | None, rel: str, log: Callable[[str], None]) -> None:
    try:
        if previous is None:
            path.unlink(missing_ok=True)
        else:
            _replace(path, previous)
    except OSError:
        log(f"observations: cannot restore '{rel}'")


def _needle(source: str, path: str, log: Callable[[str], None]) -> str | None:
    path = path.removesuffix("/")
    if not path or "'" in path:
        log(f"observations: the {source} needle is empty or quoted; dropped")
        return None
    rest = path.removeprefix("/")
    if "/" not in rest:
        log(f"observations: the {source} needle '{path}' is one path segment; dropped")
        return None
    return path


def machine_needles(
    *, worktree: str, main_repo: str, home: str | None, log: Callable[[str], None]
) -> tuple[Needle, ...]:
    found: list[Needle] = []
    worktree_needle = _needle("worktree", worktree, log)
    if worktree_needle is not None:
        found.append(Needle(worktree_needle, "worktree"))
    main_needle = _needle("main checkout", main_repo, log)
    if main_needle is not None and main_needle != worktree_needle:
        found.append(Needle(main_needle, "main"))
    home_needle = _needle("home", home or "", log)
    if home_needle is not None:
        found.append(Needle(home_needle, "home"))
    return tuple(sorted(found, key=lambda needle: -len(needle.path)))


def _is_delimiter(character: str) -> bool:
    return character == "" or character in _DELIMITERS


def _rewrite_line(line: str, needle: Needle) -> str:
    out: list[str] = []
    while (position := line.find(needle.path)) >= 0:
        out.append(line[:position])
        rest = line[position + len(needle.path) :]
        follower = rest[:1]
        if follower != "/" and not _is_delimiter(follower):
            out.append(needle.path)
            line = rest
            continue
        if needle.kind == "home":
            out.append(HOME_REPLACEMENT)
            line = rest
            continue
        if follower == "/":
            rest = rest[1:]
        end = next(
            (index for index, character in enumerate(rest) if _is_delimiter(character)),
            len(rest),
        )
        out.append(rest[:end] or ".")
        if needle.kind == "main":
            out.append(MAIN_CHECKOUT_SUFFIX)
        line = rest[end:]
    return "".join(out) + line


def rewrite_machine_paths(text: str, needles: Sequence[Needle]) -> str:
    lines = text.split("\n")
    for needle in needles:
        lines = [_rewrite_line(line, needle) for line in lines]
    return "\n".join(lines)
