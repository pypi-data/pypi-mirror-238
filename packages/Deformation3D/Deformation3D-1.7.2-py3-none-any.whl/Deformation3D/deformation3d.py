import os.path
import shutil
import sys, os
import numpy as np

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Deformation3D.generate_vox import generate_one
from Deformation3D.obj_2_points import restore_one_point_cloud, clear_pcd

import deform
import multiprocessing
from multiprocessing import Pool, Manager, set_start_method


def hello():
    print("hello")


def prepare_vega_files(txt_filepath, vega_dir, leaf_num, voxel_size=0.02, normal=True, rgb=False, semantic=False,
                       MATERIALS="\n*MATERIAL STEM\nENU, 1000, 100000, 0.01\n\n*MATERIAL LEAF\nENU, 1000, 10000000, 0.45\n"):
    """
    变形前文件准备
    :param txt_filepath: 点云文件路径： /home/xxx/datasets/pcd/1.txt
    :param vega_dir: 生成vega文件的目录:  /home/xxx/datasets/vega/
    :param voxel_size:
    :param normal:
    :param MATERIALS: 材质参数
    :return:
    """

    os.makedirs(vega_dir, exist_ok=True)
    txt_filepath_split = os.path.split(txt_filepath)
    data_root = txt_filepath_split[0]
    model_name = txt_filepath_split[1]
    generate_one(data_root, vega_dir, model_name, leaf_num, voxel_size=voxel_size, normal=normal, rgb=rgb,
                 semantic=semantic, MATERIALS=MATERIALS)


def deform_models(config_filepath, txt_filepath, vega_dir, out_dir, leaf_num, new_num,
                  min_base_force, max_base_force, integrator_times=15, stem_integrator_times=10, save_vega=False):
    """
    stem 底部
    :param config_filepath: 配置文件目录 configs/corn_vox.configs
    :param txt_filepath: 点云文件路径： /home/xxx/datasets/pcd/1.txt
    :param vega_dir: vega文件 /home/xxx/datasets/vega/
    :param out_dir: 生成 element vertices 的目录： /home/xxx/datasets/new_models_tmp/
    :param leaf_num: 叶子数量
    :param new_num: 生成新模型的数量
    :param min_base_force:  每个叶子上力的最小值
    :param max_base_force: 茎中间施加力的最小值
    :param integrator_times:  积分次数
    :param stem_integrator_times:  茎积分次数
    :param save_vega:  是否保存 vega 文件
    :return:
    """
    out_obj_dir = os.path.join(out_dir, "obj/")
    os.makedirs(out_obj_dir, exist_ok=True)
    model_name = os.path.split(txt_filepath)[1][:-4]
    deform.deform_run(config_filepath, vega_dir, out_obj_dir, model_name, leaf_num, new_num,
                      integrator_times, stem_integrator_times, min_base_force, max_base_force, save_vega)


def deform_models2(config_filepath, txt_filepath, vega_dir, out_dir, leaf_num, new_num, min_base_force, max_base_force,
                   integrator_times=15, stem_integrator_times=10, save_vega=False):
    """
    stem 中间
    :param config_filepath: 配置文件目录 configs/corn_vox.configs
    :param txt_filepath: 点云文件路径： /home/xxx/datasets/pcd/1.txt
    :param vega_dir: vega文件 /home/xxx/datasets/vega/
    :param out_dir: 生成 element vertices 的目录： /home/xxx/datasets/new_models_tmp/
    :param leaf_num: 叶子数量
    :param new_num: 生成新模型的数量
    :param min_base_force:  每个叶子上力的最小值
    :param max_base_force: 茎中间施加力的最小值
    :param integrator_times:  积分次数
    :param stem_integrator_times:  茎积分次数
    :param save_vega:  是否保存 vega 文件
    :return:
    """
    out_obj_dir = os.path.join(out_dir, "obj/")
    os.makedirs(out_obj_dir, exist_ok=True)
    model_name = os.path.split(txt_filepath)[1][:-4]
    deform.deform_run2(config_filepath, vega_dir, out_obj_dir, model_name, leaf_num, new_num, integrator_times,
                       stem_integrator_times, min_base_force, max_base_force, save_vega)


def remove_dir(dir):
    if not os.listdir(dir):
        try:
            # 使用 os.rmdir() 删除空文件夹
            os.rmdir(dir)
            print(f"空文件夹 {dir} 已成功删除。")
        except OSError as e:
            print(f"删除文件夹 {dir} 时出现错误：{e}")


def get_models_pcd(out_dir, vega_dir, outlier_th=100, outlier_e=1, remove_outlier=True, transform_axis=True,
                   normal=False, rgb=False, semantic=False, post_process=True):
    """
    从模型中恢复点云数据
    :param out_dir:
    :param vega_dir: vega文件 /home/xxx/datasets/vega/
    :param outlier_th: 去除噪点 阈值
    :param outlier_e: 去除噪点 阈值
    :param remove_outlier: 去除噪点
    :param transform_axis:
    :param normal:
    :param semantic:
    :param rgb:
    :return:
    """
    out_obj_dir = os.path.join(out_dir, "obj")
    out_src_dir = os.path.join(out_dir, "src")
    out_data_dir = os.path.join(out_dir, "data")
    os.makedirs(out_src_dir, exist_ok=True)
    os.makedirs(out_data_dir, exist_ok=True)

    for one_item in os.listdir(out_obj_dir):
        item_obj_dir = os.path.join(out_obj_dir, one_item)
        if not os.path.isdir(item_obj_dir):
            continue
        for one_vertices in os.listdir(item_obj_dir):
            if one_vertices[-12:-4] == "vertices":
                txt_name = one_vertices[:-13]
                try:
                    # 恢复点云数据
                    restore_one_point_cloud(item_obj_dir, vega_dir, out_src_dir, txt_name, rgb=rgb, semantic=semantic)
                    # 删除 vertices、elements
                    os.remove(os.path.join(item_obj_dir, f"{txt_name}_vertices.txt"))
                    os.remove(os.path.join(item_obj_dir, f"{txt_name}_elements.txt"))
                    # 去除异常数据
                    if post_process:
                        clear_pcd(out_src_dir, out_data_dir, f"{txt_name}.txt", outlier_th=outlier_th,
                                  outlier_e=outlier_e,
                                  remove_outlier=remove_outlier, transform_axis=transform_axis, normal=normal)
                        os.remove(os.path.join(out_src_dir, f"{txt_name}.txt"))
                except FileNotFoundError:
                    print("文件不存在，无法删除。")
                except OSError as e:
                    print(f"删除文件时出现错误：{e}")
                except:
                    print("其他错误")

        # 删除文件夹
        # remove_dir(item_obj_dir)
    if post_process:
        shutil.rmtree(out_src_dir)
    shutil.rmtree(out_obj_dir)


def deform_demo(
        new_num=10, integrator_times=15, leaf_num=7,
        min_base_force=np.array([
            [-40, -40, -10],  # stem
            [-100, -20, -150],  # leaf 1
            [-100, -20, -150],  # leaf 2
            [-100, -20, -150],  # leaf 3
            [-100, -20, -150],  # leaf 4
            [-100, -20, -150],  # leaf 5
            [-100, -20, -150],  # leaf 6
            [-100, -20, -150],  # leaf 7
            [-100, -20, -150],  # leaf 8
            [-100, -20, -150],  # leaf 9
            [-100, -20, -150],  # leaf 10
            [-100, -20, -150],  # leaf 11
            [-100, -20, -150],  # leaf 12
        ]),
        max_base_force=np.array([
            [40, 40, -5],  # stem
            [100, 20, 150],  # leaf 1
            [100, 20, 150],  # leaf 2
            [100, 20, 150],  # leaf 3
            [100, 20, 150],  # leaf 4
            [100, 20, 150],  # leaf 5
            [100, 20, 150],  # leaf 6
            [100, 20, 150],  # leaf 7
            [100, 20, 150],  # leaf 8
            [100, 20, 150],  # leaf 9
            [100, 20, 150],  # leaf 10
            [100, 20, 150],  # leaf 11
            [100, 20, 150],  # leaf 12
        ]),
        config_filepath="./corn_vox.configs", txt_path="./demo-7.txt", vega_dir="./deformed_models/vega/",
        out_dir="./deformed_models/data/"):
    # 生成 vega文件 只用生成一次
    prepare_vega_files(txt_path, vega_dir, leaf_num, voxel_size=0.02)

    # 开始变形  （可以开启多线程，自己编写）
    deform_models(config_filepath, txt_path, vega_dir, out_dir, leaf_num, new_num,
                  min_base_force, max_base_force, integrator_times=integrator_times)

    # 从 obj 顶点文件种恢复 点云（可以开启多线程）
    get_models_pcd(out_dir, vega_dir, transform_axis=True, normal=False)
    # multi_get_models_pcd(out_dir, vega_dir, transform_axis=True, normal=False)
