import os
import shutil

import numpy as np

from Deformation3D import prepare_vega_files, deform_models, get_models_pcd
# Deformation3D.hello()


config_filepath = "../configs/corn_vox.configs"
txt_filepath = "../demo/demo-7.txt"
vega_dir = "../demo/veg/"
out_dir = "../demo/txt/"
leaf_num = 7
new_num = 1
integrator_times = 20
stem_integrator_times = 10

min_base_force = np.array([
    [-8, -8, -40],  # stem
    [-400, -400, -400],  # leaf 1
    [-400, -400, -400],  # leaf 2
    [-400, -400, -400],  # leaf 3
    [-400, -400, -400],  # leaf 4
    [-400, -400, -400],  # leaf 5
    [-400, -400, -400],  # leaf 6
    [-400, -400, -400],  # leaf 7
    [-400, -400, -400],  # leaf 8
    [-400, -400, -400],  # leaf 9
])

max_base_force = np.array([
    [8, 8, -40],  # stem
    [400, 400, 400],  # leaf 1
    [400, 400, 400],  # leaf 2
    [400, 400, 400],  # leaf 3
    [400, 400, 400],  # leaf 4
    [400, 400, 400],  # leaf 5
    [400, 400, 400],  # leaf 6
    [400, 400, 400],  # leaf 7
    [400, 400, 400],  # leaf 8
    [400, 400, 400],  # leaf 9
])

TMP_DIR = 'tmp'
os.makedirs(TMP_DIR, exist_ok=True)

# 生成 vega文件 只用生成一次
prepare_vega_files(txt_filepath, vega_dir, leaf_num, voxel_size=0.02)

# 开始变形  （可以开启多线程）
deform_models(config_filepath, txt_filepath, vega_dir, out_dir, leaf_num, new_num,
              min_base_force, max_base_force, integrator_times=integrator_times,
              stem_integrator_times=stem_integrator_times)

# 从 obj 顶点文件种恢复 点云（可以开启多线程）
get_models_pcd(out_dir, vega_dir, transform_axis=True, normal=False)


if os.path.exists(TMP_DIR):
    shutil.rmtree(TMP_DIR)
    print(f"Folder '{TMP_DIR}' and its contents have been successfully deleted.")
else:
    print(f"Folder '{TMP_DIR}' does not exist.")