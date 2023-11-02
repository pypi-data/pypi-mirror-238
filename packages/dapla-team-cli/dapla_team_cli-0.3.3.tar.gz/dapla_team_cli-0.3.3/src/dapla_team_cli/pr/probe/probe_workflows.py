"""Probes repositories for 'atlantis plan'."""

from github.PullRequest import PullRequest
from rich import print  # noqa: W0622

from dapla_team_cli.github import get_commit
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
def probe_workflows(state: State) -> None:  # noqa: C901
    """Probes workflows for atlantis plan and checks in repositories."""
    print("\n\n[cyan]Probing repositories for check runs..")
    for repo in state.repos.values():
        print(f"[bold magenta]{repo.name}")
        if pr := get_pr(repo.pr.number, repo.name):
            _probe_check_runs(repo, pr)
    print("\n[cyan]Probing repositories for plans..")
    for repo in state.repos.values():
        print(f"[bold magenta]{repo.name}")
        if pr := get_pr(repo.pr.number, repo.name):
            _probe_plans(repo, pr)


def _probe_plans(repo: RepoState, pr: PullRequest) -> None:
    """Probes plans for success or failure."""
    comments = pr.get_issue_comments().reversed

    # We want to chooose the last plan, in case there is a new manual "atlantis plan"
    last_atlantis_plan_comment = None
    for comment in comments:
        if "Ran Plan for dir:" in comment.body and "atlantis" in comment.user.login:
            last_atlantis_plan_comment = comment
            break

    if not last_atlantis_plan_comment:
        print(RichWarning(message="plan has never been ran"))
        print(SKIPPING)
        return

    if "Plan Error" in last_atlantis_plan_comment.body:
        if "This project is currently locked by" in last_atlantis_plan_comment.body:
            print(RichFailure(message="Plan has failed due to a lock held by another PR"))
        else:
            print(RichFailure(message="Plan has failed"))

        repo.workflow.atlantis_plan = Status.FAIL
        print(SKIPPING)
        return

    repo.workflow.atlantis_plan = Status.SUCCESS
    print(RichSuccess(message="Plan succeeded"))


def _probe_check_runs(repo: RepoState, pr: PullRequest) -> int:
    """Probes check runs for success or failure."""
    commit = get_commit(pr.head.sha, repo.name)
    check_runs = commit.get_check_runs()
    check_run_success_counter = 0
    for check_run in check_runs:
        match (check_run.status, check_run.conclusion):
            case ("pending", _):
                print(RichWarning(message=f"Check {check_run.name} is pending"))
            case (_, "failure"):
                print(RichFailure(message=f"Check {check_run.name} failed"))
            case (_, "success"):
                print(RichSuccess(message=f"Check {check_run.name} succeeded"))
                check_run_success_counter += 1

    match (check_runs.totalCount, check_run_success_counter):
        case (0, _):
            print(RichWarning(message="No checks in repository"))
        case (_, 0):
            print(RichFailure(message="No checks succeeded"))
            repo.workflow.checks = Status.FAIL
        case (total, counter) if counter < total:
            print(RichWarning(message=f"Only {counter}/{total} checks succeeded"))
            repo.workflow.checks = Status.FAIL
        case _:
            print(RichSuccess(message="All checks succeeded"))
            repo.workflow.checks = Status.SUCCESS

    return check_run_success_counter
