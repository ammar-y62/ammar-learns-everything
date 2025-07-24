## 🔷 Arrays & Hashing

| #  | Problem Name                   | Difficulty | Category         | Time     | Space    | Notes                  | Link |
|----|-------------------------------|------------|------------------|----------|----------|------------------------|------|
| 1  | Contains Duplicate            | Easy       | Set     | O(1)     | O(1)     | len(nums) != len(set(nums)) | [🔗](https://neetcode.io/problems/duplicate-integer?list=blind75) |
| 2  | Valid Anagram                 | Easy       | Hashmap | O(n)     | O(1)     | Counter(s) == Counter(t)      | [🔗](https://neetcode.io/problems/is-anagram?list=blind75) |
| 3  | Two Sum                       | Easy       | Hashmap  | O(n)     | O(n)     | Save index in map, check complement in map, diff = (target-nums[i])   | [🔗](https://neetcode.io/problems/two-integer-sum?list=blind75) |
| 4  | Group Anagrams                | Medium     | Hashmap, Tuple | O(n·k) | O(n·k)  | Use 26-char freq tuple as hashmap key     | [🔗](https://neetcode.io/problems/anagram-groups?list=blind75) |
| 5  | Top K Frequent Elements       | Medium     | Bucket Sort    | O(n) | O(n)    | Group by freq in list of buckets         | [🔗](https://neetcode.io/problems/top-k-elements-in-list?list=blind75) |
| 6  | Encode and Decode Strings     | Medium     | Strings, Design  | O(n)     | O(n)     | Encode: len#str for each string      | [🔗](https://neetcode.io/problems/string-encode-and-decode?list=blind75) |
| 7  | Product of Array Except Self  | Medium     | Prefix, Postfix   | O(n)     | O(1)     | Multiply prefix and postfix on the fly   | [🔗](https://neetcode.io/problems/products-of-array-discluding-self?list=blind75) |
| 8  | Longest Consecutive Sequence | Medium     | HashSet          | O(n)     | O(n)     | Start only from sequence beginning (i-1)    | [🔗](https://neetcode.io/problems/longest-consecutive-sequence?list=blind75) |
| 9  | Valid Palindrome              | Easy       | Two Pointers   | O(n)   | O(1)   | Skip non-alphanum, compare lowercased chars      | [🔗](https://neetcode.io/problems/is-palindrome?list=blind75) |
| 10 | 3Sum                          | Medium     | Two Pointers, Sorting  | O(n²)  | O(n)   | Sort + skip duplicates + move l/r based on 3-sum    | [🔗](https://neetcode.io/problems/three-integer-sum?list=blind75) |
| 11 | Container With Most Water     | Medium     | Two Pointers, Greedy   | O(n)   | O(1)   | Move shorter height to try better area   | [🔗](https://neetcode.io/problems/max-water-container?list=blind75) |
| 12 | Shortest Uncommon Substring in an Array     | Medium     | HashMap      | O(n·L²)     | O(n·L²)  | Brute all substrings, track unique by map           | [🔗](https://leetcode.com/problems/shortest-uncommon-substring-in-an-array) |
| 13 | Insert Delete GetRandom O(1)                | Medium     | HashMap, Random, Design| O(1)        | O(n)     | Dict for index + array for values           | [🔗](https://leetcode.com/problems/insert-delete-getrandom-o1) |
| 14 | Insert Delete GetRandom O(1) – Duplicates   | Hard       | HashMap, Random, Design| O(1)        | O(n)     | Dict of sets + list    | [🔗](https://leetcode.com/problems/insert-delete-getrandom-o1-duplicates-allowed) |
| 15 | Coin Change                                 | Medium     | DP, Bottom-Up          | O(amount·n) | O(amount)| dp[i] = min coins to make amount i     | [🔗](https://leetcode.com/problems/coin-change) |
