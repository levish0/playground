import numpy as np
import matplotlib.pyplot as plt

# 1. 삼각 펄스 h(t) 정의
def h(t):
    """
    삼각 펄스 h(t): [-1, 1]에서 정의되며, 최대값 h(0)=1
    """
    # np.where는 조건에 따라 다른 값을 반환합니다.
    return np.where(
        (t >= -1) & (t <= 1),  # -1 <= t <= 1 조건
        1 - np.abs(t),         # 해당 구간: 1 - |t|
        0                      # 그 외 구간: 0
    )

# 2. 컨볼루션 결과 y(t) 정의
def y_t(t, T, num_terms=10):
    """
    y(t) = sum_{k=-inf}^{+inf} h(t - kT)를 유한한 항(num_terms)으로 근사하여 계산
    """
    y_sum = np.zeros_like(t, dtype=float)
    # k = -num_terms/2 부터 num_terms/2 까지 합산합니다.
    for k in range(-num_terms // 2, num_terms // 2 + 1):
        y_sum += h(t - k * T)
    return y_sum

# 3. 시간 벡터 정의
t = np.linspace(-6, 6, 1000)

# 4. 각 T 값에 대한 계산 및 그래프 그리기
T_values = {'(a) T = 4 (겹침 없음)': 4,
            '(b) T = 2 (경계)': 2,
            '(c) T = 3/2 = 1.5 (겹침)': 1.5,
            '(d) T = 1 (최대 겹침)': 1}

fig, axes = plt.subplots(4, 1, figsize=(10, 12), sharex=True)
fig.suptitle(r'Convolution Result: $y(t) = x(t) * h(t) = \sum_{k} h(t - kT)$', fontsize=16)

for i, (title, T) in enumerate(T_values.items()):
    ax = axes[i]
    # y(t) 계산
    y_result = y_t(t, T)

    # 그래프 그리기
    ax.plot(t, y_result, label=f'T = {T}', color='blue')

    # 축 설정
    ax.set_title(title, loc='left')
    ax.set_ylabel(r'$y(t)$', rotation=0, labelpad=20)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.set_yticks(np.arange(0, np.max(y_result) + 1, 1))

    # 주요 펄스의 중심 위치 표시 (k*T)
    center_points = np.arange(-5 * T, 5 * T, T)
    ax.axhline(0, color='black', linewidth=0.5)

axes[-1].set_xlabel(r'$t$')
plt.tight_layout(rect=[0, 0.03, 1, 0.97]) # 제목 공간 확보
plt.show()