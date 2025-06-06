import numpy as np
import matplotlib.pyplot as plt

# 데이터
V_AB = np.array([-0.510, -1.011, -1.512, -2.038, -2.504, -2.918])
I_exp = np.array([0.000061, 0.000091, 0.000152, 0.000212, 0.000242, 0.000303])  # mA
I_theo_array = np.full_like(I_exp, -8.7107279e-07)  # mA

# 그래프
plt.figure(figsize=(8, 5))
plt.plot(V_AB, I_exp, 'o-', label='Experimental Current', color='blue')
plt.plot(V_AB, I_theo_array, '--', label='Theoretical Current', color='red')
plt.xlabel('V_AB (V)')
plt.ylabel('Current (mA)')
plt.title('Reverse Bias I-V Characteristics of 1N4007 Diode')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('./reverse_iv_graph.png', dpi=300)
plt.show()
