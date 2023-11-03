# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 11:46:34 2023

@author: 22193
"""

import pandas as pd
from Bio import SearchIO

def parse_blast_xml_to_excel(input_xml, output_excel):
    # 初始化一个空的DataFrame
    columns = ['Query_ID', 'Hit_ID', 'HSP_E-value', 'HSP_Bitscore', 'HSP_Identical_sites', 'HSP_Positives']
    df = pd.DataFrame(columns=columns)

    # 解析BLAST XML文件
    blast_qresults = list(SearchIO.parse(input_xml, "blast-xml"))

    # 遍历所有查询结果（QueryResult）
    for qresult in blast_qresults:
        query_id = qresult.id

        # 遍历所有命中结果（Hit）
        for hit in qresult:
            hit_id = hit.id

            # 遍历每个命中结果的具体信息（HSP）
            for hsp in hit.hsps:
                hsp_evalue = hsp.evalue
                hsp_bitscore = hsp.bitscore
                hsp_ident_num = hsp.ident_num
                hsp_pos_num = hsp.pos_num

                # 将这些信息添加到DataFrame中
                new_row = {
                    'Query_ID': query_id,
                    'Hit_ID': hit_id,
                    'HSP_E-value': hsp_evalue,
                    'HSP_Bitscore': hsp_bitscore,
                    'HSP_Identical_sites': hsp_ident_num,
                    'HSP_Positives': hsp_pos_num
                }
                df = df.append(new_row, ignore_index=True)

    # 保存DataFrame到Excel文件
    df.to_excel(output_excel, index=False)

# =============================================================================
# # 调用函数并传递输入XML文件和输出Excel文件的路径
# input_xml = 'D:/Working/Team/Luo_Zeyu/投稿文章/BIB/改稿处理/2_独立测试集同源性划分/output/2_blast获取xml文件/blast_independent_test_results.xml'
# output_excel = 'D:/Working/Team/Luo_Zeyu/投稿文章/BIB/改稿处理/2_独立测试集同源性划分/output/3_xml读取/blast_independent_test_results.xlsx'
# 
# parse_blast_xml_to_excel(input_xml, output_excel)
# =============================================================================


























