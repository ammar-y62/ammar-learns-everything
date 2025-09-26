
# 🚀 Python Interview Prep Notes

---

## FizzBuzz

### ❓ Problem Summary
- Given a number `N`, for each integer from `1` to `N`:
  - Print `"FizzBuzz"` if divisible by both `3` and `5`.
  - Print `"Fizz"` if divisible only by `3`.
  - Print `"Buzz"` if divisible only by `5`.
  - Otherwise, print the number itself.

### Solution
```python
def funcFizzBuzz(inputNum):
    for i in range(1, inputNum + 1):
        if i % 3 == 0 and i % 5 == 0:
            print "FizzBuzz"
        elif i % 3 == 0:
            print "Fizz"
        elif i % 5 == 0:
            print "Buzz"
        else:
            print i

def main():
    inputNum = int(raw_input())
    funcFizzBuzz(inputNum)

if __name__ == "__main__":
    main()
```

###  Explanation & Analysis
- Checks divisibility using modulo `%`.
- Always checks the combined case (`%3==0 and %5==0`) first.
- **Time Complexity:** `O(N)`.


## Longest Palindromic Substring

### ❓ Problem Summary
- Given a string `S` (only uppercase A-Z).
- Find the **longest substring that is a palindrome**.
- If multiple with same length, pick the **lexicographically smallest**.
- If no palindrome longer than `1`, print `"None"`.

### Solution
```python
def funcSubstring(inputStr):
    n = len(inputStr)
    best_palindrome = ""

    for i in range(n):
        l, r = i, i
        while l >= 0 and r < n and inputStr[l] == inputStr[r]:
            curr = inputStr[l:r+1]
            if len(curr) > 1 and (len(curr) > len(best_palindrome) or
                                   (len(curr) == len(best_palindrome) and curr < best_palindrome)):
                best_palindrome = curr
            l -= 1
            r += 1

        l, r = i, i+1
        while l >= 0 and r < n and inputStr[l] == inputStr[r]:
            curr = inputStr[l:r+1]
            if len(curr) > 1 and (len(curr) > len(best_palindrome) or
                                   (len(curr) == len(best_palindrome) and curr < best_palindrome)):
                best_palindrome = curr
            l -= 1
            r += 1

    return best_palindrome if best_palindrome != "" else "None"
```

###  Explanation & Analysis
- Expands around each center (both odd & even) to find palindromes.
- Keeps longest, or if tied, smallest lex.
- **Time Complexity:** `O(N^2)`.


## Matrix: Largest in Row & Smallest in Column

### ❓ Problem Summary
- Given a matrix of size `N x M` (non-negative integers).
- Find an element that is:
  - **Largest in its row**, and
  - **Smallest in its column**.
- If no such element exists, print `-1`.

### Solution
```python
def funcMatrix(matrix):
    n = len(matrix)
    m = len(matrix[0])

    min_in_col = [min(matrix[i][j] for i in range(n)) for j in range(m)]

    for i in range(n):
        max_in_row = max(matrix[i])
        for j in range(m):
            if matrix[i][j] == max_in_row and matrix[i][j] == min_in_col[j]:
                return matrix[i][j]
    return -1
```

###  Explanation & Analysis
- Precomputes column minimums to reduce repeated work.
- Checks each cell to see if it’s the row max and col min.
- **Time Complexity:** `O(N*M)` — optimal for up to `1000x1000` matrices.


## Max distinct sums after split

###  Problem summary
Given an array `arr`, split it into two non-empty subarrays at some index `i`.
- Compute the number of **distinct integers** in each subarray.
- Find the **maximum possible sum** of these counts of distinct integers.


### Solution
Use:
- A `set` to track distinct elements in the left subarray.
- A `Counter` to track frequencies in the right subarray.

Iterate over possible splits, at each step:
1. Move the current element from right to left.
2. Compute `len(left) + len(right)` and track the maximum.

```python
from collections import Counter

def getMaxSum(arr):
    left_seen = set()
    right_count = Counter(arr)
    max_sum = 0

    for i in range(len(arr) - 1):
        left_seen.add(arr[i])
        right_count[arr[i]] -= 1
        if right_count[arr[i]] == 0:
            del right_count[arr[i]]
        max_sum = max(max_sum, len(left_seen) + len(right_count))
    return max_sum
```


### ⏱️ Complexity analysis
- **Time:** O(N), each element processed once in left & right structures.
- **Space:** O(N), for set & counter.


## Minimum visibility adjustment cost

###  Problem summary
Given a `n x m` grid `visibilityScore`, each cell has an integer visibility score.
- In each **column**, scores must **strictly increase** downward.
- You can **increase** scores at a cost of `1` per increment.
- Find the **minimum total cost** to achieve this.


### Solution
Process each column independently:
1. For each row (from second down), if `score <= above`, increase it to `above + 1`.
2. Accumulate total cost.

```python
def getMinimumCost(visibilityScore):
    n = len(visibilityScore)
    m = len(visibilityScore[0])
    cost = 0

    for col in range(m):
        for row in range(1, n):
            if visibilityScore[row][col] <= visibilityScore[row-1][col]:
                needed = visibilityScore[row-1][col] + 1 - visibilityScore[row][col]
                cost += needed
                visibilityScore[row][col] += needed

    return cost
```

### ⏱️ Complexity analysis
- **Time:** O(n * m), processes each cell once.
- **Space:** O(1) extra, modifies grid in place.

## Handle Non-Fraud Events and Track PII

### Problem Summary
You're given events with:
- `event_type`: either `"underwriting"` or `"fraud_flag"`
- `customer_details`: may contain `phone`, `email`, `address`, `ssn`

Your task is to collect and store **PII values** from **non-fraud events** only.

### Solution
```python
class EventProcessor:
    def __init__(self):
        self.pii_set = set()

    def handle_event(self, event) -> None:
        if event['event_type'] != "fraud_flag":
            self.pii_set.add(event["customer_details"]["phone"])

            if "address" in event['customer_details']:
                self.pii_set.add(event["customer_details"]["address"])
            if "email" in event['customer_details']:
                self.pii_set.add(event["customer_details"]["email"])
            if "ssn" in event['customer_details']:
                self.pii_set.add(event["customer_details"]["ssn"])
```

###  Explanation
- Ignores `fraud_flag` events completely.
- Adds all available customer fields safely using `"key" in dict` checks.
- Fixes the KeyError bug caused by assuming all keys are present.

---

## Track Suspicious Users

### Problem Summary
You need to:
- Add PII to a set when the event type is `"fraud_flag"`
- For `"underwriting"` events:
  - If any PII is in the suspicious set, the customer is suspicious → call `fraud(event)`
  - Otherwise, return `0`
- Always receive the full event in both functions.

### Solution
```python
class SuspicionTracker:
    def __init__(self):
        self.suspicious_pii = set()

    def fraud(self, event):
        customer = event["customer_details"]
        for field in ["phone", "email", "address", "ssn"]:
            if field in customer:
                self.suspicious_pii.add(customer[field])

    def is_suspicious(self, event):
        customer = event["customer_details"]

        if event["event_type"] == "fraud_flag":
            self.fraud(event)
            return 1

        elif event["event_type"] == "underwriting":
            for field in ["phone", "email", "address", "ssn"]:
                if field in customer and customer[field] in self.suspicious_pii:
                    self.fraud(event)
                    return 1
            return 0
```

### Explanation
- Shared `set` stores all flagged PII.
- If an underwriting event matches any PII → it's suspicious → propagate it via `fraud()`.
- Logic is simple, extensible, and mimics real-world fraud tracing systems.
## Load Balancer for WebSocket Connections

### ❓ Problem Summary
- Multiple Jupyter servers need to handle WebSocket connections.
- Each connection has `connectionId`, `userId`, `objectId`.
- Rules:
  - Same `objectId` must always connect to the same server.
  - Each server has a `maxConnectionsPerTarget`.
  - `"DISCONNECT"` removes connections.
  - `"SHUTDOWN"` re‑routes evicted connections in ascending `connectionId` order.
- Return log lines: `connectionId,userId,targetIndex` (1‑based).

### Solution
```python
def route_requests(numTargets, maxConnectionsPerTarget, requests):
    active_count = [0] * numTargets
    target_conn = [set() for _ in range(numTargets)]
    conn_info = {}
    object_target = {}
    object_count = {}
    log = []

    def disconnect(cid):
        user, obj, tgt = conn_info.pop(cid)
        active_count[tgt] -= 1
        target_conn[tgt].remove(cid)
        object_count[obj] -= 1
        if object_count[obj] == 0:
            del object_target[obj]
            del object_count[obj]

    def best_target(exclude=None):
        best = None
        for i in range(numTargets):
            if i == exclude or active_count[i] >= maxConnectionsPerTarget:
                continue
            if best is None or active_count[i] < active_count[best]:
                best = i
        return best

    for req in requests:
        parts = req.split(',')
        action = parts[0]
        if action == "CONNECT":
            cid, user, obj = parts[1], parts[2], parts[3]
            tgt = object_target.get(obj)
            if tgt is not None and active_count[tgt] < maxConnectionsPerTarget:
                pass
            else:
                tgt = best_target()
            if tgt is None:
                continue
            conn_info[cid] = (user, obj, tgt)
            object_target[obj] = tgt
            object_count[obj] = object_count.get(obj, 0) + 1
            active_count[tgt] += 1
            target_conn[tgt].add(cid)
            log.append(f"{cid},{user},{tgt + 1}")
        elif action == "DISCONNECT":
            cid = parts[1]
            if cid in conn_info:
                disconnect(cid)
        elif action == "SHUTDOWN":
            tgt = int(parts[1]) - 1
            evicted = sorted(target_conn[tgt])
            for cid in evicted:
                disconnect(cid)
            for cid in evicted:
                if cid in conn_info:
                    user, obj, _ = conn_info[cid]
                    tgt_new = object_target.get(obj)
                    if tgt_new is not None and active_count[tgt_new] < maxConnectionsPerTarget:
                        pass
                    else:
                        tgt_new = best_target(exclude=tgt)
                    if tgt_new is None:
                        continue
                    conn_info[cid] = (user, obj, tgt_new)
                    object_target[obj] = tgt_new
                    object_count[obj] = object_count.get(obj, 0) + 1
                    active_count[tgt_new] += 1
                    target_conn[tgt_new].add(cid)
                    log.append(f"{cid},{user},{tgt_new + 1}")
    return log
```

### Explanation & Analysis
- Tracks load per server, object affinity, and active connections.
- `"CONNECT"`: reuse mapped server if possible, else least‑loaded.
- `"DISCONNECT"`: frees slot and updates mappings.
- `"SHUTDOWN"`: removes all connections, then re‑routes them orderly.
- **Time Complexity:** `O(numTargets)` per operation in worst case.

