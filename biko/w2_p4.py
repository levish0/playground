import sys

class SegTree:
    def __init__(self):
        self.tree = {}

    def update(self, node, start, end, idx, val):
        if start == end:
            self.tree[node] = self.tree.get(node, 0) + val
        else:
            mid = (start + end) // 2
            if idx <= mid:
                self.update(2 * node + 1, start, mid, idx, val)
            else:
                self.update(2 * node + 2, mid + 1, end, idx, val)
            self.tree[node] = self.tree.get(2 * node + 1, 0) + self.tree.get(2 * node + 2, 0)

    def query(self, node, start, end, l, r):
        if r < start or end < l:
            return 0
        if l <= start and end <= r:
            return self.tree.get(node, 0)

        mid = (start + end) // 2
        left_sum = self.query(2 * node + 1, start, mid, l, r)
        right_sum = self.query(2 * node + 2, mid + 1, end, l, r)
        return left_sum + right_sum

    def update_v(self, idx, val):
        self.update(0, 1, 1000000000, idx, val)

    def range_sum(self, l, r):
        if l > r:
            return 0
        return self.query(0, 1, 1000000000, l, r)

N, M = map(int, sys.stdin.readline().split())
buildings = []

for _ in range(N):
    buildings.append(int(sys.stdin.readline()))

building_cnt = SegTree()
connected = SegTree()

for height in buildings:
    building_cnt.update_v(height, 1)

for i in range(N - 1): # 인접 쌍 -1
    min_height = min(buildings[i], buildings[i + 1])
    connected.update_v(min_height, 1)

for _ in range(M):
    ops = list(map(int, sys.stdin.readline().split()))

    if ops[0] == 1:
        water_level = ops[1]
        node_cnt = building_cnt.range_sum(water_level, 1e9)
        edge_cnt = connected.range_sum(water_level, 1e9)
        print(node_cnt - edge_cnt)

    else:
        pos = ops[1] - 1
        new_height = ops[2]
        old_height = buildings[pos]

        building_cnt.update_v(old_height, -1)
        building_cnt.update_v(new_height, 1)

        if pos > 0:
            old_min = min(old_height, buildings[pos - 1])
            new_min = min(new_height, buildings[pos - 1])
            connected.update_v(old_min, -1)
            connected.update_v(new_min, 1)

        if pos < N - 1:
            old_min = min(old_height, buildings[pos + 1])
            new_min = min(new_height, buildings[pos + 1])
            connected.update_v(old_min, -1)
            connected.update_v(new_min, 1)

        buildings[pos] = new_height