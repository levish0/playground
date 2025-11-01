def solve():
    n, m = map(int, input().split())
    heights = list(map(int, input().split()))

    for k in range(1, m + 1):
        # O(n^2m) 솔루션으로 먼저 정답 확인
        # 이후 O(nm) 최적화 필요
        INF = float('-inf')
        dp = [[INF] * (k + 1) for _ in range(n + 1)]

        dp[0][0] = 0

        for i in range(1, n + 1):
            for j in range(1, min(i, k) + 1):
                # 마지막 그룹이 l+1부터 i까지
                for l in range(j - 1, i):
                    if dp[l][j-1] == INF:
                        continue

                    # 그룹 내 최대-최소
                    group_max = max(heights[l:i])
                    group_min = min(heights[l:i])
                    cost = group_max - group_min

                    dp[i][j] = max(dp[i][j], dp[l][j-1] + cost)

        print(dp[n][k] if dp[n][k] != INF else 0)

if __name__ == "__main__":
    solve()