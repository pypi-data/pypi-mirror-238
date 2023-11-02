"""Misc. utilities for the iam_bindings module."""
from itertools import groupby
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Protocol
from typing import Sequence
from typing import TypeVar
from typing import runtime_checkable

from typeguard import typeguard_ignore


@runtime_checkable
class Comparable(Protocol):
    """Interface for classes that support igroupby."""

    def __lt__(self, __o: Any) -> bool:
        """The less than magic method."""
        ...

    def __eq__(self, __o: Any) -> bool:
        """The equals magic method."""
        ...


T = TypeVar("T")
G = TypeVar("G", bound=Comparable)


@typeguard_ignore
def igroupby(seq: Sequence[T], key: Callable[[T], G]) -> Dict[G, List[T]]:
    """Helper function to bypass some annoyances with itertools.groupby.

    - groupby does not automatically sort the sequence given to it
    - groupby returns an iterator

    This helper function sorts the sequence and returns a dictionary with list values.
    """
    return {k: list(v) for k, v in groupby(sorted(seq, key=key), key=key)}


@runtime_checkable
class Combinable(Protocol):
    """Interface defining methods needed for a class to be passed to combine_and_maximize."""

    def identifier(self) -> Comparable:
        """The "grouping variable", for example RoleIAMConfig.name to group roles by name."""
        ...

    def sorter(self) -> Comparable:
        """The "sorting variable", for example RoleIAMConfig.expiry to sort roles by expiry date."""
        ...


U = TypeVar("U", bound=Combinable)


@typeguard_ignore
def combine_and_maximize(t_list: Sequence[U]) -> List[U]:
    """Combine and choose the item with the max U.sorter value for items with the same U.identifier."""
    combined: List[U] = []
    grouped = igroupby(t_list, lambda t: t.identifier())
    for t_similar in grouped.values():
        combined.append(max(t_similar, key=lambda c: c.sorter()))
    return combined
