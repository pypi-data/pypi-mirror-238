# -*- coding:utf-8 -*-
'''
coding   : utf-8
@Project ：corn_organ_segmentation
@File    ：obj_2_points.py
@IDE     ：PyCharm
@Author  ：杨鑫
@Date    ：2023/1/5 19:17
'''
import os.path
import sys
import numpy as np
import open3d as o3d

np.random.seed(1234567)


def read_vertices_and_elements_index(vertices_filepath, elements_filepath):
    """
    读取变形后的 顶点、元素
    Args:
        vertices_filepath:
        elements_filepath:

    Returns:
        vertices
        elements
    """
    vertices = np.loadtxt(vertices_filepath)
    elements = np.loadtxt(elements_filepath).astype(int)
    return vertices, elements


def convert_element(element_index, vertices):
    """
    将 element 索引 换位坐标
    Args:
        element_index:
        vertices:

    Returns:
        element_points
    """
    element_points = []
    for one_ele in element_index:
        one_ele_p = []
        for one_e in one_ele:
            p = vertices[one_e]
            one_ele_p.append(p)
        element_points.append(one_ele_p)
    return element_points


def save_points(filepath, np_points):
    """
    保存点云
    Args:
        filepath:
        np_points:

    Returns:

    """
    np.savetxt(filepath, np_points, fmt='%.6f')


def mkdir_or_exist(dir_name, mode=0o777):
    """
    递归创建文件夹
    Args:
        dir_name:
        mode:

    Returns:

    """
    if dir_name == '':
        return
    dir_name = os.path.expanduser(dir_name)
    os.makedirs(dir_name, mode=mode, exist_ok=True)


def read_voxel_points_parameters(filepath, fmt):
    """
    读取原始 体素内点的坐标
    Args:
        filepath:
        fmt:
    Returns:
        voxel_points
    """
    voxel_points = []
    with open(filepath, 'r') as f:
        while True:
            line = f.readline()
            if line:
                one_voxel_points = line.split(';')[:-1]
                one_voxel_points_list = []
                for one_voxel_point_str in one_voxel_points:
                    one_voxel_point = [fmt(i.rstrip()) for i in one_voxel_point_str.split(',')]
                    one_voxel_points_list.append(one_voxel_point)
                voxel_points.append(np.array(one_voxel_points_list))
            else:
                break
    return voxel_points


def cal_deformed_points_labels(element_points_list, voxel_points_dist, voxel_points_labels, voxel_points_rgb=None,
                               voxel_points_sem_labels=None, e=1, m=1):
    """
    计算 变形后的点坐标 及 标签
    Args:
        element_points_list:
        voxel_points_dist:
        voxel_points_labels:
        e: 误差因子，点在 e 倍 体素大小之内
    Returns:
        deformed_points_labels:
        # error_points_statistics： [size, min, max, mean, median]
    """
    deformed_points_labels = []
    # error_points = []
    for index, one_voxel_corner_points in enumerate(element_points_list):
        X_length = one_voxel_corner_points[1][0] - one_voxel_corner_points[0][0]  # X 边的长度
        Y_length = one_voxel_corner_points[3][1] - one_voxel_corner_points[0][1]  # Y 边的长度
        Z_length = one_voxel_corner_points[4][2] - one_voxel_corner_points[0][2]  # Z 边的长度
        voxel_dist = np.linalg.norm([X_length, Y_length, Z_length])
        one_voxel_points_dist = voxel_points_dist[index]
        one_voxel_points_labels = voxel_points_labels[index]
        if voxel_points_rgb is not None:
            one_voxel_points_rgb = voxel_points_rgb[index]
        if voxel_points_sem_labels is not None:
            one_voxel_points_sem_labels = voxel_points_sem_labels[index]
        for j, d in enumerate(one_voxel_points_dist):
            # A = d / np.array([X_length, Y_length, Z_length])
            A = d
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
            p_ = 0
            for i in range(len(K)):
                p_ += K[i] * one_voxel_corner_points[i]

            # p 点到原点的距离
            p_dist = np.linalg.norm(p_ - one_voxel_corner_points[0])
            error = abs(p_dist - voxel_dist)
            if error > e * voxel_dist:
                continue
                # error_points.append(p_dist - voxel_dist)

            # 恢复到原始尺寸大小
            p_ *= m
            p_l = list(p_)
            if voxel_points_rgb is not None:
                for r in one_voxel_points_rgb[j]:
                    p_l.append(float(r))
            if voxel_points_sem_labels is not None:
                p_l.append(one_voxel_points_sem_labels[j])
            # print(index, j)
            p_l.append(one_voxel_points_labels[j])
            deformed_points_labels.append(p_l)

            # p 在 体素内
            # r_p = p_ - one_voxel_corner_points[0]
            # if 0 <= r_p[0] <= e * X_length and 0 <= r_p[1] <= e * Y_length and 0 <= r_p[2] <= e * Z_length:
            #     p_l = list(p_)
            #     p_l.append(one_voxel_points_labels[j])
            #     deformed_points_labels.append(p_l)

    # error_points_np = np.array(error_points) error_points_statistics = [error_points_np.size, error_points_np.min(
    # ), error_points_np.max(), np.mean(error_points_np), np.median(error_points_np)]
    return np.array(deformed_points_labels)


def read_voxel_points_labels(filepath, fmt):
    """

    Args:
        filepath:
        fmt:
    Returns:
        voxel_points_labels
    """
    voxel_points_labels = []
    with open(filepath, 'r') as f:
        while True:
            line = f.readline()
            if line:
                one_voxel_points_labels_list = [fmt(i.rstrip()) for i in line.split(',')]
                voxel_points_labels.append(one_voxel_points_labels_list)
            else:
                break
    return voxel_points_labels


def read_voxel_points_rgb(filepath):
    """

    Args:
        filepath:
    Returns:
        voxel_points_labels
    """

    def decode_rgb(rgb_str):
        rgb_list = [float(r) for r in rgb_str.split('R')]
        return rgb_list

    voxel_points_rgb = []
    with open(filepath, 'r') as f:
        while True:
            line = f.readline()
            if line:
                one_voxel_points_rgb = [decode_rgb(i.rstrip()) for i in line.split(',')]
                voxel_points_rgb.append(one_voxel_points_rgb)
            else:
                break
    return voxel_points_rgb


def cal_voxel_inner_points_labels(deformed_vertices_root, voxel_inner_points_root, txt_name, rgb=False, semantic=False):
    """
    还原 体素内点的坐标 及 标签
    Args:
        deformed_vertices_root:
        voxel_inner_points_root:
        txt_name:
        normalized: 是否归一化
    Returns:

    """
    # 读取变形后的 顶点 与 体素元素索引
    transformed_vertices_filepath = os.path.join(deformed_vertices_root, txt_name + '_vertices.txt')
    transformed_elements_filepath = os.path.join(deformed_vertices_root, txt_name + '_elements.txt')
    vertices, element_index = read_vertices_and_elements_index(transformed_vertices_filepath,
                                                               transformed_elements_filepath)

    # 将 element 索引 换位坐标
    element_points_list = convert_element(element_index, vertices)

    # 读取原始 体素内点的坐标
    data_name = txt_name[:-14]
    voxel_points_dist_filepath = os.path.join(voxel_inner_points_root, data_name + '_voxel_points_dist.txt')
    voxel_points_dist = read_voxel_points_parameters(voxel_points_dist_filepath, float)

    # 读取原始点对应的 label
    voxel_points_labels_filepath = os.path.join(voxel_inner_points_root, data_name + '_points_labels.txt')
    voxel_points_labels = read_voxel_points_labels(voxel_points_labels_filepath, int)

    voxel_points_rgb = None
    if rgb:
        # 读取原始点对应的 rgb
        voxel_points_labels_filepath = os.path.join(voxel_inner_points_root, data_name + '_points_rgb.txt')
        voxel_points_rgb = read_voxel_points_rgb(voxel_points_labels_filepath)
    voxel_points_sem_labels = None
    if semantic:
        # 读取原始点对应的 sem label
        voxel_points_labels_filepath = os.path.join(voxel_inner_points_root, data_name + '_points_sem_labels.txt')
        voxel_points_sem_labels = read_voxel_points_labels(voxel_points_labels_filepath, int)

    # 读取 m 缩放比例
    m = float(np.loadtxt(os.path.join(voxel_inner_points_root, data_name + '_m.txt')))
    # 计算 变形后的点坐标
    deformed_points_labels = cal_deformed_points_labels(element_points_list, voxel_points_dist, voxel_points_labels,
                                                        voxel_points_rgb, voxel_points_sem_labels, m=m)

    return deformed_points_labels


def create_x(size, rank):
    x = []
    for i in range(2 * size + 1):
        m = i - size
        row = [m ** j for j in range(rank)]
        x.append(row)
    x = np.mat(x)
    return x


def pc_scale(pc):
    # centroid = np.mean(pc, axis=0)
    # pc = pc - centroid
    m = np.max(np.sqrt(np.sum(pc ** 2, axis=1)))
    pc = pc / m
    return pc


def corn_axis_transform(xyzl, scale=True, aug=False):
    """
    玉米坐标轴旋转，缩放
    Args:
        xyzl:
        scale:
        aug: 是否随机平移茎的位置

    Returns:

    """

    def PCA(data, sort=True):
        """
        计算 主成分
        :param data:
        :param sort:
        :return:
        """
        # m,n = data.shape
        data_normal = data - np.mean(data, axis=0)
        H = data_normal.T @ data_normal
        eigenvectors, eigenvalues, eigenvectors_t = np.linalg.svd(H)  # H = U S V
        if sort:
            sort = eigenvalues.argsort()[::-1]
            eigenvalues = eigenvalues[sort]
            eigenvectors = eigenvectors[:, sort]

        v1 = eigenvectors[:, 0]
        v2 = eigenvectors[:, 1]
        v3 = eigenvectors[:, 2]
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
        v1, v2, v3 = PCA(stem_points)
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

    def concatenate_corn_data(transpose_corn_data):
        """
        将分开的玉米点云合并为一个
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

    def cal_leaf_sheath(hole_corn_cloud, hole_corn_label):
        """
        计算叶鞘
        :param hole_corn_cloud:
        :param hole_corn_label:
        :return:
        """
        size = int(hole_corn_label.max())
        stem_mask = np.where(hole_corn_label == 0)
        stem_points = hole_corn_cloud[stem_mask]
        leaf_sheath_point_list = []
        for i in range(1, size + 1):
            leaf_mask = np.where(hole_corn_label == i)
            leaf_points = hole_corn_cloud[leaf_mask]
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

    def random_move_leaf(hole_corn_cloud, hole_corn_label):
        """
        在茎上添加自由度：叶鞘沿茎随机上下平移
        Args:
            hole_corn_cloud:
            hole_corn_label:

        Returns:

        """
        leaf_num = hole_corn_label.max()
        stem_xyz_index = np.where(hole_corn_label == 0)
        stem_xyz = hole_corn_cloud[stem_xyz_index]
        stem_max = stem_xyz.max()
        stem_min = stem_xyz.min()

        def generate_random_length():
            """
            随机生成茎平移的距离
            Returns:
            """
            random_size = stem_max / leaf_num * 2
            random_list = []
            for i in range(leaf_num):
                random_dist = np.random.uniform(0, random_size) * np.random.choice([1, -1])
                random_list.append(np.array([0, 0, 1]) * random_dist)

            return np.array(random_list)

        # 叶鞘顶点
        leaf_sheath_points = cal_leaf_sheath(hole_corn_cloud, hole_corn_label)

        ran_leaf_list = [stem_xyz]
        # 随机平移的距离
        ran_arr = generate_random_length()
        for i in range(1, leaf_num + 1):
            ran_move_dist = ran_arr[i - 1][-1]
            leaf_sheath_dist = leaf_sheath_points[i - 1][-1]

            leaf_xyz_index = np.where(hole_corn_label == i)
            leaf_xyz = hole_corn_cloud[leaf_xyz_index]
            if not (leaf_sheath_dist + ran_move_dist > stem_max or leaf_sheath_dist + ran_move_dist < stem_min):
                leaf_xyz += ran_arr[i - 1]
            ran_leaf_list.append(leaf_xyz)

        random_hole_corn_cloud, random_hole_corn_label = concatenate_corn_data(ran_leaf_list)
        # print(random_move_points)
        return random_hole_corn_cloud, random_hole_corn_label

    if scale:
        # 缩放
        point_set = xyzl[:, :3]
        point_label = xyzl[:, -1]
        point_set_normalized = pc_scale(point_set)
        corn_xyzl = np.concatenate([point_set_normalized, point_label.reshape(-1, 1)], axis=1)
    else:
        corn_xyzl = xyzl

    # 旋转坐标系
    leaf_num = int(corn_xyzl[:, -1].max())
    corn_data = [[] for _ in range(leaf_num + 1)]
    for item in corn_xyzl:
        # print(item)
        corn_data[int(item[-1])].append(item[0:3])
    np_corn_data = [np.array([]) for _ in range(leaf_num + 1)]
    for index, item in enumerate(corn_data):
        np_corn_data[index] = np.ascontiguousarray(corn_data[index])

    transpose_corn_data = move_rotate_points_cloud(np_corn_data)
    hole_corn_cloud, hole_corn_label = concatenate_corn_data(transpose_corn_data)

    if aug:
        hole_corn_cloud, hole_corn_label = random_move_leaf(hole_corn_cloud, hole_corn_label)

    hole_corn_xyzl = np.concatenate([hole_corn_cloud, hole_corn_label.reshape(-1, 1)], axis=1)

    np.random.shuffle(hole_corn_xyzl)
    #
    # # 点云可视化
    # COLORS = [[0.64705882, 0.81568627, 0.41960784], [0.84313725, 0.14509804, 0.41568627],
    #           [0.18039216, 0.21960784, 0.37254902], [0.76078431, 0.61176471, 0.58823529],
    #           [0.91764706, 0.61176471, 0.90196078], [0.65490196, 0.49803922, 0.14901961],
    #           [0.79607843, 0.15686275, 0.39215686], [0.33333333, 0.45490196, 0.38431373],
    #           [0.22352941, 0.39607843, 0.1372549], [0.48235294, 0.61568627, 0.17254902],
    #           [0.70980392, 0.3254902, 0.43137255], [0.69019608, 0.19215686, 0.51764706],
    #           [0.60392157, 0.00392157, 0.67058824]]
    #
    #
    # corn_item_cloud = o3d.geometry.PointCloud()
    # corn_item_cloud.points = o3d.utility.Vector3dVector(hole_corn_cloud)
    # corn_item_cloud.paint_uniform_color([0.7, 0.7, 0.7])
    # points_i = hole_corn_label.astype(int)
    # points_rgb = []
    # for i in points_i:
    #     points_rgb.append(COLORS[i])
    # points_rgb = np.array(points_rgb)
    # corn_item_cloud.colors = o3d.utility.Vector3dVector(points_rgb)
    #
    # corn_item_cloud1 = o3d.geometry.PointCloud()
    # corn_item_cloud1.points = o3d.utility.Vector3dVector(hole_corn_cloud1)
    # corn_item_cloud1.paint_uniform_color([0.7, 0.7, 0.7])
    # points_i1 = hole_corn_label1.astype(int)
    # points_rgb = []
    # for i in points_i1:
    #     points_rgb.append(COLORS[12-i])
    # points_rgb = np.array(points_rgb)
    # corn_item_cloud1.colors = o3d.utility.Vector3dVector(points_rgb)
    #
    # mesh_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.01, origin=[0, 0, 0])
    # o3d.visualization.draw_geometries([corn_item_cloud, corn_item_cloud1, mesh_frame])

    return hole_corn_xyzl


def restore_one_point_cloud(deformed_vertices_root, voxel_inner_points_root, point_root, txt_name, aug=False, scale=1, rgb=False,
                            semantic=False, queue=None):
    """
    从 变形后的顶点中恢复点云
    :param deformed_vertices_root:
    :param voxel_inner_points_root:
    :param point_root:
    :param txt_name:
    :param aug: 将叶子在茎上平移
    :param rgb:
    :param semantic:
    :param queue:
    :return:
    """

    # 还原 体素内点的坐标 及 标签
    deformed_points_labels = cal_voxel_inner_points_labels(deformed_vertices_root, voxel_inner_points_root, txt_name, rgb=rgb, semantic=semantic)

    # if aug:
    #     # 对茎进行上下平移
    #     deformed_points_labels = corn_axis_transform(deformed_points_labels, scale=True, aug=aug)

    if deformed_points_labels is not None:
        # # 只显示茎
        # stem_label_index = np.where(deformed_points_labels[:, 3] == 0)[0]
        # deformed_points_labels = deformed_points_labels[stem_label_index]
        # 保存点云
        point_name = os.path.basename(txt_name) + '.txt'
        points_filepath = os.path.join(point_root, point_name)
        save_points(points_filepath, deformed_points_labels)
        # point_name2 = os.path.basename(txt_name) + '_old.txt'
        # points_filepath2 = os.path.join(point_root, point_name2)
        # save_points(points_filepath2, old_deformed_points)

    if queue is not None:
        queue.put(txt_name)


def one_process(deformed_vertices_root, voxel_inner_points_root, point_root, aug=False, leaf_num=None, rgb=False,
                semantic=False):
    """
    单线程处理
    Args:
        deformed_vertices_root:
        voxel_inner_points_root:
        point_root:
        aug:
        leaf_num:
        rgb:
        semantic:

    Returns:

    """

    allNum = 0
    for one_class_items in os.listdir(deformed_vertices_root):
        one_class_path = os.path.join(deformed_vertices_root, one_class_items)
        if not os.path.isdir(one_class_path):
            continue
        for one_vertices in os.listdir(one_class_path):
            if one_vertices[-12:-4] == "vertices":
                txt_name = one_vertices[:-13]
                if leaf_num is not None:
                    one_leaf_num = int(txt_name.split('-')[1])
                    if one_leaf_num not in leaf_num:
                        continue
                print(txt_name)
                restore_one_point_cloud(one_class_path, voxel_inner_points_root, point_root, txt_name, aug=aug, rgb=rgb,semantic=semantic, queue=None)
                allNum += 1


def corn_axis_transform(xyzl):
    """
    玉米坐标轴旋转，缩放
    Args:
        xyzl:
    Returns:

    """

    def PCA(data, sort=True):
        """
        计算 主成分
        :param data:
        :param sort:
        :return:
        """
        # m,n = data.shape
        data_normal = data - np.mean(data, axis=0)
        H = data_normal.T @ data_normal
        eigenvectors, eigenvalues, eigenvectors_t = np.linalg.svd(H)  # H = U S V
        if sort:
            sort = eigenvalues.argsort()[::-1]
            eigenvalues = eigenvalues[sort]
            eigenvectors = eigenvectors[:, sort]

        v1 = eigenvectors[:, 0]
        v2 = eigenvectors[:, 1]
        v3 = eigenvectors[:, 2]
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
        v1, v2, v3 = PCA(stem_points)
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

    def concatenate_corn_data(transpose_corn_data):
        """
        将分开的玉米点云合并为一个
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

    # 旋转坐标系
    leaf_num = int(xyzl[:, -1].max())
    corn_data = [[] for _ in range(leaf_num + 1)]
    for item in xyzl:
        # print(item)
        corn_data[int(item[-1])].append(item[0:3])
    np_corn_data = [np.array([]) for _ in range(leaf_num + 1)]
    for index, item in enumerate(corn_data):
        np_corn_data[index] = np.ascontiguousarray(corn_data[index])

    transpose_corn_data = move_rotate_points_cloud(np_corn_data)
    hole_corn_cloud, hole_corn_label = concatenate_corn_data(transpose_corn_data)

    hole_corn_xyzl = np.concatenate([hole_corn_cloud, hole_corn_label.reshape(-1, 1)], axis=1)

    np.random.shuffle(hole_corn_xyzl)

    return hole_corn_xyzl


def dbscan_cluster(pcd):
    """
    dbscan 聚类分割
    :param pcd:
    :return:
    """
    # -------------------密度聚类 - -------------------------
    labels = np.array(pcd.cluster_dbscan(eps=0.02,  # 邻域距离
                                         min_points=10,  # 最小点数
                                         print_progress=False))  # 是否在控制台中可视化进度条
    # ---------------------保存聚类结果------------------------
    if len(labels) > 0 and labels.max() > 1:
        clusters_idx = []
        clusters_idx_len = []
        for i in range(labels.max() + 1):
            ind = np.where(labels == i)[0]
            clusters_idx.append(ind)
            clusters_idx_len.append(len(ind))
        max_count_index = np.argmax(clusters_idx_len)
        selected_index = clusters_idx[max_count_index]
        clusters_cloud = pcd.select_by_index(selected_index)
        return clusters_cloud, selected_index
    else:
        return pcd, np.arange(len(pcd.points))


def compute_one_normal(corn_xyzl, max_nn=10):
    corn_xyz = corn_xyzl[:, 0:3]
    corn_l = np.array(corn_xyzl[:, 3:]).reshape(-1, 1)
    corn_cloud = o3d.geometry.PointCloud()
    corn_cloud.points = o3d.utility.Vector3dVector(corn_xyz)
    # 计算法线，搜索半径1cm，只考虑邻域内的30个点
    corn_cloud.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamKNN(knn=max_nn))
    normal = np.asarray(corn_cloud.normals)
    corn_xyz_normal_l = np.concatenate((corn_xyz, normal, corn_l), axis=1)
    del corn_cloud
    return corn_xyz_normal_l


def clear_pcd(src_dir, target_dir, name, outlier_th=100, outlier_e=1, remove_outlier=True, transform_axis=True,
              normal=False):
    filepath = os.path.join(src_dir, name)
    corn_data = np.loadtxt(filepath)
    leaf_num = int(np.max(corn_data[:, -1]))
    corn_list = []
    corn_np = None
    # 区域生长分割
    if remove_outlier:
        for i in range(leaf_num + 1):
            point_index = np.where(i == corn_data[:-1])[0]
            i_corn_data = corn_data[point_index]
            pcd = o3d.geometry.PointCloud()
            pcd.points = o3d.utility.Vector3dVector(i_corn_data[:, :3])
            res = pcd.remove_statistical_outlier(outlier_th, outlier_e)  # 目标点周围的邻居数, 标准偏差比率
            # 欧式聚类
            pcd1 = res[0]
            # DBSCAN 聚类
            pcd2, indexc = dbscan_cluster(pcd1)
            points_r = np.asarray(pcd2.points)
            # label = np.ones(points_r.shape[0]) * i
            point_xyzl = np.concatenate([points_r, i_corn_data[:, 3:][res[1]][indexc]], axis=1)
            corn_list.append(point_xyzl)
            del pcd, pcd1, pcd2

            # if i == 0:
            #     大于茎长（z）1/10的不处理，只处理下面的，然后拼接
            #     z_max = np.max(points[:, 2])
            #     bottom_mask = points[:, 2] < z_max/10
            #     bottom_points = points[bottom_mask]
            #     top_points = points[~bottom_mask]
            #     pcd = o3d.geometry.PointCloud()
            #     pcd.points = o3d.utility.Vector3dVector(bottom_points[:, :3])
            #     res = pcd.remove_statistical_outlier(100, 1)  # 目标点周围的邻居数, 标准偏差比率
            #     # 欧式聚类
            #     pcd1 = res[0]
            #     # DBSCAN 聚类
            #     pcd2 = dbscan_cluster(pcd1)
            #     points_b_r = np.asarray(pcd2.points)
            #
            #     pcd3 = o3d.geometry.PointCloud()
            #     pcd3.points = o3d.utility.Vector3dVector(top_points[:, :3])
            #     res3 = pcd3.remove_statistical_outlier(10, 1)  # 目标点周围的邻居数, 标准偏差比率
            #     # 欧式聚类
            #     top_points_r = np.asarray(res3[0].points)
            #
            #     points_r = np.r_[top_points_r, points_b_r]
            #     label = np.ones(points_r.shape[0]) * i
            #     point_xyzl = np.concatenate([points_r, label.reshape(-1, 1)], axis=1)
            #     corn_list.append(point_xyzl)
            #     del pcd, pcd1, pcd2, pcd3
            # else:
            #     z_min = np.min(points[:, 2])
            #     z_max = np.max(points[:, 2])
            #     z_bottom = z_min + (z_max - z_min) / 10
            #     bottom_mask = points[:, 2] < z_bottom
            #     bottom_points = points[bottom_mask]
            #     top_points = points[~bottom_mask]
            #     pcd = o3d.geometry.PointCloud()
            #     pcd.points = o3d.utility.Vector3dVector(bottom_points[:, :3])
            #     res = pcd.remove_statistical_outlier(100, 1)  # 目标点周围的邻居数, 标准偏差比率
            #     # 欧式聚类
            #     pcd1 = res[0]
            #     # DBSCAN 聚类
            #     pcd2 = dbscan_cluster(pcd1)
            #     points_b_r = np.asarray(pcd2.points)
            #
            #     pcd3 = o3d.geometry.PointCloud()
            #     pcd3.points = o3d.utility.Vector3dVector(top_points[:, :3])
            #     res3 = pcd3.remove_statistical_outlier(10, 1)  # 目标点周围的邻居数, 标准偏差比率
            #     # 欧式聚类
            #     top_points_r = np.asarray(res3[0].points)
            #
            #     points_r = np.r_[top_points_r, points_b_r]
            #     label = np.ones(points_r.shape[0]) * i
            #     point_xyzl = np.concatenate([points_r, label.reshape(-1, 1)], axis=1)
            #     corn_list.append(point_xyzl)
            #     del pcd, pcd1, pcd2
        corn_np = np.concatenate(corn_list, axis=0)
        np.random.shuffle(corn_np)
        # corn_np = np.array(corn_list[0])
    if corn_np is None:
        corn_np = corn_data

    if len(corn_np) < len(corn_data) * 0.6 or len(corn_np) < 4096:
        print("error:  ", name)
        return
    if transform_axis:
        corn_np = corn_axis_transform(corn_np)
    if normal:
        corn_np = compute_one_normal(corn_np)
    target_filepath = os.path.join(target_dir, name)
    np.savetxt(target_filepath, corn_np, fmt="%.6f")


def data_precess(src_dir, target_dir, remove_outlier=True, transform_axis=True, normal=True):
    """
    去除离群点
    :param src_dir:
    :param target_dir:
    :param remove_outlier: 是否去除离群点
    :param sample: 是否将采样
    :param transform_axis: 是否统一坐标系
    :param normal: 是否法向量
    :return:
    """
    source_list = os.listdir(src_dir)
    total = len(source_list)
    for ii, name in enumerate(source_list):
        try:
            filepath = os.path.join(src_dir, name)
            corn_data = np.loadtxt(filepath)
            leaf_num = int(np.max(corn_data[:, -1]))
            corn_list = []
            corn_np = None
            # 区域生长分割
            if remove_outlier:
                for i in range(leaf_num + 1):
                    point_index = np.where(i == corn_data[:-1])[0]
                    points = corn_data[point_index]
                    pcd = o3d.geometry.PointCloud()
                    pcd.points = o3d.utility.Vector3dVector(points[:, :3])
                    res = pcd.remove_statistical_outlier(100, 1)  # 目标点周围的邻居数, 标准偏差比率
                    # 欧式聚类
                    pcd1 = res[0]
                    # DBSCAN 聚类
                    pcd2 = dbscan_cluster(pcd1)
                    points_r = np.asarray(pcd2.points)
                    label = np.ones(points_r.shape[0]) * i
                    point_xyzl = np.concatenate([points_r, label.reshape(-1, 1)], axis=1)
                    corn_list.append(point_xyzl)
                    del pcd, pcd1, pcd2
                corn_np = np.concatenate(corn_list, axis=0)
                np.random.shuffle(corn_np)
                # corn_np = np.array(corn_list[0])
            if corn_np is None:
                corn_np = corn_data
            # if len(corn_np) < len(corn_data) * 0.6 or len(corn_np) < 4096:
            #     print("error:  ", name)
            #     continue
            if transform_axis:
                corn_np = corn_axis_transform(corn_np)
            if normal:
                corn_np = compute_one_normal(corn_np)
            target_filepath = os.path.join(target_dir, name)
            np.savetxt(target_filepath, corn_np, fmt="%.6f")
            copyRate = ii / total
            print("目前进度是 :  %.2f%%" % (copyRate * 100), "filename：", name)
        except:
            print("error:  ", name)


def main01():
    data_root = '/home/yangxin/datasets/3d_corn/deformation'
    deformed_vertices_root = os.path.join(data_root, 'txt/generate_data_leaf_num_v1_20230402')
    voxel_inner_points_root = os.path.join(data_root, 'veg/leaf_num_v1')
    point_root = os.path.join(data_root, 'txt/data_src_leaf_num_v1_20230402')
    outlier_root = os.path.join(data_root, 'txt/data')
    mkdir_or_exist(point_root)
    mkdir_or_exist(outlier_root)

    leaf_num = [4]
    one_process(deformed_vertices_root, voxel_inner_points_root, point_root, aug=False, leaf_num=None)

    print("============================ 离群点去除 =================================")
    # 离群点去除、将采样
    data_precess(point_root, outlier_root, remove_outlier=True, transform_axis=True)


if __name__ == "__main__":
    main01()
