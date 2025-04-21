import pandas as pd

# Re-define constants after state reset
r = 0.015  # radius of pulley in meters
g = 9.8   # gravitational acceleration in m/s^2

# Mass values for weights + hanger for each case (in kg)
mass_values = {
    1: 0.027,
    2: 0.047,
    3: 0.067,
    4: 0.087
}

# Angular acceleration values from the table (in rad/s^2)
angular_accelerations =  {
    1: 13.8,
    2: 24.2,
    3: 33.9,
    4: 42.8
}

# Calculate moment of inertia using I = r * m * (g - r * alpha) / alpha
results = []
for w in range(1, 5):
    m = mass_values[w]
    alpha = angular_accelerations[w]
    I = r * m * (g - r * alpha) / alpha
    results.append((w, alpha, round(I, 5)))

# Convert to DataFrame for display
df = pd.DataFrame(results, columns=["Number of weights", "Angular acceleration (rad/s^2)", "Moment of inertia (kg·m^2)"])
average_I = round(df["Moment of inertia (kg·m^2)"].mean(), 5)
print(df)
print(average_I)
