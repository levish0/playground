import sys
import heapq

n = int(sys.stdin.readline())

L = list(map(int, sys.stdin.readline().split()))

l_heap = []
r_heap = []

for index, n in enumerate(L):
    heapq.heappush(l_heap, -n)

    if r_heap and -l_heap[0] > r_heap[0]:
        heapq.heappush(r_heap, -heapq.heappop(l_heap))

    if len(l_heap) > len(r_heap) + 1:
        heapq.heappush(r_heap, -heapq.heappop(l_heap))
    elif len(r_heap) > len(l_heap):
        heapq.heappush(l_heap, -heapq.heappop(r_heap))

    if index%2 == 0:
        print(-l_heap[0], end=' ')