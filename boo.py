from sympy.logic import SOPform
from sympy import symbols

X3, X2, X1, X0 = symbols('X3 X2 X1 X0')

# Truth table에서 각 출력의 minterms
segments = {
    'Y6': [2, 3, 4, 5, 6, 8, 9],
    'Y5': [0, 1, 3, 4, 5, 6, 7, 8, 9],
    'Y4': [0, 1, 2, 3, 4, 7, 8, 9],
    'Y3': [0, 2, 3, 5, 6, 7, 8, 9],
    'Y2': [0, 5, 6, 8, 9],
    'Y1': [0, 2, 6, 8],
    'Y0': [0, 2, 3, 5, 6, 8, 9]
}

dontcares = [10, 11, 12, 13, 14, 15]

print("Boolean Expressions:\n")
for seg, minterms in segments.items():
    result = SOPform([X3, X2, X1, X0], minterms, dontcares)
    print(f"{seg} = {result}")
    print()