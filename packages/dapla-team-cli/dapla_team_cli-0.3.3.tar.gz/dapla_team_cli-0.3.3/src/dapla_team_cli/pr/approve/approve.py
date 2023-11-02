"""Commands for approving open PRs."""

import sys

import questionary
from github.GithubException import GithubException
from rich import print  # noqa: W0622

from dapla_team_cli.github import get_commit
from dapla_team_cli.github import get_pr
from dapla_team_cli.pr.batch_handler import batch_handler
from dapla_team_cli.pr.const import RepoState
from dapla_team_cli.pr.const import State
from dapla_team_cli.pr.const import Status
from dapla_team_cli.pr.probe.probe_workflows import probe_workflows
from dapla_team_cli.pr.rich_check import RichFailure
from dapla_team_cli.pr.rich_check import RichSuccess


@batch_handler
def approve_prs(state: State) -> None:  # noqa: C901
    """Approves all open PRs in state file."""
    print("Probing existing PRs..")
    probe_workflows(state)

    answer = questionary.confirm("Do you want to continue and approve PRs?").ask()
    if not answer:
        sys.exit(1)

    print("\n\n[cyan]Approving PRs..")
    for repo in state.repos.values():
        print(f"[bold magenta]{repo.name}")
        _do_approve(repo)


def _do_approve(repo: RepoState) -> None:
    """Approves PR for a single repository."""
    if pr := get_pr(repo.pr.number, repo.name):
        pr_commit = get_commit(pr.head.sha, repo.name)
        try:
            pr.create_review(commit=pr_commit, body="This is a batch-update approval", event="APPROVE")
        except GithubException as e:
            print(RichFailure(message=f"Github error: {e.data['errors'][0]}"))  # type: ignore
            repo.workflow.approved = Status.FAIL
        else:
            repo.workflow.approved = Status.SUCCESS
            print(RichSuccess(message="PR approved"))
