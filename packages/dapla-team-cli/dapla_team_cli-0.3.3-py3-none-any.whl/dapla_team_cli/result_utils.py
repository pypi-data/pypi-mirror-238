"""Prints results from API responses."""

import sys
from typing import Any
from typing import Dict

from returns.result import Result
from rich import print


def fail(message: str) -> None:
    """Exit with a message if a Failure occurs."""
    print(f"❌[red] ERROR: \n {message}")
    sys.exit(1)


def success(result: Result[Dict[str, Any], str]) -> None:
    """Exit with a success message."""
    print("✅[green] Successfully completed")
