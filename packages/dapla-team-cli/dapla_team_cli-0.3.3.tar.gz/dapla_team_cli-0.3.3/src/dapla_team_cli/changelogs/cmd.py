"""Changelog related commands.

Commands invoked by dpteam changelogs <some-command> are defined here.
"""

import re

import typer
from rich.console import Console

from dapla_team_cli.changelogs.release_logs import get_release_logs


HEADERS_TO_KEEP: str = "Change|change|Feature|feature"

console = Console(highlight=False, emoji=True)


def remove_unnecessary_content(body: str) -> str:
    """The function divides the input string into a list by splitting on the header's prefix.

    Unnecessary headers are removed by comparing each header to a regular expression.
    The list is then joined and returned as a string.

    :param body: A string with log data, divided into different contet by headers.
    :return: Log data with filtered content.
    """
    regex_pattern: str = "^[^\n]*(" + HEADERS_TO_KEEP + ")(.|\n)*$"
    body_list: list[str] = body.split("##")

    for i in range(len(body_list) - 1, -1, -1):
        if re.search(regex_pattern, body_list[i]) is None:
            body_list.pop(i)

    new_body: str = "##" + "##".join(body_list)
    return new_body


def print_changelogs(n_logs: int = typer.Option(5, "--nlogs", "-n", help="Number of latest logs to show")) -> None:
    """Prints the n last release changelogs for 'dapla-team-cli'."""
    logs = get_release_logs("dapla-team-cli", n_logs)
    for log in reversed(logs):
        console.print(f"[green]Release tag: {log.tag_name}, released on {str(log.published_at)}")
        if log.body == "":
            continue

        new_body: str = remove_unnecessary_content(log.body)
        log_lines = [line.replace("##", "[yellow]").lstrip() if "##" in line else line for line in new_body.splitlines()]

        for line in log_lines:
            console.print(line)
        console.print("\n")
