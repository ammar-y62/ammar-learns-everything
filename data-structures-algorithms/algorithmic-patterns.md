## ↔️ Prefix / Postfix Pattern
- Precompute running **sums**, **products**, or **max/min values** from left (prefix) or right (postfix).
- Helps avoid nested loops and improve time from `O(n²)` to `O(n)`.
- Often used when the result at index `i` depends on elements before and/or after it.

| Pattern        | Examples                              |
|----------------|----------------------------------------|
| Prefix product | Product of Array Except Self           |
| Prefix sum     | Running Sum, Range Sum Queries         |
| Postfix max    | Trapping Rain Water (right max array)  |

```python
# Product of Array Except Self
nums = [1,2,3,4]
res = [1] * len(nums)

# Prefix pass (left to right)
for i in range(1, len(nums)):
    res[i] = res[i-1] * nums[i-1]

# Postfix pass (right to left)
postfix = 1
for i in range(len(nums)-2, -1, -1):
    postfix *= nums[i+1]
    res[i] *= postfix
```
**Notes:**
- Prefix builds result using values before i.
- Postfix modifies result using values after i.
- Space can be optimized to O(1) by reusing the output array.

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


## 🪣 Bucket Sort
- Group items by frequency, rank, or score into buckets (lists).
- Used to avoid full sorting (`O(n log n)`) by bucketing into indexable ranges.
- Often paired with `Counter` and reverse traversal.

| Pattern               | Examples                                  |
|----------------------|-------------------------------------------|
| Buckets of frequency | Top K Frequent Elements, Char Frequency   |
| Indexed buckets      | Sort by Score, Group Elements by Count    |

```python
count = Counter(nums)
buckets = [[] for _ in range(len(nums) + 1)]
for num, freq in count.items():
    buckets[freq].append(num)

res = []
for i in range(len(buckets) - 1, -1, -1):
    for num in buckets[i]:
        res.append(num)
        if len(res) == k:
            return res
```
**Notes:**
- buckets[i] holds all elements that appear exactly i times.
- Traverse from high freq to low (range(n, -1, -1)).
- Avoids need for a heap or full sort.
- Often cleaner and faster in practice for frequency-based problems like Top K.

## 📐 Dynamic Programming (DP)
- Breaks problems into **overlapping subproblems**
- Store results to **avoid recomputation** (bottom-up or top-down)

### 🪙 Bottom-Up DP: Coin Change

```python
def coinChange(coins, amount):
    dp = [0] + [float('inf')] * amount  # dp[i] = min coins for amount i
    for i in range(1, amount + 1):
        for coin in coins:
            if coin > i:
                break  # No need to check further
            dp[i] = min(dp[i], dp[i - coin] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1
```

**Notes:**
- `dp[i]` means: minimum coins needed to make amount `i`
- Initialize with `inf`, except `dp[0] = 0`
- Try every coin at each step
- If `dp[amount] == inf`, it's impossible ➞ return -1


### 🧠 Top-Down DP: Fibonacci with Memoization

```python
def fib(n, memo={}):
    if n in memo: return memo[n]
    if n <= 1: return n
    memo[n] = fib(n - 1, memo) + fib(n - 2, memo)
    return memo[n]
```

**Notes:**
- Memoization caches results (dictionary)
- Avoids repeated recursive calls
- Useful when subproblems overlap a lot
## 💰 Greedy Pattern
- Make the **best local choice at each step**, hoping it leads to the global optimum.
- Greedy algorithms are **fast and simple**, usually `O(n)` or `O(n log n)`.
- **No backtracking or dynamic programming** — once a choice is made, it’s final.

| Pattern                  | Examples                                |
|--------------------------|------------------------------------------|
| Choose max/min locally   | Jump Game, Activity Selection            |
| Move based on best ratio | Fractional Knapsack, Gas Station         |
| Greedy traversal         | Container With Most Water                |

```python
# Jump Game: Greedy reach
nums = [2,3,1,1,4]
reach = 0
for i in range(len(nums)):
    if i > reach:
        return False
    reach = max(reach, i + nums[i])
return True
```
**Notes:**
- Greedy Choice Property: A global optimum can be reached by choosing local optimums.
- No Recalculation: No need to try all combinations (unlike DP or backtracking).
- Risk: Doesn’t always guarantee the best result unless problem fits the greedy paradigm.