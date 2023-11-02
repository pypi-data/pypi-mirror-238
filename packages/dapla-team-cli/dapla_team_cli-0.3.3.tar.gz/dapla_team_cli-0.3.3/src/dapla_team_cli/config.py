"""CLI-wide config variables."""
import math
import os
import time
from distutils.version import LooseVersion
from importlib.metadata import version
from pathlib import Path
from sys import platform

import requests
import typer
from rich.console import Console
from rich.style import Style


TIMESTAMP_DIFFERENCE: int = 60 * 60 * 24 * 5

console = Console(highlight=False)

styles = {
    "normal": Style(blink=True, bold=True),
    "error": Style(color="red", blink=True, bold=True),
    "success": Style(color="green", blink=True, bold=True),
    "warning": Style(color="dark_orange3", blink=True, bold=True),
}


def get_config_folder_path(tmp: bool = False) -> str:
    """Gets the config folder path on current machine.

    Args:
        tmp: A true/false flag that determines whether function should return temporary folder or base folder.

    Raises:
        Exception: If the platform is not linux, darwin (macos) or windows.

    Returns:
        The config folder path, or temporary folder path inside config folder.
    """
    if platform in ("linux", "darwin"):
        config_folder_path = Path.home() / ".config/dapla-team-cli"
    elif platform == "win32":
        username = os.getlogin()
        config_folder_path = Path(rf"C:\Users\{username}\AppData\dapla-team-cli")
    else:
        raise RuntimeError("Unknown platform. The CLI only supports Unix and Windows based platforms.")

    if not os.path.exists(config_folder_path):
        os.makedirs(config_folder_path)

    if tmp:
        tmp_path = config_folder_path / "tmp"

        if not os.path.exists(tmp_path):
            os.makedirs(tmp_path)

        return str(tmp_path)

    return str(config_folder_path)


__version__ = version("dapla_team_cli")


def version_cb(value: bool) -> None:
    """Prints the current version of dapla-team-cli."""
    if value:
        print(f"dapla-team-cli {__version__}")
        raise typer.Exit()


def get_version_file_content() -> str:
    """Reads a txt-file, fetching a stored timestamp.

    :return The content in the txt file.
    """
    txt_path: Path = Path(get_config_folder_path()) / "last_update_check.txt"
    content: str = ""

    if os.path.exists(txt_path) is False:
        f = open(txt_path, "w")
        f.close()

    with open(txt_path) as f:
        content = f.read()

    return content


def has_recently_checked_version() -> bool:
    """Checks if the current version should be controlled by accessing a text file.

    Inside the file a timestamp for the last performed version check is stored.

    The function takes use of the constant TIMESTAMP_DIFFERENCE. This is the time threshold in milliseconds
    before a new check should be performed.

    :return: A boolean variable. False if a check should be performed, or True if not.
    """
    txt_path: Path = Path(get_config_folder_path()) / "last_update_check.txt"
    content: str = get_version_file_content()
    epoch_time: int = 0

    if content != "":
        epoch_time = int(content)

    curr_epoch_time: int = math.floor(time.time())

    if (curr_epoch_time - epoch_time) > TIMESTAMP_DIFFERENCE:
        with open(txt_path, "w") as f:
            f.write(str(curr_epoch_time))

        return False

    return True


def warn_if_newer_version() -> None:
    """Prints a warning if there exists a newer version on PyPi."""
    if not has_recently_checked_version():
        installed_version = LooseVersion(__version__)
        pypi_url = "https://pypi.org/pypi/dapla-team-cli/json"
        response = requests.get(pypi_url, timeout=10)
        latest_version = max(LooseVersion(ver) for ver in response.json()["releases"].keys())

        if latest_version > installed_version:
            console.print(
                f"""⚠️[yellow]  WARNING: There is a newer version available.
                Current version={installed_version}, latest version={latest_version}"""
            )


try:
    __IPYTHON__  # type: ignore [name-defined]
    in_ipython_session = True
except NameError:
    in_ipython_session = False

DAPLA_TEAM_API_BASE = os.getenv("DAPLA_TEAM_API_BASE_URL", "https://team-api.dapla-staging.ssb.no")
