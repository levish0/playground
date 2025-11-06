import matplotlib.pyplot as plt
import numpy as np

# 0ns부터 200ns까지 0.1ns 간격으로 시간 배열 생성
t = np.linspace(0, 200, 2001)

# S, R, P, Q 신호를 0으로 초기화
S = np.zeros_like(t)
R = np.zeros_like(t)
P = np.zeros_like(t)
Q = np.zeros_like(t)

# --- 입력 신호 S, R 정의 ---
S[(t >= 50) & (t < 100)] = 1
R[(t >= 75) & (t < 100)] = 1

# --- 출력 신호 P, Q 계산 (위의 단계별 분석 기반) ---

# P 신호
P[t < 60] = 1
P[(t >= 60) & (t < 110)] = 0

# Q 신호
Q[t < 70] = 0
Q[(t >= 70) & (t < 85)] = 1
Q[(t >= 85) & (t < 110)] = 0

# t=110ns 이후 진동(Oscillation) 부분
for start_time in range(110, 200, 20):
    end_time_1 = start_time + 10
    end_time_2 = start_time + 20

    # 10ns 동안 1
    P[(t >= start_time) & (t < end_time_1)] = 1
    Q[(t >= start_time) & (t < end_time_1)] = 1

    # 다음 10ns 동안 0
    P[(t >= end_time_1) & (t < end_time_2)] = 0
    Q[(t >= end_time_1) & (t < end_time_2)] = 0

# --- 그래프 그리기 ---
fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, sharex=True, figsize=(12, 9))

# S 신호 플롯
ax1.plot(t, S, 'b-', label='S')
ax1.set_title('S-R Latch (NOR) Timing Diagram with 10ns Delay', fontsize=16)
ax1.set_ylabel('S', fontsize=14, rotation=0, labelpad=10)

# R 신호 플롯
ax2.plot(t, R, 'r-', label='R')
ax2.set_ylabel('R', fontsize=14, rotation=0, labelpad=10)

# P(Q_bar) 신호 플롯
ax3.plot(t, P, 'm-', label='P (Solved)')
ax3.set_ylabel('P', fontsize=14, rotation=0, labelpad=10)

# Q 신호 플롯
ax4.plot(t, Q, 'g-', label='Q (Solved)')
ax4.set_ylabel('Q', fontsize=14, rotation=0, labelpad=10)
ax4.set_xlabel('Time (ns)', fontsize=14)

# 모든 축에 공통 설정 적용
for ax in [ax1, ax2, ax3, ax4]:
    ax.set_ylim(-0.2, 1.2)
    ax.set_yticks([0, 1])
    ax.grid(True, which='both', linestyle=':', linewidth=0.5)
    ax.legend(loc='upper right')

# x축 눈금을 10ns 또는 20ns 단위로 설정
plt.xticks(np.arange(0, 201, 10), rotation=90)
ax1.vlines([50, 60, 70, 75, 85, 100, 110, 120, 130, 140], -0.2, 1.2, colors='gray', linestyles='dashed', lw=1)
ax2.vlines([50, 60, 70, 75, 85, 100, 110, 120, 130, 140], -0.2, 1.2, colors='gray', linestyles='dashed', lw=1)
ax3.vlines([50, 60, 70, 75, 85, 100, 110, 120, 130, 140], -0.2, 1.2, colors='gray', linestyles='dashed', lw=1)
ax4.vlines([50, 60, 70, 75, 85, 100, 110, 120, 130, 140], -0.2, 1.2, colors='gray', linestyles='dashed', lw=1)

plt.xlim(0, 200)
plt.tight_layout()
plt.show()