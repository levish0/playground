N = int(input())

ARR = []
u = False
start, end = '', ''
for _ in range(N):
    s = input()
    if u:
        end = s[0]
        u = False
    if s == '?':
        if ARR:
            start = ARR[-1][-1]
        u = True
    ARR.append(s)

# print(ARR, start, end)
N = int(input())
answer = ''
for _ in range(N):
    s = input()
    if start:
        if s[0] == start:
            answer = s
    else:
        answer = s
    if end:
        if not s[-1] == end:
            answer = ''

    if answer and answer not in ARR:
        break

print(answer)