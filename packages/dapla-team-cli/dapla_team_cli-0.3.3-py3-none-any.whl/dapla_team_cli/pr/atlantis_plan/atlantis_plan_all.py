"""Functions for applying atlantis changes."""

from rich import print  # noqa: W0622

from dapla_team_cli.github import get_pr
from dapla_team_cli.pr.batch_handler import batch_handler
from dapla_team_cli.pr.const import RepoState
from dapla_team_cli.pr.const import State
from dapla_team_cli.pr.const import Status
from dapla_team_cli.pr.probe.probe_workflows import probe_workflows
from dapla_team_cli.pr.rich_check import RichSuccess


@batch_handler
def atlantis_plan(state: State, max_plans: int) -> None:
    """Comments atlantis plan on all PRs where plans are failed or do not exist."""
    print("[magenta]Probing succeeded workflows and plans for repositories..")
    probe_workflows(state)
    commented_plans = 0

    print("\n\n[cyan]Commenting 'atlantis plan' in unplanned repositories")
    for repo in state.repos.values():
        if commented_plans >= max_plans:
            print("[blue]Max plans reached, stopping")
            break

        if _do_atlantis_plan(repo):
            commented_plans += 1


def _do_atlantis_plan(repo: RepoState) -> bool:
    print(f"[bold magenta]{repo.name}")

    if pr := get_pr(repo.pr.number, repo.name):
        pr.create_issue_comment("atlantis plan")
        print(RichSuccess(message="Atlantis plan commented"))
        repo.workflow.atlantis_plan = Status.STARTED
        return True
    else:
        # Don't continue if we can't find the issue
        return False
