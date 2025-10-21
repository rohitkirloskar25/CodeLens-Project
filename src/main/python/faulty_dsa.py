# DSA algorithms with subtle bugs that show up only on certain inputs.

from collections import deque
from typing import Dict, Iterable, List, Tuple, Optional


# ------------------------------------------------------------
# 1) Quicksort (BUG: drops duplicates equal to the pivot)
# ------------------------------------------------------------
def quicksort(nums: List[int]) -> List[int]:
    """
    Intended: return a sorted copy of nums.
    BUG (input-dependent): duplicates equal to the pivot are lost.
      Example: [5,5,5,5] -> returns [5] instead of [5,5,5,5]
    """
    if len(nums) <= 1:
        return nums[:]
    pivot = nums[len(nums) // 2]
    left = [x for x in nums if x < pivot]
    right = [x for x in nums if x > pivot]
    # BUG: we add a single 'pivot' but drop all other elements equal to pivot
    return quicksort(left) + [pivot] + quicksort(right)


# ------------------------------------------------------------
# 2) Binary search (BUG: misses target at the rightmost position)
# ------------------------------------------------------------
def binary_search(arr: List[int], target: int) -> int:
    """
    Returns index of target in sorted arr, or -1 if not found.
    BUG (edge-case): when target is the last element, it can return -1.
    """
    lo, hi = 0, len(arr) - 1
    while lo < hi:  # BUG: should be `<=` to examine hi as well
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return lo if lo <= hi and lo < len(arr) and arr[lo] == target else -1


# ------------------------------------------------------------
# 3) Unweighted shortest path (BUG: uses DFS behavior by popping from the right)
# ------------------------------------------------------------
def shortest_path_unweighted(
    graph: Dict[int, List[int]], start: int, goal: int
) -> Optional[List[int]]:
    """
    BFS intended for shortest path in an unweighted graph.
    BUG: uses pop() (LIFO) instead of popleft() (FIFO) -> depth-first behavior.
    On specific graphs this yields a non-minimal path length.
    """
    if start == goal:
        return [start]
    q = deque([start])
    parent = {start: None}
    while q:
        node = q.pop()  # BUG: should be popleft() for BFS
        for nbr in graph.get(node, []):
            if nbr not in parent:
                parent[nbr] = node
                if nbr == goal:
                    # reconstruct
                    path = [goal]
                    while parent[path[-1]] is not None:
                        path.append(parent[path[-1]])
                    return list(reversed(path))
                q.append(nbr)
    return None


# ------------------------------------------------------------
# 4) Disjoint Set Union / Union-Find (BUG: unions on raw nodes, not roots)
# ------------------------------------------------------------
class DSU:
    """
    Intended: union/find with path compression & union by rank.
    BUG: union(x, y) links y under x directly without finding roots.
         This breaks transitivity for sequences like union(1,2); union(2,3).
    """

    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> None:
        # BUG: should use roots rx, ry = find(x), find(y)
        # and union by rank; instead link raw nodes.
        if x == y:
            return
        self.parent[y] = x  # ❌ wrong

    def connected(self, x: int, y: int) -> bool:
        return self.find(x) == self.find(y)
