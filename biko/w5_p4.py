import sys

N = int(sys.stdin.readline())
L = []
max_end = 0

for _ in range(N):
    a, b, c = map(int, sys.stdin.readline().split())
    L.append((a,b,c))
    if b > max_end:
        max_end = b

def count(t):
    total = 0
    for start, end, step in L:
        if t < start:
            # t가 start보다 작으면 해당 수열에 등장할 수는 없음
            continue
        up = min(t, end)
        total += (up - start) // step + 1
    return total % 2 == 1

l, h = 0, max_end
answer = -1
while l <= h:
    mid = (l + h) // 2
    if count(mid) == 1:
        answer = mid
        h = mid - 1
    else:
        l = mid + 1

if answer == -1:
    print(-1)
else:
    count = 0
    for start, end, step in L:
        if start <= answer <= end and (answer - start) % step == 0:
            count += 1
    print(answer, count)