import numpy as np
import matplotlib.pyplot as plt

# --- 1. 파라미터 설정 ---
# x(t) = at + b
a = 2  # 기울기
b = 1  # y절편

# 시간 범위
t = np.linspace(-2, 3, 500)

# --- 2. 신호 정의 ---

# (a) 입력 신호: x(t) = at + b
x_t = a * t + b

# (b) 임펄스 응답: h(t)
# h(t)는 두 부분으로 나뉩니다:
# 1. 0에서 1까지 4/3 높이의 사각 펄스
# 2. t=1에서 -1/3 세기의 디랙 델타

# 사각 펄스 부분
h_pulse_t = np.array([-2, 0, 0, 1, 1, 3])
h_pulse_y = np.array([0, 0, 4/3, 4/3, 0, 0])

# (c) 출력 신호: y(t) = at + (b - a/3)
y_t = a * t + (b - a/3)


# --- 3. 그래프 그리기 ---
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12), sharex=True)
plt.rcParams['font.family'] = 'Malgun Gothic' # Windows
# plt.rcParams['font.family'] = 'AppleGothic' # Mac
plt.rcParams['axes.unicode_minus'] = False # 마이너스 폰트 깨짐 방지

# (a) x(t) 플롯
ax1.plot(t, x_t, 'b-', label=f'$x(t) = {a}t + {b}$')
ax1.set_title('입력 신호 $x(t)$', fontsize=15)
ax1.set_ylabel('$x(t)$')
ax1.legend()
ax1.grid(True)
ax1.axhline(0, color='black', linewidth=0.5)
ax1.axvline(0, color='black', linewidth=0.5)

# (b) h(t) 플롯
# 사각 펄스
ax2.plot(h_pulse_t, h_pulse_y, 'b-', label=r'사각 펄스 $\frac{4}{3}[u(t)-u(t-1)]$')
# 디랙 델타 함수 (화살표로 표현)
ax2.arrow(1, 0, 0, -1/3,
          head_width=0.08, head_length=0.15,
          fc='r', ec='r', length_includes_head=True)
# 델타 함수 레이블
ax2.text(1.1, -0.4, r'$-\frac{1}{3}\delta(t-1)$', color='r', fontsize=12)

ax2.set_title('임펄스 응답 $h(t)$', fontsize=15)
ax2.set_ylabel('$h(t)$')
ax2.set_ylim(-1, 2)
ax2.legend()
ax2.grid(True)
ax2.axhline(0, color='black', linewidth=0.5)
ax2.axvline(0, color='black', linewidth=0.5)

# (c) y(t) 플롯
ax3.plot(t, y_t, 'g-', label=f'$y(t) = {a}t + (b - a/3) = {a}t + {b - a/3 :.2f}$')
ax3.set_title('출력 신호 $y(t) = x(t) * h(t)$', fontsize=15)
ax3.set_xlabel('시간 $t$')
ax3.set_ylabel('$y(t)$')
ax3.legend()
ax3.grid(True)
ax3.axhline(0, color='black', linewidth=0.5)
ax3.axvline(0, color='black', linewidth=0.5)

# 레이아웃 조정 및 표시
plt.tight_layout()
plt.show()