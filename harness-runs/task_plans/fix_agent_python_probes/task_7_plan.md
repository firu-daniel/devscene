### Task 7 — Document `probe`, `check` and the per-unit Python check in `docs/development.md`

**Goal:** Record in the definition of done (`docs/development.md` → `## 5. Verifying a change`) that every unit's type check now runs the Python packages' lint and type legs, how an unprovisioned environment is graded there, and what the wrapper's `probe` verb is for. A maintainer reading gate 13 should learn what a unit already ran.

**Depends on:** Tasks 1, 2 and 5, as landed. Task 1's contract: `python-service.sh probe <file under the state dir's scratch/> [args]`, with an optional leading `--package <dir>`; the path is judged by `hr_scratch_path_var` and run through `uv run --frozen --no-sync --no-cache python`; the file's own status passes through; refusals exit `2`, an unprovisioned environment `3`. `python-service.sh check` runs every row's `lint` and `typecheck` and exits `0`, `1`, or `3` when none failed and at least one leg is `BLOCKED`. Task 2's contract: `scripts/typecheck.sh` runs `check` between the parse step and the build line, prints a `typecheck: python checks BLOCKED - …` line on `3` without failing, and keeps its two verdict forms. Task 5's module: `plugin/instructions/probe_route.md`. This task describes what landed and changes none of it; read the three files before writing, so the prose matches them rather than this paragraph.

### Targets

- `docs/development.md`

**Work:**

- [ ] **Gate 13.** After the sentence ending *"each is graded `BLOCKED` on the wrapper's exit `3` exactly as this paragraph states below for every leg."*, add a sentence that **every unit runs 13a, 13b, 13e and 13f's checks too**. `scripts/typecheck.sh`, which `commands.typecheck` names, runs `bash scripts/python-service.sh check`, so a Python lint or type defect fails the unit that wrote it. An unprovisioned environment prints its `BLOCKED` line there and does not fail the unit. The Run gates phase runs the same legs twice, once through `commands.typecheck` and once as gate 13, as gate 16 is run twice. Then add one sentence on `probe`: it runs one `.py` file from the state directory's `scratch/` through the package's environment, with no network and no change to the environment, and it is the package-environment form `plugin/instructions/probe_route.md` → `## The route` sends a dispatched agent to. Add one fenced example, `bash scripts/python-service.sh --package graphscene probe harness-runs/scratch/<name>.py`, one command per block (ledger, `## Adopter-facing documentation`).
- [ ] **The self-adopt `--force` bullet** naming `scripts/typecheck.sh` (*"since gate 16 added a hand-written step to it"*). It now names both hand-written steps, the parse check and the Python check, as what a re-rendered wrapper loses, and the restore line below it is unchanged.
- [ ] **Gate 16.** Where it says `scripts/typecheck.sh` *"runs `bash scripts/check-shell-parse.sh` before its `npm run build` line"*, keep the sentence true for the new order: parse, then Python check, then build.

**Verification:**

- `grep -n 'python-service.sh check\|python-service.sh --package graphscene probe\|probe_route.md' docs/development.md` finds the new text in gate 13. Each command it spells matches `scripts/python-service.sh`'s `usage()` line and each line it quotes matches `scripts/typecheck.sh`, both read after Tasks 1 and 2 landed.
- Re-run the story index's `## Scope register` derivation entry C2 verbatim. Its output must be a subset of the register's rows, and no row marked `change` for this task may remain undone.
  - **Deviations from plan:** The per-unit sentences sit right after the named sentence, as planned. The `probe` sentence and its fenced example went later in gate 13, after the `sync --with-models` block and before **13d is opt-in.**, and not right after the named sentence. A fence there would have cut the gate 13 paragraph in two, and the BLOCKED rule that the named sentence says *"this paragraph states below"* would then have been in a different paragraph.
