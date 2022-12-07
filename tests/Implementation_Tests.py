from heap_queue import HeapQueue, HeapType
import pytest
import sys
 
# adding path to correct library
sys.path.insert(0, '../')


'''
A testing file that will ensure that the implementation for all functions
work as intended for heap_queue. Additionally, ensuring that the correct
pain points are satisfied. 

When using pytest, the testing function must start with test_....
'''
class DummyClass:
  def __init__(self, val, name):
    self.val = val
    self.name = name

@pytest.fixture()
def setup_module():
  global empty_heap
  empty_heap = HeapQueue()
  global min_heap
  min_heap = HeapQueue([1, 2, 3, 4], heap_type=HeapType.MIN_HEAP)
  global max_heap
  max_heap = HeapQueue([1, 2, 3, 4], heap_type=HeapType.MAX_HEAP)
  global class_heap
  class_heap = HeapQueue([DummyClass(1, "one"), DummyClass(2, "two"), DummyClass(3, "three")], key=lambda x:x.val)
  return empty_heap, min_heap, max_heap, class_heap
  
# Init Tests
def test_init(setup_module):
  assert empty_heap != None
  assert min_heap != None
  assert max_heap != None
  assert class_heap != None 

def test_len(setup_module):
  assert len(empty_heap) == 0
  assert len(min_heap) == 4
  assert len(max_heap) == 4
  assert len(class_heap) == 3

# Peek Tests
def test_peek(setup_module):
  with pytest.raises(IndexError):
    empty_heap.peek()

  assert min_heap.peek() == 1
  assert len(min_heap) == 4
  assert max_heap.peek() == 4
  assert len(max_heap) == 4
  assert class_heap.peek().name == "one"
  assert len(class_heap) == 3
 

# Push & Push_all Tests
def test_push(setup_module):
  empty_heap.push_all([9, 6, 7])
  assert len(empty_heap) == 3
  empty_heap.push(10)
  assert len(empty_heap) == 4

  with pytest.raises(TypeError):
    empty_heap.push(DummyClass(1, "one"))
  
  with pytest.raises(TypeError):
    empty_heap.push_all([1, DummyClass(1, "one")])

  min_heap.push_all([9, 6, 7])
  assert len(min_heap) == 7
  assert min_heap.peek() == 1

  max_heap.push_all([9, 6, 7])
  assert len(max_heap) == 7
  assert max_heap.peek() == 9

  class_heap.push_all([DummyClass(9, "Nine"), DummyClass(6, "six"), DummyClass(7, "seven")])
  assert len(class_heap) == 6
  assert class_heap.peek().name == "one"
  class_heap.push(DummyClass(-100, "hunnit"))
  assert class_heap.peek().name == "hunnit"

# Pop & Pop_k Tests
def test_pop(setup_module):
  with pytest.raises(IndexError):
    empty_heap.pop()
  # no negatives
  with pytest.raises(ValueError):
    empty_heap.pop_k(-1)

  assert min_heap.pop() == 1
  assert len(min_heap) == 3
  assert min_heap.pop_k(3) == [2, 3, 4]

  assert max_heap.pop() == 4
  assert len(max_heap) == 3
  assert max_heap.pop_k(3) == [3, 2, 1]

  with pytest.raises(IndexError):
    empty_heap.pop_k(1)

  assert class_heap.pop().name == "one"
  assert len(class_heap) == 2

# __Iterable__
def test_iteration(setup_module):
  assert len(empty_heap.as_sorted_list()) == 0
  assert min_heap.as_sorted_list() == [1, 2, 3, 4]
  assert max_heap.as_sorted_list() == [4, 3, 2, 1]

  dummies = class_heap.as_sorted_list()
  for i in range(1, 4):
    assert dummies[i-1].val == i

