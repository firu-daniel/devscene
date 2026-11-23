"""The rule this module exists to enforce: this suite turns a PEP 508 requirement string into a
dependency name in one place, so the boundary test and the lock test always normalise a name the
same way (lower-cased, `-` as `_`).
"""

import re

_REQUIREMENT_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")


def dependency_name(requirement: str) -> str:
    match = _REQUIREMENT_NAME.match(requirement.strip())
    if match is None:
        raise ValueError(f"unparseable dependency: {requirement!r}")
    return match.group(0).lower().replace("-", "_")
