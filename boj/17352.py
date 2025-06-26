import sys
from collections import defaultdict

N = int(sys.stdin.readline())

island_map = {}

for i in range(N):
    island_map[i+1] = []

for i in range(N-2):
    A, B = map(int, sys.stdin.readline().split())
    island_map[A].append(B)
    island_map[B].append(A)

print(island_map)
