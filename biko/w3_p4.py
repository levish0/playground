import sys

n, m = map(int, sys.stdin.readline().split())
h = list(map(int, sys.stdin.readline().split()))

cost = [[0] * n for _ in range(n)]
for i in range(n):
    min_h = max_h = h[i]
    for j in range(i, n):
        min_h = min(min_h, h[j])
        max_h = max(max_h, h[j])
        cost[i][j] = max_h - min_h

INF = float('inf')
DP = [[-INF] * (m + 1) for _ in range(n + 1)]
DP[0][0] = 0

for i in range(1, n + 1):
    for k in range(1, min(i, m) + 1):
        for j in range(k - 1, i):
            if DP[j][k - 1] != -INF:
                DP[i][k] = max(DP[i][k], DP[j][k - 1] + cost[j][i - 1])

for k in range(1, m + 1):
    print(DP[n][k])