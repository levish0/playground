# P = 10^9 + 7 is a prime.
P = 1000000007
import sys

"""
N: A non-negative integer representing the target sequence number.
K: A positive integer representing the number of coefficients.
coefficients: A list of length K consisting non-negative integers less than P.
constant: A non-negative integer less than P.
init_values: A list of length K consisting of non-negative integers less than P.
"""
def find_nth_term(N, K, coefficients, constant, init_values):
    if N < K:
        return init_values[N] % P

    def matrix_multiply(A, B):
        ra, ca = len(A), len(A[0])
        rb, cb = len(B), len(B[0])
        result = [[0] * cb for _ in range(ra)]
        for i in range(ra):
            for j in range(cb):
                for k in range(ca):
                    result[i][j] = (result[i][j] + A[i][k] * B[k][j]) % P
        return result

    def matrix_power(matrix, power):
        n = len(matrix)
        result = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        base = [row[:] for row in matrix]

        while power > 0:
            if power % 2:
                result = matrix_multiply(result, base)
            base = matrix_multiply(base, base)
            power //= 2
        return result

    T = [[0] * (K + 1) for _ in range(K + 1)]
    for j in range(K):
        T[0][j] = coefficients[j]
    T[0][K] = constant
    for i in range(1, K):
        T[i][i-1] = 1
    T[K][K] = 1

    init_state = init_values[::-1] + [1]
    power = N - (K - 1)
    T_power = matrix_power(T, power)

    result = 0
    for j in range(K + 1):
        result = (result + T_power[0][j] * init_state[j]) % P

    return result


N, K = map(int, sys.stdin.readline().split())
line2 = list(map(int, sys.stdin.readline().split()))
coefficients = line2[:K]
constant = line2[K]
init_values = list(map(int, sys.stdin.readline().split()))

print(find_nth_term(N, K, coefficients, constant, init_values))