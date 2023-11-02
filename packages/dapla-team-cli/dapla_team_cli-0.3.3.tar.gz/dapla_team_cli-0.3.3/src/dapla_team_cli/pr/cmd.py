"""Batch update commands.

Commands invoked by dpteam batch <some-command> are defined here.
"""

import warnings

import typer

import dapla_team_cli.pr.janitor.cmd as janitor
import dapla_team_cli.pr.probe.cmd as probe
import dapla_team_cli.pr.state.cmd as current_state
from dapla_team_cli.pr.approve.cmd import approve
from dapla_team_cli.pr.atlantis_apply.cmd import apply
from dapla_team_cli.pr.atlantis_plan.cmd import plan
from dapla_team_cli.pr.merge.cmd import merge
from dapla_team_cli.pr.open.cmd import open
from dapla_team_cli.pr.ready.cmd import ready


# app = typer.Typer(name="batch", help="Batch update github repos.", no_args_is_help=True)
app = typer.Typer(no_args_is_help=True)


# Remove gcloud warnings under development
warnings.filterwarnings(
    "ignore", message="Your application has authenticated using end user credentials from Google Cloud SDK without a quota project."
)


@app.callback()
def pr() -> None:
    """Do PR operations."""
    pass


app.command()(approve)
app.command()(open)
app.command()(merge)
app.command()(apply)
app.command()(plan)
app.command()(ready)
app.add_typer(janitor.app)
app.add_typer(current_state.app)
app.add_typer(probe.app)
