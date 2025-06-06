import numpy as np

# 물체 거리 (d_o) cm
d_o = np.array([30.0, 40.0, 50.0, 60.0, 70.0])

# 이미지 거리 (d_i) cm (0cm 기준)
d_i = np.array([14.7, 26.6, 37.5, 48.1, 58.7])

# 0cm 기준에서의 이미지 거리를 거울을 기준으로 수정 (d_i' = d_i - d_o)
d_i_corrected = d_o - d_i
print("Corrected Image Distances (d_i'):", d_i_corrected)

# 렌즈 방정식 사용하여 초점 거리(f) 계산: 1/f = 1/d_o + 1/d_i'
focal_lengths = 1 / (1 / d_o + 1 / d_i_corrected)

# 이론적인 초점 거리 (cm)
theoretical_focal_length = 10.0

# 각 초점 거리의 퍼센트 오차 계산
percentage_errors = (focal_lengths - theoretical_focal_length) / theoretical_focal_length * 100

# 평균 초점 거리 계산
average_focal_length = np.mean(focal_lengths)

# 평균 절대 퍼센트 오차율 계산 (%)
average_absolute_percentage_error = np.mean(np.abs(percentage_errors))

# 결과 출력
print("\n--- Focal Length Calculation and Error Analysis ---")
for i in range(len(d_o)):
    print(f"Object Distance (d_o) = {d_o[i]:.1f} cm, Corrected Image Distance (d_i') = {d_i_corrected[i]:.2f} cm, Focal Length (f) = {focal_lengths[i]:.2f} cm, Error = {percentage_errors[i]:.2f}%")

print(f"\nAverage Focal Length (f_avg) = {average_focal_length:.3f} cm")
print(f"Theoretical Focal Length = {theoretical_focal_length:.1f} cm")
print(f"Average Absolute Percentage Error = {average_absolute_percentage_error:.2f}%")