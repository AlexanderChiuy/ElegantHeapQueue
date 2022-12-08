import heapq
import functools
from enum import Enum, auto
from typing import TypeVar, Generic, Callable, Optional
from collections.abc import Iterable
from elegant_heap_queue.comparable import ComparableT

__all__ = ['HeapType', 'HeapQueue']

class HeapType(Enum):
    """
    The HeapType enum defines the ordering of items within the HeapQueue. Specifically, it uses
    the HeapQueue key function or Python default comparison to generate an item's "priority" which it
    uses to arrange the items in the HeapQueue.

    Enumerations
    ------------
        MIN_HEAP: 
            The item with the minimal priority will always be at the top of the HeapQueue.
        MAX_HEAP: 
            The item with the maximum priority will always be at the top of the HeapQueue.
    """
    MAX_HEAP = auto()
    MIN_HEAP = auto()


T = TypeVar("T")


class HeapQueue(Generic[T]):
    
    def __init__(self,
                 items: Optional[Iterable[T]] = None,
                 *, heap_type: HeapType = HeapType.MIN_HEAP,
                 key: Optional[Callable[[T], ComparableT]] = None):
        """
        Constructs the HeapQueue.

        Time Complexity: O(n log n) (worst case)
        
        Parameters
        ----------
        items : Optional[Iterable[T]]
            Iterable of initial items to push to the HeapQueue.
        heap_type : HeapType
            Defines the ordering of the items within the HeapQueue. Default value MIN_HEAP.
        key : Optional[Callable[[T], ComparableT]]
            Key function to define the value which an item's "priority" should be generated from. Generally,
            used when the HeapQueue's type is a custom class.
            Parameters

        Raises
        ------
        TypeError
            If key function is not provided and HeapQueue type is not sortable.
        """

        if key is None and items:
            for item in items:
                if not self.__is_sortable(item):
                    raise TypeError(
                        "Cannot provide non-sortable value type if a key function is not given")

        self._key_function = key
        self.heap_type = heap_type
        self._heap: list[T] = []
        if items is not None:
            for item in items:
                internal_value: tuple[int, T] = self.__prepare_value(item)
                heapq.heappush(self._heap, internal_value)
    
    def __len__(self) -> int:
        """
        Returns the current size of the HeapQueue. 

        Time Complexity: O(1)

        Returns
        -------
        int
            Current size of the HeapQueue.
        """
        return len(self._heap)

    def __prepare_value(self, val: T) -> tuple[int, T]:
        if self._key_function is not None:
            if self.heap_type == HeapType.MIN_HEAP:
                return self._key_function(val), val
            else:
                return -self._key_function(val), val
        else:
            if self.heap_type == HeapType.MIN_HEAP:
                return self.__default_key_fn()(val), val
            else:
                return self.__default_key_fn_reversed()(val), val

    def peek(self):
        """
        Returns (but does not remove) the top item in the HeapQueue; ie. the item with the
        current highest priority.

        Time Complexity: O(1)

        Returns
        -------
        T
            The item with the highest priority currently at the top of the HeapQueue.
        """
        if len(self._heap) == 0:
            raise IndexError("Heap is empty")
        return self._heap[0][1]

    def push(self, item: T) -> None:
        """
        Pushes the ``item`` onto the HeapQueue. Its location in the HeapQueue will be determined by
        its "priority" in comparison to the existing items. 

        Time Complexity: O(log n)

        Parameters
        ----------
        item : T
            The item to push onto the HeapQueue

        Returns
        -------
        None
        
        Examples
        --------

        >>> import HeapQueue
        >>> maxHeap = HeapQueue(heap_type=HeapType.MAX_HEAP)
        >>> for num in range(3):
        >>>      maxHeap.push(num)
        >>> maxHeap.push(4)
        None
        """

        if self._key_function is None and not self.__is_sortable(item):
            raise TypeError(
                "Cannot provide non-int value type if a key function is not given")

        heapq.heappush(self._heap, self.__prepare_value(item))

    def pop(self):
        """
        Removes and returns the top item in the HeapQueue; ie. the item with the highest current
        priority. 
        
        Time Complexity: O(log n)

        Returns
        -------
        T
            The item with the highest priority removed from the top of the HeapQueue.
        
        Raises
        ------
        IndexError
            Raised when calling pop from an empty HeapQueue
        
        Examples
        --------
        >>> import HeapQueue
        >>> maxHeap = HeapQueue(heap_type=HeapType.MAX_HEAP)
        >>> maxHeap.push(3)
        >>> maxHeap.pop()
        3
        >>> maxHeap.pop()
        IndexError("pop() from empty HeapQueue")
        """

        if len(self._heap) == 0:
            raise IndexError("pop() from empty HeapQueue")

        return heapq.heappop(self._heap)[1]

    def push_all(self, items: Iterable[T]) -> None:
        """
        Iterates over the inputted ``items`` iterable and pushes the items onto the heap. Items location in the 
        HeapQueue will be determined by their "priority" in comparison to existing items.
        
        Time Complexity: O(k log n), where k is the size of ``items``
        
        Parameters
        ----------
        items : Iterable[T]
            An iterator of items to push onto the heap
        
        Returns
        -------
        None
        
        Examples
        --------

        >>> import HeapQueue
        >>> maxHeap = HeapQueue(heap_type=HeapType.MAX_HEAP)
        >>> maxHeap.push_all([1, 2, 3])
        None
        >>> maxHeap.push_all([5, 0, 4])
        None
        """
        for item in items:
            if self._key_function is None and not self.__is_sortable(item):
                raise TypeError(
                    "Cannot provide non-int value type if a key function is not given")
            heapq.heappush(self._heap, self.__prepare_value(item))

    def pop_k(self, k: int) -> list[T]:
        """
        Removes and returns the top ``k`` items from the HeapQueue.

        Time Complexity : O(k log n)
        
        Parameters
        ----------
        k : int
            The number of items to pop
        
        Returns 
        -------
        list[T]
            A list of len() == k which has the 'k' of the highest priority items removed from 
            the HeapQueue. The items in the list are sorted in descending order of priority.
        
        Raises
        ------
        ValueError
            If attempted to pop a negative number of elements (k <= 0)

        IndexError
            If attempted to pop ``k`` that is larger than size of HeapQueue (k < len(HeapQueue))
            if k is greater than the size of the heap"
        """
        
        if k <= 0:
            raise ValueError("Cannot pop a non-positive number of items")
        if k > len(self._heap):
            raise IndexError("Cannot pop k items if k is greater than the size of the heap")
        result = []
        for _ in range(k):
            result.append(heapq.heappop(self._heap)[1])
        return result

    def as_sorted_list(self):
        """
        Returns all items in the HeapQueue as a sorted list based on priority.

        Time Complexity : O(n log n)
        
        Returns 
        -------
        list[T]
            A list of all the items in the HeapQueue sorted by priority.
        """
        return list(map(lambda x: x[1], sorted(self._heap, key=lambda x: x[0])))

    @staticmethod
    def __is_sortable(obj):
        cls = obj.__class__
        return cls.__lt__ != object.__lt__ or cls.__gt__ != object.__gt__

    @staticmethod
    def __cmp_fn(a: T, b: T) -> int:
        if a > b:
            return 1
        elif a < b:
            return -1
        else:
            return 0

    @staticmethod
    def __cmp_fn_reversed(a: T, b: T) -> int:
        return HeapQueue.__cmp_fn(b, a)

    @staticmethod
    def __default_key_fn() -> Callable[[T], ComparableT]:
        """
        This is some description
        """
        return functools.cmp_to_key(HeapQueue.__cmp_fn)

    @staticmethod
    def __default_key_fn_reversed() -> Callable[[T], ComparableT]:
        """
        This is another description
        """
        return functools.cmp_to_key(HeapQueue.__cmp_fn_reversed)
