def is_inside_rectangle(shot_x, shot_y, rect_x1, rect_y1, rect_x2, rect_y2):
    return rect_x1 <= shot_x <= rect_x2 and rect_y1 <= shot_y <= rect_y2

def is_inside_circle(shot_x, shot_y, circle_x, circle_y, circle_r):
    return (shot_x - circle_x) ** 2 + (shot_y - circle_y) ** 2 <= circle_r ** 2


m = int(input())
targets = []

for _ in range(m):
    data = input().split()
    shape = data[0]
    if shape == "rectangle":
        x1, y1, x2, y2 = map(int, data[1:])
        targets.append(("rectangle", x1, y1, x2, y2))
    elif shape == "circle":
        x, y, r = map(int, data[1:])
        targets.append(("circle", x, y, r))

n = int(input())
shots = []

for _ in range(n):
    x, y = map(int, input().split())
    shots.append((x, y))

for shot_x, shot_y in shots:
    hit_count = 0
    for target in targets:
        if target[0] == "rectangle":
            _, x1, y1, x2, y2 = target
            if is_inside_rectangle(shot_x, shot_y, x1, y1, x2, y2):
                hit_count += 1
        elif target[0] == "circle":
            _, x, y, r = target
            if is_inside_circle(shot_x, shot_y, x, y, r):
                hit_count += 1
    print(hit_count)
