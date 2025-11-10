import matplotlib.pyplot as plt
import numpy as np

# x축 데이터 생성 (입력 범위 설정)
x = np.linspace(-20, 20, 400)

# 구간별 파라미터
beta = 0.1
A1 = 1000
A2 = 100
xe_threshold = 0.1

# Knee point 계산 (기울기가 변하는 지점)
# xe = 0.1일 때, y = A1 * xe = 1000 * 0.1 = 100
# 이때 x = xe + beta * y = 0.1 + 0.1 * 100 = 10.1
x_knee = xe_threshold + beta * (A1 * xe_threshold)
y_knee = A1 * xe_threshold

# 폐루프 이득 계산
Af1 = A1 / (1 + A1 * beta)
Af2 = A2 / (1 + A2 * beta)

# y값 계산 (piecewise 함수)
y = np.zeros_like(x)
for i, val in enumerate(x):
    if abs(val) <= x_knee:
        y[i] = Af1 * val
    elif val > x_knee:
        y[i] = y_knee + Af2 * (val - x_knee)
    else: # val < -x_knee
        y[i] = -y_knee + Af2 * (val + x_knee)

# 그래프 그리기
plt.figure(figsize=(8, 6))
plt.plot(x, y, 'b-', linewidth=2, label='Output (y)')
plt.xlabel('Input (x)')
plt.ylabel('Output (y)')
plt.title('Closed-loop Input-Output Relationship')
plt.grid(True)

# 주요 지점 표시
plt.plot([x_knee, -x_knee], [y_knee, -y_knee], 'ro')
plt.text(x_knee+1, y_knee-20, f'({x_knee:.1f}, {y_knee:.0f})', color='red')
plt.text(-x_knee-8, -y_knee+10, f'({-x_knee:.1f}, {-y_knee:.0f})', color='red')

# 기울기(Gain) 표시
plt.text(0, 0, f'Slope ≈ {Af1:.2f}', ha='center', va='bottom', rotation=45, color='green')
plt.text(15, 120, f'Slope ≈ {Af2:.2f}', ha='center', va='bottom', rotation=35, color='green')

plt.legend()
plt.show()