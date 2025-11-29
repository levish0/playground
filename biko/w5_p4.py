import sys
import heapq

N = int(sys.stdin.readline())
L = list(map(int, sys.stdin.readline().split()))
Q = int(sys.stdin.readline())
K = list(map(int, sys.stdin.readline().split()))
max_k = max(K)


heap = []
for i, li in enumerate(L):
    heap.append((-float(li), i, 1)) # 최대 힙
heapq.heapify(heap)

ans = [0.0] * (max_k + 1)
total = 0

while total < max_k:
    neg_v, i, p = heapq.heappop(heap)
    v = -neg_v  # 실제 길이

    total += 1
    ans[total] = v

    np = p + 1 # 쪼갬
    heapq.heappush(heap, (-(L[i] / np), i, np))

res = []
for k in K:
    res.append("{:.18f}".format(ans[k]))
print("\n".join(res))