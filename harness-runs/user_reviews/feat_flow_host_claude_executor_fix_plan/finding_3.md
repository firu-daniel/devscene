### 3. Docstrings and the README defer work to issue numbers instead of describing it

**File:** `devscene-flow-host/src/devscene_flow_host/host/claude_executor.py` (module docstring, *"Deliberately not covered:"*) — "into a run loop (#484)." and "a session manifest: the host's (#484)."; `devscene-flow-host/src/devscene_flow_host/host/session_process.py` (module docstring, *"Deliberately not covered:"*) — "the run loop's (#484)"; `devscene-flow-host/README.md` (`## What it is`) — "until the run loop (#484) and the planning cutover (#424) land"; `devscene-flow-host/README.md` (`## The executor`, **The usage sink.**) — "Building that pairing into a run loop is #484."

**Problem.** This branch added five references that defer work to an issue number. Runs cannot open issues, so the number tells a reader nothing. The references are also wrong. The "run loop" they name is already merged: it is GraphScene's provider-neutral run mode (`graphscene/src/graphscene/engine/run_loop.py`), merged before this branch as `feat: graphscene run mode (#490)`. It cannot build the usage-to-`Launch` pairing or write a `claude` stream. Both belong to the flow host's script-driven planning driver, which is the branch that moves planning onto GraphScene and is not yet merged.

These five are every issue number this branch's diff adds under `devscene-flow-host/`. The `#419` and `#472` references elsewhere in the README and in `host/round_gates.py` predate this branch, so leave them alone.

**Fix.** Describe each piece of work by what it does, with no issue number. Where a merged piece of work needs naming, use its merge-commit title from `git log --oneline` (for example `feat: graphscene run mode (#490)`).

- `claude_executor.py`, *"Deliberately not covered:"*:
  - `- Building the usage-to-`Launch` pairing into a run loop (#484).` becomes:

    ```
    - Building the usage-to-`Launch` pairing: the flow host's script-driven planning driver's,
      not yet merged. GraphScene's run mode (`graphscene/src/graphscene/engine/run_loop.py`)
      cannot build it.
    ```

  - `- Writing the stream (from `SessionUsage.stream`) or a session manifest: the host's (#484).` becomes:

    ```
    - Writing the stream (from `SessionUsage.stream`) or a session manifest: the flow host's
      script-driven planning driver's, not yet merged.
    ```

- `session_process.py`, *"Deliberately not covered:"*: `- Writing the stream anywhere: the run loop's (#484), which receives it through `ClaudeExecutor`'s `SessionUsage.stream`.` becomes:

  ```
  - Writing the stream anywhere: the flow host's script-driven planning driver's, not yet merged,
    which receives it through `ClaudeExecutor`'s `SessionUsage.stream`.
  ```

- `README.md` → `## What it is`: replace `Nothing in production calls the executor until the run loop (#484) and the planning cutover (#424) land (`## The executor`).` with:

  ```
  Nothing in production calls the executor yet: the flow host's script-driven planning driver, which moves planning onto GraphScene's run mode (`graphscene/src/graphscene/engine/run_loop.py`), is not yet merged (`## The executor`).
  ```

- `README.md` → `## The executor` → **The usage sink.**: replace `Building that pairing into a run loop is #484.` with:

  ```
  Building that pairing belongs to the flow host's script-driven planning driver, not yet merged; GraphScene's run mode (`graphscene/src/graphscene/engine/run_loop.py`) cannot build it.
  ```

  In the same paragraph's next sentence, which begins "Writing the stream, and reading a return's fields other than", change "are the host's, from this record" to "are that driver's, from this record".

Findings 1, 2 and 4 add prose to the same files. None of it names an issue or PR number.
