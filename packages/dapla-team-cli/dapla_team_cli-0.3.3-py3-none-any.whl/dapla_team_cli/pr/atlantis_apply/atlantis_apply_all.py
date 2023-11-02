"""Functions for applying atlantis changes."""

import sys

import questionary
from rich import print  # noqa: W0622

from dapla_team_cli.github import get_pr
from dapla_team_cli.pr.batch_handler import batch_handler
from dapla_team_cli.pr.const import RepoState
from dapla_team_cli.pr.const import State
from dapla_team_cli.pr.const import Status
from dapla_team_cli.pr.probe.probe_workflows import probe_workflows
from dapla_team_cli.pr.rich_check import SKIPPING
from dapla_team_cli.pr.rich_check import RichSuccess
from dapla_team_cli.pr.rich_check import RichWarning


@batch_handler
def atlantis_apply(state: State, max_apply: int) -> None:  # noqa: 3901
    """Comments atlantis apply on all uncommented and open PRs."""
    print("[magenta]Probing succeeded workflows and plans for repositories..")
    probe_workflows(state)

    answer = questionary.confirm("Do you want to proceed with 'atlantis apply'?").ask()
    if not answer:
        sys.exit(1)

    current_apply = 0
    print("\n\n[cyan]Commenting 'atlantis apply' in repositories")
    for repo in state.repos.values():
        if current_apply >= max_apply:
            print("[blue]Max applies commented, stopping")
            break

        print(f"[bold magenta]{repo.name}")
        if _do_atlantis_apply(repo):
            current_apply += 1


def _do_atlantis_apply(repo: RepoState) -> bool:
    """Comments 'atlantis apply' on a single repository."""
    # Should check if issue exists
    pr = get_pr(repo.pr.number, repo.name)
    if pr and _should_run_atlantis_apply(repo):
        pr.create_issue_comment("atlantis apply")
        repo.workflow.atlantis_apply = Status.STARTED
        print(RichSuccess(message="Atlantis apply comment created"))
        return True
    else:
        return False


def _should_run_atlantis_apply(repo: RepoState) -> bool:
    """Checks whether atlantis apply should be run."""
    if repo.workflow.atlantis_plan == Status.NOT_STARTED:
        print(RichWarning(message="Plan not found for PR"))
        print(SKIPPING)
        return False

    if repo.workflow.approved == Status.NOT_STARTED:
        print(RichWarning(message="PR was found but not approved"))
        print(SKIPPING)
        return False

    match repo.workflow.atlantis_apply:
        case Status.FAIL:
            print(RichWarning(message="Apply has been ran previously but failed, commenting apply again"))
        case Status.STARTED:
            print(RichWarning(message="Have commented 'atlantis apply' previously, but no response by atlantis has been recorded."))
            print(SKIPPING)
            return False
        case Status.SUCCESS:
            print(RichWarning(message="Successful apply found in this repository"))
            print(SKIPPING)
            return False
    return True
