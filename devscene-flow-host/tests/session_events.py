"""The rule this module exists to enforce: every fake `stream-json` event the suite builds carries
the fields a real 2.1.332 session's event carries — `init` its `type`, `subtype`, `tools` and
`session_id`; `result` its `type`, `subtype`, `is_error`, `result`, `session_id`,
`total_cost_usd`, `usage`, `modelUsage` and `permission_denials` — so a reader tested against them
reads a real session the same way.
"""

import json
from collections.abc import Mapping, Sequence


def init_event(tools: Sequence[str], session_id: str = "s-1") -> str:
    return json.dumps(
        {"type": "system", "subtype": "init", "tools": list(tools), "session_id": session_id}
    )


def result_event(
    text: str,
    *,
    subtype: str = "success",
    is_error: bool = False,
    total_cost_usd: float = 0.25,
    cache_creation_input_tokens: int = 1000,
    cache_read_input_tokens: int = 2000,
    model_usage: Mapping[str, object] | None = None,
    permission_denials: int = 0,
) -> str:
    return json.dumps(
        {
            "type": "result",
            "subtype": subtype,
            "is_error": is_error,
            "result": text,
            "session_id": "s-1",
            "total_cost_usd": total_cost_usd,
            "usage": {
                "cache_creation_input_tokens": cache_creation_input_tokens,
                "cache_read_input_tokens": cache_read_input_tokens,
            },
            "modelUsage": dict(model_usage) if model_usage is not None else {},
            "permission_denials": [
                {"tool_name": "Bash", "tool_use_id": f"t-{index}", "tool_input": {}}
                for index in range(permission_denials)
            ],
        }
    )


def return_block(document: Mapping[str, object], prose: str = "Done.") -> str:
    return f"{prose}\n\n```json\n{json.dumps(document)}\n```\n"
