import sys

n, m = map(int, sys.stdin.readline().split())
A = list(map(int, sys.stdin.readline().split()))

NEG = -float('inf')

# dp_c[j] = j -> c
# dp_p[j] = j -> +
# dp_m[j] = j -> -
dp_c = [NEG] * (m + 1)
dp_p = [NEG] * (m + 1)
dp_m = [NEG] * (m + 1)

dp_c[0] = 0

for i in range(n):
    new_c = [NEG] * (m + 1)
    new_p = [NEG] * (m + 1)
    new_m = [NEG] * (m + 1)

    for j in range(m + 1):
        if dp_c[j] != NEG:
            new_c[j] = max(new_c[j], dp_c[j])

        # new +
        if j < m and dp_c[j] != NEG:
            new_p[j + 1] = max(new_p[j + 1], dp_c[j] + A[i])

        # new -
        if j < m and dp_c[j] != NEG:
            new_m[j + 1] = max(new_m[j + 1], dp_c[j] - A[i])

        # +
        if dp_p[j] != NEG:
            new_p[j] = max(new_p[j], dp_p[j])

        # -
        if dp_m[j] != NEG:
            new_m[j] = max(new_m[j], dp_m[j])

        # + -> - -> c
        if dp_p[j] != NEG:
            new_c[j] = max(new_c[j], dp_p[j] - A[i])

        # - -> + -> c
        if dp_m[j] != NEG:
            new_c[j] = max(new_c[j], dp_m[j] + A[i])

    dp_c = new_c
    dp_p = new_p
    dp_m = new_m

for k in range(1, m + 1):
    result = dp_c[k]
    if result == NEG:
        result = 0
    print(result)