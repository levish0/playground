import sys

P = 10**9+7
N, M = map(int, sys.stdin.readline().split())
GRID = [list(sys.stdin.readline().strip()) for _ in range(N)]

def count(sy, sx, ey, ex):
    if sx > ex or sy > ey:
        return 0
    if GRID[sy][sx] == '#' or GRID[ey][ex] == '#':
        return 0

    DP = [[0]*M for _ in range(N)]
    DP[sy][sx] = 1

    for y in range(sy, ey+1):
        for x in range(sx, ex+1):
            if GRID[y][x] == '#':
                continue
            if y > sy:
                DP[y][x] = (DP[y][x] + DP[y - 1][x]) % P
            if x > sx:
                DP[y][x] = (DP[y][x] + DP[y][x - 1]) % P
    return DP[ey][ex]

p11 = count(0, 1, N-1, M-2)
p12 = count(0, 1, N-2, M-1)
p21 = count(1, 0, N-1, M-2)
p22 = count(1, 0, N-2, M-1)
# Lindström Gessel Viennot
det = (p12 * p21 - p11 * p22) % P
print(det * 2 % P)