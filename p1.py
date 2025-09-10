# 원래 식과 최종 결과가 같은지 간단 검증

def calculate_original(a, b, c):
    """원래 식: F = ((a+b')c)'(a+b)(c+a)'"""
    term1 = not ((a or (not b)) and c)  # ((a+b')c)'
    term2 = a or b  # (a+b)
    term3 = not (c or a)  # (c+a)'
    return term1 and term2 and term3


def calculate_final(a, b, c):
    """최종 결과: F = c'ba' = a'bc'"""
    return (not c) and b and (not a)


# 진리표로 비교
print("원래 식과 최종 결과 비교")
print("a b c | 원래식 | c'ba' | 일치?")
print("------|-------|-------|------")

all_match = True

for a in [0, 1]:
    for b in [0, 1]:
        for c in [0, 1]:
            original = calculate_original(a, b, c)
            final = calculate_final(a, b, c)

            match = (original == final)
            if not match:
                all_match = False

            orig_val = 1 if original else 0
            final_val = 1 if final else 0
            match_symbol = "✓" if match else "✗"

            print(f"{a} {b} {c} |   {orig_val}   |   {final_val}   |  {match_symbol}")

print(f"\n결과: {'✅ 계산이 정확합니다!' if all_match else '❌ 계산에 오류가 있습니다!'}")

if all_match:
    print("F = ((a+b')c)'(a+b)(c+a)' = c'ba' = a'bc'")
else:
    print("다시 계산해보세요.")

    # 불일치하는 경우들 출력
    print("\n불일치하는 경우들:")
    for a in [0, 1]:
        for b in [0, 1]:
            for c in [0, 1]:
                original = calculate_original(a, b, c)
                final = calculate_final(a, b, c)
                if original != final:
                    print(f"a={a}, b={b}, c={c}: 원래식={1 if original else 0}, c'ba'={1 if final else 0}")