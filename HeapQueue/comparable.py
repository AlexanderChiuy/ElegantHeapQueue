"""
Comparable Type protocols based on stack overflow answer:
https://stackoverflow.com/questions/37669222/how-can-i-hint-that-a-type-is-comparable-with-typing
"""

from abc import abstractmethod
from typing import Protocol, TypeVar, Union


class ComparableWithLT(Protocol):
    """Protocol for annotating comparable types with __lt__"""

    @abstractmethod
    def __lt__(self: 'ComparableT', other: 'ComparableT') -> bool:
        pass


class ComparableWithGT(Protocol):
    """Protocol for annotating comparable types with __gt__"""

    @abstractmethod
    def __gt__(self: 'ComparableT', other: 'ComparableT') -> bool:
        pass


class ComparableWithGE(Protocol):
    """Protocol for annotating comparable types with __ge__"""

    @abstractmethod
    def __ge__(self: 'ComparableT', other: 'ComparableT') -> bool:
        pass


class ComparableWithLE(Protocol):
    """Protocol for annotating comparable types with __le__"""

    @abstractmethod
    def __le__(self: 'ComparableT', other: 'ComparableT') -> bool:
        pass


Comparable = Union[ComparableWithLT, ComparableWithGT, ComparableWithGE, ComparableWithLE]

ComparableT = TypeVar("ComparableT", bound=Comparable)
