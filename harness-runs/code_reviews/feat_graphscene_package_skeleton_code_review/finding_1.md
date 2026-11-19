### 1. `sync --with-models` under `--package graphscene` is not refused, although the row has no `models` extra

**File:** `scripts/python-service.sh` (`package_row`, and the `sync)` arm of the sub-command `case`): "extra=(--extra models)"

The story index's decision 5 is that a table row serves only the sub-commands it can. This branch added that guard for `run` (no console script) and `container-test` (no compose project) on the `graphscene` row. It did not add it for the third row-specific capability, `sync --with-models`. That arm still hardcodes `extra=(--extra models)` for every row. So `bash scripts/python-service.sh --package graphscene sync --with-models` reaches `uv sync --frozen --group dev --extra models` against `graphscene/pyproject.toml`, which declares no `[project.optional-dependencies]` table at all.

What happens next is up to `uv`, not the wrapper. If `uv` rejects the undefined extra, the call exits `1`, "the tool reported failure", where the exit contract reserves `2` for a sub-command the row cannot serve. If `uv` accepts it, the call exits `0` and the wrapper has claimed to install an extra that does not exist. Either way, the closed table no longer decides what a row serves. The header's own description of `--with-models` ("Without the flag the `models` extra is NOT installed") and `docs/development.md`'s "`sync --with-models` stays the route that installs the `models` extra" now read as true for both rows, and they are true for only one.

**Fix:**

1. In `scripts/python-service.sh` → `package_row`, give each row a third field:

   ```bash
       docs-retrieval-service)
         row_console_script="devscene-docs-retrieval"
         row_compose_prefix="devscene-docs-retrieval-test"
         row_models_extra="models"
         ;;
       graphscene)
         row_console_script=""
         row_compose_prefix=""
         row_models_extra=""
         ;;
   ```

2. In the `sync)` arm, refuse the flag on a row with no extra before any `uv` call, and take the extra's name from the row:

   ```bash
     sync)
       extra=()
       if [ "$#" -eq 1 ] && [ "$1" = "--with-models" ]; then
         if [ -z "$row_models_extra" ]; then
           echo "python-service: package '${package}' has no models extra" >&2
           usage
           exit 2
         fi
         extra=(--extra "$row_models_extra")
       elif [ "$#" -ne 0 ]; then
   ```

3. Update the header comment to match:
   - The table sentence becomes "…with the console script `run` invokes, the compose project prefix `container-test` uses and the extra `sync --with-models` installs."
   - The `graphscene` row reads "(no console script, no compose project, no `models` extra)".
   - Exit `2`'s line gains "or `sync --with-models` on a row that has no `models` extra".

4. In `cli/test/python-service.test.mjs`, the test `` `run and container-test under --package ${LIBRARY} exit 2 with the row's refusal line and call no uv` ``:
   - Add a third entry to `refusals`: `[['--package', LIBRARY, 'sync', '--with-models'], `python-service: package '${LIBRARY}' has no models extra`]`.
   - Retitle the test to `` `run, container-test and sync --with-models under --package ${LIBRARY} exit 2 with the row's refusal line and call no uv` ``.
   - The existing `'sync carries no --no-cache, and --with-models appends --extra models'` case runs on the default row and stays as it is.

   That test file is the one this fix edits, so it is the only test file the fix runs. The full suite runs in the Run gates phase.

5. In `docs/development.md` → `**Gate 13 — the Python packages.**`'s closing paragraph, change "so `run` and `container-test` on it exit `2`" to "so `run` and `container-test` on it exit `2`, and so does `sync --with-models`, because it has no `models` extra".
