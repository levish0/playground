import sys

N, K = map(int, sys.stdin.readline().split())
A = list(map(int, sys.stdin.readline().split()))

sum_arr = [0] * (N + 1)
for i in range(N):
    sum_arr[i + 1] = sum_arr[i] + A[i]

DP = [0] * (N + 1)
sum_max = [0] * (N + 1)
sum_max[0] = DP[0] - sum_arr[0]

for i in range(1, N+1):
    if i < N:
        limit = i - K
        if limit < 0:
            limit = 0
    else:
        limit = N - 1

    c = sum_arr[i] + sum_max[limit]
    DP[i] = DP[i-1] if DP[i-1] > c else c

    val = DP[i] - sum_arr[i]
    sum_max[i] = sum_max[i-1] if sum_max[i-1] > val else val


print(DP[N])