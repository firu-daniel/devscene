#!/usr/bin/env bash
# The one route to the toolchain of this repository's Python packages. Every Python command goes
# through this file so that it is spellable as a literal an unattended run can issue, e.g.
# `bash scripts/python-service.sh test tests/test_cli.py`.
#
# Hand-written, like `scripts/run-gates.sh`: not in the set `init --force` rewrites.
#
# The package table (`PACKAGES`, `package_row`) is closed: a package directory, repo-relative at the
# root, with the console script `run` invokes and the compose project prefix `container-test` uses.
# Its rows are `docs-retrieval-service` (`devscene-docs-retrieval`, `devscene-docs-retrieval-test`)
# and `graphscene` (no console script, no compose project).
#
# Sub-commands (paths and arguments are relative to the selected package's directory):
#   [--package <dir>]    selects a table row, before the sub-command; default
#                        `docs-retrieval-service`. A directory that is not a row is refused even
#                        when it holds a `pyproject.toml`.
#   lock                 uv lock — rewrite uv.lock. Provisioning; reaches the network.
#   sync [--with-models] uv sync --frozen with the dev group. Provisioning; reaches the network.
#                        Without the flag the `models` extra is NOT installed, and a plain `sync`
#                        after a `--with-models` one removes it again.
#   provision            uv sync --frozen with the dev group for every table row, in order; takes
#                        no argument and no `--package`. The bootstrap's step (`commands.depInstall`).
#                        Where `uv` is not on PATH it prints a SKIPPED line and exits 0, writing
#                        nothing, so a host without Python still bootstraps.
#   lint                 ruff check, then ruff format --check.
#   typecheck            mypy (strict, over src and tests).
#   test [path...]       pytest, paths forwarded verbatim; default the whole suite.
#   run [args...]        the row's console script, arguments forwarded verbatim.
#   container-test       the `container`-marked tests against a throwaway Postgres: starts only the
#                        compose `postgres` service under a per-checkout project name on a
#                        per-checkout loopback port, runs `pytest -m container -rs`, and removes that
#                        project with `down -v` on every exit path. Builds the image on first use.
#                        Its image build is the one step here that may reach the network.
# lint, typecheck, test, run and container-test's pytest go through
# `uv run --frozen --no-sync --no-cache`, so they never reach the network and never change the
# environment.
#
# Exit contract:
#   0  pass
#   1  the tool reported failure (any non-zero status from it, pytest's own 2-5 included),
#      container-test could not start its Postgres, or a `provision` sync failed
#   2  usage: missing or unknown sub-command, an unknown package, or a bad option, or `run` /
#      `container-test` on a row that has no console script / no compose project
#   3  not provisioned: `uv` is not on PATH, or no synced environment exists. Never from `provision`.
#   4  container-test only: SKIPPED, because `docker` is not on PATH. A loud skip, not a pass.
#
# WHERE IT WRITES. `.venv`, `.ruff_cache` and `.mypy_cache` sit under the package directory: per
# checkout by construction, ignored by the root `.gitignore`, and skipped by gate 6a. pytest writes
# no `.pytest_cache` for `docs-retrieval-service` or `graphscene` (each one's `pyproject.toml`
# `addopts` carries `-p no:cacheprovider`); a row whose package leaves it on gets one there, covered
# the same way.
# The legs' `--no-cache` sends `uv`'s own writes to a temporary directory under $TMPDIR. Only `lock`,
# `sync` and `provision` touch the shared `uv` cache. A run copy's two sandboxes allow writes to that
# copy and to a temporary directory only (`scripts/launch-sandboxed-gates.sh` → THE BWRAP VECTOR).
#
# `provision`'s trust: it runs unsandboxed from `commands.depInstall` during `setup-worktree.sh`'s
# bootstrap, inside the residual that script's header names (THE RESIDUAL `--target` DOES NOT CLOSE).
#
# `commands.depInstall` tests for the next line with `grep -qx`, so a checkout whose wrapper predates
# `provision` still bootstraps. Do not reword or remove it while `provision` exists.
# PROVIDES: provision
#
# Deliberately no `-e`: each failure is mapped onto the exit contract above.
set -uo pipefail

PACKAGES="docs-retrieval-service graphscene"
DEFAULT_PACKAGE="docs-retrieval-service"

# Sets the row's fields; returns 1 for a directory that is not a row. An empty field means the row
# does not serve that sub-command.
package_row() {
  case "$1" in
    docs-retrieval-service)
      row_console_script="devscene-docs-retrieval"
      row_compose_prefix="devscene-docs-retrieval-test"
      ;;
    graphscene)
      row_console_script=""
      row_compose_prefix=""
      ;;
    *)
      return 1
      ;;
  esac
}

usage() {
  echo "usage: bash scripts/python-service.sh [--package <dir>] <lock|sync [--with-models]|provision|lint|typecheck|test [path...]|run [args...]|container-test>" >&2
}

package_list() {
  local list="" row
  for row in $PACKAGES; do
    list="${list:+$list, }$row"
  done
  printf '%s' "$list"
}

package="$DEFAULT_PACKAGE"
package_given=0
if [ "$#" -gt 0 ] && [ "$1" = "--package" ]; then
  package_given=1
  package="${2-}"
  if [ "$#" -lt 2 ] || ! package_row "$package"; then
    echo "python-service: unknown package '${package}'; the packages are: $(package_list)" >&2
    usage
    exit 2
  fi
  shift 2
fi
package_row "$package"

if [ "$#" -eq 0 ]; then
  echo "python-service: missing sub-command" >&2
  usage
  exit 2
fi

command_name="$1"
shift

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(git -C "$script_dir" rev-parse --show-toplevel 2>/dev/null)"
if [ -z "$repo_root" ]; then
  echo "python-service: could not resolve ${package}/ from '${script_dir}' (is git on PATH?)" >&2
  exit 1
fi

export PYTHONDONTWRITEBYTECODE=1

export_locations() {
  export UV_PROJECT_ENVIRONMENT="$repo_root/$1/.venv"
  export RUFF_CACHE_DIR="$repo_root/$1/.ruff_cache"
  export MYPY_CACHE_DIR="$repo_root/$1/.mypy_cache"
}

require_uv() {
  if ! command -v uv >/dev/null 2>&1; then
    echo "python-service: not provisioned: uv is not on PATH; install uv, then run bash scripts/python-service.sh provision outside the sandbox (a run copy's bootstrap runs it)" >&2
    exit 3
  fi
}

require_env() {
  require_uv
  if [ ! -f "$UV_PROJECT_ENVIRONMENT/pyvenv.cfg" ]; then
    echo "python-service: not provisioned: no synced environment at ${UV_PROJECT_ENVIRONMENT}; run bash scripts/python-service.sh provision outside the sandbox (a run copy's bootstrap runs it)" >&2
    exit 3
  fi
}

# Map any non-zero tool status onto the contract's `1`.
graded() {
  if "$@"; then
    exit 0
  fi
  exit 1
}

# Before the per-package `cd`: `provision` covers every row, each in its own subshell.
if [ "$command_name" = "provision" ]; then
  if [ "$#" -ne 0 ] || [ "$package_given" -eq 1 ]; then usage; exit 2; fi
  if ! command -v uv >/dev/null 2>&1; then
    echo "python-service: provision: SKIPPED — uv is not on PATH; gate 13 grades BLOCKED until uv is installed and provision is re-run" >&2
    exit 0
  fi
  provision_status=0
  for row in $PACKAGES; do
    (
      cd "$repo_root/$row" || exit 1
      export_locations "$row"
      uv sync --frozen --group dev
    )
    row_status=$?
    if [ "$row_status" -eq 0 ]; then
      echo "python-service: provisioned ${row}"
    else
      echo "python-service: provision: ${row} failed (exit ${row_status})" >&2
      provision_status=1
    fi
  done
  exit "$provision_status"
fi

if ! cd "$repo_root/$package"; then
  echo "python-service: no ${package}/ directory under the repository root '${repo_root}'" >&2
  exit 1
fi
export_locations "$package"

case "$command_name" in
  lock)
    if [ "$#" -ne 0 ]; then usage; exit 2; fi
    require_uv
    graded uv lock
    ;;
  sync)
    extra=()
    if [ "$#" -eq 1 ] && [ "$1" = "--with-models" ]; then
      extra=(--extra models)
    elif [ "$#" -ne 0 ]; then
      usage
      exit 2
    fi
    require_uv
    graded uv sync --frozen --group dev ${extra[@]+"${extra[@]}"}
    ;;
  lint)
    if [ "$#" -ne 0 ]; then usage; exit 2; fi
    require_env
    status=0
    uv run --frozen --no-sync --no-cache ruff check || status=1
    uv run --frozen --no-sync --no-cache ruff format --check || status=1
    exit "$status"
    ;;
  typecheck)
    if [ "$#" -ne 0 ]; then usage; exit 2; fi
    require_env
    graded uv run --frozen --no-sync --no-cache mypy
    ;;
  test)
    require_env
    graded uv run --frozen --no-sync --no-cache pytest "$@"
    ;;
  run)
    if [ -z "$row_console_script" ]; then
      echo "python-service: package '${package}' has no console script" >&2
      usage
      exit 2
    fi
    require_env
    graded uv run --frozen --no-sync --no-cache "$row_console_script" "$@"
    ;;
  container-test)
    if [ "$#" -ne 0 ]; then usage; exit 2; fi
    if [ -z "$row_compose_prefix" ]; then
      echo "python-service: package '${package}' has no container tests" >&2
      usage
      exit 2
    fi
    if ! command -v docker >/dev/null 2>&1; then
      echo "container-test: SKIPPED — docker is not on PATH; the container gate needs Docker" >&2
      exit 4
    fi
    require_env
    checkout_key="$(printf '%s' "$repo_root" | cksum | awk '{print $1}')"
    compose_file="$repo_root/$package/compose.yaml"
    project="${row_compose_prefix}-$checkout_key"
    # Off the compose default 5432, and per checkout, so two worktrees' runs do not collide.
    export DEVSCENE_DOCS_RETRIEVAL_PG_PORT="$((40000 + checkout_key % 20000))"
    teardown() {
      if ! docker compose -f "$compose_file" -p "$project" down -v >/dev/null 2>&1; then
        echo "container-test: warning: 'docker compose -p ${project} down -v' failed; remove that project by hand" >&2
      fi
    }
    # Set before `up`, so a failed or interrupted start is torn down too; INT and TERM route
    # through `exit` so the EXIT trap fires on them.
    trap teardown EXIT
    trap 'exit 130' INT
    trap 'exit 143' TERM
    if ! docker compose -f "$compose_file" -p "$project" up -d --wait postgres; then
      echo "container-test: could not start the compose postgres service (project ${project})" >&2
      exit 1
    fi
    # The credentials and database are compose.yaml's `postgres` service environment.
    export DEVSCENE_DOCS_RETRIEVAL_TEST_DATABASE_URL="postgresql://devscene:devscene@127.0.0.1:${DEVSCENE_DOCS_RETRIEVAL_PG_PORT}/docs_retrieval"
    if uv run --frozen --no-sync --no-cache pytest -m container -rs; then
      exit 0
    fi
    exit 1
    ;;
  *)
    echo "python-service: unknown sub-command '${command_name}'" >&2
    usage
    exit 2
    ;;
esac
