"""The rule this module exists to enforce: the suite's reviewer files and git repositories are
planted under the test's `tmp_path` only, and `git` runs isolated from the machine's
configuration (`GIT_CONFIG_GLOBAL` at `os.devnull`, `GIT_CONFIG_NOSYSTEM=1`, a fixed identity and
no signing).
"""

import os
import subprocess
from collections.abc import Sequence
from pathlib import Path
from typing import Final

PASS_BODY: Final = "verdict: PASS\n"
FAIL_BODY: Final = "verdict: FAIL\n## Must Fix\n1. **f**\n   **Class:** c\n   **Failure:** x\n"


def plant_review(folder: Path, n: int, body: str) -> Path:
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"review_{n}.md"
    path.write_text(body, encoding="utf-8")
    return path


def git(root: Path, *args: str) -> str:
    env = {**os.environ, "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1"}
    result = subprocess.run(
        [
            "git",
            "-C",
            str(root),
            "-c",
            "user.name=r",
            "-c",
            "user.email=r@r",
            "-c",
            "commit.gpgsign=false",
            *args,
        ],
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def init_repo(root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)
    git(root, "init", "-q")


def commit(root: Path, paths: Sequence[Path], message: str) -> None:
    git(root, "add", "--", *(str(path) for path in paths))
    git(root, "commit", "-q", "-m", message)
