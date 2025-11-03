from collections import deque
from typing import Dict, List, Optional


# ------------------------------------------------------------
# 1) Quicksort (fixed: preserves duplicates equal to the pivot)
# ------------------------------------------------------------
def quicksort(nums: List[int]) -> List[int]:
    """
    Return a sorted copy of nums using quicksort. Fixed to preserve
    duplicates equal to the pivot.
    """
    if len(nums) <= 1:
        return nums[:]
    pivot = nums[len(nums) // 2]
    left = [x for x in nums if x < pivot]
    middle = [x for x in nums if x == pivot]
    right = [x for x in nums if x > pivot]
    return quicksort(left) + middle + quicksort(right)


# ------------------------------------------------------------
# 2) Binary search (fixed: correct loop bounds)
# ------------------------------------------------------------
def binary_search(arr: List[int], target: int) -> int:
    """
    Returns index of target in sorted arr, or -1 if not found.
    Corrected while loop to ensure the rightmost element is examined.
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
# 3) Unweighted shortest path (fixed: use BFS by popleft)
# ------------------------------------------------------------
def shortest_path_unweighted(
    graph: Dict[int, List[int]], start: int, goal: int
) -> Optional[List[int]]:
    """
    BFS for shortest path in an unweighted graph. Uses FIFO queue
    (popleft) so the first discovered path to goal is guaranteed
    to be shortest (in number of edges).
    """
    if start == goal:
        return [start]
    q = deque([start])
    parent = {start: None}
    while q:
        node = q.popleft()  # fixed: FIFO
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
# 4) Disjoint Set Union / Union-Find (fixed: union on roots, union by rank)
# ------------------------------------------------------------
class DSU:
    """
    Union-find with path compression & union by rank.
    """

    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> None:
        # union by root and by rank
        rx = self.find(x)
        ry = self.find(y)
        if rx == ry:
            return
        if self.rank[rx] < self.rank[ry]:
            self.parent[rx] = ry
        elif self.rank[rx] > self.rank[ry]:
            self.parent[ry] = rx
        else:
            self.parent[ry] = rx
            self.rank[rx] += 1

    def connected(self, x: int, y: int) -> bool:
        return self.find(x) == self.find(y)
