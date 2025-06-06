import numpy as np
import pandas as pd

I_exp = np.array([0.000061, 0.000091, 0.000152, 0.000212, 0.000242, 0.000303])  # mA
V_AB = np.array([-0.510, -1.011, -1.512, -2.038, -2.504, -2.918])

I_S = 8.7107279e-10  # A
I_theo = -I_S * 1000  # mA
I_theo_array = np.full_like(I_exp, I_theo)

error_percent = np.abs((I_exp - I_theo_array) / I_theo_array) * 100

df = pd.DataFrame({
    'V_AB (V)': V_AB,
    'I_exp (mA)': I_exp,
    'I_theo (mA)': I_theo_array,
    'Error (%)': error_percent
})

average_error = error_percent.mean()

print(df)
print(f"Average Error: {average_error:.2f}%")
