import sys
from bisect import bisect_left, bisect_right

N = int(sys.stdin.readline().strip())
a = list(map(int, sys.stdin.readline().split()))

# p[i] = a[i-1]까지 xor
p = [0] * (N + 1)
for i in range(1, N + 1):
    p[i] = p[i-1] ^ a[i-1]

# UP[j][i]:
# 이전 xor < 현재 XOR
# j까지의 최대

# DOWN[j][i]:
# 이전 xor > 현재 xor
# j까지의 최대
UP = [None] * (N + 1)
DOWN = [None] * (N + 1)
for j in range(1, N + 1):
    UP[j] = [-1] * (j + 1)
    DOWN[j] = [-1] * (j + 1)

for i in range(1, N):
    # left
    left_list = []
    for k in range(1, i + 1):
        xor_val = p[i] ^ p[k-1]
        v_up = 1 if k == 1 else DOWN[i][k] # 하강 → 상승
        v_down = 1 if k == 1 else UP[i][k] # 상승 → 하강
        left_list.append((xor_val, v_up, v_down))

    left_list.sort(key=lambda x: x[0])
    xs = [x[0] for x in left_list]
    m = len(left_list)

    # 왼쪽부터 누적 최댓값
    left_up_max = [-1] * m
    for w in range(m):
        v = left_list[w][1]
        left_up_max[w] = v if w == 0 else max(left_up_max[w-1], v)

    # 오른쪽부터 누적 최댓값
    right_down_max = [-1] * m
    for w in range(m-1, -1, -1):
        v = left_list[w][2]
        right_down_max[w] = v if w == m-1 else max(right_down_max[w+1], v)

    # right
    for k in range(i+1, N+1):
        y = p[k] ^ p[i]

        w = bisect_left(xs, y) - 1
        if w >= 0 and left_up_max[w] > -1:
            c = left_up_max[w] + 1
            if c > UP[k][i+1]:
                UP[k][i+1] = c

        w_2 = bisect_right(xs, y)
        if w_2 < m and right_down_max[w_2] > -1:
            c2 = right_down_max[w_2] + 1
            if c2 > DOWN[k][i+1]:
                DOWN[k][i+1] = c2

ans = 1
if N >= 2:
    ans = 2

for start in range(1, N+1):
    if start == 1:
        ans = max(ans, 1)
    else:
        ans = max(ans, UP[N][start], DOWN[N][start])

print(N - ans)