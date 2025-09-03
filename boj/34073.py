import sys

n = int(sys.stdin.readline())
sentence = sys.stdin.readline().strip()

print('DORO '.join(sentence.split()), end='DORO')