N, M = map(int, input().split())

A = [[0]*100 for _ in range(100)]

for i in range(N):
    b_x, b_y, t_x, t_y = map(int, input().split())
    for x in range(b_x, t_x+1):
        for y in range(b_y, t_y+1):
            A[x-1][y-1] += 1

count = 0
for x in range(100):
    for y in range(100):
        if A[x][y] > M:
            count+=1

print(count)