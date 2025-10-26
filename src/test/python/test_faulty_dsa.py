import pytest
from src.main.python.faulty_dsa import quicksort, binary_search, shortest_path_unweighted, DSU


# ---------------------- quicksort ----------------------

def test_quicksort_basic_pass():
    assert quicksort([3, 1, 2]) == [1, 2, 3]
    assert quicksort([]) == []
    assert quicksort([7]) == [7]

def test_quicksort_duplicates_should_preserve_all_elements_but_drops():
    data = [5, 5, 5, 5, 3, 3, 9]
    out = quicksort(data)
    # Correct output should contain same multiset (length preserved)
    assert out == sorted(data)
    assert len(out) == len(data)  # ❌ Fails: buggy impl drops equal-to-pivot items


# -------------------- binary search --------------------

def test_binary_search_found_middle_pass():
    arr = [1, 3, 4, 9, 12]
    assert binary_search(arr, 9) == 3

def test_binary_search_rightmost_edge_bug():
    arr = [1, 2, 4, 6]
    # correct index for target=6 is 3; buggy code can return -1
    assert binary_search(arr, 6) == 3  # ❌ may fail due to off-by-one while loop


# ----------------- unweighted shortest path ------------

def test_shortest_path_simple_pass():
    g = {0: [1], 1: [2], 2: []}
    assert shortest_path_unweighted(g, 0, 2) == [0, 1, 2]

def test_shortest_path_should_use_bfs_but_acts_like_dfs():
    # Graph where BFS shortest path is of length 2, DFS likely takes longer.
    # 0 -> 1 -> 4
    #  \        ^
    #   \-> 2 -> 3 -/
    g = {
        0: [1, 2],
        1: [4],
        2: [3],
        3: [4],
        4: []
    }
    path = shortest_path_unweighted(g, 0, 4)
    assert path == [0, 1, 4]     # ❌ buggy DFS-like order usually yields [0,2,3,4]


# -------------------------- DSU ------------------------

def test_dsu_trivial_pass():
    d = DSU(5)
    assert d.connected(0, 0) is True
    assert d.connected(0, 1) is False

def test_dsu_chain_union_should_connect_but_doesnt():
    d = DSU(5)
    d.union(1, 2)
    d.union(2, 3)  # with a proper union-by-root, 1 and 3 become connected
    assert d.connected(1, 3) is True   # ❌ fails: union linked raw nodes, not roots
