# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 17:27:14 2023

@author: 22193
"""
import os
import sys
import subprocess
from Bio.Blast import NCBIXML
from Bio.Blast.Applications import NcbimakeblastdbCommandline
from Bio.Blast.Applications import NcbiblastpCommandline
from Bio.Blast.Applications import NcbiblastnCommandline

def contains_space_or_chinese(text):
    # 检查文本中是否包含空格或中文字符
    if ' ' in text or any('\u4e00' <= char <= '\u9fff' for char in text):
        return True
    return False

def create_blast_database(input_fasta_path, output_db_path, dbtype):
    """
    创建BLAST数据库

    Parameters:
        input_fasta_path (str): 输入的FASTA文件路径。
        output_db_path (str): 输出数据库的路径。
        dbtype (str): 数据库类型，可以是'prot'（蛋白质）或'nucl'（核酸）。

    Returns:
        str: 执行结果消息，成功时返回成功消息，否则返回错误消息。
    """
    # 检查输入路径和输出路径是否包含空格或中文字符
    if contains_space_or_chinese(input_fasta_path) or contains_space_or_chinese(output_db_path):
        print("路径中不能包含空格或中文字符，请更正路径后重试。")
        sys.exit(1)  # 终止程序执行并返回错误代码 1

    try:
        # 创建makeblastdb命令行对象
        makeblastdb_cline = NcbimakeblastdbCommandline(
            input_file=input_fasta_path,
            dbtype=dbtype,
            out=output_db_path
        )

        # 执行makeblastdb命令
        stdout, stderr = makeblastdb_cline()

        # 检查执行结果
        if stderr:
            print(f"An error occurred: {stderr}")
            sys.exit(1)  # 终止程序执行并返回错误代码 1
        
        else:
            print("BLAST database created successfully.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)  # 终止程序执行并返回错误代码 1

# 示例用法
# =============================================================================
# input_fasta_path = "<your_train_data_path/train_data.fasta>"
# output_db_path = "<Blast_database_path/Train_protein_seq_database>"
# dbtype = "prot"  # 蛋白质数据库
# 
# result_message = create_blast_database(input_fasta_path, output_db_path, dbtype)
# =============================================================================

def run_blastn(query_fasta_path, blast_db_path, output_file_path, custom_outfmt):
    """
    执行blastn搜索并保存结果为指定格式的文件

    Parameters:
        query_fasta_path (str): 查询的FASTA文件路径。
        blast_db_path (str): BLAST核酸数据库的路径。
        output_file_path (str): 结果保存的文件路径。
        custom_outfmt (str): 自定义输出格式字符串。

    Returns:
        str: 执行结果消息，成功时返回成功消息，否则返回错误消息。
    """
    # 检查查询文件路径、数据库路径和输出文件路径是否包含不允许的字符
    if contains_space_or_chinese(query_fasta_path) or contains_space_or_chinese(blast_db_path) or contains_space_or_chinese(output_file_path):
        print("路径中不能包含空格或中文字符，请更正路径后重试。")
        sys.exit(1)  # 终止程序执行并返回错误代码 1
    
    try:
        # 创建blastn命令行对象
        blastn_cline = NcbiblastnCommandline(
            query=query_fasta_path,
            db=blast_db_path,
            out=output_file_path,
            outfmt=custom_outfmt  # 设置自定义输出格式
        )

        # 执行blastn搜索
        stdout, stderr = blastn_cline()

        # 检查执行结果
        if stderr:
            print(f"An error occurred: {stderr}")
            sys.exit(1)  # 终止程序执行并返回错误代码 1
        else:
            print("BLAST analysis completed successfully.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)  # 终止程序执行并返回错误代码 1


def run_blastp(query_fasta_path, blast_db_path, output_file_path, custom_outfmt):
    """
    执行blastp搜索并保存结果为指定格式的文件

    Parameters:
        query_fasta_path (str): 查询的FASTA文件路径。
        blast_db_path (str): BLAST数据库的路径。
        output_file_path (str): 结果保存的文件路径。
        custom_outfmt (str): 自定义输出格式字符串。

    Returns:
        str: 执行结果消息，成功时返回成功消息，否则返回错误消息。
    """
    # 检查查询文件路径、数据库路径和输出文件路径是否包含不允许的字符
    if contains_space_or_chinese(query_fasta_path) or contains_space_or_chinese(blast_db_path) or contains_space_or_chinese(output_file_path):
        print("路径中不能包含空格或中文字符，请更正路径后重试。")
        sys.exit(1)  # 终止程序执行并返回错误代码 1
    
    try:
        # 创建blastp命令行对象
        blastp_cline = NcbiblastpCommandline(
            query=query_fasta_path,
            db=blast_db_path,
            out=output_file_path,
            outfmt=custom_outfmt  # 设置自定义输出格式
        )

        # 执行blastp搜索
        stdout, stderr = blastp_cline()

        # 检查执行结果
        if stderr:
            print(f"An error occurred: {stderr}")
            sys.exit(1)  # 终止程序执行并返回错误代码 1
        else:
            print("BLAST database created successfully.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)  # 终止程序执行并返回错误代码 1

# 示例用法
# =============================================================================
# query_fasta_path = "<your_test_data_path/test_data.fasta>"
# blast_db_path = "<Blast_database_path/Train_protein_seq_database>"
# output_file_path = "<your_save_path/test_data_blast_results.xml>"
# custom_outfmt = 5  # 自定义输出格式
# 
# result_message = run_blastp(query_fasta_path, blast_db_path, output_file_path, custom_outfmt)
# =============================================================================

import subprocess
import sys
from Bio.Blast import NCBIXML

# 之前的三个函数的代码...

def execute_blast_workflow(input_fasta_path, output_db_path, dbtype, query_fasta_path, custom_outfmt, xml_result_path):
    try:
        # 创建BLAST数据库
        create_result = create_blast_database(input_fasta_path, output_db_path, dbtype)
        if create_result.startswith("An error occurred"):
            return create_result  # 如果创建数据库失败，返回错误消息
        
        # 执行blastp搜索
        blastp_result = run_blastp(query_fasta_path, output_db_path, xml_result_path, custom_outfmt)
        if blastp_result.startswith("An error occurred"):
            return blastp_result  # 如果blastp搜索失败，返回错误消息

        return "BLAST search completed successfully."

    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == "__main__":
    input_fasta_path = "your_input.fasta"
    output_db_path = "your_output_db"
    query_fasta_path = "your_query.fasta"
    custom_outfmt = "your_custom_outfmt"
    xml_result_path = "your_custom_xml_result.xml"  # 自定义XML结果的保存位置
    
    result = execute_blast_workflow(input_fasta_path, output_db_path, query_fasta_path, custom_outfmt, xml_result_path)
    
    if result == "BLAST search completed successfully.":
        print(f"XML结果已保存到：{xml_result_path}")
    else:
        print(result)


