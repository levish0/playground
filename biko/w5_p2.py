import sys

N = int(sys.stdin.readline())
L = list(map(int, sys.stdin.readline().split()))
K = int(sys.stdin.readline())

low, high = 0, max(L) #O(N)

for _ in range(64): # log2(10^9) - k ≤ -9 log2(10) -> k 대충 60이상 정도
    mid = (low + high) / 2
    if mid == 0:
        break
    cnt = 0
    for x in L:
        cnt += int(x / mid)
        if cnt >= K:
            break
    if cnt >= K:
        low = mid
    else:
        high = mid

print("{:.18f}".format(low))