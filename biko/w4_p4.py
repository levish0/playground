import sys

T = int(sys.stdin.readline().strip())
cases = []
for i in range(T):
    a, b = map(int, sys.stdin.readline().split())
    cases.append((a,b))

MOD = 10**9 + 7

a = [c[0] for c in cases]
b = [c[1] for c in cases]
S = [a[i] + b[i] for i in range(T)]
max_tot = max(S)

# 최대 i
max_i = 0
while (max_i+1)*(max_i+2)//2 <= max_tot:
    max_i += 1

ans = [0]*T
dp = [0]*(max_tot+1)   # dp[s] = #부분집합(1..i) 합이 s
dp[0] = 1

for i in range(1, max_i + 1):
    step = i
    for s in range(max_tot, step-1, -1):
        dp[s] = (dp[s] + dp[s - step]) % MOD

    total_i = i * (i + 1) // 2
    # pref[s] 합 dp[t] 0~total_i
    pref = [0] * (total_i + 1)
    acc = 0
    for s in range(total_i + 1):
        acc += dp[s]
        if acc >= MOD:
            acc -= MOD
        pref[s] = acc

    for t in range(T):
        if S[t] < total_i:
            continue
        L = total_i - b[t]
        if L < 0:
            L = 0
        R = a[t] if a[t] <= total_i else total_i
        if L <= R:
            add = pref[R] - (pref[L - 1] if L > 0 else 0)
            ans[t] = (ans[t] + add) % MOD

out = '\n'.join(map(str, ans))
print(out)