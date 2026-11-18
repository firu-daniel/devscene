### Task 15 — Document `init --upgrade` in `docs/cli.md`

**Goal:** Make `docs/cli.md` the complete adopter reference for the command, the local additions file, the new write policy and the new `doctor` checks.

**Depends on:** Task 10 for the command and Task 11 for the check ids and grades. Read both shipped behaviours rather than restating this plan.

The story index's `## Scope register` rows owned by Task 15 are this task's sites, and rows marked `no-change` in this file stay as they are. Every command an adopter is meant to run goes in a fenced block, one command per line (`harness-runs/lessons.md`).

### Targets

- `docs/cli.md`

**Work:**

- [ ] `## 1.` and `## 2.`: add the `--upgrade` flag row, state that it refuses `--force` and every other `init` flag except `--reference-toolchain-path`, and add an updating subsection with the steps: update the plugin, then run the command below from the CLI of the same version, with `<version>` as the placeholder. In the `## 1.` `--force` row, the closing clause "every `allow` entry naming a plugin root this machine resolves" excepts an entry the local file supplies or the replaced profile records as local.

  ```
  npx devscene@<version> init --upgrade
  ```
- [ ] `## 2.`, the retrieval paragraph: replace the forced route with a plain `init`, which merges `.mcp.json` and the ignore rules and sets up retrieval, followed by `init --upgrade`, each in its own fenced line.
- [ ] `## 3.`: change the policy count, add `replace-if-changed` and its atomic replacement, update the outer-loop and profile rows, add the local file and its ignore rule, state what `--upgrade` leaves alone, and state that backups live under `<git-common-dir>/devscene/upgrade-backups/<timestamp>/` with none for an unchanged file. In the `devscene-trigger.yml` and `devscene-control.yml` rows, keep `--force` after a `.bak` as each workflow's upgrade path and remove the claim that it shares the scripts' re-run contract. State the same exception wherever this section describes the carry-forward: in the profile row, "the one run that does replace it", "**carries forward every `allow` entry naming a plugin root this machine resolves**" and "it carries every absolute entry outside the checkout forward **unverified**"; and in the bullet "`--force` upgrades `create-if-absent` only", only the clause "A **profile entry** is kept when it names a plugin root this machine resolves".
- [ ] `## 5.` and `## 6.`: update the sites the register names, and describe generated-plus-local ownership: the four addable lists, the refused keys, render-time merging, the first-upgrade report of entries not moved, the plugin-root carry-forward, that a local entry is never carried so deleting it takes effect on the next `init --upgrade`, the tracked-file refusal, the placeholder shapes read as absent, and remote jobs running without the file. In "Both conditions are the gate", change only the retrieval clause, so that turning retrieval on later points at §2's plain `init` followed by `init --upgrade`; the browser half keeps its forced route. In `### The sandbox block and the permission mode`, add the main checkout's local additions file to the write-protected set beside "the profile itself in the main checkout".
- [ ] `## 7.`: add table rows and grading bullets for `profile-drift`, `outer-loop-scripts` and `plugin-cli-version`, and change the ownership clauses of the `command-permissions`, `profile-paths` and `profile-write-protection` bullets so each grade rests on the profile being generated and on the run still proceeding. The remedies those checks print stay as they are. In the `plugin-permissions` bullet, change only the clause "the same set `init --force` carries forward unverified on that arm (§3)": the count can also include entries the local file supplies or the profile records as local, which that run does not carry. The check's message stays as it is.

**Verification:**

- The `## 7.` table lists every id in `CHECKS`, which `grep -n "id: '" cli/src/doctor/checks.ts` confirms.
- Re-running D1, D2, D5 and D7 over `docs/cli.md` reaches only sites the register lists.
- `grep -nE 'file the adopter owns|hand-tuned|shares their re-run contract|forced re-run in §2' docs/cli.md` finds nothing.
- Every line `grep -nE 'plugin root this machine resolves|every absolute entry|carries forward unverified|same set .init --force.' docs/cli.md` returns that describes what a forced run keeps also states that an entry the local file supplies or the replaced profile records as local is not carried.
- Each adopter command added sits alone on a line in a fenced block.
