# -*- coding: utf-8 -*-
"""
Created on Sat Oct  7 19:33:31 2023

@author: 22193
"""

import os
import pandas as pd
from Bio import SeqIO

def read_files_and_store(open_path):
    # 获取指定路径下的所有文件名
    file_names = os.listdir(open_path)

    # 创建一个空字典来存储数据
    data_dict = {}

    # 支持的文件扩展名
    supported_extensions = ['.xlsx', '.xls', '.csv', '.sql', '.txt', '.fasta']  # 添加FASTA格式

    # 逐个读取文件中的数据
    for file_name in file_names:
        file_path = os.path.join(open_path, file_name)
        
        # 检查文件扩展名是否在支持的列表中
        file_extension = os.path.splitext(file_name)[1].lower()
        
        if file_extension in supported_extensions:
            if file_extension == '.xlsx' or file_extension == '.xls':
                # 读取Excel文件
                df = pd.read_excel(file_path)
            elif file_extension == '.csv':
                # 读取CSV文件
                df = pd.read_csv(file_path)
            elif file_extension == '.sql':
                # 读取SQL数据库
                df = pd.read_sql(file_path)
            elif file_extension == '.txt':
                # 读取文本文件
                df = pd.read_csv(file_path, delimiter='\t')  # 假设是以制表符分隔的文本文件
            elif file_extension == '.fasta':
                # 读取FASTA文件
                sequences = list(SeqIO.parse(file_path, "fasta"))
                # 创建包含序列数据的数据帧
                df = pd.DataFrame({"ID": [seq.id for seq in sequences], "Sequence": [str(seq.seq) for seq in sequences]})
            
            # 将数据帧添加到字典中，以文件名为键
            data_dict[file_name] = df
    
    return data_dict

#=======================================================================================================================
# 调用函数，并传递打开路径作为参数
#open_path = r'D:\Working\Team\Luo_Zeyu\Sub_articles\BIB\Revision_processing\VAE_Feature_all_inference\3_dhomo_indpendent_test\data'
#result_data = read_files_and_store(open_path)
#=======================================================================================================================


import os

def list_files_and_folders(target_path):
    # 创建空列表来存储文件和文件夹的名称
    file_and_folder_names = []

    # 遍历目标路径下的所有文件和文件夹
    for root, dirs, files in os.walk(target_path):
        # 将文件夹添加到列表中
        for directory in dirs:
            file_and_folder_names.append(os.path.join(root, directory))
        
        # 将文件添加到列表中
        for file in files:
            file_and_folder_names.append(os.path.join(root, file))

    return file_and_folder_names

#=======================================================================================================================
# 调用函数，并传递目标路径作为参数
#target_path = r'D:\Working\Team\Luo_Zeyu\Sub_articles\BIB\Revision_processing\VAE_Feature_all_inference\3_dhomo_indpendent_test\data'
#result_list = list_files_and_folders(target_path)
#=======================================================================================================================

import importlib
import subprocess
import sys

def check_and_import(module_name, last_error_module=None):
    try:
        # 尝试导入模块
        imported_module = importlib.import_module(module_name)
        print(f"{module_name} 已成功导入。")
        return imported_module
    except OSError as e:
        if "cannot allocate memory in static TLS block" in str(e):
            print(f"OSError: {e}。这可能是由于共享库与系统或其他库存在冲突导致的。")
            print(f"请考虑重新排序导入{module_name}的顺序或者尝试其他解决方案。")
        else:
            print(f"你引入的包{module_name}发生了一个不可预见的OSError: {e}")
        return None
    except ImportError as e:
        missing_package = str(e).split("'")[-2]  # 更精确地获取缺失的包名

        # 判断是否需要停止递归
        if missing_package == last_error_module:
            print(
                f"该依赖包 {missing_package} 可能不存在，或者不符合本函数操作模式，请自行检查工具包 {missing_package} 的名称或下载方式，并自行下载。")
            return None

        # 特殊处理
        if missing_package == 'torch':
            print(
                f"Package torch is pytorch, please check your CUDA version and download the corresponding version of PyTorch accordingly.")
            return None
        if missing_package == 'sklearn':
            missing_package = 'scikit-learn'
        if missing_package == 'moxing':
            print(
                f"Moxing is designed for Huawei Cloud's ModelArts. Since your working environment does not support Moxing, " \
                "it is recommended to switch to using Huawei Cloud's ModelArts platform for related operations.")
            return None

        # 在终端中使用pip安装模块和缺失的依赖
        print(f"{missing_package} 不存在。尝试安装中...")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', missing_package,'-i https://pypi.tuna.tsinghua.edu.cn/simple'])
        except Exception as e:
            print(f"无法通过pip安装 {missing_package}：{e}")
            return None

        # 再次尝试导入模块
        return check_and_import(module_name, last_error_module=missing_package)