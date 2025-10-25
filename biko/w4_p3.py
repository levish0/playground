import sys

s = sys.stdin.readline().strip()
n = len(s)

match = [-1] * n
stack = []
for i in range(n):
    if s[i] == '(':
        stack.append(i)
    elif stack:
        j = stack.pop()
        match[j] = i
        match[i] = j

def is_symmetric(start, end):
    length = end - start + 1
    for i in range(length // 2):
        if s[start + i] == s[end - i]:
            return False
    return True

count = 0
for i in range(n):
    if s[i] == ')' and match[i] != -1:
        j = match[i]
        if is_symmetric(j, i):
            count += 1

        k = j - 1
        while k >= 0 and s[k] == ')' and match[k] != -1:
            start = match[k]
            if is_symmetric(start, i):
                count += 1
            k = match[k] - 1

print(count)