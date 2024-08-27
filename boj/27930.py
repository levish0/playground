import sys
from collections import deque

IN = sys.stdin.readline().strip()

STR_1 = deque(list('KOREA'))
STR_2 = deque(list('YONSEI'))
for s in IN:
    if STR_1:
        if s == STR_1[0]:
            STR_1.popleft()
    else:
        print('KOREA')
        break
    if STR_2:
        if s == STR_2[0]:
            STR_2.popleft()
    else:
        print('YONSEI')
        break
