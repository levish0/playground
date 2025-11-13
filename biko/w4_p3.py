import math
import sys

S = sys.stdin.readline().strip()
n = len(S)

# ( = +1, ) = -1 로 미리 괄호 균형 계산
S_p = [0] * (n + 1)
for i in range(n):
    S_p[i+1] = S_p[i] + (1 if S[i] == '(' else -1)

LOG = math.floor(math.log2(n+1)) + 1
st = [S_p[:]]

for k in range(1, LOG):
    prev = st[k-1]
    size = n + 1 - (1 << k)
    row = [0] * (size + 1)
    for i in range(size + 1):
        # min(st[k-1][i], st[k-1][i + 2^(k-1)])
        row[i] = min(prev[i], prev[i + (1 << (k-1))])
    st.append(row)

lg = [0] * (n + 2)
for i in range(2, n + 2):
    lg[i] = lg[i // 2] + 1

def rmq_min(l, r):
    k = lg[r - l + 1]
    return min(st[k][l], st[k][r - (1 << k) + 1])

def is_valid(l, r):
    if S_p[r+1] - S_p[l] !=0:
        return False
    return rmq_min(l+1, r+1) - S_p[l] >= 0

ans = 0
if n >= 2:
    prev = [0]*(n-1)
    for i in range(n-1):
        if S[i] != S[i+1]:
            prev[i] = 1
            if is_valid(i, i+1):
                ans += 1

    # 짝수만 가능
    d = 4
    while d <= n:
        new = [0]*(n-d+1)
        for l in range(n-d+1):
            r = l + d - 1
            # S[l..r]이 팰린드롬 ->  S[l+1..r-1]이 팰린드롬, S[l] != S[r]
            if prev[l+1] and S[l] != S[r]:
                new[l] = 1
                if is_valid(l, r):
                    ans += 1
        prev = new
        d += 2

print(ans)
