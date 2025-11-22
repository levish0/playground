import matplotlib.pyplot as plt
import numpy as np


def plot_full_timing_diagram():
    # --- 설정 ---
    # 시뮬레이션할 클럭 사이클 수
    cycles = 6

    # 1. 입력 신호 정의 (문제의 파형 그림을 보고 패턴 입력)
    # Sh: 처음 2번은 Low(0), 그 이후는 High(1)
    sig_Sh = [0, 0, 1, 1, 1, 1]

    # Ld: 1번(Load), 2~3번(Low), 4~5번(High-하지만 Sh가 1이라 무시됨), 6번(Low)
    # 문제의 파란색 선 모양을 그대로 흉내 냅니다.
    sig_Ld = [1, 0, 0, 1, 1, 0]

    # 병렬 입력 데이터 (Fixed Inputs)
    DA, DB, DC, DD = 0, 1, 0, 1

    # 2. 출력 상태 계산
    # 초기 상태
    QA, QB, QC, QD = 0, 0, 0, 0

    # 그래프용 데이터 저장소 (초기값)
    trace_QA = [QA]
    trace_QB = [QB]
    trace_QC = [QC]  # = SI
    trace_QD = [QD]

    print(f"Initial: QA={QA}, QB={QB}, QC={QC}, QD={QD}")

    # 사이클별 로직 계산
    for i in range(cycles):
        sh_val = sig_Sh[i]
        ld_val = sig_Ld[i]

        # SI는 현재(직전) QC 값
        SI = QC

        next_QA, next_QB, next_QC, next_QD = QA, QB, QC, QD

        # 로직 적용 (우선순위: Sh > Ld)
        # Function Table 참조
        if sh_val == 1:  # Shift Mode (Ld is Don't Care)
            next_QA = SI
            next_QB = QA
            next_QC = QB
            next_QD = QC
            mode = "Shift"
        elif ld_val == 1:  # Load Mode
            next_QA, next_QB, next_QC, next_QD = DA, DB, DC, DD
            mode = "Load"
        else:  # Hold Mode
            mode = "Hold"

        # 상태 업데이트
        QA, QB, QC, QD = next_QA, next_QB, next_QC, next_QD

        trace_QA.append(QA)
        trace_QB.append(QB)
        trace_QC.append(QC)
        trace_QD.append(QD)

        print(f"Clock {i + 1} ({mode}): QA={QA}, QB={QB}, QC={QC}, QD={QD}")

    # --- 그래프 그리기 ---
    fig, ax = plt.subplots(figsize=(12, 10))

    # 시간 축 데이터 생성 (0 ~ 6)
    t = np.arange(cycles + 1)

    # Clock 신호 생성 (0.5 단위로 High/Low 반복하는 사각형 파형)
    # 시각적 표현을 위해 더 촘촘한 시간축 생성
    t_fine = np.linspace(0, cycles, 500)
    # Clock: 위아래로 진동 (Falling edge가 정수 지점에 오도록 위상 조정)
    clk_wave = 0.5 * (np.sign(np.cos(2 * np.pi * t_fine + 0.01)) + 1)

    # Y축 배치 순서 및 오프셋 설정
    # 위에서부터: Clock, Sh, Ld, QA, QB, SI(=QC), QD
    signals = [
        (None, 'Clock', 'black', 9.0, 'clock'),  # Clock은 따로 처리
        (sig_Sh + [1], '$Sh$', '#008CBA', 7.5, 'step'),  # 파란색 계열
        (sig_Ld + [0], '$Ld$', '#008CBA', 6.0, 'step'),
        (trace_QA, '$Q_A$', 'blue', 4.5, 'step'),
        (trace_QB, '$Q_B$', 'blue', 3.0, 'step'),
        (trace_QC, '$SI=Q_C$', 'blue', 1.5, 'step'),
        (trace_QD, '$Q_D$', 'blue', 0.0, 'step')
    ]

    for data, label, color, offset, plot_type in signals:
        # 기준선(Low)과 High 라인 그리기 (점선)
        ax.axhline(y=offset, color='lightgray', linestyle='-', linewidth=0.5)
        ax.axhline(y=offset + 0.8, color='lightgray', linestyle=':', linewidth=0.5)

        if plot_type == 'clock':
            # 클럭 그리기
            ax.plot(t_fine, clk_wave * 0.8 + offset, color=color, linewidth=1.5, label=label)
        else:
            # 데이터 신호 그리기
            # step(where='post')를 사용하여 디지털 로직처럼 그림
            # data 값을 0.8배 하여 높이 조절 + offset
            y_vals = [x * 0.8 + offset for x in data]
            ax.step(t, y_vals, where='post', color=color, linewidth=2, label=label)

        # 라벨 표시 (왼쪽)
        ax.text(-0.8, offset + 0.3, label, fontsize=14, fontweight='bold', color=color)

    # Falling Edge 표시 (세로 점선)
    for i in range(1, cycles + 1):
        ax.axvline(x=i, color='red', linestyle='--', alpha=0.5, linewidth=1)
        ax.text(i, -1.5, f'Clk {i}\n↓', ha='center', color='red')

    # 그래프 꾸미기
    ax.set_title('74178 Shift Register Timing Diagram (Full)', fontsize=18)
    ax.set_yticks([])  # Y축 눈금 제거
    ax.set_xticks(t)  # X축 정수 지점만 표시
    ax.set_xlim(-0.5, cycles + 0.5)
    ax.set_ylim(-2, 10.5)

    # 테두리 제거
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    plot_full_timing_diagram()