import pybullet as p
import pybullet_data
import time
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# 물리 시뮬레이션 초기화
p.connect(p.GUI)

# PyBullet의 기본 데이터 경로 추가
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# 중력 설정
p.setGravity(0, 0, -9.8)

# 간단한 평면 추가
plane_id = p.createCollisionShape(p.GEOM_PLANE)
plane_body_id = p.createMultiBody(0, plane_id)


# 바닥의 마찰 계수와 탄성 계수 설정 함수
def set_floor_properties(friction, restitution):
    p.changeDynamics(plane_body_id, -1, lateralFriction=friction, restitution=restitution)


# 주사위 속성 설정
cube_half_extents = [0.016, 0.016, 0.016]  # 주사위 크기
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


# 사용자 설정 파라미터
dice_mass = 0.041
initial_position = [0, 0, 0.3]  # 주사위 초기 위치
initial_orientation = [np.pi / 6, np.pi / 6, 0]  # 초기 기울기 (Euler angles)
initial_force = [0, 0, 0]  # 초기 힘 (X, Y, Z 방향)
initial_torque = [0, 0, 0]  # 초기 토크 (회전력)
floor_friction = 0.1  # 바닥 마찰 계수
floor_restitution = 1  # 바닥 탄성 계수

# 바닥 속성 설정
set_floor_properties(floor_friction, floor_restitution)

# 주사위 생성
cube_id = create_dice(initial_position, initial_orientation, dice_mass)

# 초기 힘과 토크 적용
apply_initial_force(cube_id, initial_force, initial_torque)

# 시뮬레이션 루프
for _ in range(240 * 5):  # 5초 동안 시뮬레이션 (240Hz)
    p.stepSimulation()
    time.sleep(1. / 240.)

# 주사위의 최종 위치와 회전 가져오기
final_position, final_orientation = p.getBasePositionAndOrientation(cube_id)
final_orientation_euler = p.getEulerFromQuaternion(final_orientation)

print(f'Final Position: {final_position}')
print(f'Final Orientation (Euler Angles): {final_orientation_euler}')

# 면 번호와 방향 벡터 매핑 (로컬 좌표계 기준)
# 예: 면 1 = [0, 0, 1], 면 6 = [0, 0, -1]
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


# 최종 상태에서 위쪽 면 확인
top_face = get_top_face(final_orientation)
print(f"The top face is: {top_face}")


# 3D 플로팅 함수
def plot_dice_3d(position, orientation, color):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim(-0.3, 0.3)
    ax.set_ylim(-0.3, 0.3)
    ax.set_zlim(0, 0.6)

    half_extents = np.array(cube_half_extents)
    vertices = np.array([
        [-half_extents[0], -half_extents[1], -half_extents[2]],
        [half_extents[0], -half_extents[1], -half_extents[2]],
        [half_extents[0], half_extents[1], -half_extents[2]],
        [-half_extents[0], half_extents[1], -half_extents[2]],
        [-half_extents[0], -half_extents[1], half_extents[2]],
        [half_extents[0], -half_extents[1], half_extents[2]],
        [half_extents[0], half_extents[1], half_extents[2]],
        [-half_extents[0], half_extents[1], half_extents[2]]
    ])

    rotation_matrix = np.array(p.getMatrixFromQuaternion(p.getQuaternionFromEuler(orientation))).reshape(3, 3)
    rotated_vertices = np.dot(vertices, rotation_matrix.T) + position

    faces = [
        [rotated_vertices[j] for j in [0, 1, 2, 3]],
        [rotated_vertices[j] for j in [4, 5, 6, 7]],
        [rotated_vertices[j] for j in [0, 1, 5, 4]],
        [rotated_vertices[j] for j in [2, 3, 7, 6]],
        [rotated_vertices[j] for j in [0, 3, 7, 4]],
        [rotated_vertices[j] for j in [1, 2, 6, 5]]
    ]

    poly3d = Poly3DCollection(faces, facecolors=color[:3], linewidths=1, edgecolors='r', alpha=color[3])
    ax.add_collection3d(poly3d)

    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    ax.set_zlabel('Z-axis')
    ax.set_title('Final Dice State')
    plt.show()


# 최종 상태 플로팅
plot_dice_3d(final_position, final_orientation_euler, [0.5, 0.5, 1, 1])

# 연결 종료
p.disconnect()
