import numpy as np
import matplotlib.pyplot as plt

# 파라미터 설정
I0 = 5e-3        # 입력 전류 진폭 (5 mA)
R1 = 1e3         # 저항 1 kΩ
V_D = 0.7        # 다이오드 전압강하 (0.7 V, 실리콘 다이오드)
omega = 2 * np.pi * 60  # 60 Hz
t = np.linspace(0, 1/60, 1000)  # 한 주기 동안

# 입력 전류
I_in = I0 * np.cos(omega * t)

# 다이오드 모델 적용
V_out = I_in * R1
V_out_clipped = np.where(V_out > V_D, V_D, V_out)

# 그래프
plt.figure(figsize=(8,4))
plt.plot(t * 1000, V_out, label="Without Diode (I_in * R1)", linestyle='--')
plt.plot(t * 1000, V_out_clipped, label="With Diode (V_out)", linewidth=2)
plt.axhline(V_D, color='r', linestyle=':', label='V_D = 0.7 V')
plt.title("Output Voltage with Constant-Voltage Diode Model")
plt.xlabel("Time (ms)")
plt.ylabel("Voltage (V)")
plt.legend()
plt.grid(True)
plt.show()
