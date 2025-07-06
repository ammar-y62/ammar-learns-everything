## 🔑 Core Concepts

### 1. Arrays
- **Definition**: Ordered collection of elements. Access by index `O(1)`.
- **Common operations**:
  - Access: `arr[i]` → `O(1)`
  - Insert/Delete at end: `O(1)`
  - Insert/Delete at start or middle: `O(n)`

### 2. Hashing (HashMap / Set)
- **HashMap / Dictionary**
  - Stores key-value pairs.
  - Lookup/Insert/Delete: `O(1)` average.
- **HashSet**
  - Stores unique values only.
  - Great for checking existence: `if x in set`.

---
## 🧠 Common Problems Cheat Sheet

| Problem Type              | Key Idea                      | Common Tools |
|---------------------------|-------------------------------|--------------|
| Contains Duplicate        | Use a `set()`                 | HashSet      |
| Valid Anagram             | Use `Counter` or sort         | HashMap      |
| Two Sum                   | Store `target - num` in map   | HashMap      |
| Group Anagrams            | Key = sorted string           | HashMap      |
| Top K Frequent Elements   | Bucket sort / heap + hashmap  | HashMap + Heap|
| Product Except Self       | Prefix & Suffix products      | Arrays       |
| Longest Consecutive Seq   | Use `set()` to skip O(n log n)| HashSet      |
| 3Sum                      | Sort + Two Pointers           | Two Pointers |
| Subarray Sum Equals K     | Prefix sum + hashmap count    | HashMap      |
| Sliding Window Max/Min    | Monotonic deque               | Deque        |

---
## 🧰 Handy Python Snippets
```text
mapS[s[i]] = mapS.get(s[i], 0) + 1  # manual counter with default 0

from collections import Counter
mapS = Counter(s)  # easy one-liner frequency counter (slightly slower due to function overhead)

d = defaultdict(int)  # auto-creates 0 for missing keys (useful for counting)

d = defaultdict(list)  # auto-creates [] for missing keys (useful for grouping)

map1[tuple(value)].append(i)  # group values by tuple key (like sorted chars → indices)

key = tuple(sorted(word))  # sorting ensures all anagrams share the same key

return [item for item, freq in count.most_common(k)]  # most_common gives list sorted by freq

return heapq.nlargest(k, count.keys(), key=count.get) # get the k keys with largest counts using a heap (count.get as sorting key)

for i, n in count.items(): # Example: if count = {'a': 2, 'b': 3}, then first i='a', n=2; then i='b', n=3

res.append(s[i+1:i+1+length])  # adds substring starting after '#' of length `length` to res

res += str(len(i)) + "#" + i    # encodes: adds "<length>#<string>" to the result string

s[j:i]                          # gets substring from index j up to (but not including) i

for i in range(len(nums)-2, -1, -1):  # starts from second-last index, counts down to 0
    # e.g. if len(nums)=5, then range(3, -1, -1) (start, stop, step)➞ [3, 2, 1, 0]
    # so i takes values 3,2,1,0

# Iterate over a set
my_set = {3, 1, 4}
for x in my_set:
    print(x)  # prints 3,1,4 in any order

# Iterate over dict keys
my_map = {"a": 10, "b": 20}
for k in my_map:
    print(k)  # prints "a", "b"

# Iterate over dict values
for v in my_map.values():
    print(v)  # prints 10, 20

# Iterate over dict key-value pairs
for k, v in my_map.items():
    print(k, v)  # prints "a 10", then "b 20"

```