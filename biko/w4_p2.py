import sys
from array import array
from bisect import bisect_left, bisect_right

INF_NEG = -1

def solve():
    N = int(sys.stdin.readline().strip())
    a = list(map(int, sys.stdin.readline().split()))

    # p[i] = a[0] ^ a[1] ^ ... ^ a[i-1]
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
        UP[j] = array('i', [INF_NEG] * (j + 1))
        DOWN[j] = array('i', [INF_NEG] * (j + 1))

    for t in range(1, N):
        # left
        left_list = []
        for i in range(1, t + 1):
            xor_val = p[t] ^ p[i-1]
            val_up = 1 if i == 1 else DOWN[t][i] # 하강 → 상승
            val_down = 1 if i == 1 else UP[t][i] # 상승 → 하강
            left_list.append((xor_val, val_up, val_down))

        left_list.sort(key=lambda item: item[0])
        xs = [item[0] for item in left_list]
        m = len(left_list)

        pref_up = [INF_NEG] * m
        for idx in range(m):
            v = left_list[idx][1]
            pref_up[idx] = v if idx == 0 else max(pref_up[idx-1], v)

        suff_down = [INF_NEG] * m
        for idx in range(m-1, -1, -1):
            v = left_list[idx][2]
            suff_down[idx] = v if idx == m-1 else max(suff_down[idx+1], v)

        # right
        for k in range(t+1, N+1):
            y = p[k] ^ p[t]

            idx = bisect_left(xs, y) - 1
            if idx >= 0 and pref_up[idx] > INF_NEG:
                cand = pref_up[idx] + 1
                if cand > UP[k][t+1]:
                    UP[k][t+1] = cand

            idx2 = bisect_right(xs, y)
            if idx2 < m and suff_down[idx2] > INF_NEG:
                cand2 = suff_down[idx2] + 1
                if cand2 > DOWN[k][t+1]:
                    DOWN[k][t+1] = cand2

    best = 1
    if N >= 2:
        best = 2

    for start in range(1, N+1):
        if start == 1:
            # 구간 [1,N] 전체가 하나의 조각
            best = max(best, 1)
        else:
            # 구간 [start,N]이 마지막 조각인 경우
            # 상승/하강 패턴 모두 고려
            best = max(best, UP[N][start], DOWN[N][start])

    # 최소 연산 횟수 = N - (최대 조각 수)
    # 많은 조각을 유지할수록 적게 삭제해도 됨
    print(N - best)

if __name__ == "__main__":
    solve()