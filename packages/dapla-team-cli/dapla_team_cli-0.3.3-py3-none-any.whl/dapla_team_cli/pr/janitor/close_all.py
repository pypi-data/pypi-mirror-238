"""Functions for janitor sub-command. Cleanup related commands."""

import sys
from typing import Optional

import questionary
from github.Organization import Organization
from rich import print  # noqa: W0622

from dapla_team_cli.github import delete_remote_branch
from dapla_team_cli.github import get_github_org
from dapla_team_cli.github import get_pr
from dapla_team_cli.pr.batch_handler import batch_handler
from dapla_team_cli.pr.const import RepoState
from dapla_team_cli.pr.const import State
from dapla_team_cli.pr.rich_check import RichSuccess
from dapla_team_cli.pr.rich_check import RichWarning
from dapla_team_cli.pr.state.state_commands import show_state


@batch_handler
def close_all(state: State, keep_remote_branches: bool) -> None:
    """Closes all opened PRs in state file."""
    print(RichWarning(message="The following pull requests will be closed:"))
    show_state(state)
    answer = questionary.confirm("Are you sure you want to close all listed pull requests?").ask()
    if not answer:
        sys.exit(1)

    _close_all_prs(state, keep_remote_branches)


def _close_all_prs(state: State, keep_remote_branches: bool) -> None:
    print("\n\n[cyan]Closing pull requests..")
    for repo in state.repos.values():
        _close_pr(repo)

    if not keep_remote_branches:
        print("\n[cyan]Deleting all remote branches..")
        for repo in state.repos.values():
            _delete_remote_branch(repo)


def _close_pr(repo: RepoState) -> None:
    print(f"[bold magenta]{repo.name}")
    if pr := get_pr(repo.pr.number, repo.name):
        pr.edit(state="closed")
        print(RichSuccess(message="Closed PR"))


def _delete_remote_branch(repo: RepoState, gh_org: Optional[Organization] = None) -> None:
    if gh_org is None:
        gh_org = get_github_org()
    print(f"[bold magenta]{repo.name}")
    branch = repo.pr.branch_name
    if branch is not None:
        delete_remote_branch(branch, gh_org.get_repo(repo.name))
    print(RichSuccess(message=f"Deleted remote branch {branch}"))
