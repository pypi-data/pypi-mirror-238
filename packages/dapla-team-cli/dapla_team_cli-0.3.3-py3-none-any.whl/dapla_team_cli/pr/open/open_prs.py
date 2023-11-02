"""Functions for open-prs command."""

import questionary
from git import CommandError
from git import Repo
from rich import print  # noqa: W0622

from dapla_team_cli.github import get_repo
from dapla_team_cli.pr.batch_handler import batch_handler
from dapla_team_cli.pr.const import RepoState
from dapla_team_cli.pr.const import State
from dapla_team_cli.pr.const import Status
from dapla_team_cli.pr.rich_check import SKIPPING
from dapla_team_cli.pr.rich_check import RichSuccess
from dapla_team_cli.pr.rich_check import RichWarning


@batch_handler
def open_prs(state: State, override: bool, max_prs: int, target_branch_name: str, commit_message: str) -> None:
    """Opens PRs."""
    opened_prs = 0
    print("\n\n[cyan]Opening PRs..")
    for repo in state.repos.values():
        if opened_prs >= max_prs:
            print("[blue] Max PRs opened, stopping")
            break

        print(f"[bold magenta]{repo.name}")

        if (
            _check_override(repo, override)
            and _do_push_repo(repo, target_branch_name, commit_message)
            and _do_open_pr(repo, target_branch_name, commit_message)
        ):
            opened_prs += 1


def _check_override(repo_state: RepoState, override: bool) -> bool:
    """Checks if the PR has been pushed and opened and whether to override."""
    # Skip open PRs unless override
    if all([s is Status.NOT_STARTED for s in [repo_state.workflow.pushed, repo_state.workflow.opened]]):
        return True
    else:
        print(RichWarning(message="Changes in this repository have been pushed or a PR has been opened"))
        if not override:
            print(SKIPPING)
            return False
        else:
            answer = questionary.confirm("Do you want to open a new PR anyway?").ask()
            if answer:
                return True
            else:
                print(SKIPPING)
                return False


def _do_push_repo(repo_state: RepoState, target_branch_name: str, commit_message: str) -> bool:
    """Push a repository for a single repo."""
    repo = Repo(repo_state.local_path)

    try:
        repo.git.checkout("-b", target_branch_name)
    except CommandError as e:
        if f"fatal: a branch named '{target_branch_name}' already exists" in str(e):
            repo.git.checkout(target_branch_name)
            print(RichWarning(message=f"Using existing local branch with name: {target_branch_name}"))
        else:
            raise e

    # If there are no modified, unstaged files or there are no new untracked files
    if not (repo.is_dirty() or repo.index.diff(None) or repo.untracked_files):
        print(RichWarning(message="Found no changes in the working copy"))
        print(SKIPPING)
        return False

    repo.git.add(all=True)
    try:
        repo.git.commit(message=commit_message)
    except CommandError as e:
        if "nothing to commit, working tree clean" in str(e):
            print(RichWarning(message="Working tree is clean"))
            print(SKIPPING)
            return False
        else:
            raise e

    origin = repo.remote(name="origin")
    origin.push(target_branch_name, set_upstream=True)
    repo_state.workflow.pushed = Status.SUCCESS
    print(RichSuccess(message=f"Successfully pushed branch {target_branch_name}"))
    return True


def _do_open_pr(repo_state: RepoState, target_branch_name: str, commit_message: str) -> bool:
    """Open a PR for a single repository."""
    gh_repo = get_repo(repo_state.name)
    pr = gh_repo.create_pull(
        title=f"[BATCH-UPDATE] {commit_message}", head=target_branch_name, base=gh_repo.default_branch, body=commit_message
    )
    repo_state.pr.url = pr.html_url
    repo_state.pr.number = pr.number
    repo_state.pr.branch_name = target_branch_name

    repo_state.workflow.opened = Status.SUCCESS

    print(RichSuccess(message=f"Successfully opened PR with URL {pr.html_url}"))
    return True
