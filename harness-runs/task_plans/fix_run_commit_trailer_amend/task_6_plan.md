### Task 6 — Record the attribution measurement, the owed ref-deny row and the guard decisions

**Goal:** Give every protection this branch relies on a row of record. Measured facts are entered with what was run and what it printed. The new sandbox protection is graded `owed` until a probe takes it. The probe's CS3 expectation, which the new protection makes wrong, is flagged before the next probe run reads it as a regression. This is a catch-all task, so its implementer reads every configured layer's conventions document.

**Depends on:**

- **Task 1.** The run copy's new protected rows, `.git/HEAD` (`file`), `.git/refs/heads` (`directory`) and `.git/packed-refs` (`file`), all `bubblewrapDenyWrite: true`.
- **Task 2.** The profile's `"attribution": {"commit": "", "pr": ""}`.
- **Task 4.** The commit guard's contract, the sixteen payloads of `task_4_plan.md`'s table, restated here so this file stands alone. On an ordinary branch: `allow` for `git -C <dir> commit -m x`, `git -C <dir> add f && git -C <dir> commit -m x`, `cd <dir> && git commit -m x` and `git -C <dir> commit --fixup=HEAD`; no output for `… commit --amend -m x`, `… commit --amen --no-edit`, `… commit "--amend" -m x`, `… commit $F -m x`, and for `git -C <dir> commit -m x` followed by `&& git -C <dir> commit --amend -m y`, `&& git -C <dir> reset --hard HEAD~1`, `&& git -C <dir> update-ref refs/heads/<b> HEAD~1`, `&& git -C <dir> rebase HEAD~1`, `&& bash ./x.sh`, or `| cat`. On a protected branch and on a detached HEAD: `ask` for `git -C <dir> commit --amend -m x`, unchanged.

This task changes no code and adds no probe leg. It ships before **Task 7**, which cites AT1, AT2, CS16 and PD32 by those ids, so every row Task 7 cites already exists when it lands.

### Targets

- `docs/sandbox-verification.md`
- `docs/guard-verification.md`
- `docs/development.md`

**Work:**

- [ ] `docs/sandbox-verification.md` → `## 4. The profile's denials`: add row **AT1**, *"`attribution` set through `--settings` switches off Claude Code's commit-attribution instruction"*, graded **pass**. Record it as measured by hand in a supervised session on 2026-11-16, Claude Code 2.1.325, three `claude -p --model haiku` sessions each asked to quote any instruction in its system context about lines to end a git commit message with. Record the three readings exactly as the task prompt's `## Checked before this run` states them. Quote them as data with that source, between the markers of `plugin/instructions/untrusted_input.md` → `## The markers`, or as an attributed quotation:
  - no `--settings`: `End git commit messages with:` followed by `Co-Authored-By: Claude Haiku 5.5 <noreply@anthropic.com>`;
  - `--settings '{"attribution":{"commit":"","pr":""}}'`: no attribution lines;
  - `--settings '{"attribution":false}'`: no attribution lines.

  Also record that this was an inline JSON `--settings`, not the rendered profile file. Then add row **AT2**, graded **owed** (roadmap item 21): the same question asked of a session launched on a rendered per-run profile carrying Task 2's key, through §0's launch line, on macOS and on Linux.
- [ ] `docs/sandbox-verification.md` → `### The clone layout (owed)`: add row **CS16**, graded **owed** (roadmap item 21), *"the run copy's branch-ref store and HEAD under the real `<run profile>`"*. Its calls are one each, cwd = `<clone>` on its run branch, through `--allowedTools` where the profile refuses one: `git commit -m "<subject>"`, `git commit --amend --no-edit`, `git stash push`, `git switch -c <x>`, and a `dd if=/dev/null of=<clone>/.git/packed-refs conv=notrunc`. Expected: each is refused at the sandbox layer, and `git rev-parse refs/heads/<branch>`, `git symbolic-ref HEAD` and `packed-refs`' `shasum` are unchanged. Controls `git add <file>` and `git status` succeed. On Linux, also record whether an absent `.git/packed-refs` read as the placeholder inside the session, and whether `git status` there still succeeds. Add **CS16 (Linux)** in `## 8. The Linux legs (owed)`, also owed.
- [ ] `docs/sandbox-verification.md`, rows **CS3** and **CS3 (Linux)**: append to each `Expected` cell a note. Since this branch, the clone's `refs/heads`, `packed-refs` and `HEAD` are write-denied, so CS3's `git commit`, `git stash push`/`pop` and `git switch -c` are expected to be refused. CS16 measures that, and the CS3 leg still grades them as calls expected to succeed (PD32). Leave every recorded result as it stands. Then add row **PD32** to §5's failure table, after PD31: *"CS3's probe leg expects `commit`, `stash push`/`pop` and `switch -c` to succeed, which the run copy's ref write-deny now refuses"*. Fixes: owed. Moving those calls from `scripts/lib/sandbox-probe/legs-protection.sh` → `sp_leg_git`'s CS3 grading into a CS16 leg is deferred under roadmap item 21. Until then, a CS3 `fail` naming only those calls is that expectation and not a regression.
- [ ] `docs/guard-verification.md`: add a short subsection under `## 3. Decision changes across the port` → `### 3.1 Narrowed — \`allow\` → SILENT`, holding Task 4's sixteen payloads against `plugin/hooks/git-commit-branch-guard.sh` on a throwaway `git init` fixture under the system temp directory. The fixture carries a `devscene.config.json`, has one ordinary branch and one in the protected set, can be put on a detached HEAD, and is never this checkout. Record each row's command, the branch state, and the exact outcome observed: the JSON object, or *no output, exit 0*. A row that cannot be driven in this run is entered `owed`, never with an assumed outcome. Do not retake or edit the §1.2 latency table: a wall-clock figure is taken by hand outside any session (`harness-runs/lessons.md` → `## Evidence and measurement`).
- [ ] `docs/development.md`, the Gate 12 probe-leg table's `git` row. It currently reads *"ordinary git in the clone succeeds under the real per-run profile"*. Qualify it: ordinary git that writes only the index and objects succeeds, and the calls that move `refs/heads`, `packed-refs` or `HEAD` are expected to be refused, which CS16 measures (owed). Cite PD32 for the CS3 leg's interim `fail`. Leave the Linux table's `as macOS` row and every dated result unchanged.

**Verification:**

- `grep -n -E "^\| (AT1|AT2|CS16|CS16 \(Linux\)|PD32) \|" docs/sandbox-verification.md` shows each new id as exactly one row, and none of them collides with an existing id.
- Every new row graded `pass` carries its date, its Claude Code version, the command and the exact output. Every other new row is graded `owed` and names roadmap item 21, which has its row in `docs/development.md` → `## 6. The roadmap this tree defers to`.
- The new `docs/guard-verification.md` rows name the fixture's shape and quote outcomes, and none claims a decision that was not driven.- No citation added in any of the three files carries a line number.
