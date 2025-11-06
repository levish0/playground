import numpy as np
import matplotlib.pyplot as plt

# --- 파라미터 설정 (예시 값) ---
# 이 값들을 바꾸면 그래프 모양이 변합니다.
Ao = 1000.0  # DC 이득 (A_o). 1000은 60dB입니다.
wp0 = 1e3    # 첫 번째 극점(pole) 주파수 (1,000 rad/s)
wp1 = 1e5    # 두 번째 극점(pole) 주파수 (100,000 rad/s)
# ---------------------------------

# 1. 주파수 범위(w) 설정 (log 스케일)
# 10^1 부터 10^7 까지 1000개의 점을 생성합니다.
w = np.logspace(1, 7, 1000)

# 2. s = jw (복소수) 정의
# 파이썬에서 j는 복소수를 의미합니다.
s = 1j * w

# 3. 전달 함수 (Transfer Function) 계산
# A = Ao / ((1 + s/wp0) * (1 + s/wp1))
# 극점이 1개라면 (1 + s/wp1) 부분을 지우면 됩니다.
denominator = (1 + s / wp0) * (1 + s / wp1)
A = Ao / denominator

# 4. 크기(Magnitude)를 dB 스케일로 변환
# 20 * log10(|A|)
magnitude_dB = 20 * np.log10(np.abs(A))

# 5. 그래프 그리기
plt.figure(figsize=(10, 6))

# X축을 log 스케일로 설정 (semilogx)
plt.semilogx(w, magnitude_dB, linewidth=2, label='Bode Magnitude Plot')

# 기준선 (점근선) 그리기 (참고용)
plt.axhline(20 * np.log10(Ao), color='r', linestyle='--', label=f'DC Gain = {20*np.log10(Ao):.0f} dB')
plt.axvline(wp0, color='g', linestyle=':', label=f'Pole $\omega_{{P0}}$ = {wp0:.0e} rad/s')
plt.axvline(wp1, color='m', linestyle=':', label=f'Pole $\omega_{{P1}}$ = {wp1:.0e} rad/s')

# 그래프 설정
plt.title('Bode Magnitude Plot (2-Pole System)')
plt.xlabel('Frequency $\omega$ (rad/s)')
plt.ylabel('Magnitude |A| (dB)')
plt.grid(True, which="both", ls="-", alpha=0.5) # 'which="both"'는 주/부 눈금선 모두 표시
plt.legend()
plt.show()