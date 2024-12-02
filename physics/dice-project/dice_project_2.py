import pybullet as p
import pybullet_data
import time
import numpy as np
import matplotlib.pyplot as plt

# 물리 시뮬레이션 초기화
p.connect(p.DIRECT)  # GUI 대신 DIRECT로 실행하여 시뮬레이션 속도 향상

# PyBullet의 기본 데이터 경로 추가
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# 중력 설정
p.setGravity(0, 0, -9.8)


# 바닥의 마찰 계수와 탄성 계수 설정 함수
def set_floor_properties(friction, restitution):
    p.changeDynamics(plane_body_id, -1, lateralFriction=friction, restitution=restitution)


# 바닥 생성
plane_id = p.createCollisionShape(p.GEOM_PLANE)
plane_body_id = p.createMultiBody(0, plane_id)

# 주사위 속성 설정
cube_half_extents = [0.008, 0.008, 0.008]  # 주사위 크기
cube_col_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=cube_half_extents)
cube_visual_shape = p.createVisualShape(
    shapeType=p.GEOM_BOX,
    halfExtents=cube_half_extents,
    rgbaColor=[0.5, 0.5, 1, 1]  # 색상 설정
)


# 주사위 생성 함수
def create_dice(initial_position, initial_orientation, mass):
    return p.createMultiBody(
        baseMass=mass,
        baseCollisionShapeIndex=cube_col_shape,
        baseVisualShapeIndex=cube_visual_shape,
        basePosition=initial_position,
        baseOrientation=p.getQuaternionFromEuler(initial_orientation)
    )


# 초기 힘을 주는 함수
def apply_initial_force(cube_id, force_vector, torque_vector):
    p.applyExternalForce(
        objectUniqueId=cube_id,
        linkIndex=-1,
        forceObj=force_vector,
        posObj=[0, 0, 0],  # 힘이 적용되는 지점 (주사위의 중심)
        flags=p.WORLD_FRAME
    )
    p.applyExternalTorque(
        objectUniqueId=cube_id,
        linkIndex=-1,
        torqueObj=torque_vector,
        flags=p.WORLD_FRAME
    )


# 면 번호와 방향 벡터 매핑 (로컬 좌표계 기준)
dice_faces = {
    1: [0, 0, 1],  # 위쪽 (+Z)
    6: [0, 0, -1],  # 아래쪽 (-Z)
    2: [0, 1, 0],  # 앞쪽 (+Y)
    5: [0, -1, 0],  # 뒤쪽 (-Y)
    3: [1, 0, 0],  # 오른쪽 (+X)
    4: [-1, 0, 0]  # 왼쪽 (-X)
}


# 주사위 위쪽 면 판별 함수
def get_top_face(final_orientation):
    max_dot = -1
    top_face = None
    # 쿼터니언에서 회전 행렬 생성
    rotation_matrix = np.array(p.getMatrixFromQuaternion(final_orientation)).reshape(3, 3)

    # 각 면 벡터를 월드 좌표계로 변환하여 가장 위쪽 면 찾기
    for face, local_vector in dice_faces.items():
        world_vector = np.dot(rotation_matrix, local_vector)  # 로컬 -> 월드 변환
        dot_product = np.dot(world_vector, [0, 0, 1])  # 월드 Z축과의 내적
        if dot_product > max_dot:
            max_dot = dot_product
            top_face = face

    return top_face


# 사용자 설정 파라미터
dice_mass = 0.041
initial_position = [0, 0, 0.3]  # 주사위 초기 위치
initial_orientation = [np.pi / 6, np.pi / 6, 0]  # 초기 기울기 (Euler angles)
initial_torque = [0, 0, 0]  # 초기 토크 (회전력)
floor_friction = 0.2  # 바닥 마찰 계수
floor_restitution = 0.4  # 바닥 탄성 계수

# 결과 저장 변수
results = []
# 반복 시뮬레이션
for i in range(1000):
    # 초기 조건 설정
    x_force = 0.041  # Force remains fixed
    initial_force = [x_force, 0, 0]  # X 방향 힘만 증가
    initial_orientation = [np.pi / 180 * i, np.pi / 180 * i, np.pi / 180 * i]

    # 물리 시뮬레이션 초기화
    p.resetSimulation()
    p.setGravity(0, 0, -9.8)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())

    # 바닥 재설정
    plane_id = p.createCollisionShape(p.GEOM_PLANE)
    plane_body_id = p.createMultiBody(0, plane_id)
    set_floor_properties(floor_friction, floor_restitution)

    # 주사위 생성 및 초기 힘 적용
    cube_id = create_dice(initial_position, initial_orientation, dice_mass)
    apply_initial_force(cube_id, initial_force, initial_torque)

    # 시뮬레이션 루프
    for _ in range(240 * 5):  # 5초간 시뮬레이션
        p.stepSimulation()

    # 최종 위치 및 회전 가져오기
    final_position, final_orientation = p.getBasePositionAndOrientation(cube_id)

    # 위쪽 면 판별
    top_face = get_top_face(final_orientation)
    results.append((i, top_face))  # Using 'i' as x-axis value

# 시뮬레이션 종료
p.disconnect()

# 결과 데이터 처리 및 그래프화
iterations = [result[0] for result in results]  # Use 'i' for x-axis
top_faces = [result[1] for result in results]

# 그래프 그리기
plt.figure(figsize=(10, 6))
plt.scatter(iterations, top_faces, c='blue', alpha=0.7, edgecolors='k')
plt.xlabel('Iteration')
plt.ylabel('Top Face Number')
plt.title('Top Face Distribution with Varying Parameters')
plt.grid(True)
plt.show()
