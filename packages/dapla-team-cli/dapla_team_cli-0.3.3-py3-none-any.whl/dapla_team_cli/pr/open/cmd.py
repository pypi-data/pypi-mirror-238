"""Commands for generating PRs."""
import sys
from typing import Optional

import questionary
import typer
from prompt_toolkit.document import Document
from rich import print  # noqa: W0622
from typing_extensions import Self

from dapla_team_cli.pr.open.open_prs import open_prs
from dapla_team_cli.pr.prompt_utils import confirm_input
from dapla_team_cli.pr.state.state_utils import state_object_handler


class BranchNameValidator(questionary.Validator):
    """Validation class for branch names."""

    def validate(self: Self, document: Document) -> None:
        """Validation cheks for branch name validator object."""
        if len(document.text) == 0:
            raise questionary.ValidationError(
                message="Please enter a value",
                cursor_position=len(document.text),
            )
        if " " in document.text:
            raise questionary.ValidationError(
                message="You cannot have whitespace in a branch name",
                cursor_position=len(document.text),
            )


def open(
    override: bool = typer.Option(
        False, "--override", "-o", help="Yields an option to open PRs that the state file records as having already been opened"
    ),
    max_prs: int = typer.Option(sys.maxsize, "--max", "-m", help="Max PRs to open in one run."),
    input_target_branch_name: Optional[str] = typer.Option(
        None, "--target-branch-name", "-b", help="Name of the branches in the opened pull requests"
    ),
    commit_message: Optional[str] = typer.Option(
        None, "--commit-messsage", "-c", help="Name of the commit message in the opened pull requests"
    ),
) -> None:
    """Opens a pull request for all folders in a given parent folder."""
    if not input_target_branch_name:
        input_target_branch_name = confirm_input(
            "What will be the name of branches? (they will be prefixed with 'batch-update-')", BranchNameValidator
        )
    target_branch_name = f"batch-update-{input_target_branch_name}"
    if not commit_message:
        commit_message = confirm_input("What will be the name of the commit? (will also be used for PR titles)")

    if state := state_object_handler.get_user_state():
        open_prs(state, override, max_prs, target_branch_name, commit_message)
    else:
        sys.exit(1)

    print("\n[yellow] Hint: You can check the status of the Atlantis plans with 'dpteam pr probe plan'")
    print(
        "[yellow] Next step: \
            Perhaps you would want someone else to approve the PRs with 'dpteam pr approve' after plans are successful?"
    )
