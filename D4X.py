import matplotlib.pyplot as plt
import numpy as np


def draw_timing_diagram():
    # 1. 초기 상태 설정 (0, 0)
    q1 = 0
    q2 = 0

    # 2. 입력 X 시퀀스 설정
    # 원본 이미지의 패턴을 그대로 따릅니다.
    # 순서: [초기, Pulse1, Gap, Pulse2, Gap, Pulse3(길게)]
    # Pulse3 구간이 우리가 논쟁 중인 (1,0 -> 1,1 -> 0,0) 구간입니다.
    x_seq = [0, 1, 0, 1, 0, 1, 1, 0]

    # 데이터 저장을 위한 리스트
    q1_list = [0]
    q2_list = [0]
    z_list = [0]
    x_plot = [0]

    # 3. 클럭별 시뮬레이션 (Rising Edge 기준)
    print(f"{'CLK':<5} {'X':<5} {'Present(Q1 Q2)':<15} {'Next(Q1 Q2)':<15} {'Output(Z)':<10}")
    print("-" * 60)

    for i, x in enumerate(x_seq):
        # 현재 상태 기록
        current_state = f"{q1}{q2}"

        # --- [제가 이해한 논리식 적용] ---
        # Z = X XOR Q2
        z = x ^ q2

        # Q2_next = X XOR Q2
        q2_next = x ^ q2

        # Q1_next = Q1 XOR (X AND Q2)  <-- 여기가 핵심입니다.
        q1_next = q1 ^ (x & q2)
        # ------------------------------

        next_state = f"{q1_next}{q2_next}"
        print(f"{i:<5} {x:<5} {current_state:<15} {next_state:<15} {z:<10}")

        # 상태 업데이트
        q1 = q1_next
        q2 = q2_next

        # 그래프용 데이터 추가 (Step 형태 유지를 위해)
        q1_list.append(q1)
        q2_list.append(q2)
        z_list.append(z)
        x_plot.append(x)

    # 4. 그래프 그리기
    fig, ax = plt.subplots(4, 1, figsize=(10, 8), sharex=True)

    # 계단형 그래프 (step plot)
    time_steps = range(len(x_plot))

    ax[0].step(time_steps, x_plot, where='post', color='black', linewidth=2)
    ax[0].set_ylabel('Input X')
    ax[0].set_ylim(-0.2, 1.2)

    ax[1].step(time_steps, q1_list, where='post', color='blue', linewidth=2)
    ax[1].set_ylabel('Q1')
    ax[1].set_ylim(-0.2, 1.2)

    # 1->1로 유지되는 구간 하이라이트
    ax[1].text(5.5, 0.5, "Look Here!\n(1 -> 1)", color='red', fontweight='bold', ha='center')

    ax[2].step(time_steps, q2_list, where='post', color='green', linewidth=2)
    ax[2].set_ylabel('Q2')
    ax[2].set_ylim(-0.2, 1.2)

    ax[3].step(time_steps, z_list, where='post', color='purple', linewidth=2)
    ax[3].set_ylabel('Output Z')
    ax[3].set_ylim(-0.2, 1.2)

    plt.xlabel('Clock Cycles')
    plt.suptitle(f"Simulation of Q1+ = Q1^(X&Q2), Q2+ = X^Q2", fontsize=14)
    plt.show()


draw_timing_diagram()