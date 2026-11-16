### Task 6 — Document the attribution switch, the ref write-deny and the narrowed raw commit in the docs of record

**Goal:** Bring the three documents of record that describe the unattended profile, the per-run copy and the residuals into line with what Tasks 1, 2 and 3 shipped, so that no document still says a sandboxed commit in a clone lands, or that a run copy has six protected `.git` paths. This is the catch-all task, so its implementer reads every configured layer's conventions document.

**Depends on:**

- **Task 1.** The profile gains `"attribution": {"commit": "", "pr": ""}` (the object form, because of the v2.1.281 floor), loses `Bash(git commit:*)` from `allow`, and gains `Bash(git commit --amend:*)` in `deny`.
- **Task 2.** `COPY_GIT_PATHS` and `RUN_PROFILE_COPY_GIT_PATHS` gain `.git/HEAD` (`file`), `.git/refs/heads` (`directory`) and `.git/packed-refs` (`file`), each with `bubblewrapDenyWrite: true`. That makes nine rows, and the bubblewrap `omit` trio is unchanged.
- **Task 3.** `hr_copy_sync_in_var`'s diverged refusal names the cause and the two `update-ref` repair commands.

This task changes no code. The measurement rows these statements cite — AT1, AT2 and CS16 — are written by **Task 7**. Cite them by those ids.

### Targets

- `docs/cli.md`
- `docs/watcher.md`
- `docs/sandbox-record.md`

**Work:**

- [ ] `docs/cli.md`, the paragraph opening **The unattended profile runs every Bash command…**: add three statements.
  - **The attribution key.** The profile sets `attribution` to `{"commit": "", "pr": ""}`, which removes Claude Code's instruction to append its attribution lines to commits and pull-request bodies. That honoured from `--settings` is measured in AT1, and AT2 is owed. Say why not `false`: the v2.1.281 floor, an older version skipping the whole file, and the silent skip of residual 11. Say that the adopter's commit-message policy still decides whether a trailer is wanted.
  - **The raw-commit grant.** The profile no longer allows `Bash(git commit:*)`, and it denies `Bash(git commit --amend:*)`, which the harness plugin's commit guard backs by withholding its own `allow`.
  - **Existing profiles.** A profile written before this release gains these entries only through `init --force` or a hand edit, because the file is the adopter's from the first write. This repository's `_README` paragraph says the same.
- [ ] `docs/cli.md`, the paragraphs **Four scripts run outside the sandbox…**, **Everything that runs outside the sandbox is write-protected on both sides** and **Each run adds its own copy's paths by exact path…** with its clone bullet.
  - Replace *"a sandboxed commit in a clone lands on the clone's own ref alone"* with the new state: a sandboxed git that would move the clone's `refs/heads/<branch>`, its `packed-refs` or its `HEAD` is refused by the per-run copy's exact entries. Mark this as derived from the code, and owed until CS16 is taken.
  - Name the set's three new run-copy paths in the write-protected paragraph.
  - Change *"the six `.git` paths above"* to the nine, and keep the bubblewrap clause naming only the trio as omitted.
- [ ] `docs/watcher.md`: in **Branch visibility.**, replace *"A sandboxed commit made directly in the clone, which no flow issues, leaves it behind"* with the new state, which is refused by the per-run copy's entries (owed: CS16). Keep the second lag case. In **What it adds.** → the clone bullet, list `.git/HEAD`, `.git/refs/heads` and `.git/packed-refs` after the existing six, and keep the bubblewrap trio clause as it is. Add one sentence saying that the diverged refusal names the cause and gives both `git update-ref` repair commands (`lib/harness-run-lib.sh` → `hr_copy_sync_in_var`).
- [ ] `docs/sandbox-record.md` → `## 6. The residuals`:
  - item 2: add the three new paths to *"its six `.git` paths"* and make the count nine;
  - item 9: change *"every other `.git` file but the six protected paths"* to *"nine"*, and name the three;
  - item 10: change its first lag case, a sandboxed commit in the clone, to *refused by the per-run copy's ref entries, derived, owed until CS16*. Its second case, the swap's `5`, stays.
- [ ] `docs/sandbox-record.md` → `## 6. The residuals`: append one new numbered residual, after the last existing one, opening with what is left.
  - **Ref-moving git calls in a run copy are refused, by design.** A sandboxed `git commit`, `git switch`, branch creation and `git stash push` in a run copy are expected to be refused by Task 2's entries. That stash push is refused is derived, not measured: it runs `git reset --hard`, which locks `refs/heads/<branch>`. A session needing any of them is refused with git's lock error, and no flow issues one (CS16, owed under roadmap item 21).
  - **The `packed-refs` placeholder.** On a bubblewrap host an absent `.git/packed-refs` gets the placeholder the exact entry mounts. Whether git in the run copy reads it cleanly is owed, also under CS16.
  - **`attribution.sessionUrl` is not set.** Its `Claude-Session` trailer applies only to cloud and Remote Control sessions, which is documented but not measured for a local or job `-p` session.
  - **The trailer rests on the commit point.** A trailer an agent writes on its own still reaches a commit if the commit point passes it, because the wrapper builds the message from its arguments and does not refuse. The committer's post-commit read-back reports one.

**Verification:**

- `grep -n "six .git\|six \`.git\` paths\|six protected" docs/cli.md docs/watcher.md docs/sandbox-record.md` has no hit that describes the run copy's protected set.
- `grep -n "sandboxed commit" docs/cli.md docs/watcher.md docs/sandbox-record.md` has no hit that says one lands in a clone.
- `grep -n "attribution" docs/cli.md` hits the new statement, and it cites AT1.
- Every measured claim added carries its row id, every derived one is marked derived, and no line number appears in any citation.
