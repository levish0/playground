import matplotlib.pyplot as plt
import numpy as np

# 임의의 소자 값 설정 (형태 확인용)
R1 = 9e3  # 9 kOhm
R2 = 1e3  # 1 kOhm
C1 = 1e-6 # 1 uF

# 주파수 범위 설정 (log scale)
f = np.logspace(0, 5, 1000) # 1Hz ~ 100kHz
w = 2 * np.pi * f

# 전달 함수 H(jw) 계산
# Z1 = R1 // (1/jwC1) = R1 / (1 + jw*R1*C1)
# Vo/Vi = R2 / (Z1 + R2)
Z1 = R1 / (1 + 1j * w * R1 * C1)
H = R2 / (Z1 + R2)
H_mag = np.abs(H)           # 선형 스케일 magnitude
H_db = 20 * np.log10(H_mag) # dB 스케일

# 주요 레벨 계산
gain_dc_linear = R2 / (R1 + R2)
gain_hf_linear = 1.0
fz = 1 / (2 * np.pi * R1 * C1)
fp = (R1 + R2) / (2 * np.pi * R1 * R2 * C1)

# 그래프 그리기
plt.figure(figsize=(8, 6))
plt.semilogx(f, H_mag, 'b-', linewidth=2)

# 주요 레벨 및 주파수 표시
plt.axhline(y=gain_dc_linear, color='r', linestyle='--', label=f'DC Gain: R2/(R1+R2)')
plt.axhline(y=gain_hf_linear, color='g', linestyle='--', label='HF Gain: 1')
plt.axvline(x=fz, color='k', linestyle=':', label='Zero Freq (fz)')
plt.axvline(x=fp, color='k', linestyle=':', label='Pole Freq (fp)')

plt.xlabel('Frequency [Hz]')
plt.ylabel('|Vo/Vi| (Linear Scale)')
plt.title('Frequency Response |Vo/Vi|')
plt.grid(True, which="both", ls="-")
plt.legend()
plt.show()