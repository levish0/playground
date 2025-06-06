import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

V_diode = np.array([0.566, 0.599, 0.619, 0.633, 0.643, 0.651, 0.657, 0.664, 0.670,
                    0.674, 0.679, 0.682, 0.686, 0.690, 0.692, 0.694, 0.698, 0.701, 0.702, 0.705])  # V_AB
I_exp = np.array([0.288, 0.591, 0.906, 1.224, 1.521, 1.806, 2.124, 2.448, 2.739, 3.039,
                  3.364, 3.642, 3.976, 4.270, 4.561, 4.873, 5.170, 5.470, 5.782, 6.091])  # mA
I_exp_amp = I_exp / 1000

q = 1.602e-19  # C
k = 1.381e-23  # J/K
T = 300  # K

def shockley_eq(V, I_S, n):
    V_T = k * T / q
    return I_S * (np.exp(V / (n * V_T)) - 1)

initial_guess = [1e-12, 1.5]
params, _ = curve_fit(shockley_eq, V_diode, I_exp_amp, p0=initial_guess, maxfev=10000)

I_S_fit, n_fit = params


I_fit = shockley_eq(V_diode, I_S_fit, n_fit) * 1000
error_percent_fit = np.abs((I_exp - I_fit) / I_fit) * 100

df_fit = pd.DataFrame({
    'V_diode (V)': V_diode,
    'I_exp (mA)': I_exp,
    'I_fit (mA)': I_fit,
    'Error (%)': error_percent_fit
})

print(params, df_fit.head(10))
