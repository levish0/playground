import sys
import bisect

n = int(sys.stdin.readline())

S = []
add = 0

for i in range(n):
    op, x = map(int, sys.stdin.readline().split())

    if op == 1:
        new_x = x - add
        pos = bisect.bisect_left(S, new_x)

        if pos < len(S) and S[pos] == new_x:
            S.pop(pos)
        else:
            S.insert(pos, new_x)

    elif op == 2:
        add += x

    elif op == 3:
        pos = bisect.bisect_left(S, x-add)

        if pos < len(S):
            print(S[pos] + add)
        else:
            print("NONE")