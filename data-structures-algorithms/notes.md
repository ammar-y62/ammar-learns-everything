
# 🔑 Core Concepts

---

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
    # starts from second-last index, counts down to 0
    # e.g. if len(nums)=5, nums = [10, 20, 30, 40, 50], i ➞ 3,2,1,0

for x in arr:
    print(x)

for i, n in enumerate(arr):
    print(i, n)
```

---

## 🗂 Sets
- Unordered collection of unique values.
- Fast membership check `O(1)`.

```python
my_set = {3, 1, 4}
my_set.add(5)
my_set.remove(3)

# Iterate over set
for x in my_set:
    print(x)  # prints 3,1,4 in any order
```

---

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

---

## 🚀 Counting & Grouping

```python
# manual counter with default 0
mapS[s[i]] = mapS.get(s[i], 0) + 1

# Counter for frequency
from collections import Counter
mapS = Counter(s)  # easy one-liner frequency counter (slightly slower due to function overhead)

# defaultdict auto-creates missing keys
from collections import defaultdict
d = defaultdict(int)    # auto-creates 0 for missing keys (useful for counting)
d = defaultdict(list)   # auto-creates [] for missing keys (useful for grouping)

# group by tuple key (like sorted chars for anagrams)
map1[tuple(value)].append(i)
key = tuple(sorted(word))  # sorting ensures all anagrams share the same key
```

---

## 🏆 Top-K patterns

```python
from collections import Counter
count = Counter(arr)

count.most_common(k)             # returns list of (element, freq) pairs sorted by freq
[item for item, freq in count.most_common(k)]  # extract just items

import heapq
heapq.nlargest(k, count.keys(), key=count.get) # get the k keys with largest counts using a heap
```

---

## 🔀 Two Pointers
- Use **two indices** to scan from ends or together, reducing `O(n^2)` to `O(n)`.
- Works for sorted arrays / sliding windows / linked list cycles.

| Pattern                  | Examples                            |
|---------------------------|------------------------------------|
| Towards each other        | 2Sum, 3Sum                         |
| Move together (window)    | longest substring, sliding max/min |
| Fast & slow               | detect linked list cycle           |

```python
l, r = 0, len(nums)-1
while l < r:
    if nums[l] + nums[r] < target:
        l += 1
    else:
        r -= 1
```
---

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

---

## 📚 Queues (FIFO)
- First-In-First-Out structure
- Use `collections.deque` for O(1) enqueue/dequeue
- Useful for BFS, scheduling, streaming data

```python
from collections import deque
queue = deque()
queue.append(1)     # enqueue
queue.append(2)
queue.popleft()     # returns 1
queue[0]            # peek front element
```