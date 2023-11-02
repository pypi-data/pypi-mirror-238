"""Functions for merge command."""

import sys

import questionary
from rich import print  # noqa: W0622

from dapla_team_cli.github import delete_remote_branch
from dapla_team_cli.github import get_pr
from dapla_team_cli.github import get_repo
from dapla_team_cli.pr.batch_handler import batch_handler
from dapla_team_cli.pr.const import RepoState
from dapla_team_cli.pr.const import State
from dapla_team_cli.pr.const import Status
from dapla_team_cli.pr.probe.probe_atlantis_apply import probe_atlantis_apply
from dapla_team_cli.pr.rich_check import SKIPPING
from dapla_team_cli.pr.rich_check import RichFailure
from dapla_team_cli.pr.rich_check import RichSuccess
from dapla_team_cli.pr.rich_check import RichWarning


@batch_handler
def merge_all(state: State, override: bool) -> None:  # noqa: 3901
    """Merges all open Pull requests in state file."""
    probe_atlantis_apply(state)

    answer = questionary.confirm("Do you want to proceed with merge?").ask()
    if not answer:
        sys.exit(1)

    print("\n\n[cyan]Merging all repositories")
    for repo in state.repos.values():
        print(f"[bold magenta]{repo.name}")
        if _check_override(repo, override):
            _do_merge(repo)


def _check_override(repo: RepoState, override: bool) -> bool:
    """Checks if PR has been merged with optional override."""
    if repo.workflow.merged == Status.SUCCESS:
        print(RichWarning(message="Repository has been merged"))
        if not override:
            print(SKIPPING)
            return False
        else:
            answer = questionary.confirm("Do you want to open attempt a merge anyway?").ask()
            if not answer:
                print(SKIPPING)
                return False

    return True


def _do_merge(repo: RepoState) -> None:
    """Performs a merge given a single repository."""
    if not (pr := get_pr(repo.pr.number, repo.name)):
        return

    gh_repo = get_repo(repo.name)
    if not pr.mergeable:
        print(RichFailure(message="PR has not been approved"))
        print(RichFailure(message="Skipping.."))
        return

    merge_status = pr.merge(merge_method="squash")
    if merge_status.merged:
        repo.workflow.merged = Status.SUCCESS
        branch = repo.pr.branch_name
        print(RichSuccess(message="Merged branch"))
        if branch is not None:
            delete_remote_branch(branch, gh_repo)
        print(RichSuccess(message="Deleted remote branch"))
    else:
        print(RichFailure(message=f"Merge failed with message: {merge_status.message}"))
        repo.workflow.merged = Status.FAIL
