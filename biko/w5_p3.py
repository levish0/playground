import sys

N = int(sys.stdin.readline())
L = list(map(int, sys.stdin.readline().split()))
Q = int(sys.stdin.readline())
K = list(map(int, sys.stdin.readline().split()))

for k in K:
    low, high = 0.0, float(max(L))

    for _ in range(64): # log2(10^9) - k ≤ -9 log2(10) -> k 대충 60이상 정도
        mid = (low + high) / 2
        if mid == 0:
            break
        cnt = 0
        for x in L:
            cnt += int(x / mid)
            if cnt >= k:
                break
        if cnt >= k:
            low = mid
        else:
            high = mid

    print("{:.18f}".format(low))