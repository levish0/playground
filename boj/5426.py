N = int(input())

for _ in range(N):
    s = input()
    length = int(len(s)**0.5)
    start = length-1
    decrypted = ''
    for l in range(length):
        for k in range(length):
            decrypted += s[start+length*k]
        start-=1
    print(decrypted)