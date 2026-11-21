#!/usr/bin/env bash
# The one route to the toolchain of this repository's Python packages. Every Python command goes
# through this file so that it is spellable as a literal an unattended run can issue, e.g.
# `bash scripts/python-service.sh test tests/test_cli.py`.
#
# Hand-written, like `scripts/run-gates.sh`: not in the set `init --force` rewrites.
#
# The package table (`PACKAGES`, `package_row`) is closed: a package directory, repo-relative at the
# root, with the console script `run` invokes, the compose project prefix `container-test` uses and
# the extra `sync --with-models` installs. Its rows are `docs-retrieval-service`
# (`devscene-docs-retrieval`, `devscene-docs-retrieval-test`, `models`) and `graphscene` (no console
# script, no compose project, no `models` extra).
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
#   probe <scratch-file> [args...]
#                        python on one `.py` file under `<state_dir>/scratch/`, in the selected
#                        row's synced environment, from the package directory. The file's path is
#                        relative to the REPOSITORY ROOT, or absolute — unlike every other verb's —
#                        and is judged by `hr_scratch_path_var`, the test `scratch-run.sh` applies.
#                        The remaining arguments are forwarded verbatim.
#   check                `lint`, then `typecheck`, for every table row in order, each leg run as
#                        `bash <this file> --package <row> <leg>`; prints one stdout line per leg,
#                        `python-service: check: <row> <leg> PASS|FAIL|BLOCKED` (exit 0 / 3 / any
#                        other), and runs every leg even after a failure. Takes no argument and no
#                        `--package`.
# lint, typecheck, test, run, probe and container-test's pytest go through
# `uv run --frozen --no-sync --no-cache`, so they never reach the network and never change the
# environment.
#
# Exit contract:
#   0  pass
#   1  the tool reported failure (any non-zero status from it, pytest's own 2-5 included),
#      container-test could not start its Postgres, a `provision` sync failed, a `check` leg
#      failed, or `probe` could not read `lib/harness-run-lib.sh`
#   2  usage: missing or unknown sub-command, an unknown package, or a bad option, or `run` /
#      `container-test` on a row that has no console script / no compose project, or
#      `sync --with-models` on a row that has no `models` extra, or a `probe` path refused
#   3  not provisioned: `uv` is not on PATH, or no synced environment exists. Never from `provision`.
#      From `check`: no leg failed and at least one was BLOCKED.
#   4  container-test only: SKIPPED, because `docker` is not on PATH. A loud skip, not a pass.
# `probe` is exempt from mapping onto `1`: once its file runs, the file's own exit status passes
# through unmodified, so a probe may exit 2 or 3 itself. What tells a refusal apart is its stderr
# line `python-service: probe: <reason>`, as `scratch-run.sh`'s header states for its own codes.
#
# WHERE THE REPOSITORY IS. Placed by `hr_script_root` (`scripts/lib/harness-run-lib.sh`) when that
# library is readable beside this file (F15: inside a bubblewrap sandbox, git's discovery from
# `scripts/` dies on the `<scriptsDir>/.git` placeholder); by the bare `git rev-parse` otherwise.
#
# WHAT probe IS FOR, AND WHAT IT DOES NOT CONTAIN. An agent's language probe that must import what a
# package declares — which `scratch-run.sh` cannot give it: that table's single-token interpreter
# cannot name a package's environment (`scripts/scratch-run.sh` → WHAT THAT COSTS). One file and
# no inline program: no `-c`, and a first argument starting with `-` is refused. The fence is over
# WHICH FILE RUNS and nothing it does; it runs inside the session's sandbox. `<state_dir>/scratch/`
# is gitignored by its contents, so nothing run from there reaches a commit.
#
# WHO RUNS lock, sync AND provision. An agent can reach all three: the script-allowlist guard
# auto-allows this file. They stay callable from a run because inside its sandbox they fail closed
# (no network, the shared `uv` cache not writable) and change nothing outside the copy, and because
# `provision` is run legitimately inside a run copy by its bootstrap (`commands.depInstall`). No
# record the session cannot write tells that caller from an agent, and an environment variable is
# not such a record (`harness-runs/lessons.md` → `## Trust checks`), so none is refused here.
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
      row_models_extra="models"
      ;;
    graphscene)
      row_console_script=""
      row_compose_prefix=""
      row_models_extra=""
      ;;
    *)
      return 1
      ;;
  esac
}

usage() {
  echo "usage: bash scripts/python-service.sh [--package <dir>] <lock|sync [--with-models]|provision|lint|typecheck|test [path...]|run [args...]|container-test|probe <scratch-file> [args...]|check>" >&2
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
hr_lib="$script_dir/lib/harness-run-lib.sh"
if [ -r "$hr_lib" ]; then
  # shellcheck source=lib/harness-run-lib.sh
  . "$hr_lib"
  hr_lib_loaded=1
  repo_root="$(hr_script_root "$script_dir")"
else
  hr_lib_loaded=0
  repo_root="$(git -C "$script_dir" rev-parse --show-toplevel 2>/dev/null)"
fi
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

# Before the per-package `cd`: each leg is this file's own gate leg, run as a child.
if [ "$command_name" = "check" ]; then
  if [ "$#" -ne 0 ] || [ "$package_given" -eq 1 ]; then usage; exit 2; fi
  check_failed=0
  check_blocked=0
  for row in $PACKAGES; do
    for leg in lint typecheck; do
      bash "$script_dir/python-service.sh" --package "$row" "$leg"
      leg_status=$?
      if [ "$leg_status" -eq 0 ]; then
        verdict=PASS
      elif [ "$leg_status" -eq 3 ]; then
        verdict=BLOCKED
        check_blocked=1
      else
        verdict=FAIL
        check_failed=1
      fi
      echo "python-service: check: ${row} ${leg} ${verdict}"
    done
  done
  if [ "$check_failed" -eq 1 ]; then exit 1; fi
  if [ "$check_blocked" -eq 1 ]; then exit 3; fi
  exit 0
fi

# Before the per-package `cd`: a probe's path is repository-relative, so it is judged here.
if [ "$command_name" = "probe" ]; then
  if [ "$#" -lt 1 ] || [ -z "$1" ]; then
    echo "python-service: probe: no file argument" >&2
    usage
    exit 2
  fi
  requested="$1"
  shift
  case "$requested" in
    -*)
      echo "python-service: probe: '${requested}' is an option, not a file — refusing, a probe takes no inline program" >&2
      exit 2
      ;;
  esac
  if [ "$hr_lib_loaded" -ne 1 ]; then
    echo "python-service: probe: cannot read ${hr_lib} — refusing to run anything" >&2
    exit 1
  fi
  hr_scratch_path_var "$repo_root" "$requested"
  case "$HR_SCRATCH_WHY" in
    "") ;;
    dotdot)
      echo "python-service: probe: '${requested}' carries '..' — refusing, a scratch path names no parent" >&2
      exit 2
      ;;
    charset)
      echo "python-service: probe: '${requested}' carries a character outside A-Za-z0-9._/- — refusing" >&2
      exit 2
      ;;
    outside)
      echo "python-service: probe: '${requested}' resolves to '${HR_SCRATCH_PARENT}', outside '${HR_SCRATCH_DIR}' — refusing" >&2
      exit 2
      ;;
    itself)
      echo "python-service: probe: '${requested}' names the scratch directory itself — refusing" >&2
      exit 2
      ;;
    symlink)
      echo "python-service: probe: '${requested}' is a symlink — refusing, its target is outside this script's judgement" >&2
      exit 2
      ;;
    no-parent)
      echo "python-service: probe: '${requested}' names no existing directory under '${repo_root}'" >&2
      exit 2
      ;;
    no-config)
      echo "python-service: probe: cannot resolve '${repo_root}/devscene.config.json' — refusing to run anything" >&2
      exit 2
      ;;
    no-scratch)
      echo "python-service: probe: '$(hr_state_path "$repo_root" "$HR_SCRATCH_SUBDIR")' does not exist — re-run 'init' to materialize the state tree" >&2
      exit 2
      ;;
    *)
      echo "python-service: probe: no file argument" >&2
      usage
      exit 2
      ;;
  esac
  probe_target="$HR_SCRATCH_TARGET"
  case "${probe_target##*/}" in
    ?*.py) ;;
    *)
      echo "python-service: probe: '${probe_target##*/}' is not a .py file — refusing" >&2
      exit 2
      ;;
  esac
  if [ ! -f "$probe_target" ] || [ ! -r "$probe_target" ]; then
    echo "python-service: probe: '${probe_target}' is not a readable regular file" >&2
    exit 2
  fi
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
      if [ -z "$row_models_extra" ]; then
        echo "python-service: package '${package}' has no models extra" >&2
        usage
        exit 2
      fi
      extra=(--extra "$row_models_extra")
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
  probe)
    require_env
    # `exec`, not `graded`: the file's own status is the answer.
    exec uv run --frozen --no-sync --no-cache python "$probe_target" "$@"
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
