"""Command-line interface.

CLI commands are generally structured according to this convention:
<root> <command-group> <command>

Example:
    Given the command ´dpteam tf iam-bindings´ then...
    ´dpteam´ is the root (CLI name)
    ´tf´ is the command group and
    ´iam-bindings´ is the actual command

Command groups must be mounted here to become available.

Each sub-command's modules should be grouped into a separate python package.
"""
import logging
from enum import Enum
from threading import Thread
from typing import Optional

import typer

import dapla_team_cli.auth.cmd as auth
import dapla_team_cli.changelogs.cmd as changelogs
import dapla_team_cli.doctor.cmd as doctor
import dapla_team_cli.groups.cmd as groups
import dapla_team_cli.pr.cmd as pr
import dapla_team_cli.secrets.cmd as secrets
import dapla_team_cli.tf.cmd as tf
import dapla_team_cli.transfer_service.cmd as ts
from dapla_team_cli.config import in_ipython_session
from dapla_team_cli.config import version_cb
from dapla_team_cli.config import warn_if_newer_version


app = typer.Typer(no_args_is_help=True, pretty_exceptions_show_locals=False)
logging.basicConfig()


class LogLevel(str, Enum):
    """Logging levels for dapla-team-cli."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


def set_loglevel(loglevel: LogLevel) -> None:
    """Initialize dpteam logger and set logging level."""
    logger = logging.getLogger("dpteam")
    logger.setLevel(getattr(logging, loglevel.value))
    logger.debug("Set logging level to %s", loglevel)


@app.callback()
def dpteam(
    _version: Optional[bool] = typer.Option(  # noqa: B008  # pylint: disable=unused-argument
        None, "--version", callback=version_cb, is_eager=True
    ),
    loglevel: LogLevel = typer.Option(  # noqa: B008  # pylint: disable=unused-argument
        LogLevel.WARN, "--loglevel", "-v", callback=set_loglevel, is_eager=True, case_sensitive=False
    ),
) -> None:
    """Work seamlessly with Dapla teams from the command line.

    \b

    Use `dpteam <command> <subcommand> --help` for more information about a command.

    For an introduction to Dapla Team CLI, read the guide at https://statisticsnorway.github.io/dapla-team-cli/guide
    """
    pass


def main() -> None:
    """Main function of dpteam."""
    app()


app.add_typer(tf.app)
app.add_typer(secrets.app)
app.add_typer(auth.app)
app.add_typer(groups.app)
if not in_ipython_session:  # Batch update should only be used outside of Jupyter
    app.add_typer(pr.app)
    app.add_typer(ts.app)
app.command()(doctor.doctor)
app.command("changelogs")(changelogs.print_changelogs)

warn_thread = Thread(target=warn_if_newer_version)
warn_thread.start()

if __name__ == "__main__":
    main()

warn_thread.join()
