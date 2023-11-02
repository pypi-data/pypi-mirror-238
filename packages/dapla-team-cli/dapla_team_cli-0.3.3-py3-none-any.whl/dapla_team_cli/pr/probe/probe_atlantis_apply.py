"""Probes repositories for 'atlantis apply'."""

from github.PullRequest import PullRequest
from rich import print

from dapla_team_cli.github import get_pr
from dapla_team_cli.pr.batch_handler import batch_handler
from dapla_team_cli.pr.const import RepoState
from dapla_team_cli.pr.const import State
from dapla_team_cli.pr.const import Status
from dapla_team_cli.pr.rich_check import SKIPPING
from dapla_team_cli.pr.rich_check import RichFailure
from dapla_team_cli.pr.rich_check import RichSuccess
from dapla_team_cli.pr.rich_check import RichWarning


@batch_handler
def probe_atlantis_apply(state: State) -> None:
    """Probes atlantis apply."""
    print("\n\n[cyan]Probing repositories for 'atlantis apply'")
    for repo in state.repos.values():
        print(f"[bold magenta]{repo.name}")
        if pr := get_pr(repo.pr.number, repo.name):
            _do_probe_atlantis_apply(repo, pr)


def _do_probe_atlantis_apply(repo: RepoState, pr: PullRequest) -> None:
    """Probes atlantis apply for a single repository."""
    comments = pr.get_issue_comments().reversed
    # We want to chooose the last apply, in case there is a new manual "atlantis apply"
    last_atlantis_apply_comment = None
    for comment in comments:
        if "Ran Apply for dir:" in comment.body and "atlantis" in comment.user.login:
            last_atlantis_apply_comment = comment
            break

    if not last_atlantis_apply_comment:
        print(RichWarning(message="'atlantis apply' has never been ran"))
        print(SKIPPING)
        return

    if "Apply Error" in last_atlantis_apply_comment.body:
        print(RichFailure(message="Apply has failed"))
        print(SKIPPING)
        repo.workflow.atlantis_apply = Status.FAIL
        return

    repo.workflow.atlantis_apply = Status.SUCCESS
    print(RichSuccess(message="Apply is successful"))
