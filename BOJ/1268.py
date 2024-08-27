import sys

n = int(sys.stdin.readline())

students = [[0] * n for _ in range(n)]
datas = [list(map(int, sys.stdin.readline().split())) for _ in range(n)]

for j in range(5):
    for i in range(n):
        for k in range(n):
            if datas[i][j] == datas[k][j]:
                students[i][k] = 1

answers = [sum(students[i]) for i in range(n)]

def printAnswer(answers):
    max_count = max(answers)
    for i in range(n):
        if answers[i] == max_count:
            print(i + 1)
            return

printAnswer(answers)
