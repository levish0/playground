import numpy as np
import matplotlib.pyplot as plt

# 미분 방정식의 기울기 정의
def dy_dt(y):
    return y**2 - 1

# 벡터 필드 그리기
y_values = np.linspace(-2, 2, 20)
t_values = np.linspace(-10, 10, 40)
Y, T = np.meshgrid(y_values, t_values)
dY = dy_dt(Y)

plt.figure(figsize=(10, 6))

# 벡터 필드 플로팅
plt.quiver(T, Y, np.ones_like(T), dY, angles='xy', scale_units='xy', scale=1, color='r')

# 초기 조건으로 미분 방정식의 해를 플로팅
from scipy.integrate import solve_ivp

def dy_dt_func(t, y):
    return y**2 - 1

y0 = [-3/2]  # 초기 조건 (y(0) = 1/2)
t_span = (0, 10)  # 시간 범위
solution = solve_ivp(dy_dt_func, t_span, y0, t_eval=np.linspace(t_span[0], t_span[1], 300))

plt.plot(solution.t, solution.y[0], label="y(t)", color='b')

plt.xlabel('t')
plt.ylabel('y')
plt.title("Vector Field and Solution of dy/dt = y^2 - 1")
plt.legend()
plt.grid(True)
plt.show()
