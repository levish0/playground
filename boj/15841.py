D = [1, 1] + [0]*489

for i in range(2, 491):
    D[i] = D[i-1]+D[i-2]

while 1:
    n = int(input())
    if n == -1:
        break

    print(f"Hour {n}: {D[n - 1]} cow(s) affected")