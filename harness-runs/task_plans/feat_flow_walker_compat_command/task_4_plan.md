### Task 4 — Parse `flow-walker.sh`'s verbs and flags in `commands/arguments.py`

**Goal:** Read a command line exactly as `flow-walker.sh` → `# --- Arguments` does — the four verbs, each verb's flags, the value checks and the same refusal texts — so a caller that switches to the command at #419 is refused for the same input with the same words. One flag is added: `--flows <dir>`, which the launcher supplies because bash finds its graph beside itself (`<this script's dir>/flows/`) and the Python command cannot.

**Where this layer stops.** This module parses and refuses usage only; it reads no file, resolves no path and loads no graph. **Task 5** turns a `UsageError` into exit `1` with one `flow-walker: <message>` line and resolves `flows` and `findings` against the repository root.

**The contract this task produces:**

- `devscene_flow_host.commands.arguments.parse(argv: Sequence[str]) -> Invocation`, raising `UsageError(message)` (an `Exception` subclass carrying the bash text, without the `flow-walker: ` prefix).
- `Invocation`, a frozen dataclass: `command: Literal["start", "next", "current", "check-round-file"]`, `flow`, `branch`, `entry`, `skipped`, `outcome`, `findings`, `node`, `flows`, each `str | None` and `None` when its flag was not given.

**The grammar** (`cli/templates/scripts/flow-walker.sh` → the header's `USAGE` and `# --- Arguments`), with `--flows` added to the three walk verbs:

| Verb | Flags |
|---|---|
| `start` | `--flow`, `--branch`, `--flows`, `--entry`, `--skipped` |
| `next` | `--flow`, `--branch`, `--flows`, `--outcome`, `--node`, `--findings`, `--skipped` |
| `current` | `--flow`, `--branch`, `--flows` |
| `check-round-file` | `--findings` only |

Refusals, each the exact text, checked in bash's order: `missing subcommand: start, next, current or check-round-file`; `unknown subcommand '<cmd>': expected start, next, current or check-round-file`; `'<flag>' is not a flag of '<cmd>'`; `<flag> requires a value`; `the value of <flag> carries a newline`; `the value of --findings carries a tab`; `'<value>' is not a node name` (`--node` outside `[a-z0-9_]`, or empty); then for `check-round-file` `missing required flag --findings`; otherwise `missing required flag --flow`, `missing required flag --branch`, `missing required flag --flows`, and for `next` `missing required flag --outcome`, `outcome '<o>' is not an outcome name` (outside `[A-Za-z0-9_]`), `outcome FAIL requires --findings with the reviewer's findings_file`; last `unknown flow '<flow>'` for a flow outside `[a-z0-9_]`. A repeated flag keeps its last value, as bash's loop does.

### Targets

- `devscene-flow-host/src/devscene_flow_host/commands/arguments.py` (new)
- `devscene-flow-host/tests/test_arguments.py` (new)

**Work:**

- [ ] `commands/arguments.py`: `UsageError`, `Invocation` and `parse` as the contract states — a hand-written loop over the flag table, not `argparse`, because bash's per-verb flag table and its exact refusal texts and order are the contract and `argparse` writes its own. The flag table is one module-level `Final` mapping from verb to its flags, read by the loop and nowhere restated.
- [ ] Its docstring: *"The rule:"* — reads as `flow-walker.sh` → `# --- Arguments`, naming the one added flag and why — and *"Deliberately not covered"*: resolving a path, the repository root and the exit status (Task 5's `commands/flow_walker.py`).
- [ ] `tests/test_arguments.py`: one case per refusal above asserting its exact text; one parsed `Invocation` per verb; `--flows` refused on `check-round-file` and `--skipped` on `current`; `--findings` with a tab refused while a `--flow` value with a tab is not (bash refuses a tab in `--findings` only); a repeated flag's last value kept. Literals written from `flow-walker.sh`'s argument section; the module docstring opens *"The rule this file exists to enforce"*.

**Verification:**

- `bash scripts/python-service.sh --package devscene-flow-host test tests/test_arguments.py` passes, run as one foreground command from the repository root.
- Every refusal string in `commands/arguments.py` appears verbatim in `cli/templates/scripts/flow-walker.sh`'s argument section, except the one naming `--flows`.
