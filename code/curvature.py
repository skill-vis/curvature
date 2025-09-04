import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline

################################
# データディレクトリ
################################
data_dir = '/Users/ohta/Library/CloudStorage/Dropbox/．sync/．SkillVis/Qiita/curvature/data'
data = pd.read_csv(data_dir + '/' + 'ball_trajectory.csv', header=0).values
# data2 = pd.read_csv(data_dir + '/' + 'ball_trajectory_har.csv', header=0).values

################################
# Parameters
################################
weight_v = .00007 # 速度用のフィルタ重み係数
weight_a = .00009 # 加速度用のフィルタ重み係数
sf = 1000. # サンプリング周波数

################################
# Math Functions
################################
# ノルム（大きさ）
def norm(vec_array):
    if vec_array.ndim == 1:
        return np.linalg.norm(vec_array)
    else:
        return np.linalg.norm(vec_array, axis=1)

# 単位ベクトル
def unit_vec(data_vec):
    if data_vec.ndim == 1:
        data_norm = np.linalg.norm(data_vec)
    else:
        data_norm = np.linalg.norm(data_vec, axis=1)[:,np.newaxis]
    return data_vec/data_norm

# 内積
def dot_product(a, b):
    if a.ndim == 1 and b.ndim == 1:
        return np.sum(a * b)
    elif a.ndim == 2 and b.ndim == 2:
        return np.sum(a * b, axis=1)

# 外積
def cross_product(a, b):
    if a.ndim == 1 and b.ndim == 1:
        return np.cross(a, b)
    elif a.ndim == 2 and b.ndim == 2:
        return np.cross(a, b, axis=1)

################################
# Smoothing Spline
################################
# スプライン平滑化：データの微分に利用
def smoothing_spline(data, weights=1.0, sf=1000.0, order=0, degree=4):

    """
    UnivariateSplineを用いて時系列データを平滑化（および微分）する。

    Parameters
    ----------
    data : array-like
        平滑化したい時系列データ。1次元または2次元配列
    weights : float or array-like 
        平滑化の重み。スカラーまたは配列．配列の場合データの列数とし，各列ごとに個別に重みを与えることができる
    sf : float
        サンプリング周波数（Hz）
    order : int, optional
        微分の次数（0なら平滑化のみ）。デフォルトは0
    degree : int, optional
        スプラインの次数。デフォルトは4．加速度まで計算する場合はデフォルトの4とする．

    Returns
    -------
    smoothed : ndarray
        平滑化（または微分）されたデータ
    """

    data = np.asarray(data)
    if data.ndim == 1:
        data = data[:, None]
    
    # weightがスカラーまたはデータの列数と一致する配列であることを確認
    if not np.isscalar(weights):
        assert len(weights) == data.shape[1], f"weights must be scalar or array of length {data.shape[1]}, but got length {len(weights)}"
    
    # data = np.asarray(data)
    if data.ndim == 1:
        data = data[:, None]

    n_samples, n_series = data.shape
    t = np.arange(n_samples) / sf

    # 出力配列
    result = np.full_like(data, np.nan, dtype=np.float64)

    for i in range(n_series):
        y = data[:, i]
        valid = ~np.isnan(y)
        if np.sum(valid) < degree + 1:
            continue  # 有効な点が少なすぎる場合はスキップ

        x_valid = t[valid]
        y_valid = y[valid]

        # 重み処理
        w_valid = np.full_like(y_valid, 1, dtype=np.float64)
        

        # スプラインフィッティング
        if np.isscalar(weights):
            spline = UnivariateSpline(x_valid, y_valid, w=w_valid, k=degree, s=weights)
        else:
            spline = UnivariateSpline(x_valid, y_valid, w=w_valid, k=degree, s=weights[i])
            
        result[:, i] = spline(t) if order == 0 else spline.derivative(order)(t)

    return result.squeeze()

# 運動学：位置から速度と加速度を計算
def kinematics(posi_vec, sf=sf, weights_a=weight_a, weights_v=weight_v):
    vel = smoothing_spline(posi_vec, weights = weights_v, sf = sf, order = 1)
    acc = smoothing_spline(posi_vec, weights = weights_a, sf = sf, order = 2)
    return vel, acc


# 曲率半径
def curvature_radius(vel, acc):
    return norm(vel)**3 / dot_product(acc, vel)

# 単位主法線ベクトル
def unit_principal_normal_vec(vel, acc):
    return cross_product(vel, cross_product(acc, vel)) / (norm(cross_product(acc, vel)) * norm(vel))[:,np.newaxis]

# 単位接線ベクトル
def unit_tangent_vec(vel):
    return vel / norm(vel)

# 曲率ベクトル
def curvature_vec(vel, acc):
    norm_part = norm(vel)**2 / norm(cross_product(acc, vel))**2
    return norm_part[:,np.newaxis] * cross_product(vel, cross_product(acc, vel))

################################
# Main
################################
data = data[1:]

release_frame = -10

vel, acc = kinematics(data, sf=sf, weights_a=weight_a, weights_v=weight_v)
vel_trim, acc_trim = vel[1:release_frame], acc[1:release_frame]
data_trim = data[1:release_frame]
curvature_radius1 = curvature_radius(vel_trim, acc_trim)
unit_principal_normal_vec1 = unit_principal_normal_vec(vel_trim, acc_trim)
# unit_tangent_vec = unit_tangent_vec(vel_trim)
curvature_vec1 = data_trim + curvature_radius1[:,np.newaxis] * unit_principal_normal_vec1


# data2 = data2[1:]
# vel2, acc2 = kinematics(data2, sf=sf, weights_a=weight_a, weights_v=weight_v)
# vel_trim2, acc_trim2 = vel2[1:release_frame], acc2[1:release_frame]
# data_trim2 = data2[1:release_frame]
# curvature_radius2 = curvature_radius(vel_trim2, acc_trim2)
# unit_principal_normal_vec2 = unit_principal_normal_vec(vel_trim2, acc_trim2)
# # unit_tangent_vec = unit_tangent_vec(vel_trim)
# curvature_vec2 = data_trim2 + curvature_radius2[:,np.newaxis] * unit_principal_normal_vec2

# Create time array centered at release (t=0)
t = np.arange(len(vel_trim))/sf - len(vel_trim)/sf

# Create figure with two y-axes
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()

# Plot velocity components on left axis (m/s)
ax1.plot(t, vel_trim, label=['x', 'y', 'z'])
ax1.plot(t, norm(vel_trim), 'k--', label='Norm speed')
ax1.set_xlabel('Time [s]')
ax1.set_ylabel('Velocity [m/s]')
ax1.set_title('Ball velocity')

# Plot velocity on right axis (km/h) 
ax2.plot(t, norm(vel_trim)*3.6, 'k--', alpha=0)  # Invisible plot to set scale
ax2.set_ylabel('Velocity [km/h]')
ax1.axvline(x=0, color='k', linestyle='--', alpha=0.5, label='Release')

# Add legend
ax1.legend()
plt.show()

################################
# 3D Plot
################################
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
delete_frame = 3

# Plot data points (original trajectory)
ax.scatter(data_trim[:, 0], data_trim[:, 1], data_trim[:, 2], c='red', label='ball trajectory', s=2)

# Plot curvature vector points
ax.scatter(curvature_vec1[1:-delete_frame, 0], curvature_vec1[1:-delete_frame, 1], curvature_vec1[1:-delete_frame, 2], c='blue', label='center of curvature', s=5)

# Draw lines between corresponding points
for i in range(1, len(data_trim)-delete_frame):
    ax.plot([data_trim[i, 0], curvature_vec1[i, 0]], 
            [data_trim[i, 1], curvature_vec1[i, 1]], 
            [data_trim[i, 2], curvature_vec1[i, 2]], 
            'k-', linewidth=0.5, alpha=0.3)


# ax.scatter(data_trim2[:, 0], data_trim2[:, 1], data_trim2[:, 2], c='green', label='ball trajectory', s=2)
# ax.scatter(curvature_vec2[1:-delete_frame, 0], curvature_vec2[1:-delete_frame, 1], curvature_vec2[1:-delete_frame, 2], c='green', label='curvature points', s=5)
# for i in range(1, len(data_trim2)-delete_frame):
#     ax.plot([data_trim2[i, 0], curvature_vec2[i, 0]], 
#             [data_trim2[i, 1], curvature_vec2[i, 1]], 
#             [data_trim2[i, 2], curvature_vec2[i, 2]], 
#             'k-', linewidth=0.5, alpha=0.3)


# Add 'Release' text annotation near the last point of data_trim
last_point = data_trim[-1]
# Add 'Release' text at the last point
ax.text(last_point[0], last_point[1], last_point[2], 'Release', fontsize=10)
# Add 'MER' text at the first point
first_point = data_trim[0]
ax.text(first_point[0], first_point[1], first_point[2], 'MER', fontsize=10)


ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
# Set the viewing angle
ax.view_init(elev=30, azim=170)  # elev: elevation angle, azim: azimuth angle

ax.set_aspect('equal')
ax.legend()
plt.show()
