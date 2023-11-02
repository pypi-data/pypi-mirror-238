"""
体素网格生成
"""
import math
import os.path
import random
import sys
from collections import Counter
import numpy as np
import open3d as o3d


def pc_normalize(pc):
    """
    归一化，不平移
    Args:
        pc:

    Returns:

    """
    # centroid = np.mean(pc, axis=0)
    # pc = pc - centroid
    m = np.max(np.sqrt(np.sum(pc ** 2, axis=1)))
    pc = pc / m
    return pc, m


def get_stem_leafs(data_root, corn_name, leaf_num, normal=True):
    """
    读取 玉米茎叶
    Args:
        data_root:
        corn_name:
        normal:

    Returns:

    """

    corn_path = os.path.join(data_root, corn_name)
    # leaf_num = int(corn_name.split('-')[1])
    corn_xyzl = np.loadtxt(corn_path)
    point_set = corn_xyzl[:, :3]
    point_set, m = pc_normalize(point_set) if normal else point_set
    point_label = corn_xyzl[:, -1]

    corn_data = []
    for i in range(leaf_num + 1):
        i_index = np.where(point_label == i)
        i_point_set = point_set[i_index]
        # i_point_label = point_label[i_index]
        corn_data.append(i_point_set)

    return corn_data


def cal_x1_x2_distance(x1, x2):
    """
    两点之间距离
    :param x1:
    :param x2:
    :return:
    """
    return np.sqrt(np.sum(np.power(np.array(x1) - np.array(x2), 2)))


def pca_compute(data):
    """
    计算 点云的主成分
    :param data: numpy
    :return: v1
    """
    data_cloud = o3d.geometry.PointCloud()
    data_cloud.points = o3d.utility.Vector3dVector(data)
    [center, covariance] = data_cloud.compute_mean_and_covariance()  # 质心 协方差
    eigenvectors, eigenvalues, _ = np.linalg.svd(covariance)  # SVD
    sort = eigenvalues.argsort()[::-1]
    # w = eigenvalues[sort]
    v = eigenvectors[:, sort]
    v1 = v[:, 0]
    v2 = v[:, 1]
    v3 = v[:, 2]
    return v1, v2, v3


def rotate_cloud(data, bottom_point):
    """
    点云旋转
    :param data: 茎叶点云
    :param bottom_point: 茎底部点
    :return: 旋转后的点云
    """
    leaf_point = data[-1][0]
    stem_points = data[0]
    v1, v2, v3 = pca_compute(stem_points)
    # 主方向朝向顶叶
    v1 = v1 if np.dot(leaf_point - bottom_point, v1) > 0 else -v1
    # 主成分 1 已经改变方向， v2 = v3 x v1
    v2 = np.cross(v3, v1)
    rotate_corn_data = []
    # 旋转矩阵
    rotate_matrix = np.array([v2, v3, v1])
    for corn_item in data:
        # 将玉米 旋转到 茎 第一主成分 与 X 重合
        corn_item = np.dot(rotate_matrix, np.array(corn_item).T).T
        rotate_corn_data.append(corn_item)
    del data
    return rotate_corn_data


def move_corn(corn_data):
    """
    平移到茎的最低点
    :param corn_data:
    :return:
    """
    leaf_point = corn_data[-1][0]
    # 获得 叶子中一点 到 茎的最大距离对应的点
    stem_point_cloud = corn_data[0]
    v = leaf_point - stem_point_cloud
    max_index = np.argmax(np.sum(v * v, axis=1))
    bottom_point = stem_point_cloud[max_index]
    # print(bottom_point)
    # 平移
    move_corn_data = [np.array([]) for _ in corn_data]
    for i in range(len(corn_data)):
        move_corn_data[i] = corn_data[i] - bottom_point
    del corn_data
    return move_corn_data, bottom_point


def move_rotate_points_cloud(corn_data):
    """
    1. 将玉米 平移到茎的最低点
    2. 将玉米 旋转到 茎 第一主成分 位置
    :param corn_data:
    :return: 点云
    """
    # 平移到茎的最低点
    move_corn_data, bottom_point = move_corn(corn_data)
    # 旋转到茎主轴方向
    corn_data = rotate_cloud(move_corn_data, bottom_point)
    return corn_data

    # 坐标系转化点云可视化
    # corn_point_cloud = []
    # for corn_item in corn_data:
    #     corn_item_cloud = o3d.geometry.PointCloud()
    #     corn_item_cloud.points = o3d.utility.Vector3dVector(corn_item)
    #     corn_item_cloud.paint_uniform_color([0.7, 0.7, 0.7])
    #     corn_point_cloud.append(corn_item_cloud)
    # mesh_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=100, origin=[0, 0, 0])
    # corn_point_cloud.append(mesh_frame)
    # o3d.visualization.draw_geometries(corn_point_cloud)


def create_voxel_from_cloud(np_cloud, np_label, np_rgb, np_sem_label, voxel_size=10):
    """
    从点云中创建体素网格
    :param np_cloud: numpy 格式点云
    :param np_label: numpy 格式点云 label
    :param np_rgb: numpy 格式 rgb
    :param np_sem_label: numpy 格式 semantic label
    :param voxel_size: 体素分辨率
    :return: voxel_data_dict
    """

    # 计算每个点的体素坐标
    voxel_coordinates = np.floor_divide(np_cloud, voxel_size).astype(int)

    # leaf_sheath_voxels = set(tuple(coord) for coord in np.floor_divide(leaf_sheath_list, voxel_size).astype(int))

    # 创建一个字典以存储每个体素的数据
    voxel_data_dict = {}

    # 遍历每个点，将其数据添加到相关的体素中
    for i, coord in enumerate(voxel_coordinates):
        tuple_coord = tuple(coord)
        if tuple_coord not in voxel_data_dict:
            voxel_data_dict[tuple_coord] = {
                'voxel_point': np.array(tuple_coord) * voxel_size,
                'points': [],
                'point_labels': [],
                'rgbs': [],
                'sem_labels': []
            }

        voxel_data_dict[tuple_coord]['points'].append(np_cloud[i])
        voxel_data_dict[tuple_coord]['point_labels'].append(np_label[i])

        if np_rgb is not None:
            voxel_data_dict[tuple_coord]['rgbs'].append(np_rgb[i])

        if np_sem_label is not None:
            voxel_data_dict[tuple_coord]['sem_labels'].append(np_sem_label[i])

    # 转换列表为numpy数组，更便于进一步的操作和处理
    for key, value in voxel_data_dict.items():
        counter = Counter(value['point_labels'])
        most_common_label, _ = counter.most_common(1)[0]
        value['voxel_label'] = most_common_label
        value['points'] = np.array(value['points'])
        value['point_labels'] = np.array(value['point_labels'])
        if np_rgb is not None:
            value['rgbs'] = np.array(value['rgbs'])
        if np_sem_label is not None:
            value['sem_labels'] = np.array(value['sem_labels'])


    return voxel_data_dict


def create_voxel_from_cloud1(np_cloud, np_label, np_rgb, np_sem_label, leaf_sheath_list, voxel_size=10):
    """
    从点云中创建体素网格
    :param np_cloud: numpy 格式点云
    :param np_label: numpy 格式点云 label
    :param np_rgb: numpy 格式 rgb
    :param np_sem_label: numpy 格式 semantic label
    :param leaf_sheath_list: 叶鞘点云列表
    :param voxel_size: 体素分辨率
    :return: voxel_grid_x_y_z, voxel_grid_points_label, voxel_grid_points, leaf_sheath_voxel_list
    """

    def rgb_str(i_rbg):
        i_rgb_str = ""
        for i in i_rbg:
            i_rgb_str = i_rgb_str + f"{i}R"
        i_rgb_str = i_rgb_str[:-1]
        return i_rgb_str

    scale = 100  # 提速生成有去整操作，所以必须大于1 不能太小

    leaf_size = voxel_size * scale
    point_cloud = np_cloud * scale
    # 1、计算边界点
    # 计算体素网格的边界
    min_bound = np.min(point_cloud, axis=0)
    max_bound = np.max(point_cloud, axis=0)

    # 计算体素网格的维度
    dims = np.ceil((max_bound - min_bound) / leaf_size).astype(int)


    # 得到原点坐标的索引
    O_index = np.where(np_cloud == [0, 0, 0])[0][0]
    O_voxel_grid = None
    # 叶鞘对应的体素坐标
    leaf_sheath_voxel_list = []

    # 体素坐标
    # voxel_grid_dict = {}
    # 体素坐标内对应的 点云坐标
    voxel_grid_points_dict = {}
    # 体素坐标内对应的 标签
    voxel_grid_points_label_dict = {}
    voxel_grid_points_rgb_dict = {}
    voxel_grid_points_sem_label_dict = {}
    for i in range(len(point_cloud)):
        hx = math.ceil((point_cloud[i][0] - min_bound[0]) / leaf_size)
        hy = math.ceil((point_cloud[i][1] - min_bound[1]) / leaf_size)
        hz = math.ceil((point_cloud[i][2] - min_bound[2]) / leaf_size)
        key = f"{hx}:{hy}:{hz}"
        if key not in voxel_grid_points_dict:
            voxel_grid_points_dict[key] = [point_cloud[i] / scale]
            voxel_grid_points_label_dict[key] = [int(np_label[i])]
            if np_rgb is not None:
                voxel_grid_points_rgb_dict[key] = [rgb_str(np_rgb[i])]
            if np_sem_label is not None:
                voxel_grid_points_sem_label_dict[key] = [int(np_sem_label[i])]
            # voxel_grid_dict[key] = [int(np_label[i])]
        else:
            voxel_grid_points_dict[key].append(point_cloud[i] / scale)
            voxel_grid_points_label_dict[key].append(int(np_label[i]))
            if np_rgb is not None:
                voxel_grid_points_rgb_dict[key].append(rgb_str(np_rgb[i]))
            if np_sem_label is not None:
                voxel_grid_points_sem_label_dict[key].append(int(np_sem_label[i]))
        if O_index == i:
            O_voxel_grid = [hx, hy, hz]

        # 叶鞘对应的 voxel
        for item in leaf_sheath_list:
            if (item * scale == point_cloud[i]).all():
                leaf_sheath_voxel_list.append(key)

    voxel_grid_l = []
    voxel_grid_x_y_z = []
    voxel_grid_points = []
    voxel_grid_points_label = []
    voxel_grid_points_rgb = []
    voxel_grid_points_sem_label = []
    leaf_sheath_voxel_index_list = []
    i = 0
    for key in voxel_grid_points_dict:

        voxel_grid_x_y_z.append([float(i) for i in key.split(':')])
        one_grid_points = np.array(voxel_grid_points_dict[key])
        voxel_grid_points.append(one_grid_points)
        one_grid_points_label = np.array(voxel_grid_points_label_dict[key])
        voxel_grid_points_label.append(one_grid_points_label)
        if np_rgb is not None:
            voxel_grid_points_rgb.append(voxel_grid_points_rgb_dict[key])
        if np_sem_label is not None:
            voxel_grid_points_sem_label.append(voxel_grid_points_sem_label_dict[key])
        # 去体素中 label 最多的作为体素的标签，
        if one_grid_points_label.max() == 0:
            one_voxel_label = 0
        else:
            label_num = [0 for _ in range(one_grid_points_label.max() + 1)]
            for i in range(one_grid_points_label.max() + 1):
                label_num[i] = np.sum(one_grid_points_label == i)
            # label_num = np.array(label_num)
            label_num_sorted_index = np.argsort(label_num)
            if label_num[label_num_sorted_index[-1]] != label_num[label_num_sorted_index[-2]]:
                one_voxel_label = int(label_num_sorted_index[-1])
            else:
                one_voxel_label = int(label_num_sorted_index[-2])
        voxel_grid_l.append(one_voxel_label)
        for item in leaf_sheath_voxel_list:
            if item == key:
                leaf_sheath_voxel_index_list.append(i)
        i += 1
    voxel_grid_x_y_z = np.array(voxel_grid_x_y_z)
    # 将体素平移到 原点
    voxel_grid_x_y_z -= O_voxel_grid
    voxel_grid_x_y_z /= scale
    voxel_grid_x_y_z *= leaf_size

    leaf_sheath_voxel_points = []
    for idx in leaf_sheath_voxel_index_list:
        leaf_sheath_voxel_points.append(voxel_grid_x_y_z[idx])
    # select 4
    # dist = np.linalg.norm(leaf_sheath_voxel_points, axis=1)
    # sorted_index = np.argsort(dist)
    # selected_index = sorted_index[-3:]
    # leaf_sheath_voxel_points_selected = np.array(leaf_sheath_voxel_points)[selected_index]
    leaf_sheath_voxel_points_str_list = [f"{i[0]};{i[1]};{i[2]}" for i in leaf_sheath_voxel_points]
    return (voxel_grid_x_y_z, np.array(voxel_grid_l), voxel_grid_points,
            voxel_grid_points_label, voxel_grid_points_rgb, voxel_grid_points_sem_label,
            leaf_sheath_voxel_points_str_list)


def generate_cubic1(voxel_grid_x_y_z, voxel_grid_l, voxel_grid_points, leaf_sheath_voxel_list, voxel_size):
    """
    创建 6 面体，获得顶点坐标、元素、顶点label、面、插值参数
    Args:
        voxel_grid_x_y_z:
        voxel_grid_l:
        voxel_grid_points:
        leaf_sheath_voxel_list:
        voxel_size:

    Returns:
        vertices_dict, element_list, element_label, vertices_label_list, face_list, voxel_points_dist_list, leaf_sheath_voxel_index_list
    """
    basic_cubic = [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0], [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]]
    face_index = [[0, 1, 5, 4], [0, 3, 2, 1], [0, 4, 7, 3], [1, 2, 6, 5], [2, 3, 7, 6], [4, 5, 6, 7]]
    cubic_point_dict = {}
    cubic_label_dict = {}
    element_list = []
    element_label = []
    face_list = []
    face_dict = {}
    voxel_points_dist_list = []
    voxel_points_label_list = []
    # voxel_points_closest_index_list = []
    leaf_sheath_voxel_index_list = []

    i = 0
    precision = len(str(voxel_size)) - str(voxel_size).find('.') - 1
    for index, xyz in enumerate(voxel_grid_x_y_z):
        one_cubic_index_list = []
        one_cubic_label = voxel_grid_l[index]
        one_inner_voxel_points = voxel_grid_points[index]
        one_voxel_corner_points = []
        for corner in basic_cubic:
            cubic_point = xyz + np.array(corner) * voxel_size
            one_voxel_corner_points.append(cubic_point)
            # cubic_point_str = f"{cubic_point[0]}:{cubic_point[1]}:{cubic_point[2]}"
            cubic_point_str = f"%.{precision}f:%.{precision}f:%.{precision}f" % (
                cubic_point[0], cubic_point[1], cubic_point[2])
            if cubic_point_str not in cubic_point_dict:
                cubic_point_dict[cubic_point_str] = i
                cubic_label_dict[cubic_point_str] = one_cubic_label
                one_cubic_idx = i
                i += 1
            else:
                one_cubic_idx = cubic_point_dict[cubic_point_str]
            one_cubic_index_list.append(one_cubic_idx)
            for item in leaf_sheath_voxel_list:
                item_arr = np.array([float(i) for i in item.split(';')])
                if (item_arr == xyz).all():
                    leaf_sheath_voxel_list.remove(item)
                    leaf_sheath_voxel_index_list.append(one_cubic_idx)
        # 计算 点在 体素坐标系 下的坐标
        one_voxel_points_dist = cal_voxel_points_dist(one_voxel_corner_points, one_inner_voxel_points, voxel_size)
        voxel_points_dist_list.append(one_voxel_points_dist)
        # voxel_grid_l[index]
        # voxel_points_closest_index_list.append(one_voxel_points_closest_index)

        # 立方体的面
        for one_face in face_index:
            one_cubic_face_index_list = []
            for one_face_idx in one_face:
                cubic_point = xyz + np.array(basic_cubic[one_face_idx]) * voxel_size
                # cubic_point_str = f"{cubic_point[0]}:{cubic_point[1]}:{cubic_point[2]}"
                cubic_point_str = f"%.{precision}f:%.{precision}f:%.{precision}f" % (
                    cubic_point[0], cubic_point[1], cubic_point[2])
                one_cubic_idx = cubic_point_dict[cubic_point_str]
                one_cubic_face_index_list.append(one_cubic_idx + 1)
            # 去除共面
            # 计算面的法线，得到平面方程，判断是否存在共面的

            sorted_one_cubic_face_index_list = sorted(one_cubic_face_index_list)
            key = str(sorted_one_cubic_face_index_list)[1:-1].replace(", ", ':')
            if key not in face_dict:
                face_dict[key] = one_cubic_face_index_list
            # else:
            #     print(key, one_cubic_face_index_list)
            # face_list.append(one_cubic_face_index_list)
        element_list.append(one_cubic_index_list)
        element_label.append(voxel_grid_l[index])

    vertices_dict = {}
    vertices_label_list = np.zeros(len(cubic_point_dict)).astype(int)
    for key in cubic_point_dict:
        vertices_dict[cubic_point_dict[key]] = key
        vertices_label_list[cubic_point_dict[key]] = cubic_label_dict[key]

    # 面
    for key in face_dict:
        face_list.append(face_dict[key])

    return vertices_dict, element_list, element_label, vertices_label_list, np.array(face_list).astype(
        int), voxel_points_dist_list, leaf_sheath_voxel_index_list


def generate_cubic(voxel_data_dict, voxel_size):
    """
    创建 6 面体，获得顶点坐标、元素、顶点label、面、插值参数
    Args:
        voxel_data_dict:
        voxel_size:

    Returns:
        vertices, vertices_labels, elements, elements_labels, faces, voxel_inner_differences, voxel_points_rgbs, voxel_points_sem_labels, voxel_points_labels
    """

    basic_cubic = np.array([
        [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0], [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]
    ]) * voxel_size

    face_index = [[0, 1, 5, 4], [0, 3, 2, 1], [0, 4, 7, 3], [1, 2, 6, 5], [2, 3, 7, 6], [4, 5, 6, 7]]


    vertices = []
    face_set = set()  # Using set to ensure face uniqueness
    faces = []

    vertices_labels = []

    elements = []
    elements_labels = []

    voxel_inner_differences = []
    voxel_points_rgbs = []
    voxel_points_sem_labels = []
    voxel_points_labels = []

    vertex_index_dict = {}  # Store the unique vertex and its index
    for voxel_coord, voxel_data in voxel_data_dict.items():
        voxel_point = np.round(np.array(voxel_data['voxel_point']), 2)

        # Calculate the 8 vertices for this voxel
        voxel_vertices = basic_cubic + voxel_point
        voxel_vertices = np.round(voxel_vertices, 2)


        voxel_inner_points = np.array(voxel_data['points'])
        # Compute the difference with origin for each vertex
        voxel_differences = (voxel_inner_points - voxel_point) / voxel_size
        voxel_inner_differences.append(voxel_differences)
        voxel_points_rgbs.append(voxel_data['rgbs'])
        voxel_points_sem_labels.append(voxel_data['sem_labels'])
        voxel_points_labels.append(voxel_data['point_labels'])

        # Check for vertex uniqueness and store unique vertices
        current_vertex_indices = []
        for vertex in voxel_vertices:
            vertex_tuple = tuple(vertex)
            if vertex_tuple not in vertex_index_dict:
                vertex_index_dict[vertex_tuple] = len(vertices)
                vertices.append(vertex)
                vertices_labels.append(voxel_data['voxel_label'])
            current_vertex_indices.append(vertex_index_dict[vertex_tuple])

        elements.append(current_vertex_indices)
        elements_labels.append(voxel_data['voxel_label'])
        # Generate faces for this voxel using the face_index
        for face in face_index:
            voxel_face = [current_vertex_indices[idx] for idx in face]
            voxel_face_tuple = tuple(sorted(voxel_face))  # Ensure the face is represented in the same order
            if voxel_face_tuple not in face_set:  # Ensure the face is unique
                face_set.add(voxel_face_tuple)
                faces.append(voxel_face)

    return vertices, vertices_labels, elements, elements_labels, faces, voxel_inner_differences, voxel_points_rgbs, voxel_points_sem_labels, voxel_points_labels


def cal_voxel_points_dist(one_voxel_corner_points, one_inner_voxel_points, voxel_size=1):
    """
    计算 点在 体素坐标系 下的 三线性插值距离
    Args:
        one_voxel_corner_points:
        one_inner_voxel_points:
        voxel_size:

    Returns:
        d_list:
    """

    d_list = []
    # closest_corner_index_list = []
    for p in one_inner_voxel_points:
        # 计算 p 离那个顶点最近
        # d_v = np.array(one_voxel_corner_points) - np.array(p)
        # d_dist = np.sum(np.power(d_v, 2), axis=1)
        # d_index = np.argmin(d_dist)
        w0 = one_voxel_corner_points[0]
        # dist = (p - w0) / voxel_size
        dist = p - w0
        d_list.append(dist)
        # closest_corner_index_list.append(d_index)

    return d_list


def trilinear_interpolation(one_voxel_corner_points, one_voxel_points, voxel_size):
    """
    对一个体素内的所有点进行三线性插值
    Args:
        one_voxel_corner_points: 体素顶点坐标
        one_voxel_points: 体素内的点
        voxel_size: 体素大小
    Returns:
        KK: 插值参数
    """
    L = voxel_size
    # interpolated_points = []
    KK = []
    for p in one_voxel_points:
        # 计算 p 离那个顶点最近
        d_v = np.array(one_voxel_corner_points) - np.array(p)
        d_dist = np.sum(np.power(d_v, 2), axis=1)
        d_index = np.argmin(d_dist)
        w0 = one_voxel_corner_points[d_index]
        A = (p - w0) / L
        a, b, c = A
        K = []
        K.append((1 - a) * (1 - b) * (1 - c))
        K.append(a * (1 - b) * (1 - c))
        K.append(a * b * (1 - c))
        K.append((1 - a) * b * (1 - c))
        K.append((1 - a) * (1 - b) * c)
        K.append(a * (1 - b) * c)
        K.append(a * b * c)
        K.append((1 - a) * b * c)
        KK.append(K)
        # p_ = 0
        # for i in range(len(K)):
        #     p_ += K[i] * one_voxel_corner_points[i]

        # interpolated_points.append(p_)

    return KK


def save_leaf_sheath(leaf_sheath_index, filepath):
    """
    保存叶鞘
    :param leaf_sheath_index:
    :param filepath:
    :return:
    """

    with open(filepath, 'w') as f:
        for item in leaf_sheath_index:
            f.write(f"{item},")


def save_bottom_index(vertices_dict, leaf_sheath_index, bottom_filepath, bottom_num=5):
    """
    获取最底部的几个顶点，并保存叶鞘顶点
    :param vertices_dict:
    :param leaf_sheath_index:
    :param bottom_filepath:
    :param bottom_num:
    :return:
    """

    pass
    # v_list = []
    # # v_dist = []
    # for key in vertices_dict:
    #     value = np.array([float(i) for i in vertices_dict[key].split(':')])
    #     v_list.append(value)
    #     # v_dist.append(abs(value[0]) + abs(value[1]) + abs(value[2]))
    # v_arr = np.array(v_list)
    # v_dist = np.array(v_dist)
    # min_index = np.argsort(v_arr[:, -1])[:bottom_num]
    # min_index = np.argsort(np.sum(np.power(v_arr, 2), axis=1))[:bottom_num]
    # min_index = list(min_index)
    # bottom_arr = v_arr[min_index]

    #
    # with open(bottom_filepath, 'w') as f:
    #     for item in min_index:
    #         f.write(f"{item + 1},")
    # for item in leaf_sheath_index:
    #     f.write(f"{item + 1},")


def save_bottom_first_index(vertices_first_np, bottom_filepath, bottom_num=5):
    """
    获取最底部的几个顶点
    :param vertices_first_np:
    :param bottom_filepath:
    :param bottom_num:
    :return:
    """

    v_dist = np.sqrt(
        np.power(vertices_first_np[:, 0], 2) + np.power(vertices_first_np[:, 1], 2) + np.power(vertices_first_np[:, 2],
                                                                                               2))
    min_index = np.argsort(v_dist)[:bottom_num]
    min_index = list(min_index * 8)
    # bottom_arr = v_arr[min_index]

    with open(bottom_filepath, 'w') as f:
        f.write(str(min_index)[1:-1].replace(',', ''))


def create_veg_file(filepath, vertices, elements, element_label,
                    MATERIALS = "\n*MATERIAL STEM\nENU, 1000, 100000, 0.01\n\n*MATERIAL LEAF\nENU, 1000, 10000000, 0.45\n"):
    """
    创建 veg 文件
    :param filepath:
    :param vertices_dict:
    :param element_list:
    :param element_label:
    :param MATERIALS: 材料参数
    :return:
    """

    vertices_count = len(vertices)
    elements_count = len(elements)

    # 文件头
    FILE_HEADER = "# Vega mesh file.\n"
    FILE_INFO = f"# {vertices_count} vertices, {elements_count} elements\n"

    # 顶点 VERTICES
    VERTICES_name = "\n*VERTICES\n"
    VERTICES_info = f"{vertices_count} 3 0 0\n"
    VERTICES_value = ""
    for index, v in enumerate(vertices):
        # value = [float(i) for i in vertices_dict[key].split(':')]
        VERTICES_value += f"{index+1} {v[0]} {v[1]} {v[2]}\n"

    # 元素 ELEMENTS
    ELEMENTS_name = "\n*ELEMENTS\n"
    ELEMENTS_type = "CUBIC\n"
    ELEMENTS_info = f"{elements_count} 8 0\n"
    ELEMENTS_value = ""
    for index, element in enumerate(elements):
        ELEMENTS_value += f"{index+1} {element[0]+1} {element[1]+1} {element[2]+1} {element[3]+1} {element[4]+1} {element[5]+1} {element[6]+1} {element[7]+1}\n"

    # 材料
    '''
    质量密度
    杨氏模量越大，越不容易变形
    泊松比是指在材料的比例极限内，由均匀分布的纵向应力引起的横向应变与相应的纵向应变之比的值
    '''
    # MATERIAL_name0 = "\n*MATERIAL STEM\n"
    # MATERIAL_value0 = "ENU, 1000, 100000, 0.01\n"
    #
    # MATERIAL_name1 = "\n*MATERIAL LEAF\n"
    # MATERIAL_value1 = "ENU, 1000, 10000000, 0.45\n"


    # 集合
    SET_name0 = "\n*SET set0\n"
    SET_value0 = ""
    count = 0
    for i in range(len(element_label)):
        if element_label[i] == 0:
            SET_value0 += f"{i+1}, "
            count += 1
        if count == 7:
            SET_value0 += "\n"
            count = 0

    SET_name1 = "\n*SET set1\n"
    SET_value1 = ""
    count = 0
    for i in range(len(element_label)):
        if element_label[i] != 0:
            SET_value1 += f"{i+1}, "
            count += 1
        if count == 7:
            SET_value1 += "\n"
            count = 0

    # REGION
    REGION_name0 = "\n*REGION\n"
    REGION_value0 = "set0, STEM\n"
    REGION_name1 = "\n*REGION\n"
    REGION_value1 = "set1, LEAF\n"

    with open(filepath, 'w') as f:
        f.write(FILE_HEADER)
        f.write(FILE_INFO)

        f.write(VERTICES_name)
        f.write(VERTICES_info)
        f.write(VERTICES_value)

        f.write(ELEMENTS_name)
        f.write(ELEMENTS_type)
        f.write(ELEMENTS_info)
        f.write(ELEMENTS_value)

        # f.write(MATERIAL_name0)
        # f.write(MATERIAL_value0)
        # f.write(MATERIAL_name1)
        # f.write(MATERIAL_value1)
        f.write(MATERIALS)

        f.write(SET_name0)
        f.write(SET_value0)
        f.write(SET_name1)
        f.write(SET_value1)

        f.write(REGION_name0)
        f.write(REGION_value0)
        f.write(REGION_name1)
        f.write(REGION_value1)

    return 1


def create_obj_file(filepath, vertices, face_list):
    """
    创建 obj 文件
    :param filepath:
    :param vertices:
    :param face_list:
    :return:
    """
    vertices_count = len(vertices)
    normals = 0
    faces = len(face_list)
    groups = 1

    # 文件头
    FILE_HEADER = "# Vega mesh file.\n"
    FILE_INFO = f"# Number of vertices: {vertices_count}\n"
    FILE_INFO += f"# Number of texture coordinates: 0\n"
    # FILE_INFO += f"# Number of normals: {normals}\n"
    FILE_INFO += f"# Number of faces: {faces}\n"
    FILE_INFO += f"# Number of groups: {groups}\n"

    # 顶点 VERTICES
    VERTICES = ""
    for v in vertices:
        # value = [float(i) for i in vertices_dict[key].split(':')]
        VERTICES += f"v {v[0]} {v[1]} {v[2]}\n"

    # group
    GROUP = "g Default\n"

    # face
    FACES = ""
    for face_one in face_list:
        FACES += f"f {face_one[0]+1} {face_one[1]+1} {face_one[2]+1} {face_one[3]+1}\n"

    with open(filepath, 'w') as f:
        f.write(FILE_HEADER)
        f.write(FILE_INFO)

        f.write(VERTICES)
        f.write(GROUP)
        f.write(FACES)


def mkdir_or_exist(dir_name, mode=0o777):
    """
    递归创建文件夹
    :param dir_name:
    :param mode:
    :return:
    """
    if dir_name == '':
        return
    dir_name = os.path.expanduser(dir_name)
    os.makedirs(dir_name, mode=mode, exist_ok=True)


def concatenate_corn_data(transpose_corn_data):
    """
    将分开的玉米点云合并为一个，并保留 label
    :param transpose_corn_data:
    :return:
    """
    label = []
    for index, item in enumerate(transpose_corn_data):
        count = item.shape[0]
        item_label = np.ones(count).astype(int) * index
        label.append(item_label)
    hole_corn_cloud = np.concatenate(transpose_corn_data)
    hole_corn_label = np.concatenate(label)
    return hole_corn_cloud, hole_corn_label


def save_random_choice_leaf_vertices(vertices_label_list, filepath, per_num=2):
    """
    叶子中随即点选取, 并保存
    :param vertices_label_list: 顶点 label
    :param filepath: 保存的文件名
    :param per_num: 每个叶子随机选取的顶点个数
    :return:
    """
    group_leaf = []
    n = vertices_label_list.max()
    for i in range(1, n + 1):
        leaf_index_list = np.where(vertices_label_list == i)[0]
        leaf_random_index = np.random.choice(leaf_index_list, size=per_num)
        group_leaf.append(leaf_random_index)
    group_leaf = list(np.array(group_leaf).reshape(-1))
    with open(filepath, 'w') as f:
        for item in group_leaf:
            f.write(f"{item},")


def save_random_choice_leaf_vertices_improve(vertices, vertices_label, filepath, per_num=-1):
    """
    叶尖（x，y 方向上 距 0 点的 1/4 作为叶尖）中随即点选取, 并保存
    :param vertices: 顶点
    :param vertices_label: 顶点 label
    :param filepath: 保存的文件名
    :param per_num: 每个叶子随机选取的顶点个数, -1 叶尖全部
    :return:
    """
    group_leaf = []
    vertices_label_list = np.array(vertices_label).astype(int)
    n = vertices_label_list.max()
    # vis_point = []
    real_stem_bottom_index = None
    mid_stem_index_list = None
    # 叶
    for i in range(0, n + 1):
        leaf_index_list = np.where(vertices_label_list == i)[0]
        # 叶子对应的顶点坐标
        leaf_points_list = []
        for leaf_index in leaf_index_list:
            value = vertices[leaf_index]
            leaf_points_list.append(value)
        leaf_points_arr = np.array(leaf_points_list)
        if i != 0:
            dist = np.linalg.norm(leaf_points_arr, axis=1)
            min_index_dist = np.argmin(dist)
            min_point = leaf_points_arr[min_index_dist]
            dist2 = np.linalg.norm(leaf_points_arr - min_point, axis=1)
            d = dist2.max()
            d_ = d - d / 5
            leaf_top_index_list = np.where(dist2 >= d_)[0]
        else:
            # 茎
            # dist = np.linalg.norm(leaf_points_arr, axis=1)
            dist = leaf_points_arr[:, 2]
            dist_sorted = np.argsort(dist)
            # leaf_top_index_list = [np.argmin(dist)]
            leaf_top_index_list = dist_sorted[:8]
            stem_bottom_index = dist_sorted[-4:]
            real_stem_bottom_index = leaf_index_list[stem_bottom_index]

            # stem 1/5 2/5 3/5 4/5
            max_dist = dist[dist_sorted[-1]] - dist[dist_sorted[1]]
            t_dist = max_dist/3
            mid_stem_index_list = np.where((dist > t_dist) & (dist <= 2*t_dist))[0]

        real_leaf_top_index_list = leaf_index_list[leaf_top_index_list]
        # vis_point.append(leaf_points_arr[leaf_top_index_list])
        if per_num != -1:
            leaf_random_index = np.random.choice(real_leaf_top_index_list, size=per_num)
            group_leaf.append(list(leaf_random_index))
        else:
            group_leaf.append(real_leaf_top_index_list)

    # 施加力的点
    for index, one_leaf in enumerate(group_leaf):
        with open(filepath.replace(".bou", f"_{index}.bou"), 'w') as f:
            for item in one_leaf:
                f.write(f"{item + 1},")

    # 固定茎的顶部
    if real_stem_bottom_index is not None:
        with open(filepath.replace('_random_leaf', ''), 'w') as f:
            for item in real_stem_bottom_index:
                f.write(f"{item + 1},")

    # 茎的顶点全部固定
    stem_index_list = np.where(vertices_label_list == 0)[0]
    with open(filepath.replace('_random_leaf', '_stem'), 'w') as f:
        for item in stem_index_list:
            f.write(f"{item + 1},")

    # 茎的中间顶点
    with open(filepath.replace('_random_leaf', f'_stem_mid'), 'w') as f:
        for index, item in enumerate(mid_stem_index_list):
            f.write(f"{item + 1},")

def save_vertices(filepath, vertices_dict):
    """
    保存顶点坐标
    :param filepath
    :param vertices_dict
    """
    # 顶点 VERTICES
    VERTICES = ""
    for key in vertices_dict:
        value = [float(i) for i in vertices_dict[key].split(':')]
        VERTICES += f"{value[0]} {value[1]} {value[2]}\n"

    with open(filepath, 'w') as f:
        f.write(VERTICES)
    return 1


def save_vertices_labels(filepath, vertices_label_list):
    """
    保存顶点坐标和label的对应关系
    :param filepath
    :param vertices_label_list
    """
    np.savetxt(filepath, vertices_label_list, fmt='%d')


def save_voxel_points_parameters(filepath, voxel_points_list, fmt):
    """
    保存 点在 对应体素坐标系 下的坐标
    Args:
        filepath:
        voxel_points_list:
        fmt:
    Returns:

    """
    f = open(filepath, 'w')
    for one_voxel in voxel_points_list:
        tmp_str = ""
        for one_point in one_voxel:
            one_point_str = ""
            for item in one_point:
                one_point_str += f"{fmt}," % item
            one_point_str = one_point_str[:-1]
            tmp_str += f"{one_point_str};"
        f.write(f"{tmp_str}\n")

    f.close()


def save_points_labels(filepath, voxel_grid_points_label, fmt):
    """
    保存体素内点云坐标和label的对应关系
    Args:
        filepath:
        voxel_grid_points_label:
         fmt:
    Returns:

    """
    f = open(filepath, 'w')
    for one_voxel in voxel_grid_points_label:
        tmp_str = ""
        for one_label in one_voxel:
            tmp_str += f"{fmt(one_label)},"
        tmp_str = tmp_str[:-1]
        f.write(f"{tmp_str}\n")

    f.close()


def f_log(string):
    print("......%s......" % string)


def cal_leaf_sheath(hole_corn_cloud, hole_corn_label, num=2):
    """
    计算叶鞘
    :param hole_corn_cloud:
    :param hole_corn_label:
    :param num: 每个叶鞘固定的点数
    :return:
    """
    size = int(hole_corn_label.max())
    stem_mask = np.where(hole_corn_label == 0)
    stem_points = hole_corn_cloud[stem_mask]
    leaf_sheath_point_list = []
    for i in range(1, size + 1):
        leaf_mask = np.where(hole_corn_label == i)
        leaf_points = hole_corn_cloud[leaf_mask]
        if len(leaf_points) == 0:
            continue
        dist = sys.maxsize
        min_p = None
        for p in leaf_points:
            p_d = np.linalg.norm(stem_points - p, axis=1)
            # d_min_index = np.argsort(d)[0]
            if p_d.min() < dist:
                dist = p_d.min()
                min_p = p
        leaf_sheath_point_list.append(min_p)
    return leaf_sheath_point_list


def get_data_split(data_root, corn_name, normal=True, rgb=False, semantic=False):
    """
    分割数据
    :param data_root:
    :param corn_name:
    :param normal:
    :param rgb: 是否存在 rgb
    :param semantic:  是否存在 semantic label
    :return:
    """

    corn_path = os.path.join(data_root, corn_name)
    # leaf_num = int(corn_name.split('-')[1])
    corn_xyzl = np.loadtxt(corn_path)
    point_set = corn_xyzl[:, :3]
    point_set, m = pc_normalize(point_set) if normal else point_set
    point_rgb = corn_xyzl[:, 3:6] if rgb else None
    point_sem_label = corn_xyzl[:, 6] if semantic else None
    point_ins_label = corn_xyzl[:, -1]

    return point_set, point_rgb, point_sem_label, point_ins_label, m


def generate_one(data_root, veg_root, corn_name, leaf_num, voxel_size=0.02, normal=True, rgb=False, semantic=False,
                 MATERIALS = "\n*MATERIAL STEM\nENU, 1000, 100000, 0.01\n\n*MATERIAL LEAF\nENU, 1000, 10000000, 0.45\n"):
    """
    生成一个基础的模板
    :param data_root:
    :param veg_root:
    :param corn_name:
    :param voxel_size:
    :param normal: 是否归一化
    :param rgb:
    :param semantic:
    :param MATERIALS:

    :return:
    """
    # scale = 2000
    # corn_data = get_stem_leafs(data_root, corn_name, leaf_num, normal=normal)
    # # 坐标系转化
    # transpose_corn_data = move_rotate_points_cloud(corn_data)
    # hole_corn_cloud, hole_corn_label = concatenate_corn_data(transpose_corn_data)

    hole_corn_cloud, hole_corn_rgb, hole_corn_sem_l, hole_corn_label, m = get_data_split(data_root, corn_name, normal=normal, rgb=rgb, semantic=semantic)
    # 获取叶鞘
    # leaf_sheath_list = cal_leaf_sheath(hole_corn_cloud, hole_corn_label)

    # 体素网格生成
    # voxel_grid_x_y_z, voxel_grid_l, voxel_grid_points, voxel_grid_points_label, voxel_grid_points_rgb, voxel_grid_points_sem_label, leaf_sheath_voxel_points = \
    #     create_voxel_from_cloud(hole_corn_cloud,
    #                             hole_corn_label,
    #                             hole_corn_rgb,
    #                             hole_corn_sem_l,
    #                             leaf_sheath_list,
    #                             voxel_size=voxel_size)

    voxel_data_dict = create_voxel_from_cloud(hole_corn_cloud,
                                hole_corn_label,
                                hole_corn_rgb,
                                hole_corn_sem_l,
                                voxel_size=voxel_size)
    f_log("体素化")
    # # 点云可视化
    # corn_item_cloud = o3d.geometry.PointCloud()
    # corn_item_cloud.points = o3d.utility.Vector3dVector(voxel_grid_x_y_z)
    # corn_item_cloud.paint_uniform_color([0.7, 0.7, 0.7])
    # mesh_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.01, origin=[0, 0, 0])
    # corn_item_cloud2 = o3d.geometry.PointCloud()
    # corn_item_cloud2.points = o3d.utility.Vector3dVector(hole_corn_cloud)
    # corn_item_cloud2.paint_uniform_color([1, 0, 0.7])
    # o3d.visualization.draw_geometries([corn_item_cloud, corn_item_cloud2, mesh_frame])

    # 六面体生成
    # vertices_dict, element_list, element_label, vertices_label_list, face_list, voxel_points_dist_list, leaf_sheath_voxel_index_list = \
    #     generate_cubic(voxel_data_dict[''], voxel_grid_l, voxel_grid_points, leaf_sheath_voxel_points, voxel_size)

    (vertices, vertices_labels, elements, elements_labels, faces, voxel_inner_differences, voxel_points_rgbs,
     voxel_points_sem_labels, voxel_points_labels) = generate_cubic(voxel_data_dict, voxel_size)
    f_log("六面体生成")


    # veg 文件生成
    veg_filepath = os.path.join(veg_root, f"{os.path.splitext(corn_name)[0]}.veg")
    create_veg_file(veg_filepath, vertices, elements, elements_labels, MATERIALS=MATERIALS)
    f_log(f"veg 文件生成: 立方体个数： {len(elements)}")

    # 叶子中随即点选取
    # fix: 包括茎
    random_leafs_filepath = os.path.join(veg_root, f"{os.path.splitext(corn_name)[0]}_random_leaf.bou")
    save_random_choice_leaf_vertices_improve(vertices, vertices_labels, random_leafs_filepath)
    f_log("叶子中随即点选取")

    # 底部顶点
    # leaf_sheath_filepath = os.path.join(veg_root, f"{os.path.splitext(corn_name)[0]}_leaf_sheaths.bou")
    # save_leaf_sheath(leaf_sheath_voxel_index_list, leaf_sheath_filepath)
    # save_bottom_index(vertices_dict, leaf_sheath_voxel_index_list, bottom_filepath, bottom_num=6)
    # save_bottom_first_index(vertices_first_np, bottom_filepath, bottom_num=5)
    # f_log("叶鞘顶点")

    # obj 文件生成
    obj_filepath = os.path.join(veg_root, f"{os.path.splitext(corn_name)[0]}.obj")
    create_obj_file(obj_filepath, vertices, faces)
    f_log("obj 文件生成")

    # # 保存顶点坐标
    # vertices_filepath = os.path.join(veg_root, f"{os.path.splitext(corn_name)[0]}_vertices.txt")
    # save_vertices(vertices_filepath, vertices_dict)
    # f_log("保存顶点坐标")

    # # 保存顶点坐标和label的对应关系
    # label_filepath = os.path.join(veg_root, f"{os.path.splitext(corn_name)[0]}_vertices_labels.txt")
    # save_vertices_labels(label_filepath, vertices_label_list)

    # 保每个体素内的插值参数
    voxel_points_dist_filepath = os.path.join(veg_root, f"{os.path.splitext(corn_name)[0]}_voxel_points_dist.txt")
    save_voxel_points_parameters(voxel_points_dist_filepath, voxel_inner_differences, fmt='%.6f')
    f_log("保每个体素内的插值参数")

    # 保存体素内点云坐标和label的对应关系 voxel_inner_differences, voxel_points_rgbs, voxel_points_sem_labels, voxel_points_labels
    points_label_filepath = os.path.join(veg_root, f"{os.path.splitext(corn_name)[0]}_points_labels.txt")
    save_points_labels(points_label_filepath, voxel_points_labels,  fmt=int)
    points_label_filepath = os.path.join(veg_root, f"{os.path.splitext(corn_name)[0]}_points_rgb.txt")
    rgb_lambda = lambda i_rgb: ''.join([f"{i}R" for i in i_rgb])[:-1]
    save_points_labels(points_label_filepath, voxel_points_rgbs,  fmt=rgb_lambda)
    points_label_filepath = os.path.join(veg_root, f"{os.path.splitext(corn_name)[0]}_points_sem_labels.txt")
    save_points_labels(points_label_filepath, voxel_points_sem_labels,  fmt=int)
    f_log("保存体素内点云坐标和label的对应关系")



    # # 保存缩放平移后的点云
    # scaled_points_filepath = os.path.join(veg_root, f"{os.path.splitext(corn_name)[0]}_pointcloud.txt")
    # np.savetxt(scaled_points_filepath, hole_corn_cloud, fmt='%.6f')
    # f_log("保存缩放平移后的点云")

    # 保存归一化比例
    np.savetxt(os.path.join(veg_root, f"{os.path.splitext(corn_name)[0]}_m.txt"), np.array([m]))

def main():
    # /home/yangxin/datasets/3d_corn/miao_corn
    # /Users/yang/datasets/corn_20221226
    # /home/keys/datasets/Corn
    deform_dir = "leaf_7_1000_30"
    data_root = "/home/yangxin/datasets/3d_corn/deformation/"
    deform_root = os.path.join(data_root, "deform_root", deform_dir)
    veg_root = os.path.join(data_root, "veg", deform_dir)
    mkdir_or_exist(veg_root)
    # # 10-5-1 11-5-1
    # # corn_name_dict = {
    # #     "LD145-4-2-1": 0.002,
    # #     "LD145-5-2-1": 0.003,
    # #     "LD145-6-3-1": 0.003,
    # #     "LD145-7-3-1": 0.01,
    # #     "LD145-8-4-1": 0.01,
    # #     "LD145-9-5-1": 0.01,
    # #     "LD145-10-5-1": 0.01,
    # #     "LD145-11-5-1": 0.008,
    # # }
    # corn_name_list = [
    #     "LD145-4-2-1",
    #     "LD145-5-2-1",
    #     "LD145-6-3-1",
    #     "LD145-7-3-1",
    #     "LD145-8-4-1",
    #     "LD145-9-5-1",
    #     "LD145-10-5-1",
    #     "LD145-11-5-1",
    # ]
    corn_name_list = [i.split('.')[0] for i in os.listdir(deform_root)]
    voxel_size = 0.02
    for key in corn_name_list:
        f_log(f" ==={key} 开始 === ")
        # voxel_size = corn_name_dict[key]
        corn_name = key + '.txt'
        # 生成一个
        generate_one(deform_root, veg_root, corn_name, voxel_size, normal=True)
        f_log(f"=== {key} 完成 === \n")
    f_log("-----------结束--------------")


if __name__ == "__main__":
    main()
