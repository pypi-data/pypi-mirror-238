"""Helper classes for doctor checks."""
from pydantic import BaseModel


class Check(BaseModel):
    """Holds a success status and a success/failure message for a single doctor check."""

    success: bool
    message: str

    def __bool__(self) -> bool:
        """Simplify expressions.

        E.g. 'if check' instead of 'if check.success'
        """
        return self.success

    def __str__(self) -> str:
        """Simplify expressions.

        E.g. 'print(check)' instead of 'print(check.message)'
        """
        return self.message


class Success(Check):
    """A successful check."""

    success: bool = True


class Failure(Check):
    """A failed check."""

    success: bool = False
