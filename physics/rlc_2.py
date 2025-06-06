import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# 엑셀 파일 경로
file_path = "RLC circuit data det.xlsx"
print("Reading Excel file...")

# 시트 확인
xls = pd.ExcelFile(file_path)
print("Available sheets:", xls.sheet_names)

# 첫 번째 시트 로드 (헤더 없음)
df = pd.read_excel(file_path, sheet_name=0, header=None)

# 헤더 자동 판별
if any(isinstance(x, str) and any(k in str(x) for k in ['Time', 'VR']) for x in df.iloc[1]):
    print("Using second row as header")
    df.columns = df.iloc[1]
    df = df.iloc[2:].reset_index(drop=True)
else:
    print("No headers found, using default column names")
    df.columns = ['Time', 'Voltage'] + [f'Col_{i}' for i in range(2, len(df.columns))]

# 데이터 숫자 변환 및 결측 제거
df['Time'] = pd.to_numeric(df.iloc[:, 0], errors='coerce')
df['Voltage'] = pd.to_numeric(df.iloc[:, 1], errors='coerce')
df = df.dropna(subset=['Time', 'Voltage'])

# numpy 배열로 변환
time = df['Time'].to_numpy()/ 1000
voltage = df['Voltage'].to_numpy()

print(f"\nSuccessfully loaded {len(time)} data points")

# 피크 탐색
peaks, _ = find_peaks(voltage, prominence=0.00001)
peak_voltages = voltage[peaks]
peak_times = time[peaks]

# 로그 감쇠율 계산
log_ratios = np.log(peak_voltages[:-1] / peak_voltages[1:])
average_log_decrement = np.mean(log_ratios)

# 평균 주기 및 감쇠 상수 계산
periods = np.diff(peak_times)
average_period = np.mean(periods)
delta = average_log_decrement / average_period

# 공진 주파수 및 감쇠 주파수
f_0 = 1 / average_period
omega_0 = 2 * np.pi * f_0
omega_d = np.sqrt(omega_0**2 - delta**2)

# 그래프 출력
plt.figure(figsize=(12, 6))
plt.plot(time, voltage, label='Voltage (V)')
plt.plot(peak_times, peak_voltages, 'ro', label='Peaks')
plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')
plt.title('RLC Circuit Damped Oscillation')
plt.legend()
plt.grid(True)

# 그래프 저장
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
