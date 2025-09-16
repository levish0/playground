import sys

N = int(sys.stdin.readline())
arr = list(map(int, sys.stdin.readline().split()))

stack = []
tot = 0

for j in range(N):
    while stack and arr[stack[-1]] <= arr[j]:
        stack.pop()
    prev = stack[-1] if stack else -1
    if j >= 1:
        tot += (j - prev - 1)
    stack.append(j)

print(tot)
