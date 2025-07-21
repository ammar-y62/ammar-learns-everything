
# 🚀 Python Interview Prep Notes

---

## 1️⃣ FizzBuzz

### ❓ Problem Summary
- Given a number `N`, for each integer from `1` to `N`:
  - Print `"FizzBuzz"` if divisible by both `3` and `5`.
  - Print `"Fizz"` if divisible only by `3`.
  - Print `"Buzz"` if divisible only by `5`.
  - Otherwise, print the number itself.

### ✅ Solution (Python 2.7)
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

### 📝 Explanation & Analysis
- Checks divisibility using modulo `%`.
- Always checks the combined case (`%3==0 and %5==0`) first.
- **Time Complexity:** `O(N)`.

---

## 2️⃣ Longest Palindromic Substring

### ❓ Problem Summary
- Given a string `S` (only uppercase A-Z).
- Find the **longest substring that is a palindrome**.
- If multiple with same length, pick the **lexicographically smallest**.
- If no palindrome longer than `1`, print `"None"`.

### ✅ Solution (Expand Around Center)
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

### 📝 Explanation & Analysis
- Expands around each center (both odd & even) to find palindromes.
- Keeps longest, or if tied, smallest lex.
- **Time Complexity:** `O(N^2)`.

---

## 3️⃣ Matrix: Largest in Row & Smallest in Column

### ❓ Problem Summary
- Given a matrix of size `N x M` (non-negative integers).
- Find an element that is:
  - **Largest in its row**, and
  - **Smallest in its column**.
- If no such element exists, print `-1`.

### ✅ Solution (Efficient)
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

### 📝 Explanation & Analysis
- Precomputes column minimums to reduce repeated work.
- Checks each cell to see if it’s the row max and col min.
- **Time Complexity:** `O(N*M)` — optimal for up to `1000x1000` matrices.


# 📓 Coding Notes: HackerRank Problems

---

## 🚀 Question 1: Max distinct sums after split

### 📝 Problem summary
Given an array `arr`, split it into two non-empty subarrays at some index `i`.
- Compute the number of **distinct integers** in each subarray.
- Find the **maximum possible sum** of these counts of distinct integers.

---

### 💡 Solution
Use:
- A `set` to track distinct elements in the left subarray.
- A `Counter` to track frequencies in the right subarray.

Iterate over possible splits, at each step:
1. Move the current element from right to left.
2. Compute `len(left) + len(right)` and track the maximum.

#### ✅ Python code
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

---

### ⏱️ Complexity analysis
- **Time:** O(N), each element processed once in left & right structures.
- **Space:** O(N), for set & counter.

---

## 🚀 Question 2: Minimum visibility adjustment cost

### 📝 Problem summary
Given a `n x m` grid `visibilityScore`, each cell has an integer visibility score.
- In each **column**, scores must **strictly increase** downward.
- You can **increase** scores at a cost of `1` per increment.
- Find the **minimum total cost** to achieve this.

---

### 💡 Solution
Process each column independently:
1. For each row (from second down), if `score <= above`, increase it to `above + 1`.
2. Accumulate total cost.

#### ✅ Python code
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

---

### ⏱️ Complexity analysis
- **Time:** O(n * m), processes each cell once.
- **Space:** O(1) extra, modifies grid in place.

---
