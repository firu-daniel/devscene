### Task 7 — Add `FileStateStore`, a locked, atomically replaced state file, in `adapters/state_file.py`

**Goal:** Give the walker its first `StateStore`: a file at a path the caller names, behind an exclusive lock, with its locking behaviour defined. The lock holds across processes and threads, is bounded, and is released on every exit path. A write replaces the file atomically, so a lock-free `read` is never torn. Concurrent `next` calls for the gates of one set then see each other's records, and exactly one of them joins.

**Depends on:** Task 6, whose `state_to_json(state: WalkState) -> str` and `state_from_json(text: str) -> WalkState` this task calls. `state_from_json` raises `ValueError(f"{path}: {reason}")` for a malformed document. It also depends on Task 2's `StateStore` Protocol, which this class satisfies:

- `read(self) -> WalkState | None`;
- `write(self, state: WalkState) -> None`;
- `lock(self) -> contextlib.AbstractContextManager[None]`.

**Where this layer stops.** Holding the lock around a read-step-write is the **engine's** `Walker` (Task 5). This store only provides the lock. Making `FileStateStore` public, and proving exactly one join under concurrent gate calls end to end, is **Task 8's**. The store knows nothing of flows or graphs.

### Targets

- `graphscene/src/graphscene/adapters/state_file.py` (new)
- `graphscene/src/graphscene/adapters/__init__.py`: the docstring's first paragraph only, adding "and the file a walk's state is kept in" to what the layer touches. *"The rule:"* is unchanged.
- `graphscene/tests/adapters/test_state_file.py` (new)

**Work:**

- [ ] **Docstring and construction.** The module docstring has a *"The rule:"* paragraph:
  - the store writes only the state file and its sibling lock file `<name>.lock`;
  - `write` goes through a temporary file in the same directory and `os.replace`;
  - `lock` is `fcntl.flock(LOCK_EX | LOCK_NB)` on the lock file, polled every 0.1 s until `lock_timeout` seconds have passed, then `TimeoutError` naming the lock file;
  - the lock is released and its descriptor closed in a `finally`.

  Add a *"Deliberately not covered:"* list: platforms without `fcntl`, and a lock file left behind, which is harmless because `flock` dies with its process. Then `FileStateStore(path: pathlib.Path, *, lock_timeout: float = 120.0)`.
- [ ] **`read`.** Return `None` when the file does not exist. Otherwise return `state_from_json(text)`, re-raising its `ValueError` as `ValueError(f"{path}: {error}")` so the message names the file. Any other `OSError` propagates unchanged, as `graphscene/src/graphscene/adapters/json_file.py` → *"The rule:"* lets one.
- [ ] **`write` and `lock`.**
  - `write` creates the parent directory when it is missing, writes UTF-8 to a `tempfile.NamedTemporaryFile(dir=path.parent, delete=False)`, flushes and `fsync`s it, `os.replace`s it onto `path`, and removes the temporary file if any step before the replace fails.
  - `lock` is a `contextlib.contextmanager` that opens `<path>.lock` anew on every call (a separate open file description, so threads exclude each other as processes do).
  - **Deviations from plan:** `lock` also creates the parent directory when it is missing, as `write` does. The `Walker` takes the lock before the first `write`, so without this a store whose directory does not exist yet would fail with `FileNotFoundError` on its first `start`.
  - **Deviations from plan:** `read` decodes UTF-8 inside the same `try` as `state_from_json`. A `UnicodeDecodeError` is a `ValueError`, so a file that is not UTF-8 gets the same `<path>: <reason>` wrapping instead of escaping without the file's path.
- [ ] **`test_state_file.py`.** Its module docstring opens *"The rule this file exists to enforce"*. Everything is under `tmp_path`, never inside the checkout. Cover these:
  - `read` of an absent file is `None`;
  - a `write` then `read` round trip;
  - a malformed file raises `ValueError` whose text starts with the file's path;
  - a failed write leaves the previous file byte-identical and no temporary file behind (make the directory read-only after the first write, then restore it);
  - a second `lock()` taken from another thread while the first is held, with `lock_timeout=0.3`, raises `TimeoutError` naming `<path>.lock`, and succeeds once the first is released;
  - the lock is released when the body raises.

**Verification:**

- [ ] `bash scripts/python-service.sh --package graphscene test tests/adapters/test_state_file.py` passes.
- [ ] `state_file.py` imports `graphscene.adapters.walk_json`, `graphscene.model` and the standard library only, never `graphscene.engine` (`graphscene-layers`).
