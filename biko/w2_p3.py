import sys

input = sys.stdin.readline

n, q = map(int, input().split())

card_values = [i % 13 + 1 for i in range(52)]

deck_states = [None] * n
has_been_modified = [False] * n

for _ in range(q):
    query = list(map(int, input().split()))

    if query[0] == 0:
        _, a, b, i, j = query
        if b <= a or i == j:
            continue
        for deck_idx in range(a, min(b, n)):
            if not has_been_modified[deck_idx]:
                deck_states[deck_idx] = list(range(52))
                has_been_modified[deck_idx] = True
            deck = deck_states[deck_idx]
            deck[i], deck[j] = deck[j], deck[i]
    else:
        _, a, b = query
        if b <= a:
            print(0)
            continue
        total = 0
        for deck_idx in range(a, min(b, n)):
            if has_been_modified[deck_idx]:
                top_card = deck_states[deck_idx][51]
            else:
                top_card = 51
            total += card_values[top_card]
        print(total)
