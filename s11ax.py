import matplotlib.pyplot as plt
import numpy as np

# 0ns부터 200ns까지 0.1ns 간격으로 시간 배열 생성
t = np.linspace(0, 200, 2001)

# S, R, P, Q 신호를 0으로 초기화
S = np.zeros_like(t)
R = np.zeros_like(t)
P = np.zeros_like(t)
Q = np.zeros_like(t)

# --- 입력 신호 S, R 정의 (사용자 시나리오) ---
# t=50~100ns: S=1
S[(t >= 50) & (t < 100)] = 1
# t=140ns~ : S=1
S[t >= 140] = 1

# t=50~100ns: R=1
R[(t >= 50) & (t < 100)] = 1


# --- 출력 신호 P, Q 계산 (위의 단계별 분석 기반) ---

# P 신호
P[t < 60] = 1                 # 0~60ns: 초기값 1
P[(t >= 60) & (t < 110)] = 0  # 60~110ns: P=0 (S=1,R=1 안정 상태)
P[(t >= 110) & (t < 120)] = 1 # 110~120ns: 진동 1
P[(t >= 120) & (t < 130)] = 0 # 120~130ns: 진동 0
P[(t >= 130) & (t < 140)] = 1 # 130~140ns: 진동 1
P[t >= 140] = 0               # 140ns 이후: P=0 (t=140에서 0, t=160에서 0유지)

# Q 신호
Q[t < 110] = 0                # 0~110ns: 초기값 0, S=1,R=1 안정값 0
Q[(t >= 110) & (t < 120)] = 1 # 110~120ns: 진동 1
Q[(t >= 120) & (t < 130)] = 0 # 120~130ns: 진동 0
Q[(t >= 130) & (t < 140)] = 1 # 130~140ns: 진동 1
Q[(t >= 140) & (t < 150)] = 0 # 140~150ns: 진동 0 & S=1 불안정
Q[t >= 150] = 1               # 150ns 이후: Q=1 (최종 'Set' 상태)


# --- 그래프 그리기 ---
fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, sharex=True, figsize=(12, 9))
fig.suptitle("S-R Latch Timing (User Scenario: S=R=1 at 50ns)", fontsize=16, y=1.02)

# S 신호 플롯
ax1.plot(t, S, 'b-', label='S')
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
vlines = [50, 60, 100, 110, 120, 130, 140, 150, 160]
for ax in [ax1, ax2, ax3, ax4]:
    ax.set_ylim(-0.2, 1.2)
    ax.set_yticks([0, 1])
    ax.grid(True, which='both', linestyle=':', linewidth=0.5)
    ax.legend(loc='upper right')
    for v in vlines:
        ax.axvline(v, color='gray', linestyle='dashed', lw=1)

# x축 눈금
plt.xticks(np.arange(0, 201, 10), rotation=90)
plt.xlim(0, 200)
plt.tight_layout()
plt.show()