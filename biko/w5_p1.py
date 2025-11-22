import sys

N = int(sys.stdin.readline().strip())
L = list(map(int, sys.stdin.readline().split()))
K = int(sys.stdin.readline().strip())

l, h = 1, max(L)
ans = 0

while l <= h:
    mid = (l + h) // 2
    cnt = 0
    for u in L:
        cnt += u // mid
        if cnt >= K:
            break
    if cnt >= K:
        ans = mid
        l = mid + 1
    else:
        h = mid - 1

print(ans)
