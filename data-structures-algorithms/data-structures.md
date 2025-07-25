
## 📚 Arrays (Lists)
- Ordered collection, index access (arr[i] = x) `O(1)`
- Insert/delete at end `O(1)`, else `O(n)`

```python
arr = [10, 20, 30]
arr.append(40)  # add to end
arr.pop()       # remove from end
arr[-1]         # last index
random.choice(arr) # random item in array

s[j:i]          # gets substring or sublist from index j up to (but not including) i
```

**Iterating:**
```python
for i in range(len(nums)-2, -1, -1):
    # (start, stop, step), starts from second-last index, counts down to 0
    # e.g. if len(nums)=5, nums = [10, 20, 30, 40, 50], i ➞ 3,2,1,0

for i in range(1, len(word) + 1, 1):  # (start, stop, step), counts up from 1 to len(word)
    # e.g. word = "cab", i ➞ 1, 2, 3

for l in range(1, len(word) + 1):  # (substring length), tries all lengths from 1 to full word
    for start in range(len(word) - l + 1):  # (start index), slides window of length l over word
        # e.g. word = "cab", l = 2 ➞ substrings: "ca", "ab"

num if num != float('inf') else -1  # return num if valid, else -1

for x in arr:
    print(x)

for i, n in enumerate(arr):
    # i is index, n in value
```
## 🔒 Tuples
- Immutable, ordered collection (like read-only lists)
- Supports indexing, slicing, unpacking
- Hashable (can be dict keys if all elements are hashable)

```python
t = (1, 2, 3)
t[0]          # ➞ 1
len(t)        # ➞ 3
t + (4,)      # ➞ (1, 2, 3, 4) — creates new tuple
a, b = (10, 20)  # unpacking
```

Notes:
- No .append() / .pop() / item assignment
- (5,) is a single-element tuple — comma is required

## 🗂 Sets
- Unordered collection of unique values.
- Fast membership check `O(1)`.

```python
my_set = {3, 1, 4}
my_set = set()
my_set.add(5)
my_set.remove(3)

# Iterate over set
for x in my_set:
    print(x)  # prints 3,1,4 in any order
```
## 🗄 Maps (Dict / HashMap)
- Stores key-value pairs, lookup/insert/delete `O(1)`.

```python
my_map = {}
my_map["a"] = 10
my_map[5] = "hello"
my_map[1].append(10)
del my_map[i]

# keys
for k in my_map:
    print(k)

# values
for v in my_map.values():
    print(v)

# key-value pairs
for k, v in my_map.items():
    print(k, v)  # e.g. "a 10"
```


### Counting & Grouping

```python
# manual counter with default 0
mapS[s[i]] = mapS.get(s[i], 0) + 1

# Counter for frequency
from collections import Counter
count = Counter(s)  # easy one-liner frequency counter (slightly slower due to function overhead)

count.most_common(k)             # returns list of (element, freq) pairs sorted by freq
[item for item, freq in count.most_common(k)]  # extract just items

# defaultdict auto-creates missing keys
from collections import defaultdict
d = defaultdict(int)    # auto-creates 0 for missing keys (useful for counting)
d = defaultdict(list)   # auto-creates [] for missing keys (useful for grouping)
d = defaultdict(set)   # auto-creates set() for missing keys (useful for grouping unique items)

# group by tuple key (like sorted chars for anagrams)
map1[tuple(value)].append(i)
key = tuple(sorted(word))  # sorting ensures all anagrams share the same key
```

## 📚 Stacks (LIFO)
- Last-In-First-Out structure
- Use `.append(x)` to push, `.pop()` to remove
- Often used for undo functionality, balanced parentheses, DFS, etc.

```python
stack = []
stack.append(1)  # push
stack.append(2)
stack.pop()      # returns 2
stack[-1]        # peek top element
```

## 📚 Queues (FIFO)
- First-In-First-Out structure
- Use `collections.deque` for O(1) enqueue/dequeue
- Useful for BFS, scheduling, streaming data

```python
from collections import deque
d = deque()

d.append(1)      # add to right
d.appendleft(0)  # add to left

d.pop()          # remove from right ➞ 1
d.popleft()      # remove from left ➞ 0

d[0]             # peek front (leftmost)
d[-1]            # peek back (rightmost)
```