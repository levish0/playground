import itertools
import pandas as pd

rows = []

for A, B, X1, X2 in itertools.product([0, 1], repeat=4):
    # RS FF for A
    R = (not X1) and B and X2
    S = (not X1) and (not B) and (not X2)
    A_next = S or (A and (not R))

    # Right 4 AND gates
    t1 = (not X1) and B and A
    t2 = (not X1) and (not B) and (not A)
    t3 = (not X2) and B and (not A)
    t4 = (not X2) and (not B) and A

    # OR combinations
    T = t1 or t2
    Z1 = t2 or t3
    Z2 = t3 or t4

    # T FF for B
    B_next = B ^ T  # XOR

    rows.append((A, B, X1, X2, int(R), int(S), int(A_next), int(T), int(B_next), int(Z1), int(Z2)))

df = pd.DataFrame(rows, columns=["A", "B", "X1", "X2", "R", "S", "A+", "T", "B+", "Z1", "Z2"])
print(df)
