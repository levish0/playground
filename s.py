import sys

def solve_knapsack():
    # 짐 목록: (무게, 가치)
    luggage = [
        (10, 17),
        (9, 15),
        (7, 12),
        (4, 7),
        (3, 6)
    ]
    # 최대 허용 무게
    capacity = 15

    # DP 테이블(배열)을 초기화합니다.
    # dp[w]는 무게 한도가 w일 때의 최대 가치를 저장합니다.
    # 인덱스 0부터 15까지 총 16개의 공간이 필요합니다.
    dp = [0] * (capacity + 1)

    # 각 짐(item)에 대해 순회합니다.
    for weight, cost in luggage:
        # DP 테이블을 뒤에서부터 앞으로 갱신합니다.
        # (같은 짐을 여러 번 선택하는 것을 방지하기 위해 역순으로 순회)
        # w는 현재 고려하는 무게 한도를 의미합니다.
        for w in range(capacity, weight - 1, -1):
            # 짐을 선택하는 경우와 선택하지 않는 경우 중 더 이득이 되는 값을 선택합니다.
            # 1. 짐을 선택하지 않는 경우: 가치는 그대로 dp[w]
            # 2. 짐을 선택하는 경우: (현재 짐의 가치) + (현재 짐의 무게를 뺀 무게 한도에서의 최대 가치)
            #    = cost + dp[w - weight]
            dp[w] = max(dp[w], dp[w - weight] + cost)

    # 모든 짐을 고려한 후, dp[capacity] (dp[15])에
    # 15kg 한도 내에서의 최대 가치가 저장됩니다.
    max_cost = dp[capacity]
    print(f"주어진 짐 목록: {luggage}")
    print(f"무게 한도: {capacity}kg")
    print(f"달성 가능한 최대 가치 합계: {max_cost}")

solve_knapsack()