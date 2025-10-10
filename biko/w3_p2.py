import sys

N = int(sys.stdin.readline())

COST = []
for i in range(N):
    COST.append(list(map(int, sys.stdin.readline().split())))

DP = [[float('inf')] * N for _ in range(1 << N)] #DP[mask][i] -> 방문상태가 mask이고 현재 위치가 i일때의 cost
DP_from = [[(-1, -1)] * N for _ in range(1 << N)]

DP[1 << 0][0] = 0 # 0번 -> 순환경로-> 값 같음

for mask in range(1 << N):
    for i in range(N):
        if DP[mask][i] == float('inf'):
            continue
        if not (mask & (1 << i)):
            continue

        for j in range(N):
            if mask & (1 << j):
                continue
            if COST[i][j] == 0:
                continue

            n_mask = mask | (1 << j)
            n_cost = DP[mask][i] + COST[i][j]

            if n_cost < DP[n_mask][j]:
                DP[n_mask][j] = n_cost
                DP_from[n_mask][j] = (mask, i)

full_mask = (1 << N) - 1
best_end = -1

res = float('inf')
path = []
for end_pos in range(N):
    if DP[full_mask][end_pos] == float('inf'):
        continue
    if COST[end_pos][0] == 0:
        continue

    tot = DP[full_mask][end_pos] + COST[end_pos][0]

    if tot < res:
        res = tot
        best_end = end_pos

path = []
mask = full_mask
pos = best_end

while pos != -1:
    path.append(pos + 1)
    prev_mask, prev_pos = DP_from[mask][pos]
    mask = prev_mask
    pos = prev_pos

path.reverse()
print(res)
print(' '.join(map(str, path)))