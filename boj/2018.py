import sys

N = int(sys.stdin.readline())

l_pointer, r_pointer = 1,1
TOT = 1
count = 1

if N == 1 or N == 2:
    print(1)

else:
    while r_pointer < N:
        if TOT == N:
            count += 1
            r_pointer += 1
            TOT += r_pointer
        elif TOT < N:
            r_pointer += 1
            TOT += r_pointer
        else:
            TOT -= l_pointer
            l_pointer += 1
        # print(l_pointer, r_pointer, TOT, count)

    print(count)