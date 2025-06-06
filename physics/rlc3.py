import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# 텍스트 파일 경로
file_path = "3.txt"  # 실제 파일 경로로 수정하세요
print("Reading text file...")

# 첫 번째 몇 줄 미리 보기로 헤더 유무 판단
with open(file_path, 'r') as f:
    for _ in range(3):
        print(f.readline().strip())
# 데이터 로딩: 구분자는 필요 시 ',' 또는 '\t'로 조정
df = pd.read_csv(file_path, sep=None, engine='python', header=None)

# 헤더 자동 판별
if any(isinstance(x, str) and any(k in str(x) for k in ['Time', 'VR']) for x in df.iloc[1]):
    print("Using second row as header")
    df.columns = df.iloc[1]
    df = df.iloc[2:].reset_index(drop=True)
else:
    print("No headers found, using default column names")
    df.columns = ['Time', 'Voltage'] + [f'Col_{i}' for i in range(2, len(df.columns))]

# 숫자형 변환 및 결측 제거
df['Time'] = pd.to_numeric(df.iloc[:, 0], errors='coerce')
df['Output Voltage (V)'] = pd.to_numeric(df.iloc[:, 4], errors='coerce')  # Output Voltage로 변경
df = df.dropna(subset=['Time', 'Output Voltage (V)'])  # Output Voltage로 변경

# numpy 배열
time = df['Time'].to_numpy() / 1000  # ms → s
output_voltage = df['Output Voltage (V)'].to_numpy()  # Output Voltage로 변경

print(f"\nSuccessfully loaded {len(time)} data points")

# 피크 탐색
peaks, _ = find_peaks(output_voltage, prominence=0.00001)  # Output Voltage 사용
peak_voltages = output_voltage[peaks]
peak_times = time[peaks]

# 로그 감쇠율 및 감쇠 상수
log_ratios = np.log(peak_voltages[:-1] / peak_voltages[1:])
average_log_decrement = np.mean(log_ratios)
periods = np.diff(peak_times)
average_period = np.mean(periods)
delta = average_log_decrement / average_period

# 공진 주파수 및 감쇠 주파수
f_0 = 1 / average_period
omega_0 = 2 * np.pi * f_0
omega_d = np.sqrt(omega_0**2 - delta**2)

# 그래프 출력 및 저장
plt.figure(figsize=(12, 6))
plt.plot(time, output_voltage, label='Output Voltage (V)')  # Output Voltage 사용
plt.plot(peak_times, peak_voltages, 'ro', label='Peaks')
plt.xlabel('Time (s)')
plt.ylabel('Output Voltage (V)')  # Output Voltage 사용
plt.title('RLC Circuit Oscillation')
plt.legend()
plt.grid(True)
plot_path = 'rlc_damped_plot.png'
plt.savefig(plot_path, dpi=300, bbox_inches='tight')
print(f"Plot saved to: {os.path.abspath(plot_path)}")
plt.show()

# 결과 출력
print("\n=== RLC Circuit Analysis Results ===")
print(f"평균 주기: {average_period:.6f} s")
print(f"로그 감쇠율 평균: {average_log_decrement:.6f}")
print(f"감쇠 상수 (delta): {delta:.6f}")
print(f"공진 주파수 (f₀): {f_0:.2f} Hz")
print(f"감쇠 주파수 (ω_d): {omega_d:.2f} rad/s")
