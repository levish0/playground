import sys
from collections import deque

N = int(sys.stdin.readline())
S = list(map(int, sys.stdin.readline().split()))

if S[N-1] < 0:
    print(-1)
    exit()

seg_size = 1
while seg_size < N:
    seg_size *= 2

seg_base = N  # 세그트리 노드는 N부터 시작
seg_total = 2 * seg_size
total_nodes = seg_base + seg_total

GRAPH = [[] for _ in range(total_nodes)]
indeg = [0] * total_nodes

def add_edge(u, v):
    GRAPH[u].append(v)
    indeg[v] += 1
for pos in range(N):
    idx = seg_size+pos
    add_edge(pos, seg_base+idx)

for idx in range(2, 2 * seg_size):
    parent = idx // 2
    add_edge(seg_base + idx, seg_base + parent)

def add_range_to_target(left, right, target):
    if left > right:
        return
    l = left + seg_size
    r = right + seg_size
    while l <= r:
        if l & 1:  # l이 오른쪽 자식
            add_edge(seg_base + l, target)
            l += 1
        if not (r & 1):  # r이 왼쪽 자식
            add_edge(seg_base + r, target)
            r -= 1
        l //= 2  # 부모로 이동
        r //= 2

for i in range(N):
    if S[i] > 0:
        # 범위 내 모든 건물이 자신보다 낮음
        left = i + 1
        right = min(N - 1, i + S[i] - 1)
        if left <= right:
            add_range_to_target(left, right, i)  # 범위 → i
    else:
        # S[i]번째에 더 높은 건물이 필요
        distance = -S[i]
        j = min(N - 1, i + distance)
        add_edge(i, j)  # i → j (A_i < A_j)

queue = deque()
for i in range(total_nodes):
    if indeg[i] == 0:
        queue.append(i)

order = []
while queue:
    node = queue.popleft()
    order.append(node)
    for i in GRAPH[node]:
        indeg[i] -= 1
        if indeg[i] == 0:
            queue.append(i)

if len(order) != total_nodes:
    print(-1)
    exit()

heights = [0] * N
curr = 1
for node in order:
    if 0 <= node < N:
        heights[node] = curr
        curr += 1

print(' '.join(map(str, heights)))