### Task 5 — Add the `devscene-flow-walker` command in `commands/flow_walker.py` with its exit codes

**Goal:** The command itself: locate and load the graph, open the branch's walk, call the host's three entry points, render the step, and map every outcome to `flow-walker.sh`'s exit codes 0–3 with one `flow-walker: <cause>` line on stderr — declared as the console script `devscene-flow-walker` and runnable as `python -m devscene_flow_host.commands.flow_walker`.

**Depends on:** Task 4, Task 3, Task 2 and Task 1, whose contracts this task calls as stated here:

- Task 4: `commands/arguments.py` → `parse(argv) -> Invocation` (fields `command`, `flow`, `branch`, `entry`, `skipped`, `outcome`, `findings`, `node`, `flows`, each `None` when not given), raising `UsageError(message)` with bash's text and no prefix.
- Task 3: `commands/render.py` → `render(step: HostStep, *, graph, repo_root, state_dir, branch) -> str`, the whole stdout for a non-`Refused` step, raising `ValueError` for bash's exit-2 rendering faults.
- Task 2: `host/predicates.py` → `HarnessPredicateHost.last_refusal: str | None`, the reason of the last predicate the host could not answer.
- Task 1: `HostStep.revision_findings` is filled by `record_outcome`, `start_walk` and `current_step`; nothing here touches it.

**What it calls, and never bypasses.** `start` → `host/walking.py` → `open_walker(repo_root, branch, graph, skipped=…)` then `host/re_entry.py` → `start_walk(walker, repo_root, branch, entry)`; `next` → `host/round_gates.py` → `record_outcome(walker, repo_root, branch, outcome, node=…, findings=…)`; `current` → `host/re_entry.py` → `current_step(walker, repo_root, branch)`; `check-round-file` → `records/round_files.py` → `round_file_problem(round_file_path(repo_root, findings))`. It never calls `Walker.start`, `Walker.next` or `Walker.current` directly: that would skip the round-file check, the refusal count and the `refused:` lines.

**The exit contract** (`cli/templates/scripts/flow-walker.sh` → the header's `EXIT CODES`; the departures are listed by Task 7):

| Exit | When | stderr |
|---|---|---|
| `0` | an action was rendered and written to stdout; `check-round-file` found the file valid (no output) | nothing |
| `1` | a `UsageError`; a `Refused` step; no saved walk at `next` / `current`; `--flows/<flow>.v4.graph.json` absent | `flow-walker: <bash text>`; for a `Refused`, `walker.host.last_refusal` when it is not `None`, else `Refused.reason`; for no saved walk, `no walk in progress at <walk_state_path(repo_root, state_dir, branch)>: run 'start' first`; for the graph, `unknown flow '<flow>': no <graph file>` |
| `2` | not inside a git repository; a `RecordError`; a `GraphError` loading the graph; a graph whose `flow` is not `--flow`; any `OSError`, `ValueError` (a malformed walk, refusal or findings record, a round gate with no `findingsFolder`, a rendering fault) or `TimeoutError` (either lock); any other exception | `flow-walker: not inside a git repository`; `flow-walker: cannot load <file>: <first violation>`; `flow-walker: graph <file> declares flow '<x>', not '<flow>'`; otherwise the error's message; for an unanticipated type `flow-walker: internal error: <TypeName>: <message>` |
| `3` | `check-round-file`: the file is invalid or absent | `flow-walker: <--findings as given>: <reason>` |

Every non-zero exit writes **exactly one line** to stderr (a message carrying a newline is flattened to one line) and **nothing** to stdout, and leaves the saved walk as it was. **No exception escapes `main`**: Python's own exit status for an uncaught exception is `1`, which the orchestrator reads as *"no saved walk"* (`plugin/instructions/task_plan_writing_instructions_core.md` → the paragraph after **Continuing a saved walk.**).

### Targets

- `devscene-flow-host/src/devscene_flow_host/commands/flow_walker.py` (new)
- `devscene-flow-host/pyproject.toml` — `[project.scripts]`
- `devscene-flow-host/tests/test_flow_walker.py` (new)

**Work:**

- [ ] `commands/flow_walker.py`: `main(argv: Sequence[str] | None = None, *, stdout: TextIO | None = None, stderr: TextIO | None = None, cwd: Path | None = None) -> int` — defaults `sys.argv[1:]`, `sys.stdout`, `sys.stderr` and the process's working directory — and `if __name__ == "__main__": raise SystemExit(main())`. Order, as bash's: parse; the repository root from a bare `git rev-parse --show-toplevel` run with a fixed argument vector in `cwd` (`subprocess.run`, no shell); `check-round-file` answers here and reads no configuration or graph; otherwise `read_config(repo_root).state_dir`, the graph at `<flows>/<flow>.v4.graph.json` (`--flows` relative resolves under the root) through `graphscene.load_graph_file`, its `flow` checked against `--flow`; for `next` and `current`, `walk_store(repo_root, state_dir, branch).read() is None` refuses as no saved walk before the host is called; then the verb, `render`, and stdout.
- [ ] The failure mapping in one function, `failure(error: BaseException) -> tuple[int, str]`, used by the one `except Exception` clause `main` wraps around the run (never `except BaseException`, so `KeyboardInterrupt` and `SystemExit` pass through): `RecordError` → 2; `GraphError` → 2 with its first violation (checked **before** `ValueError`, which it subclasses); `TimeoutError` → 2 (checked before `OSError`, which it subclasses); `OSError`, `ValueError` → 2; anything else → 2 as `internal error: <TypeName>: <message>`. `UsageError` and a `Refused` are not failures and never reach it: they are exit-1 refusals `main` writes itself.
- [ ] `devscene-flow-host/pyproject.toml`: add `[project.scripts]` with `devscene-flow-walker = "devscene_flow_host.commands.flow_walker:main"`, as `graphscene/pyproject.toml` declares `graphscene`. Nothing else in the manifest changes; `uv.lock` records no entry point, so no re-lock is owed, and if it ever must move it moves only through `bash scripts/python-service.sh --package devscene-flow-host lock`.
- [ ] The module docstring: what it owns, *"The rule:"* — the exit table above, the order of the checks, and that the host's three entry points are the only route to the walk — and *"Deliberately not covered"*: the launch route and `uv` (#419's), the bash walker's own flat state file, and comparing the two walkers (`devscene-flow-host/README.md` → the differences section Task 7 writes).
- [ ] `tests/test_flow_walker.py`: drive `main` with `io.StringIO` streams and `cwd` pointed at a git repository planted under `tmp_path` (`round_fixtures.init_repo`, `plant_review`, a planted `devscene.config.json`, git's environment isolated as `tests/test_re_entry.py` → `_isolated_git` does), with `--flows` naming the checkout's own `cli/templates/scripts/flows` directory read-only — never a fixture inside the checkout. Cases: the `flow-walker.sh` `REPRO` walk end to end (`start` → `plan_writer` initial; `returned` → the three-gate set; the three gates' `PASS` → two `wait`s then `round: 0 PASS`, `ledger: P1` and `ui_writer`; on to `<terminal_handoff>` with its `report:` lines); a `FAIL` round's revision with its `arg.findings_file:` lines; `ui_review`'s `FAIL` reaching `ui_writer`'s revision with `arg.findings_file: <that file>` (the gap Task 1 closes, end to end); `current` re-printing the pending action; `next` and `current` with no saved walk → exit 1 and the exact text naming `<stateDir>/.flow_walker_state/<branch>.json`; a run-mode refusal → exit 1 with the host's text; `check-round-file` → 0 with no output, and 3 with `flow-walker: bad.md: Must Fix entry 1 lacks **Class:**`; an unknown flow → 1; a directory outside any git repository → 2; a malformed saved walk → 2 with the file byte-identical afterwards; `failure` for a constructed `TimeoutError`, `RecordError` and `KeyError`; the console script declared in `devscene-flow-host/pyproject.toml` (one fixed file, read with `tomllib`); and one subprocess run of `sys.executable -m devscene_flow_host.commands.flow_walker` writing to the real stdout. Literals from `flow-walker.sh`'s `REPRO` and `EXIT CODES`; module docstring opens *"The rule this file exists to enforce"*. No case reads a tree of files, so this suite owes no `treeGuards` entry.

**Verification:**

- `bash scripts/python-service.sh --package devscene-flow-host test tests/test_flow_walker.py` passes, run as one foreground command from the repository root.
- The `REPRO` walk's outputs line up with `cli/templates/scripts/flow-walker.sh`'s header `REPRO` block, line by line, wherever that block states one.
- `git grep -n -e 'Walker(' -e '\.start(' -e '\.next(' -e '\.current(' -- devscene-flow-host/src/devscene_flow_host/commands/` returns no hit that constructs a `Walker` or calls one of its methods: every walk goes through `open_walker`, `start_walk`, `record_outcome` or `current_step`.

**Deviations from plan:**

- `main` carries a second `except` clause, ahead of the one `except Exception`: it catches the module's private `_Exit`, the exit `main` itself decided on (a `UsageError`, a `Refused`, no saved walk, an unknown flow, not inside a repository, a graph load fault, a foreign `flow`, an invalid round file), so those refusals are written by `main` and never reach `failure`, as the plan requires. Every other exception still reaches `failure` through the one `except Exception`.
- The graph-load `GraphError` is caught where the graph is loaded, so its cause can name the file (`cannot load <file>: <first violation>`); the first violation is still taken through `failure`.
- The module docstring's *"Deliberately not covered"* adds one item the plan did not list: a rendering fault after `start` or `next` has saved the walk leaves the walk saved, where bash renders before writing. The exit-2 line and empty stdout still hold.
