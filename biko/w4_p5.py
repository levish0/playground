import sys
import bisect

n = int(sys.stdin.readline())
points = []

# X=x−y / Y=x+y
for _ in range(n):
    x, y = map(int, input().split())
    tx = x - y
    ty = x + y
    points.append((tx, -ty))

points.sort()
LIS = []
for x, y in points:
    y = -y
    pos = bisect.bisect_left(LIS, y)
    if pos == len(LIS):
        LIS.append(y)
    else:
        LIS[pos] = y

print(len(LIS))
