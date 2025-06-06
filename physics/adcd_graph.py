import matplotlib.pyplot as plt
import numpy as np

V_diode = np.array([0.566, 0.599, 0.619, 0.633, 0.643, 0.651, 0.657, 0.664, 0.670,
                    0.674, 0.679, 0.682, 0.686, 0.690, 0.692, 0.694, 0.698, 0.701, 0.702, 0.705])  # V_AB
I_exp = np.array([0.288, 0.591, 0.906, 1.224, 1.521, 1.806, 2.124, 2.448, 2.739, 3.039,
                  3.364, 3.642, 3.976, 4.270, 4.561, 4.873, 5.170, 5.470, 5.782, 6.091])  # in mA

I_S = 8.7107279e-10  # saturation current (A)
q = 1.602e-19  # electron charge (C)
k = 1.381e-23  # Boltzmann constant (J/K)
T = 300  # temperature (K)
n = 1.7298  # ideality factor

I_theo = I_S * (np.exp((q * V_diode) / (n * k * T)) - 1) * 1000  # mA
plt.figure(figsize=(8, 5))
plt.plot(V_diode, I_exp, 'o-', label='Experimental Current')
plt.plot(V_diode, I_theo, 's--', label='Theoretical Current (Shockley)')
plt.xlabel('Diode Voltage $V_{D}$ (V)')
plt.ylabel('Current $I$ (mA)')
plt.title('Diode I-V Characteristics (1N-4007)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
