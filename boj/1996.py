import sys

n = int(sys.stdin.readline())

ARR = []
for _ in range(n):
    ARR.append(list(sys.stdin.readline().strip()))

NEW_ARR = [['' for _ in range(n)] for _ in range(n)]

for y in range(n):
    for x in range(n):
        if ARR[y][x].isdigit():
            NEW_ARR[y][x] = "*"
            continue
        surroundings = [(y-1, x), (y-1, x+1), (y-1, x-1), (y, x-1), (y, x+1), (y+1, x), (y+1, x-1), (y+1, x+1)]
        mine_count = 0
        for pos in surroundings:
            if 0 <= pos[0] < n and 0<=pos[1] < n:
                if ARR[pos[0]][pos[1]].isdigit():
                    mine_count += int(ARR[pos[0]][pos[1]])
        if mine_count >= 10:
            NEW_ARR[y][x] = 'M'
        else:
            NEW_ARR[y][x] = str(mine_count)

for _ in range(n):
    print(''.join(NEW_ARR[_]))