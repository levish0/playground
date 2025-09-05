import sys

n = int(sys.stdin.readline())

for i in range(n):
    k = int(sys.stdin.readline())
    j = k*(k+1)//2
    jj = j**2

    print(j, jj, jj)