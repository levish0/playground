N = int(input())

K = int(N**0.5)
if not K == N**0.5:
    K += 1

if N == 1:
    print(4)
else:
    if (K-1)*K > N:
        print((2*K-3)*2)
    else:
        print((K-1)*4)
