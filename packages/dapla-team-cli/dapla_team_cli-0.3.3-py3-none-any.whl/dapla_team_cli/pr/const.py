"""Global variables for batch update commands."""

from enum import Enum
from enum import auto
from pathlib import Path
from typing import Optional

from pydantic import BaseModel
from typing_extensions import TypeAlias


STATE_BUCKET_NAME_URI = "ssb-batch-update-statefiles"
BATCH_PROJECT_ID = "batch-update-p-3f"
STATE_FIELDS = [
    "pushed-to-remote",
    "pr-opened",
    "workflows-success",
    "atlantis-plan-success",
    "pr-approved",
    "atlantis-apply",
    "atlantis-apply-success",
    "pr-merged",
    "issue-url",
    "issue-nr",
    "branch",
]

StateObjectName: "TypeAlias" = Optional[str]


class Status(Enum):
    """Possible statuses for a single workflow item."""

    NOT_STARTED = auto()
    STARTED = auto()
    SUCCESS = auto()
    FAIL = auto()


class PrMetadata(BaseModel):
    """Metadata for a Pull Request on Github."""

    number: Optional[int] = None
    url: Optional[str] = None
    branch_name: Optional[str] = None


class WorkflowStatus(BaseModel):
    """Status of stages in the workflow for a single repo."""

    pushed: Status = Status.NOT_STARTED
    opened: Status = Status.NOT_STARTED
    checks: Status = Status.NOT_STARTED
    atlantis_plan: Status = Status.NOT_STARTED
    approved: Status = Status.NOT_STARTED
    atlantis_apply: Status = Status.NOT_STARTED
    merged: Status = Status.NOT_STARTED


class RepoState(BaseModel):
    """The state of a single repo."""

    name: str
    local_path: Path
    pr: PrMetadata
    workflow: WorkflowStatus


class State(BaseModel):
    """Model representing the state of all repos in a run."""

    name: str
    repos: dict[str, RepoState] = {}
    version: str = "0.0.1"

    def get_repo_state(self, repo_name: str) -> RepoState:
        """Get the state of a single repo."""
        return self.repos[repo_name]
