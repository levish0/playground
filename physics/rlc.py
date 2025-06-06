import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks


# 엑셀 파일 로드
file_path = "RLC circuit data det.xlsx"
print("Reading Excel file...")

# 시트 이름 확인
xls = pd.ExcelFile(file_path)
print("Available sheets:", xls.sheet_names)

# 첫 번째 시트 로드 (헤더 없이)
df = pd.read_excel(file_path, sheet_name=0, header=None)

# 데이터 정리
# 첫 번째 행이 헤더인지 확인
if any(isinstance(x, str) and any(keyword in str(x) for keyword in ['Time', 'VR']) for x in df.iloc[1]):
    print("\nUsing second row as header")
    # 두 번째 행을 헤더로 사용
    df.columns = df.iloc[1]
    # 첫 두 행 제거
    df = df.iloc[2:].reset_index(drop=True)
else:
    print("\nNo headers found, using default column names")
    df.columns = ['Time', 'Voltage'] + [f'Col_{i}' for i in range(2, len(df.columns))]

print("\nFirst 5 rows of the data:")
print(df.head())

# 시간 및 전압 데이터 추출
time = pd.to_numeric(df.iloc[:, 0], errors='coerce').dropna().to_numpy()
voltage = pd.to_numeric(df.iloc[:, 1], errors='coerce').dropna().to_numpy()

print(f"\nSuccessfully loaded {len(time)} data points")

# 최대 전압 (최대 진폭) 탐색
peaks, _ = find_peaks(voltage)
peak_voltages = voltage[peaks]
peak_times = time[peaks]

# 로그 감쇠율 계산용: ln(V_n / V_{n+1})
log_ratios = np.log(peak_voltages[:-1] / peak_voltages[1:])
average_log_decrement = np.mean(log_ratios)

# 감쇠 상수 delta = log_decrement / 주기
periods = np.diff(peak_times)
average_period = np.mean(periods)
delta = average_log_decrement / average_period

# 공진 주파수 및 감쇠 주파수 계산
f_0 = 1 / average_period  # 공진 주파수 (Hz)
omega_0 = 2 * np.pi * f_0
omega_d = np.sqrt(omega_0**2 - delta**2)

# 그래프 그리기
plt.figure(figsize=(12, 6))
plt.plot(time, voltage, 'b-', label='Voltage (V)')
plt.plot(peak_times, peak_voltages, 'ro', label='Peaks')
plt.xlabel('Time (ms)')
plt.ylabel('Voltage (V)')
plt.title('RLC Circuit Damped Oscillation')
plt.legend()
plt.grid(True)

# Save the plot
plot_path = 'rlc_damped_plot.png'
plt.savefig(plot_path, dpi=300, bbox_inches='tight')
print(f"Plot saved to: {os.path.abspath(plot_path)}")
plt.show()

# 결과 출력
print(f"평균 주기: {average_period:.6f} s")
print(f"로그 감쇠율 평균: {average_log_decrement:.6f}")
print(f"감쇠 상수 (delta): {delta:.6f}")
print(f"공진 주파수 (f₀): {f_0:.2f} Hz")
print(f"감쇠 주파수 (ω_d): {omega_d:.2f} rad/s")
