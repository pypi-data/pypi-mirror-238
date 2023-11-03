import glob
import os
import sys
from typing import List
from typing import Tuple

import click
import pytest

from tecton.cli import cli_utils
from tecton.cli import printer
from tecton.cli.command import TectonCommand
from tecton.cli.repo_utils import get_tecton_objects
from tecton_core import repo_file_handler


def get_test_paths(repo_root) -> List[str]:
    # Be _very_ careful updating this:
    #    `glob.glob` does bash-style globbing (ignores hidden files)
    #    `pathlib.Path.glob` does _not_ do bash-style glob (it shows hidden)
    #
    # Ignoring hidden files is a very important expectation for our usage of
    # pytest. Otherwise, we may test files that user does not intend us to
    # (like in their .git or .tox directories).
    #
    # NOTE: This won't filter out hidden files for Windows. Potentially:
    #    `bool(os.stat(filepath).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN)`
    # would filter hidden files for Windows, but this would need some testing.
    candidate_test_files = glob.iglob(f"{repo_root}/**/tests/**/*.py", recursive=True)

    VIRTUAL_ENV = os.getenv("VIRTUAL_ENV")
    if VIRTUAL_ENV:
        return list(filter(lambda f: not f.startswith(VIRTUAL_ENV), candidate_test_files))

    return list(candidate_test_files)


def run_tests(debug: bool, pytest_extra_args: Tuple[str, ...] = ()):
    repo_root = repo_file_handler._maybe_get_repo_root()
    if repo_root is None:
        printer.safe_print("Tecton tests must be run from a feature repo initialized using 'tecton init'!")
        sys.exit(1)

    get_tecton_objects(debug)

    tests = get_test_paths(repo_root)
    if len(tests) == 0:
        printer.safe_print("⚠️  Running Tests: No tests found.")
        return

    os.chdir(repo_root)
    args = ["--disable-pytest-warnings", "-s", *tests]

    if pytest_extra_args:
        args.extend(pytest_extra_args)

    printer.safe_print("🏃 Running Tests")
    exitcode = pytest.main(args)

    if exitcode == 5:
        # https://docs.pytest.org/en/stable/usage.html#possible-exit-codes
        printer.safe_print("⚠️  Running Tests: No tests found.")
        return None
    elif exitcode != 0:
        printer.safe_print("⛔ Running Tests: Tests failed :(")
        sys.exit(1)
    else:
        printer.safe_print("✅ Running Tests: Tests passed!")


@click.command(uses_workspace=True, requires_auth=False, cls=TectonCommand)
@click.argument("pytest_extra_args", nargs=-1)
@click.pass_context
def test(ctx, pytest_extra_args: Tuple[str, ...]):
    """Run Tecton tests.
    USAGE:
    `tecton test`: run all tests (using PyTest) in a file that matches glob("TECTON_REPO_ROOT/**/tests/**/*.py")
    `tecton test -- -k "test_name"`: same as above, but passes the `-k "test_name"` args to the PyTest command.
    """
    # NOTE: if a user wanted to do the equivalent of a `pytest -k "test_name"`
    # they could do `tecton test -- -k "test_name"`.
    run_tests(debug=cli_utils.get_debug(ctx), pytest_extra_args=pytest_extra_args)
