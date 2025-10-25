import statistics
import numpy as np

# 점수 리스트
scores = [
    47, 54, 49, 24, 17, 16, 44, 79, 82, 22, 65, 63, 65, 73, 17, 44, 18, 79,
    51, 74, 48, 82, 19, 22, 27, 69, 51, 4, 64, 72, 75, 79, 13, 11, 35, 63.5,
    64, 67, 77, 11, 64, 48, 63, 47, 9, 76, 35, 16, 25, 46, 2, 50, 68, 66, 3,
    35, 83, 73, 45, 41, 42, 54, 40, 14, 23, 12, 46, 60, 34, 24, 71, 75, 78,
    72, 25, 46, 41, 41, 74, 81, 68, 23, 68, 46, 58, 54, 14, 10, 25, 69, 73,
    61.5, 67, 1, 71, 10, 30, 14, 77, 76, 35
]

# 통계 계산
scores_sorted = sorted(scores, reverse=True)  # 내림차순 정렬 (등수 계산 편리)
total = len(scores)

Q1 = np.percentile(scores, 25)
Q2 = np.percentile(scores, 50)
Q3 = np.percentile(scores, 75)

print(f"총 점수 수: {total}")
print(f"Q1: {Q1}")
print(f"Q2 (중앙값): {Q2}")
print(f"Q3: {Q3}")

