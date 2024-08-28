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
p.createMultiBody(0, plane_id)

# 정육면체 속성 설정
cube_half_extents = [0.5, 0.5, 0.5]  # 정육면체의 절반 크기
cube_col_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=cube_half_extents)

# 여러 정육면체 초기 설정
cube_start_positions = [[0, 0, 5], [0, 0, 4], [-2, -2, 10]]
cube_orientations = [
    p.getQuaternionFromEuler([np.pi / 6, np.pi / 6, np.pi / 6]),
    p.getQuaternionFromEuler([np.pi / 4, np.pi / 4, np.pi / 4]),
    p.getQuaternionFromEuler([np.pi / 3, np.pi / 3, np.pi / 3])
]
cube_colors = [[0, 1, 1, 1], [1, 0, 1, 1], [1, 1, 0, 1]]  # RGBA 색상 리스트

# 정육면체 생성
cube_ids = []
for pos, orient, color in zip(cube_start_positions, cube_orientations, cube_colors):
    cube_visual_shape = p.createVisualShape(
        shapeType=p.GEOM_BOX,
        halfExtents=cube_half_extents,
        rgbaColor=color  # 색상 설정
    )
    cube_id = p.createMultiBody(
        baseMass=1,
        baseCollisionShapeIndex=cube_col_shape,
        baseVisualShapeIndex=cube_visual_shape,
        basePosition=pos,
        baseOrientation=orient
    )
    p.changeDynamics(cube_id, -1, lateralFriction=1.0, restitution=0.8)  # 마찰 계수와 탄성 계수 설정
    cube_ids.append(cube_id)

# 시뮬레이션 루프
for _ in range(240 * 5):
    p.stepSimulation()
    time.sleep(1. / 240.)

# 정육면체의 위치와 회전 가져오기
cubes_states = [p.getBasePositionAndOrientation(cube_id) for cube_id in cube_ids]
cubes_positions = [np.array(state[0]) for state in cubes_states]
cubes_orientations = [np.array(p.getEulerFromQuaternion(state[1])) for state in cubes_states]

print(f'Final Positions: {cubes_positions}')
print(f'Final Orientations (Euler Angles): {cubes_orientations}')

# 정육면체의 면과 축을 플로팅하는 함수
def plot_cubes_3d(positions, orientations, colors):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_zlim(0, 15)

    for pos, orient, color in zip(positions, orientations, colors):
        # 정육면체의 8개 꼭지점을 정의합니다.
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

        # 회전 행렬을 적용하여 정육면체의 회전을 적용합니다.
        rotation_matrix = p.getMatrixFromQuaternion(p.getQuaternionFromEuler(orient))
        rotation_matrix = np.array(rotation_matrix).reshape(3, 3)
        rotated_vertices = np.dot(vertices, rotation_matrix.T) + pos

        # 정육면체의 면을 정의합니다.
        faces = [
            [rotated_vertices[j] for j in [0, 1, 2, 3]],
            [rotated_vertices[j] for j in [4, 5, 6, 7]],
            [rotated_vertices[j] for j in [0, 1, 5, 4]],
            [rotated_vertices[j] for j in [2, 3, 7, 6]],
            [rotated_vertices[j] for j in [0, 3, 7, 4]],
            [rotated_vertices[j] for j in [1, 2, 6, 5]]
        ]

        # 면을 그립니다.
        poly3d = Poly3DCollection(faces, facecolors=color[:3], linewidths=1, edgecolors='r', alpha=color[3])
        ax.add_collection3d(poly3d)

        # 축을 그립니다.
        ax.quiver(*pos, *orient, length=1, normalize=True, color='k')

    ax.set_title('Cubes Position and Orientation')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    ax.set_zlabel('Z-axis')
    plt.show()

# 정육면체의 위치와 회전을 3D로 플로팅
plot_cubes_3d(cubes_positions, cubes_orientations, cube_colors)

# 연결 종료
p.disconnect()
