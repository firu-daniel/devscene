### 3. The exit contract leaves out `--help`, which exits `0` with non-JSON text on stdout

**Files:**
- `graphscene/src/graphscene/facade/cli.py` (module docstring) — "every command prints one ASCII-only JSON document on stdout"
- `graphscene/README.md` (`## The command line`) — "| `0` | The graph loaded (`check`), or the walk returned an action. |"

Two places state the command line's contract: the module docstring's *"The rule:"* paragraph and the README's exit table. Both say that every command prints one JSON document on stdout, and that exit `0` means *"the graph loaded (`check`), or the walk returned an action"*. Neither is true of `graphscene --help` or `graphscene <command> --help`. `_Parser.print_help` writes argparse's help text to stdout, and `_Parser.exit(0)` returns status `0`. `graphscene/tests/facade/test_cli.py` → `test_help_goes_to_stdout_and_exits_0` asserts exactly this behaviour. So the code and its test agree with each other but not with the documented contract. A host that treats exit `0` as "stdout is a JSON document" fails to parse the help text. The behaviour itself is reasonable, so the fix is to the two contract statements, not to the code.

**Fix:**

1. In `graphscene/src/graphscene/facade/cli.py`, change the module docstring's sentence `The rule: every command prints one ASCII-only JSON document on stdout, followed by a newline, and exits by this contract:` to:

   ```
   The rule: every command prints one ASCII-only JSON document on stdout, followed by a newline, and
   exits by this contract; `--help`, on the command line or on a command, is the one exception: it
   prints argparse's help text on stdout and exits `0`.
   ```

   Keep the bullet list that follows unchanged. Wrap the text at 100 columns.

2. In `graphscene/README.md` → `## The command line`, directly after the exit table, add this sentence:

   ```
   `--help`, on `graphscene` or on any command, is the one exception to the one-JSON-document rule: it prints the help text on stdout and exits `0`.
   ```

This changes only a docstring and README prose, so no test changes and the fix runs no test.
