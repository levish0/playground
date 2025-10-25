MOD = 998244353
INV6 = pow(6, MOD - 2, MOD)

def solve():
    import sys
    input = sys.stdin.readline
    n = int(input().strip())

    dp = [0] * (n + 1)
    dp[n] = 1  # n장의 카드에서 시작

    for i in range(n, 1, -1):
        cnt = i
        next_i = i * 5 // 6
        dp[next_i] = (dp[next_i] + dp[i]) % MOD

    inv_sum = pow(sum(dp[1:]) % MOD, MOD - 2, MOD)
    for i in range(1, n + 1):
        print(dp[i] * inv_sum % MOD)
