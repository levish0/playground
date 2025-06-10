import sys
import heapq

N, M = map(int, sys.stdin.readline().split())
heap = []
GRID = []
visited = set()
directions = [(1,0),(-1,0),(0,1),(0,-1)]

for i in range(N):
    line = list(map(int, sys.stdin.readline().split()))
    GRID.append(line)
    for j in range(len(line)):
        if i == 0 or i == N - 1 or j == 0 or j == M - 1:
            heapq.heappush(heap, (-line[j], (i, j)))
            visited.add((i, j))

K = int(sys.stdin.readline())

for i in range(K):
    max_val, (pos_x, pos_y) = heapq.heappop(heap)
    print(pos_x+1, pos_y+1)

    for dir in directions:
        grid_x = pos_x + dir[0]
        grid_y = pos_y + dir[1]

        if 0 <= grid_x < N and 0 <= grid_y < M and (grid_x, grid_y) not in visited:
            heapq.heappush(heap, (-GRID[grid_x][grid_y], (grid_x, grid_y)))
            visited.add((grid_x, grid_y))