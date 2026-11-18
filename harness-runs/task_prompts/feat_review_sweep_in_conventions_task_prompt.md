`feat_review_sweep_in_conventions` moves the end-of-branch reviewer's Pass 0 grep sweep out of the shipped agent file and into one dedicated sweep document that the adopter owns. `/devscene:analyze` fills that document from the repository's own code, and `branch-reviewer` reads its sweep from there.

> ⚠️ **Find every anchor in this prompt by its quoted text, heading or function name, never by line number.**

## What is known

- `plugin/agents/branch-reviewer.md` → `### Pass 0 — the deterministic sweep` has two halves. Half **(b)**, the new-exported-symbol caller check, always runs. Half **(a)**, the grep sweep, greps the diff's added lines for one regex per *escape class*. The regexes live in a table inside the agent file itself, and that file calls the table "a **stub, to be edited**". Every `Regex` cell ships empty, so half (a) never matches anything.
- **No adopter can fill it.** The table is part of the plugin. An adopter runs the installed plugin, so a local edit is overwritten by the next plugin update. Nothing an adopter owns feeds the sweep: no `devscene.config.json` key, no template under `cli/templates/`, and no conventions-document section. This repository can edit the table only because it self-adopts and reads `plugin/` in place, and filling it there would ship this repository's regexes to every adopter.
- **It has never run here.** Every code review under `harness-runs/code_reviews/` that mentions Pass 0 reports the grep half empty, in words such as "no regexes configured", "empty sweep list" and "had nothing to sweep". The latest is `feat_structured_outputs_docs_qa_code_review.md`: "The grep half was skipped because this definition's sweep list has no regexes filled in, which is a configuration gap."
- **The default escape classes assume a UI application:** styling literals, timing literals, duplicated shared constants, raw console calls, casts in place of mappings, navigation or dialog calls from the wrong layer, and open literal sets. A project like this one (bash, jq, Markdown contracts and a TypeScript CLI) has different escape classes. Some examples:
  - an absolute machine path, which `scripts/check-machine-paths.sh` already catches at the gate;
  - an attribution trailer in committed text;
  - a literal state-dir name where `<state_dir>` belongs;
  - a plugin path not rooted at `${CLAUDE_PLUGIN_ROOT}`;
  - a GNU-only `sed -i` or `date` flag under the Bash 3.2 floor.

  The classes vary per project as well as the regexes.
- **Who reads what today.**
  - `branch-reviewer`'s `## Read first` already loads every conventions document `<layer_path_map>` names.
  - `layer-implementer` and `layer-reviewer` load only their own layer's document.
  - Sweep rows written into the per-layer documents would therefore reach every per-unit agent, which has no use for them. That is why they get a document of their own.
- **Lessons stay in the ledger.** The agent's current rule is to add a sweep row "when `<state_dir>/lessons.md` records a new one", and nothing can carry it out. The sweep document lives under `.claude/`, which a headless run cannot write: the tool layer refuses the edit ahead of any permission entry (`plugin/agents/task-plan-writer.md` → the conventions-document prohibition). The ledger is written after the run, once the user's review lands. The reviewers already read `lessons.md` as named checks, so a lesson needs no sweep row to be applied.

## What to read first

- `plugin/agents/branch-reviewer.md`: `## Read first`, `### Pass 0 — the deterministic sweep`, the `<convention_symbols>` and `<impl_stack>` rows of its resolved-values table, and the steps that run Pass 0.
- `cli/templates/claude/context/`: the skeletons `init` writes, and how `init` renders and keeps them (`cli/src/generators/claudeContext.ts`).
- `plugin/commands/analyze.md`: how a skeleton is classified (`action: write` / merge / skip) and the provenance-note rule.
- `plugin/agents/conventions-writer.md` and `plugin/agents/conventions-reviewer.md`: what each pass (`pass: document` and `pass: corpus`) writes and checks.
- `plugin/schemas/branch-reviewer.return.json`, `plugin/schemas/conventions-writer.return.json` and `plugin/schemas/conventions-reviewer.return.json`: every agent's return is now a schema-checked JSON object, so a new return field or outcome is a schema change as well as a prose change.
- `plugin/agents/skeptic-reviewer.md` and `plugin/agents/review-plan-reviewer.md`: whether either one re-runs or checks Pass 0, and what each says about it.
- `.claude/context/conventions.md`, `.claude/context/cli.md` and `.claude/context/plugin.md`: this repository's own conventions, which this repository's sweep document is derived from.
- `cli/templates/claude/settings.autonomous.json`, `cli/src/generators/permissionProfile.ts`, `plugin/hooks/autonomous-script-allowlist-guard.sh` and `cli/src/generators/writeProtection.ts`: what a run may execute and which main-checkout scripts it cannot write, for the script proposal below.

## The goal

1. **One dedicated sweep document.** `init` writes it as a skeleton under `.claude/`, and the adopter owns it from then on. A re-run of `init` keeps the adopter's copy, as it keeps the conventions documents. Each row gives:
   - an escape class;
   - its regex;
   - the layer paths it covers, and any paths it exempts;
   - what a hit is a candidate for.

   No per-layer conventions document carries sweep rows, so no per-unit agent loads them.
2. **`branch-reviewer` takes its sweep from that document.** It no longer carries a table of its own. It keeps the method: added lines only, every covered layer path in the pathspec, the `<state_dir>` exclusions, and every hit verified in context before it becomes a finding. A missing or unfilled sweep document is reported as a configuration gap. Half (b) and the rest of the review run either way.
3. **`/devscene:analyze` fills it.** The conventions writer derives the escape classes and their regexes from the repository's real code and its stated conventions, not from the UI defaults. The conventions reviewer runs each regex against the code it covers. A regex that matches nothing there, or matches nearly every line, is a finding.
4. **The `lessons.md` row rule goes.** The agent's "add a row when `<state_dir>/lessons.md` records a new one" sentence is removed, and no other document takes it over. The sweep document is maintained by the user, by hand or through `/devscene:analyze`.
5. **This repository's own sweep document is not written by this branch.** Every file under `.claude/` is outside what the branch writes. After the merge, the user fills this repository's sweep document by running `/devscene:analyze`, so that this repository's own end-of-branch reviews finally run half (a). That run is also the first real-world check of goal 3.

## Proposals — for planning to settle, not constraints

The plan decides which of these to take, in what combination, or something better, and says why. Each one needs its own check against the code before the plan commits to it.

- **A generic sweep script in place of the reviewer's own grep.** One script ships through `init` with the other outer-loop scripts and is tested once under `cli/test/`. It reads the sweep document's rows as data, so nothing writes a script per repository. It applies each row to the branch's added lines and returns:
  - `0`: no hits;
  - `1`: hits, printed as `file:line: class`;
  - `2`: a configuration error, such as a missing or empty sweep document or an invalid regex.

  The reviewer verifies each hit in context and never builds the grep itself. Most hits are candidates, not defects (the file that owns the styling tokens holds styling literals), which is why a hit is a lead and not a failure. Planning checks:
  - **Tamper resistance.** The rows already sit under `.claude/`, which the run cannot write. The script would have to be invoked from the main checkout, as `commit-on-branch.sh` is, so that a branch cannot weaken its own check by editing the run copy's script.
  - **Permission cost.** An unattended run needs an allow rule to execute the script. This is the one permission this branch may add, and only if the script is taken.
  - **Whether it beats the agent's grep at all,** given that verifying each hit still takes judgment.
- **A gate tier for exact rows.** A row precise enough to have no false positives could be marked as a gate row. Run gates would then fail the branch on a hit, as it fails on `scripts/check-machine-paths.sh` today, catching it before the review. Planning decides whether that is worth a second row kind, and how it fits the Run gates phase and `treeGuards`.
- **The row format.** A Markdown table is easy to read, but a `|` inside a regex has to be escaped. A plain table (TSV or similar) is easier for a script to parse and harder for a person to read. Planning settles the format, the grep dialect (`grep -E`, as today) and how a regex containing the separator is written.
- **Doctor.** `devscene doctor` could warn when the sweep document is missing or unfilled. Its `setup-analysis` check and the two-part unfilled-skeleton test (`UNFILLED_STUB_MARKER` in `cli/src/generators/claudeContext.ts`) already detect an unfilled skeleton, so a sweep check could reuse them. Planning decides whether that is worth a check.
- **The stub's UI classes.** They could move into the sweep document's skeleton as worked examples for a front-end adopter, so they are not lost from the plugin.

## Constraints

- **This is a wire change in the plugin corpus.** The document path and heading the reviewer reads, and any literal it quotes, appear in every file that cites it. Rename or add one in every citer in the same change, including the `plugin/schemas/*.return.json` of any agent whose return changes.
- **No backward compatibility for existing adopters.** No migration step and no fallback to the old in-agent table.
- **No new permission in any profile,** except the single allow rule for the sweep script, if planning takes that proposal.
- Bash 3.2 floor. `bash scripts/typecheck.sh` and `scripts/run-gates.sh` pass.
- The self-adopted copies of every template this branch changes are re-rendered and byte-identical to their templates, where the repository keeps such a copy outside `.claude/`. The copies under `.claude/`, the sweep document's among them, are left to the user (goal 5).



