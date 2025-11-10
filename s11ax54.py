import matplotlib.pyplot as plt
import numpy as np

# 시간 축 설정 (한 사이클을 20 단위로)
t = np.linspace(0, 100, 1001)

# 초기화
CLK = np.zeros_like(t)
X = np.zeros_like(t)
Q1 = np.zeros_like(t)
Q2 = np.zeros_like(t)
Z = np.zeros_like(t)

# 클럭 생성 (주기 20, 듀티 50%)
for i in range(5):
    CLK[(t >= 20 * i) & (t < 20 * i + 10)] = 1

# 입력 X 시퀀스: 1, 0, 0, 1, 1
# 문제 조건: "falling과 rising 사이 중간에 변한다" -> 클럭이 0일 때 변한다고 가정 (t=15, 35...)
X[(t >= 0) & (t < 15)] = 1  # 첫 번째 값 1
X[(t >= 15) & (t < 35)] = 0  # 두 번째 값 0
X[(t >= 35) & (t < 55)] = 0  # 세 번째 값 0
X[(t >= 55) & (t < 75)] = 1  # 네 번째 값 1
X[(t >= 75) & (t <= 100)] = 1  # 다섯 번째 값 1

# Q1, Q2 상태 업데이트 (하강 에지: t=10, 30, 50, 70, 90)
# 초기값 0
falling_edges = [10, 30, 50, 70, 90]
q1_val, q2_val = 0, 0

for i in range(len(t)):
    # 하강 에지 감지 및 상태 업데이트
    if t[i] in falling_edges:
        # 현재 입력 X값 확인
        x_val = X[i]

        # 차기 상태 계산 (J-K FF 식 이용)
        # Q1_next = X*Q2*Q1' + X'*Q1
        q1_next = (x_val and q2_val and not q1_val) or (not x_val and q1_val)
        # Q2_next = X*Q1'*Q2' + X'*Q2
        q2_next = (x_val and not q1_val and not q2_val) or (not x_val and q2_val)

        q1_val, q2_val = int(q1_next), int(q2_next)

    Q1[i] = q1_val
    Q2[i] = q2_val

# 출력 Z 계산 (Mealy Machine: Z = X XOR Q2)
# np.logical_xor를 사용하여 비트별 XOR 연산
Z = np.logical_xor(X.astype(int), Q2.astype(int)).astype(int)

# --- 그래프 그리기 ---
fig, axes = plt.subplots(5, 1, sharex=True, figsize=(10, 8))
fig.suptitle('Timing Chart for Input X = 10011', fontsize=16)

signals = [CLK, X, Q1, Q2, Z]
labels = ['Clock', 'Input X', 'Q1', 'Q2', 'Output Z']
colors = ['k', 'b', 'm', 'g', 'r']

for i, ax in enumerate(axes):
    ax.plot(t, signals[i], color=colors[i], linewidth=1.5)
    ax.set_ylabel(labels[i], rotation=0, labelpad=20, fontsize=12)
    ax.set_ylim(-0.2, 1.2)
    ax.set_yticks([0, 1])
    ax.grid(True, axis='x', linestyle='--', alpha=0.6)
    # 하강 에지 표시
    for edge in falling_edges:
        ax.axvline(x=edge, color='r', linestyle=':', alpha=0.5)

axes[-1].set_xlabel('Time', fontsize=12)
plt.tight_layout()
plt.show()