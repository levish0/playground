import sys

class SegTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.tree = {}
        self.build(arr, 0, 0, self.n - 1)

    def build(self, arr, node, start, end):
        if start == end:
            self.tree[node] = arr[start]
        else:
            mid = (start + end) // 2
            self.build(arr, 2 * node + 1, start, mid)
            self.build(arr, 2 * node + 2, mid + 1, end)
            self.tree[node] = self.tree[2 * node + 1] ^ self.tree[2 * node + 2]

    def update(self, node, start, end, idx, val):
        if start == end:
            self.tree[node] = val
        else:
            mid = (start + end) // 2
            if idx <= mid:
                self.update(2 * node + 1, start, mid, idx, val)
            else:
                self.update(2 * node + 2, mid + 1, end, idx, val)
            self.tree[node] = self.tree[2 * node + 1] ^ self.tree[2 * node + 2]

    def query(self, node, start, end, l, r):
        if r < start or end < l:
            return 0
        if l <= start and end <= r:
            return self.tree[node]

        mid = (start + end) // 2
        left_xor = self.query(2 * node + 1, start, mid, l, r)
        right_xor = self.query(2 * node + 2, mid + 1, end, l, r)
        return left_xor ^ right_xor

    def update_v(self, idx, val):
        self.update(0, 0, self.n - 1, idx, val)

    def range_xor(self, l, r):
        return self.query(0, 0, self.n - 1, l, r)

N, Q = map(int, sys.stdin.readline().split())
mascots = list(map(int, sys.stdin.readline().split()))

seg_tree = SegTree(mascots)

for _ in range(Q):
    query = list(map(int, sys.stdin.readline().split()))
    t = query[0]
    a = query[1]
    b = query[2]

    if t == 1:
        mascots[a-1] = b
        seg_tree.update_v(a-1, b)
    else:
        result = seg_tree.range_xor(a-1, b-1)
        print(result)