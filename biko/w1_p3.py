import sys

n = int(sys.stdin.readline())
r, c = map(int, sys.stdin.readline().split())

GRID = [[0]*(2**n) for _ in range(2**n)]

tile_id = 0

def tile_unit(current_y, current_x, size, blank_y, blank_x):
    global tile_id

    if size == 2:
        tile_id+=1
        for i in range(2):
            for j in range(2):
                if current_y + i != blank_y or current_x + j != blank_x:
                    GRID[current_y+i][current_x+j] = tile_id
        return
    
    half = size // 2
    mid_y, mid_x = current_y + half, current_x + half
    
    if blank_y < mid_y and blank_x >= mid_x: quad = 0
    elif blank_y < mid_y and blank_x < mid_x: quad = 1
    elif blank_y >= mid_y and blank_x < mid_x: quad = 2
    else: quad = 3

    centers = [
        (mid_y - 1, mid_x), # 우상
        (mid_y - 1, mid_x - 1), # 좌상
        (mid_y, mid_x - 1), # 좌하
        (mid_y, mid_x) # 우하
    ]

    tile_id+=1
    for i, (y,x) in enumerate(centers):
        if i!=quad:
            GRID[y][x] = tile_id

    # 우상
    by, bx = (blank_y, blank_x) if quad == 0 else centers[0]
    tile_unit(current_y, current_x + half, half, by, bx)
    # 좌상
    by, bx = (blank_y, blank_x) if quad == 1 else centers[1]
    tile_unit(current_y, current_x, half, by, bx)
    # 좌하
    by, bx = (blank_y, blank_x) if quad == 2 else centers[2]
    tile_unit(current_y + half, current_x, half, by, bx)
    # 우하
    by, bx = (blank_y, blank_x) if quad == 3 else centers[3]
    tile_unit(current_y + half, current_x + half, half, by, bx)

tile_unit(0, 0, 2**n, r-1, c-1)

for row in GRID:
    print(" ".join(map(str, row)))