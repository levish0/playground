import sys

N, P, Q = map(int, sys.stdin.readline().split())

n, m, a, b, c, d = map(int, sys.stdin.readline().split())

# 팩토리얼을 미리 구함
factorial = [1]*N
for i in range(1, N):
    factorial[i] = (factorial[i-1]*i) % P

inv_factorial = [1]*N
inv_factorial[N-1] = pow(factorial[N-1], P-2, P)
for i in range(N-2, -1, -1):
    inv_factorial[i] = (inv_factorial[i+1] * (i+1)) % P

def binomial(n,m):
    if m > n or m < 0 or n < 0:
        return 0
    if m ==0 or m == n :
        return 1
    return (factorial[n] * inv_factorial[m] % P) * inv_factorial[n-m] % P

res = 0
for i in range(1, Q+1):
    if m <= n:
        c_i = binomial(n, m)
    else:
        c_i = binomial(m, n)

    res ^= i* c_i

    if i < Q:
        n = (a*n + b)%N
        m = (c*m + d)%N

print(res)