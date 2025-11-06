import matplotlib.pyplot as plt
import numpy as np

# 0부터 12까지의 시간을 0.01 단위로 세밀하게 나눔
t = np.linspace(0, 12, 1201)

# S, R, Q 신호를 0으로 초기화
S = np.zeros_like(t)
R = np.zeros_like(t)
Q = np.zeros_like(t)

# --- S 입력 신호 정의 ---
# 이미지의 S 파형을 시간대에 맞게 1로 설정
S[(t >= 1) & (t < 2)] = 1
S[(t >= 4) & (t < 5)] = 1
S[(t >= 6) & (t < 7)] = 1

# --- R 입력 신호 정의 ---
# 이미지의 R 파형을 시간대에 맞게 1로 설정
R[(t >= 3) & (t < 4)] = 1
R[(t >= 9) & (t < 10)] = 1

# --- Q 출력 신호 계산 ---
# 문제의 조건: Q는 1에서 시작
Q[0] = 1

# 시간(t)을 1부터 끝까지 순회하며 Q 값을 계산
for i in range(1, len(t)):
    s_val = S[i]
    r_val = R[i]
    q_prev = Q[i-1]  # 바로 직전의 Q 값

    if s_val == 1 and r_val == 0:
        # Set 조건
        Q[i] = 1
    elif s_val == 0 and r_val == 1:
        # Reset 조건
        Q[i] = 0
    elif s_val == 0 and r_val == 0:
        # Hold 조건
        Q[i] = q_prev
    else:
        # S=1, R=1 (금지된 상태, 이 문제에선 없음)
        # 만약 발생한다면, 이전 상태를 유지하거나 불안정(NaN) 처리
        Q[i] = q_prev

# --- 그래프 그리기 ---
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True, figsize=(12, 7))

# S 신호 플롯
ax1.plot(t, S, 'b-', label='S')
ax1.set_title('S-R Latch Timing Diagram Solution', fontsize=16)
ax1.set_ylabel('S', fontsize=14)

# R 신호 플롯
ax2.plot(t, R, 'r-', label='R')
ax2.set_ylabel('R', fontsize=14)

# 계산된 Q 신호 플롯
ax3.plot(t, Q, 'g-', label='Q (Solved)')
ax3.set_ylabel('Q', fontsize=14)
ax3.set_xlabel('Time (arbitrary units)', fontsize=14)

# 모든 축에 공통 설정 적용
for ax in [ax1, ax2, ax3]:
    ax.set_ylim(-0.2, 1.2)  # y축 범위
    ax.set_yticks([0, 1])   # y축 눈금
    ax.grid(True, which='both', linestyle=':', linewidth=0.5) # 그리드
    ax.legend(loc='upper right')

# x축 눈금을 1 단위로 설정
plt.xticks(np.arange(0, 13, 1))
plt.tight_layout()  # 그래프 레이아웃 최적화
plt.show()