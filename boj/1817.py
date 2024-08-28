N, M = map(int, input().split())

if N == 0:
    print(0)
else:
    L = list(map(int, input().split()))
    i, BOX, count = 0, 0, 1
    for box in L:
        if BOX + box <= M:
            BOX+=box
        else:
            BOX = box
            count += 1
    print(count)