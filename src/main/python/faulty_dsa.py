from collections import deque
from typing import Dict, List, Optional

# ------------------------------------------------------------
# 1) Quicksort — fixed (keeps all duplicates)
# ------------------------------------------------------------
def quicksort(nums: List[int]) -> List[int]:
    """
    Return a sorted copy of nums (stable on equal values).
    Fix: partition into < pivot, == pivot, > pivot so duplicates are preserved.
    """
    if len(nums) <= 1:
        return nums[:]
    pivot = nums[len(nums) // 2]
    left  = [x for x in nums if x < pivot]
    mid   = [x for x in nums if x == pivot]
    right = [x for x in nums if x > pivot]
    return quicksort(left) + mid + quicksort(right)


# ------------------------------------------------------------
# 2) Binary search — fixed (checks rightmost element too)
# ------------------------------------------------------------
def binary_search(arr: List[int], target: int) -> int:
    """
    Returns index of target in sorted arr, or -1 if not found.
    Fix: loop condition uses <= so hi is examined.
    """
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


# ------------------------------------------------------------
# 3) Unweighted shortest path — fixed (true BFS with FIFO queue)
# ------------------------------------------------------------
def shortest_path_unweighted(
    graph: Dict[int, List[int]], start: int, goal: int
) -> Optional[List[int]]:
    """
    BFS shortest path in an unweighted graph. Returns node list from start to goal,
    or None if unreachable.
    Fix: use popleft() to ensure FIFO (BFS), store parents to reconstruct path.
    """
    if start == goal:
        return [start]

    q = deque([start])
    parent = {start: None}

    while q:
        node = q.popleft()
        for nbr in graph.get(node, []):
            if nbr not in parent:
                parent[nbr] = node
                if nbr == goal:
                    # reconstruct path back to start
                    path = [goal]
                    while parent[path[-1]] is not None:
                        path.append(parent[path[-1]])
                    return list(reversed(path))
                q.append(nbr)
    return None


# ------------------------------------------------------------
# 4) Disjoint Set Union / Union-Find — fixed (union by rank on roots)
# ------------------------------------------------------------
class DSU:
    """
    Union-Find with path compression & union by rank.
    Fix: union(x, y) unions the roots, not the raw nodes.
    """

    def _init_(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> None:
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return
        # union by rank
        if self.rank[rx] < self.rank[ry]:
            self.parent[rx] = ry
        elif self.rank[rx] > self.rank[ry]:
            self.parent[ry] = rx
        else:
            self.parent[ry] = rx
            self.rank[rx] += 1

    def connected(self, x: int, y: int) -> bool:
        return self.find(x) == self.find(y)
