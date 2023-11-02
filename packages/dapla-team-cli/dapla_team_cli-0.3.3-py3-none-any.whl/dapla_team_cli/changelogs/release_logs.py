"""Business logic for gathering release changelogs."""

from typing import List

from github.GitRelease import GitRelease

from dapla_team_cli.github import get_repo


def get_release_logs(repo_name: str, n_logs: int = 5) -> List[GitRelease]:
    """Returns the release changelogs for the 'n' last GitHub releases in a repository."""
    dpteam_repo = get_repo(repo_name)
    releases = dpteam_repo.get_releases()
    latest_releases: List[GitRelease] = releases[: min(releases.totalCount, n_logs)]
    latest_releases = list(latest_releases)

    return latest_releases
