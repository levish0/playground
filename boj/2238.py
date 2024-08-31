import sys
from collections import defaultdict

U, N = map(int, sys.stdin.readline().split())

D = defaultdict(list)
for i in range(N):
    p, c = map(str, sys.stdin.readline().split())
    c = int(c)

    if c <= U:
        D[c].append(p)

count = float('inf')
min_cost = float('inf')
for cost in sorted(D.keys()):
    if len(D[cost]) < count:
        count = len(D[cost])
        min_cost = cost

print(D[min_cost][0], min_cost)