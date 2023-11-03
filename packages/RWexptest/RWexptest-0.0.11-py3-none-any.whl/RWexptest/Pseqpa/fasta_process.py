# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 11:39:00 2023

@author: 22193
"""

import os

# 定义一个函数将序列批次保存为fasta文件
def save_fasta(sequences, output_file):
    with open(output_file, 'w') as file:
        for sequence_id, sequence in sequences.items():
            file.write(f">{sequence_id}\n")
            file.write(f"{sequence}\n")

# 定义一个函数读取fasta文件并将其分割成多个批次
def process_fasta_files(input_directory, output_directory, batch_size, min_length=10, max_length=6000):
    # 确保输出目录存在
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # 获取输入目录下的所有fasta文件
    fasta_files = [f for f in os.listdir(input_directory) if f.endswith('.fasta')]

    # 处理每个fasta文件
    for fasta_file in fasta_files:
        file_path = os.path.join(input_directory, fasta_file)
        sequences = read_fasta(file_path, min_length, max_length)

        # 划分成批次
        sequence_batches = []
        current_batch = {}
        count = 0

        for sequence_id, sequence in sequences.items():
            current_batch[sequence_id] = sequence
            count += 1
            if count == batch_size:
                sequence_batches.append(current_batch.copy())
                current_batch.clear()
                count = 0

        # 处理可能剩余的序列
        if current_batch:
            sequence_batches.append(current_batch)

        # 确定输出目录名（使用原始文件名的简写）
        output_folder_name = os.path.splitext(fasta_file)[0]  # 获取不带扩展名的原始文件名
        output_folder_path = os.path.join(output_directory, output_folder_name)

        # 创建文件夹
        os.makedirs(output_folder_path, exist_ok=True)

        # 保存每个批次为fasta文件
        for i, batch in enumerate(sequence_batches):
            output_file = os.path.join(output_folder_path, f"{fasta_file}_batch_{i+1}.fasta")
            save_fasta(batch, output_file)

# 定义一个函数来读取fasta文件并划分序列
def read_fasta(file_path, min_length, max_length=None):
    sequences = {}  # 创建一个字典来存储蛋白质序列
    current_sequence = ''  # 用于存储当前序列的变量
    current_id = ''  # 用于存储当前序列的ID的变量

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('>'):  # 如果是序列ID行
                if current_id and current_sequence:  # 如果已经有了序列ID和序列内容
                    # 检查序列长度是否在指定的范围内，或者 max_length 为 None（不限制最大长度）
                    if min_length <= len(current_sequence) and (max_length is None or len(current_sequence) <= max_length):
                        sequences[current_id] = current_sequence  # 将满足长度条件的序列存储到字典中
                current_id = line[1:]  # 获取新的序列ID（去掉开头的">"）
                current_sequence = ''  # 重置当前序列内容
            else:
                current_sequence += line  # 将行添加到当前序列内容中

    # 处理最后一个序列
    if current_id and current_sequence and min_length <= len(current_sequence) and (max_length is None or len(current_sequence) <= max_length):
        sequences[current_id] = current_sequence

    return sequences

# =============================================================================
# # 指定输入目录、输出目录、批次大小以及最小和最大蛋白质序列长度
# input_directory = "D:/Working/Team/Luo_Zeyu/投稿文章/BIB/改稿处理/2_deeploc2.0亚细胞定位预测/1_fasta格式文件500序列分/data"
# output_directory = "D:/Working/Team/Luo_Zeyu/投稿文章/BIB/改稿处理/2_deeploc2.0亚细胞定位预测/1_fasta格式文件500序列分/output"
# batch_size = 500
# min_sequence_length = 10
# max_sequence_length = 6000
# 
# # 处理fasta文件并将其分成批次，只保留符合长度条件的序列
# process_fasta_files(input_directory, output_directory, batch_size, min_sequence_length, max_sequence_length)
# =============================================================================



