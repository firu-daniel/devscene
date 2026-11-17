### Task 3 — Name a split branch's cause and repair in the sync-in divergence refusal

**Goal:** When a clone's branch and the main checkout's have diverged, the one sentence every wrapper and the watcher's copy check surface must say what happened and how a person repairs it. The sentence then reaches a park through the committer's `error:`, `push-branch.sh`'s `refusing to push:` line or `HR_RUN_REFUSAL`, and that park names the split and its repair the way the maintainer had to work it out by hand for Park 1.

**Where this layer stops.** One sentence, in one function. It moves no ref and adds no repair path: the refusal still moves nothing. The committer's report of a commit that landed wrong is **Task 5's**, and the documentation is **Task 7's**. This repository's own `scripts/lib/harness-run-lib.sh` is re-rendered by hand after merge (story index → `Manual setup required`).

### Targets

- `cli/templates/scripts/lib/harness-run-lib.sh` — `hr_copy_sync_in_var`, the diverged arm (`merge-base --is-ancestor` both ways answering `1`).
- `cli/test/clone-sync.test.mjs` — a new case for the rewritten-tip refusal.

**Work:**

- [ ] `hr_copy_sync_in_var`, the diverged arm: before setting `HR_SYNC_REFUSAL`, read whether the two tips share their first parent and their tree. Read each with the existing `hr_copy_sync_main_git "$cmain" rev-parse --verify --quiet "<oid>^"` and `"<oid>^{tree}"` calls, which the main checkout can answer because sync-in has already fetched the clone's tip. A read that fails leaves the relation unknown, and is never a refusal of its own.
- [ ] Rewrite the sentence so that it **keeps the substring `have diverged`** (`cli/test/clone-sync.test.mjs` and `cli/test/wrapper-clone-arm.test.mjs` match on it) and carries, as one line:
  - **What happened.** Both tips, abbreviated as today, followed by the cause clause. When the parents match, the clause is *"the clone's tip rewrote the main checkout's outside the wrappers (same parent, same tree)"*, or *"… (same parent, different tree)"*. Otherwise it is *"one of them moved outside the wrappers"*.
  - **That nothing moved.**
  - **The repair, with full 40- or 64-hex ids.** To keep the clone's tip, a person runs `git -C <cmain> update-ref refs/heads/<branch> <clone oid> <main oid>`. To keep the main checkout's, they run `git -C <clone> update-ref refs/heads/<branch> <main oid> <clone oid>`, and when the trees differ, they also bring the clone's working tree to that tip. Then they answer the park.

  Spell the commands as text inside the message only. The library runs neither.
- [ ] Keep the function's contract unchanged: return `1`, set `HR_SYNC_REFUSAL` to one line with no newline, and leave both refs unmoved. Update the function's header comment if it describes the diverged sentence. Bash 3.2 floor; no new external binary.
- [ ] `cli/test/clone-sync.test.mjs`: add one case, following the file's existing clone fixtures. Make a commit through the existing sync path so that both refs are equal. Then rewrite the clone's tip with a plain `git commit --amend -m <new subject>` in the clone, giving the same parent and the same tree. Call sync-in and assert:
  - it refuses;
  - `HR_SYNC_REFUSAL` matches `/have diverged/` and `/same parent, same tree/`;
  - it carries both full commit ids and both `update-ref refs/heads/<branch>` repair commands;
  - neither ref moved.

**Verification:**

- `npm test --workspace cli -- test/clone-sync.test.mjs` passes.
- `bash scripts/typecheck.sh` exits 0.
- `HR_SYNC_REFUSAL` on the new case is a single line.
- In the clone-sync fixture's own temporary repositories, the repair command it names for the clone's tip, run there, puts both refs on the clone's tip.
