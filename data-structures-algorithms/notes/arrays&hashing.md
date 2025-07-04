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

```