# a.txt → JSON용 문자열 변환
with open("a.txt", "r", encoding="utf-8") as f:
    content = f.read()

# JSON에서 사용할 수 있도록 이스케이프 처리
import json
escaped = json.dumps(content)

# json.dumps는 큰따옴표로 감싸므로, 감싸는 따옴표 제거하고 내부 문자열만 출력
escaped_str = escaped[1:-1]

print(escaped_str)  # 복사해서 JSON 문자열로 사용

# 결과를 c.txt에 저장
with open("a2.txt", "w", encoding="utf-8") as f:
    f.write(escaped_str)

print("변환된 내용이 a2.txt에 저장되었습니다.")