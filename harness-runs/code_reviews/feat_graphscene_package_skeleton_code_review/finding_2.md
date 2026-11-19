### 2. The nightly `uv-audit` job does not audit the new `graphscene/uv.lock`

**File:** `.github/workflows/supply-chain.yml` (job `uv-audit`): "working-directory: docs-retrieval-service"

This branch commits a second `uv` lockfile, `graphscene/uv.lock`, which pins 14 packages (`ruff`, `mypy`, `pytest` and what they pull in). Every run copy's bootstrap now installs those packages through `provision` (`commands.depInstall`). The nightly supply-chain audit exists to "Re-audit the supply chain every night … and fail loudly on a finding" (the workflow's header). Its `uv-audit` job audits only `docs-retrieval-service/uv.lock`, so an advisory against any package that only `graphscene/uv.lock` pins is never reported.

`docs/development.md` → `## 8. The nightly supply-chain audit` describes the job the same narrow way, so the gap shows in neither place.

**Fix:**

1. In `.github/workflows/supply-chain.yml`, append a second step to the `uv-audit` job after the existing one, at the same indentation:

   ```yaml
         - working-directory: graphscene
           run: uv audit --preview-features audit-command --frozen
   ```

   In the header comment, change "uv-audit (known\n# vulnerabilities in docs-retrieval-service/uv.lock)" to "uv-audit (known\n# vulnerabilities in docs-retrieval-service/uv.lock and graphscene/uv.lock)", re-wrapping the comment lines to stay within 100 columns.

2. In `docs/development.md` → `## 8. The nightly supply-chain audit`:
   - In the `uv-audit` table row, change "Every package `docs-retrieval-service/uv.lock` pins" to "Every package `docs-retrieval-service/uv.lock` or `graphscene/uv.lock` pins".
   - Change the line "`uv-audit`, from `docs-retrieval-service/`:" to "`uv-audit`, once from `docs-retrieval-service/` and once from `graphscene/`:". The fenced command under it stays as it is.

No test file covers this workflow, so the fix runs no test. Gate 14's and the nightly `zizmor-online` audits of this repository's `.github` cover it in their own rounds.
