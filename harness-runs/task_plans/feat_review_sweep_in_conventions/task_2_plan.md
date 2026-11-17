### Task 2 — Ship `review-sweep.sh`, which applies the sweep rows to a branch's added lines, with its test suite

**Goal:** Add the outer-loop script that turns the sweep document's rows into hits. It reads the rows as data, applies each to the branch's added lines inside that row's scope, and answers with exit `0` / `1` / `2`, so no repository needs a script of its own and the reviewer never builds a grep.

**Depends on:** Task 1, which fixes the document path `.claude/review-sweep.md` and the row format this script parses. The format, as this script must read it:
- the one table directly under the exact heading `## Sweep rows`;
- header row exactly `| Escape class | Regex | Covers | Exempts | A hit is a candidate for |`, then a separator row, then one row per class;
- the table ends at the first line not beginning with `|`;
- `Regex` is exactly one backtick code span holding a `grep -E` pattern, in which `\|` stands for a literal `|`;
- `Covers` is one or more code-spanned repo-relative paths separated by `, `, with `.` for the whole repository;
- `Exempts` is code-spanned paths or pathspec globs separated by `, `, or `—` for none.

**Where this task stops.** It ships the template and its test only. The `OUTER_LOOP_SCRIPTS` row that makes `init` write it and grants the allow rule is **Task 3's**. The self-adopted copy `scripts/review-sweep.sh` is **Task 9's**. The reviewer's call is **Task 8's**, and Task 8 calls the script exactly as follows: `bash <MAIN_REPO>/<scripts_dir>/review-sweep.sh --repo <repo_root>`, reading the exit status and stdout described here.

### Targets

- `cli/templates/scripts/review-sweep.sh` (new).
- `cli/test/review-sweep.test.mjs` (new). It reads one fixed file, the template, and builds its own fixtures, so it is **not** a tree-reading test and owes no `treeGuards` entry.

**Work:**

- [ ] **The script's frame.**
  - `#!/usr/bin/env bash`, a `# review-sweep.sh — …` header in the shape of `cli/templates/scripts/task-offer-check.sh`'s: what it decides, an `EXIT MAP`, `WHO RUNS IT`, `REUSED FROM lib/harness-run-lib.sh`, why there is no `set -e`, and a `REPRO` block that reproduces each exit against a throwaway fixture.
  - Bash 3.2 floor: no `mapfile`, no associative arrays, no `${var,,}`.
  - It needs only `git`, `grep` and the shell utilities its sibling scripts already use, and writes no file. A temporary file, if one proves unavoidable, follows the `mktemp` discipline the other shipped scripts use.
  - Source `lib/harness-run-lib.sh` from beside itself through `${BASH_SOURCE[0]}`. Resolve its own root with `hr_script_root`, and read `defaultBranch` and `stateDir` from that root's `devscene.config.json` (`hr_config_load`, `hr_default_branch`, `hr_state_dir`). Never read them from the `--repo` target's configuration.
  - Usage: `review-sweep.sh [--repo <checkout>]`. `--repo` defaults to the script's own root and must be a git work tree.
- [ ] **Reading the rows.**
  - Read the document with `git -C <repo> show <default_branch>:.claude/review-sweep.md`, never from the working tree, so a branch cannot edit its own sweep.
  - Parse only the table under `## Sweep rows`. Split each row on unescaped `|` and turn each `\|` in the `Regex` cell into `|`. Strip the code-span backticks. Split `Covers` and `Exempts` on `, `, where `—` in `Exempts` means none.
  - Validate each regex once with `grep -E -e <regex>` against empty input. Exit status 2 there is an invalid regex.
- [ ] **Applying the rows.** For each row, in document order:
  - Diff `git -C <repo> diff --no-color --no-ext-diff --unified=0 <default_branch>...HEAD -- <covers…> ':(top,exclude)<state_dir>' <each exempt as ':(top,exclude)<exempt>'>`, with any trailing slash stripped from `<state_dir>` first.
  - Track the current file from the `+++` line and the new-file line number from each `@@ … +c[,d] @@` header.
  - Match `grep -E` against the content of each added line only: lines starting `+`, excluding the `+++` header.
  - Print one `<path>:<line>: <escape class>` line per matching added line on stdout.
- [ ] **The exit map.** `0` means no hit and nothing printed. `1` means at least one hit. `2` means a configuration error, with exactly one line on stderr naming the cause:
  - bad usage;
  - the configuration unreadable;
  - `--repo` not a work tree;
  - `<default_branch>` not resolvable;
  - the document absent from `<default_branch>` (say "not committed on `<default_branch>`");
  - the document still an untouched skeleton, meaning it carries both `<!-- devscene:unfilled -->` and `**What belongs here**`;
  - no `## Sweep rows` heading, a header row that differs from the exact one, or no data row;
  - a malformed row: a cell count other than five, a `Regex` cell that is not one code span, or an empty `Covers`;
  - an invalid regex, naming its escape class.
- [ ] **`cli/test/review-sweep.test.mjs`.** Open with the rule the suite enforces. Build throwaway fixture repositories under the system temp directory with `cli/test/helpers/fixture.mjs`, copying the template and `lib/harness-run-lib.sh` into the fixture's `scriptsDir`; follow an existing script suite such as `cli/test/run-test-suite.test.mjs`. Cases:
  - exit `0` on a branch with no matching added line;
  - exit `1` with the exact `<path>:<line>: <class>` lines, the line number being the branch file's;
  - a match on a context or removed line is not a hit;
  - `Covers` scoping and `Exempts` exclusion;
  - a hit under `<state_dir>` is never reported;
  - a regex using `\|` alternation matches both arms;
  - a working-tree edit to `.claude/review-sweep.md` that is not committed on the default branch changes nothing;
  - exit `2`, with its stderr cause, for each configuration error above: absent, untouched skeleton, missing heading, malformed row, invalid regex.

**Verification:**

- `npm test --workspace cli -- test/review-sweep.test.mjs` passes. It is this task's own new test file.
- `bash -n cli/templates/scripts/review-sweep.sh` parses.
- Each `REPRO` line in the header reproduces its stated exit against a throwaway fixture.
  - **Deviations from plan:**
    - `bash -n cli/templates/scripts/review-sweep.sh`: the direct call was refused in this session's permission mode. The claim rests instead on `bash scripts/typecheck.sh`, whose shell-parse step printed `check-shell-parse: 134 files checked with /bin/bash (bash 3.2.57(1)-release), 0 failed`. That step covers untracked, non-ignored `*.sh` files, the new script included.
    - The `REPRO` lines were not hand-run, because the direct `bash` call was refused the same way. Each stated exit is reproduced instead by a case in `cli/test/review-sweep.test.mjs`, which passed 18/18: not committed → `a document absent from the default branch…`; no hit → `a branch adding no matching line…`; hit → `each matching added line…`; bad usage → `bad usage, a --repo…`. The fixture shapes differ: the cases commit through the fixture identity and do not use `git init -b`.
    - Beyond the plan's exit-2 list, the script also refuses an empty `Escape class` cell, a `Covers` or `Exempts` entry that is not a code span, an empty `Exempts` cell (`—` is required for none), and a `git diff` that git refuses (for example, no merge base). Each one exits 2 with a single stderr line. Without these checks, the output would be a hit line with no class or a silently wrong scope.
    - The diff command adds `-c core.quotePath=false --src-prefix=a/ --dst-prefix=b/` to the planned flags. This keeps the `+++` path parse independent of the adopter's `diff.noprefix` / `diff.mnemonicPrefix` / `core.quotePath` settings.
