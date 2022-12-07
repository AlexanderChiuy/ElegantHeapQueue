# Elegant Heap Queue v1.0.0 #

At last a better and more elegant Heap Queue library for Python! We developed this library as a result of our interactions with established Python PriorityQueue and heapq libraries through Carnegie Mellon computing courses and Leetcode grinding. Explicitly, we noticed that the Python standard libraries, while useful and implementing correct heap behavior, do not allow for expressive code. They have limitations which lead to potentially opaque and difficult to maintain code, using several "hacks" to achieve what is normal in other languages like Java. To understand better our pain points, consider a classic Leetcode question--Median Finder. Below shows an implementation that uses the heapq Python standard library...

```python
class MedianFinderStandard:

   def __init__(self):
	 # smaller half of data. maxHeap[0] stores the biggest data in smaller half
       self.maxHeap = []
	 # bigger half of data. minHeap[0] stores the smallest data in bigger half 
       self.minHeap = []
      
   def addNum(self, num: int) -> None:
       if len(self.maxHeap) > len(self.minHeap):
           x = heapq.heappushpop(self.maxHeap, -num)
           heapq.heappush(self.minHeap, -x)
       else:
           y = heapq.heappushpop(self.minHeap, num)
           heapq.heappush(self.maxHeap, -y)

   def findMedian(self) -> float:
       # if number of element is odd, median is biggest element in maxHeap
       if (len(self.maxHeap) + len(self.minHeap)) % 2 != 0:
           return -(self.maxHeap[0])
       # if number of element is even, median is the mean of two heaps top elems
       return (-self.maxHeap[0] + self.minHeap[0]) / 2
```

Compare this code to a re-implementation using our library...

```python
class MedianFinderElegant:

    def __init__(self):
        self.maxHeap = HeapQueue(heap_type=HeapType.MAX_HEAP)
        self.minHeap = HeapQueue(heap_type=HeapType.MIN_HEAP)

    def addNum(self, num: int) -> None:
        if len(self.maxHeap) > len(self.minHeap):
            self.maxHeap.push(num)
            x = self.maxHeap.pop()
            self.minHeap.push(x)
        else:
            self.minHeap.push(num)
            y = self.minHeap.pop()
            self.maxHeap.push(y) # negations no more

    def findMedian(self) -> float:
        # if number of element is odd, median is biggest element in maxHeap
        if (len(self.maxHeap) + len(self.minHeap)) % 2 != 0:
            return (self.maxHeap.peek())
       # if number of element is even, median is the mean of two heaps top elems
        return (self.maxHeap.peek() + self.minHeap.peek()) / 2
```

Hopefully, you will notice that latter is significantly more expressive. The code is cleaner and it tells you exactly what it is doing, there is no need for negations or understanding of how the library works under-the-hood to understand the code: what you see is what you get. The Python PQ libraries also get worse when we start to involve classes, a problem since Python is used often in an Object-Oriented-Programming manner in real applications. Below are two different Java code snippets from Pinterest's memq project and Hadoop hdds using PQs with classes:

```java
Map<String, PriorityQueue<Broker>> rackBrokerCapacityMap = new HashMap<>();
for (Broker broker : brokerList) {
    Integer capacity = throughputMap.getOrDefault(broker.getInstanceType(),
        DEFAULT_CAPACITY);
    if (broker.getTotalNetworkCapacity() == 0) {
    broker.setTotalNetworkCapacity(capacity);
    }
    PriorityQueue<Broker> priorityQueue = rackBrokerCapacityMap.computeIfAbsent(
        broker.getLocality(),
        k -> new PriorityQueue<>(
            (o1, o2) -> Integer.compare(o2.getAvailableCapacity(), o1.getAvailableCapacity())
        )
    );
    priorityQueue.add(broker);
}
```

```java
FindSourceGreedy(NodeManager nodeManager) {
    sizeLeavingNode = new HashMap<>();
    potentialSources = new PriorityQueue<>((a, b) -> {
      double currentUsageOfA = a.calculateUtilization(
          -sizeLeavingNode.get(a.getDatanodeDetails()));
      double currentUsageOfB = b.calculateUtilization(
          -sizeLeavingNode.get(b.getDatanodeDetails()));
      //in descending order
      int ret = Double.compare(currentUsageOfB, currentUsageOfA);
      if (ret != 0) {
        return ret;
      }
      UUID uuidA = a.getDatanodeDetails().getUuid();
      UUID uuidB = b.getDatanodeDetails().getUuid();
      return uuidA.compareTo(uuidB);
    });
    this.nodeManager = nodeManager;
}
```

In standard Python, you can _not_ integrate the logic to get "priority" for the HeapQueue into the data structure itself! It has to be done at each `heappush(...)` call using a tuple hack: `(item_priority, item)`. Alternatively, it can be achieved by overriding a classes `__lt__()` method; however, these hacks all lead back to our initial problem with lack of expression. These hacks all require knowledge of how the libraries (heapq, queue) are implemented in order to "hack" together solutions. The result is code which is difficult to maintain, easy to generate subtle bugs, and hard to read. With our library, this feature is enabled which allows a HeapQueue to encapsulate the logic for generating its items priority via a "key function". In essence, you define it once at creation time and never worry about it again. The Java excerpts could be re-implemented in our library like so...

```python
rack_broker_capacity_dict = {}
for broker in brokerList:
    capacity = throughput_dict.get(broker.get_instance_type(), DEFAULT_CAPACITY)
    if broker.get_total_network_capacity() == 0:
        broker.set_total_network_capacity(capacity)
    pq = rack_broker_capacity_dict.get(
        broker.get_locality(),
        HeapQueue(
            heap_type=HeapType.MIN_HEAP,
            key=lambda o: o.get_available_capacity()
        )
    )
    '''
    Push and pop items from pq object with Heap guarantees using key for 
    "priority" and heap_type for ordering priority
    '''
```

```python
def find_source_greedy(node_manager):
    size_leaving_node = {}
    potential_sources = HeapQueue(
        heap_type=HeapType.MIN_HEAP,
        key=lambda a: ( # tuple key for fallback priorities if equal on first
            a.calculate_utilization(-size_leaving_node.get(a.get_datanode_details())),
            a.get_datanode_details().get_uuid()
        )
    )
    self.node_manager = node_manager
```

Similar real world examples where this would be useful can involve load balancing, scheduling, encoding, algorithms, and more, where classes that encapsulate lots of knowledge are used and an objects "priority" is not always a simple calculation. Inspirations for the library stem from Java and C++ implementations as well as use of the Python platform. We hope that you find this library useful in your future endeavors and want to give a shout-out to our Professor [Charlie Garrod](https://www.cs.cmu.edu/~charlie/). For more information on the library see the sections below.

## Installation ##

With a standard Python installation, to install do: 

```
pip install HeapQueue
```

It's also possible to use the library files uploaded to the PyPI [website]() directly in your projects.

## Getting Started with Elegant Priority Queue ##

### Constructor Arguments ###
The most basic way to instantiate a HeapQueue, `heap = HeapQueue()`. However, there are many different
arguments that help elevate the usefulness of this library:

| Argument Name | Description | Example |
| ----          | ----        | ----    |
| items         | Iterable of initial items to push to the HeapQueue | `heap = HeapQueue(items=[1, 2, 3])` |
| heap_type     | Defines the ordering of the items within the HeapQueue. Default value MIN_HEAP | `heap = HeapQueue(HeapQueue(heap_type=HeapType.MAX_HEAP))` |
| key           | Key function to define the value which an item's "priority" should be generated from. Generally, used when the HeapQueue's type is a custom class | `heap = HeapQueue(key=lambda x: x.val)` |

### Core Functions ###

|Function         |Description     |Example|
| ------          | ------         |------ |
| `peek`          | Returns (but does not remove) the highest priority item | `heap.peek()` |
| `push`          | Pushes the ``item`` onto the HeapQueue, while maintaining heap invariant | `heap.push(1)` |
| `push_all`      | Takes an iterable which will add all elements to heap | `heap.push([1, 2, 3])` |
| `pop`           | Returns and removes the highest priority item         | `heap.pop()` |
| `pop_k`         | Returns and removes the *k* highest priority items    | `heap.pop_k(2)` |
| `as_sorted_list`| Returns all items in the HeapQueue as a sorted list based on priority | `for item in heap.as_sorted_list(): ...` |

### Miscellaneous ###
TODO: theory ([overview](https://www.geeksforgeeks.org/priority-queue-set-1-introduction/), [heapq notes](https://docs.python.org/3/library/heapq.html#theory), [In-Depth CMU Lecture Notes](https://www.cs.cmu.edu/~15122/handouts/17-pq.pdf)), etc.... 

## License ##
MIT

## Authors ##
- [Alex](https://github.com/AlexanderChiuy)
- [David](https://github.com/hdavidethan)
- [Tyler](https://github.com/tylowe-labs)
- [Shou-San](https://github.com/HandSam0822)
