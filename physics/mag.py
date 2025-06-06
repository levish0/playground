import matplotlib.pyplot as plt

# 데이터셋 정의
datasets = {
    "Straight Wire": {
        "distance": [4.25, 4.75, 5.25, 5.75, 6.25, 6.75, 7.25, 7.75, 8.25, 8.75],
        "Bx": [-0.020, -0.020, -0.010, 0.050, 0.020, 0.050, 0.050, 0.050, 0.050, 0.030],
        "By": [-0.210, -0.190, -0.180, -0.170, -0.160, -0.150, -0.140, -0.130, -0.130, -0.120],
        "Bz": [-0.080, -0.070, -0.060, -0.060, -0.060, -0.050, -0.050, -0.040, -0.040, -0.040],
    },
    "Circular Wire": {
        "distance": [4.25, 4.75, 5.25, 5.75, 6.25, 6.75, 7.25, 7.75, 8.25, 8.75],
        "Bx": [0.200, 0.200, 0.210, 0.200, 0.200, 0.200, 0.200, 0.200, 0.200, 0.190],
        "By": [-0.010]*10,
        "Bz": [0.000]*10,
    },
    "Solenoid": {
        "distance": [3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5],
        "Bx": [7.6, 7.6, 7.7, 7.7, 7.7, 7.6, 7.7, 7.6, 7.6, 7.5],
        "By": [0.1, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "Bz": [0.4]*10,
    },
    "Helmholtz Coil": {
        "distance": [3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 8.5],
        "Bx": [1.8]*10,
        "By": [0.2, 0.1, 0.1, 0.2, 0.1, 0.1, 0.2, 0.1, 0.1, 0.1],
        "Bz": [0.1, 0.1, 0.2, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
    }
}

# 그래프 저장용 리스트
figures = []

# 각각 개별 그래프 그리기
for title, data in datasets.items():
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(data["distance"], data["Bx"], marker='o', label="$B_x$")
    ax.plot(data["distance"], data["By"], marker='s', label="$B_y$")
    ax.plot(data["distance"], data["Bz"], marker='^', label="$B_z$")
    ax.set_title(f"{title}")
    ax.set_xlabel("Distance (mm)")
    ax.set_ylabel("Magnetic Field (G)")
    ax.legend()
    ax.grid(True)
    figures.append(fig)


