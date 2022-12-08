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
    the HeapQueue key function (if provided during construction) or Python default comparison to 
    generate an item's "priority" which it uses to arrange the items in the HeapQueue.
    Enumerations
    ------------
        MIN_HEAP: 
            The item with the minimal priority will always be at the top of the HeapQueue.
        MAX_HEAP: 
            The item with the maximum priority will always be at the top of the HeapQueue.
    Examples
    --------
    >>> from elegant_heap_queue import *
    >>> maxHeap = HeapQueue(heap_type=HeapType.MAX_HEAP) # will use Python default comparison for items passed
    >>> maxHeap.push_all([x for x in range(5)])
    >>> maxHeap.peek()
    4
    >>> minHeap = HeapQueue(heap_type=HeapType.MIN_HEAP)
    >>> minHeap.push_all([x for x in range(5)])
    >>> minHeap.peek()
    0
    >>> class DataNode:
        def __init__(self, val, next=None):
            self.val = val
            self.next = next
    >>> maxHeap = HeapQueue(key=lambda n: n.val, heap_type=HeapType.MAX_HEAP) # will use key function for items passed (DataNode instances)
    >>> maxHeap.push_all([DataNode(x) for x in range(5)])
    >>> maxHeap.peek().val
    4
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
        Constructs a HeapQueue which is an implementation of a priority queue data structure where every element has some "priority" associated with it. 
        The priority of the elements in a queue combined with its ordering (``HeapType``) determine the order in which elements are served.
        If ``items`` iterable argument is passed it MUST be all the same data type, otherwise it is undefined behavior and there are no guarantees on the 
        HeapQueue invariants. Similar, if a ``key`` function is used, but items passed to the HeapQueue are not of the key function data type,
        it is undefined behavior.
        Time Complexity: O(n log n) --> worst case when ``items`` iterable passed.
        
        Parameters
        ----------
        items : Optional[Iterable[T]]
            Iterable of initial items to push to the HeapQueue.
        heap_type : HeapType
            Defines the ordering of the items within the HeapQueue. Default value MIN_HEAP.
        key : Optional[Callable[[T], ComparableT]]
            Key function to define the value which an item's "priority" should be generated from. Generally,
            used when the HeapQueue's type is a custom class.
        Raises
        ------
        TypeError
            If key function is not provided and HeapQueue type is not sortable.
        Examples
        --------
        >>> from elegant_heap_queue import *
        >>> minHeap = HeapQueue() # creates an empty min HeapQueue
        >>> maxHeap = HeapQueue(heap_type=HeapType.MAX_HEAP) # creates an empty max HeapQueue
        >>> minHeap = HeapQueue( # creates a min HeapQueue with initial values
            ["Alex", "Tyler", "Shou-San", "David"]
        ) 
        >>> minHeap.peek()
        "Alex"
        >>> maxHeap = HeapQueue( # creates a max HeapQueue with initial values
            ["Alex", "Tyler", "Shou-San", "David"],
            heap_type=HeapType.MAX_HEAP
        ) 
        >>> maxHeap.peek()
        "Tyler"
        >>> class ServerNode:
            def __init__(self, id):
                self.id = id
            def calculate_utilization():
                # some custom logic
                return res
        >>> minHeap = HeapQueue( # creates a min HeapQueue with a custom class
            [ServerNode(x) for x in range(10)],
            key=lambda sn: sn.calculate_utilization() 
        )
        >>> minHeap.peek()
        lowest utilization node
        >>> maxHeap = HeapQueue( # creates a max HeapQueue with a custom class
            [ServerNode(x) for x in range(10)],
            heap_type=HeapType=MAX_HEAP,
            key=lambda sn: sn.calculate_utilization() 
        )
        >>> maxHeap.peek()
        highest utilization node
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
        Examples
        --------
        >>> minHeap = HeapQueue([x for x in range(100)])
        >>> len(minHeap)
        100
        """
        return len(self._heap)

    def peek(self):
        """
        Returns (but does not remove) the top item in the HeapQueue; ie. the item with the
        current highest priority.
        Time Complexity: O(1)
        Returns
        -------
        T
            The item with the highest priority currently at the top of the HeapQueue.
        Examples
        --------
        >>> minHeap = HeapQueue([x for x in range(5)])
        >>> minHeap.peek() # 0 still on top of HeapQueue
        0
        >>> maxHeap = HeapQueue([x for x in range(5)])
        >>> maxHeap.peek() # 4 still on top of HeapQueue
        4
        """
        if len(self._heap) == 0:
            raise IndexError("Heap is empty")
        return self._heap[0][1]

    def push(self, item: T) -> None:
        """
        Pushes the ``item`` onto the HeapQueue. Its location in the HeapQueue will be determined by
        its "priority" in comparison to the existing items in the HeapQueue. ``Item`` MUST be the same data type
        as the items in the HeapQueue, otherwise it is undefined behavior and there are no guarantees
        on the HeapQueue invariants.
        Time Complexity: O(log n)
        Parameters
        ----------
        item : T
            The item to push onto the HeapQueue
        Returns
        -------
        None
        Raises
        ------
        TypeError
            Raised when the ``item`` is not sortable and there is no key function for the HeapQueue
        
        Examples
        --------
        >>> from elegant_heap_queue import *
        >>> maxHeap = HeapQueue(heap_type=HeapType.MAX_HEAP)
        >>> for num in range(3):
        >>>      maxHeap.push(num)
        >>> maxHeap.push(4) # 4 at the top of HeapQueue now
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
        >>> maxHeap.pop() # 3 is no longer in the HeapQueue
        3
        >>> len(maxHeap)
        0
        >>> maxHeap.pop()
        IndexError("pop() from empty HeapQueue")
        """
        if len(self._heap) == 0:
            raise IndexError("pop() from empty HeapQueue")

        return heapq.heappop(self._heap)[1]

    def push_all(self, items: Iterable[T]) -> None:
        """
        Iterates over the inputted ``items`` iterable and pushes the items onto the heap. Items location in the 
        HeapQueue will be determined by their "priority" in comparison to the existing items in the HeapQueue. ``Items`` 
        iterable MUST be all the same data type and the same type as the items in the HeapQueue, otherwise it is undefined 
        behavior and there are no guarantees on the HeapQueue invariants.
        
        Time Complexity: O(k log n), where k is the size of ``items``
        
        Parameters
        ----------
        items : Iterable[T]
            An iterator of items to push onto the heap
        
        Returns
        -------
        None
        Raises
        ------
        TypeError
            Raised when an item in ``items`` is not sortable and there is no key function for the HeapQueue
        
        Examples
        --------
        >>> import HeapQueue
        >>> maxHeap = HeapQueue(heap_type=HeapType.MAX_HEAP)
        >>> maxHeap.push_all([1, 2, 3])
        None
        >>> maxHeap.push_all([5, 0, 4])
        None
        >>> maxHeap.peek()
        5
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
        Examples
        --------
        >>> maxHeap = HeapQueue(heap_type=HeapType.MAX_HEAP)
        >>> maxHeap.push_all([1, 2, 3])
        None
        >>> maxHeap.push_all([5, 0, 4])
        None
        >>> maxHeap.pop_k(-1)
        ValueError("Cannot pop a non-positive number of items")
        >>> maxHeap.pop_k(7)
        IndexError("Cannot pop k items if k is greater than the size of the heap")
        >>> maxHeap.pop_k(3)
        [5, 4, 3]
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
        Examples
        --------
        >>> maxHeap = HeapQueue(heap_type=HeapType.MAX_HEAP)
        >>> maxHeap.push_all([1, 2, 3])
        None
        >>> maxHeap.push_all([5, 0, 4])
        None
        >>> for item in maxHeap.as_sorted_list():
            # do useful work with the sorted values
            print(item)
        # prints: 5, 4, 3, 2, 1, 0
        """
        return list(map(lambda x: x[1], sorted(self._heap, key=lambda x: x[0])))

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
        return functools.cmp_to_key(HeapQueue.__cmp_fn)

    @staticmethod
    def __default_key_fn_reversed() -> Callable[[T], ComparableT]:
        return functools.cmp_to_key(HeapQueue.__cmp_fn_reversed)