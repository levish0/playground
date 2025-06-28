# b.txt → 실제 줄바꿈 적용
with open("b.txt", "r", encoding="utf-8") as f:
    content = f.read()

# 문자열에 있는 \n 문자를 실제 줄바꿈으로 변환
converted = content.replace("\\n", "\n")

# 결과를 c.txt에 저장
with open("c.txt", "w", encoding="utf-8") as f:
    f.write(converted)

print("변환된 내용이 c.txt에 저장되었습니다.")
