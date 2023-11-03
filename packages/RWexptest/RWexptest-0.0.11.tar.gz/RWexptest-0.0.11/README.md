# RWexptest

This is a simple example package.

## Pseqpa

这个工具包是用于对蛋白质序列进行简单处理的工作，其中涉及的主要函数功能有：

### excel_csv_to_fasta

```python
from RWexptest import Pseqpa

# 指定输入和输出文件夹路径
input_folder = "<需要转换的目标文件的路径>"
output_folder = "<保存路径>"
entry_column_name = "Entry"  # 请替换为您的entry列的名称
sequence_column_name = "Sequence"  # 请替换为您的sequence列的名称

# 调用函数并传递输入和输出文件夹路径
excel_csv_to_fasta(input_folder, output_folder, entry_column_name, sequence_column_name)
```

### process_fasta_files

```python
from RWexptest import Pseqpa

# 指定输入目录、输出目录、批次大小以及最小和最大蛋白质序列长度
input_directory = "<fasta格式文件路径>"
output_directory = "<处理后的保存路径>"
batch_size = 500 #将fasta格式蛋白质序列按500个进行一次划分
min_sequence_length = 10 #筛选蛋白质序列最低不能小于10个氨基酸
max_sequence_length = 6000 #筛选蛋白质序列最高不能超过6000个氨基酸

# 处理fasta文件并将其分成批次，只保留符合长度条件的序列
process_fasta_files(input_directory, output_directory, batch_size, min_sequence_length, max_sequence_length)
```

### create_blast_database（需要你的终端环境已经配置好了NCBI Blast工具）

```python
from RWexptest import Pseqpa

# 指定构建数据库对象、数据库位置和数据库类型
input_fasta_path = "<your_train_data_path/train_data.fasta>" #路径不能有空格，路径必须是英文
output_db_path = "<Blast_database_path/Train_protein_seq_database>" #路径不能有空格，路径必须是英文
dbtype = "prot"  # 蛋白质数据库

# 构建数据库
result_message = create_blast_database(input_fasta_path, output_db_path, dbtype)
```

### run_blastp（需要你的终端环境已经配置好了NCBI Blast工具）

```python
from RWexptest import Pseqpa

# 指定balst对象、数据库、结果目录和结果格式
query_fasta_path = "<your_test_data_path/test_data.fasta>" #路径不能有空格，路径必须是英文
blast_db_path = "<Blast_database_path/Train_protein_seq_database>" #路径不能有空格，路径必须是英文
output_file_path = "<your_save_path/test_data_blast_results.xml>" #路径不能有空格，路径必须是英文
custom_outfmt = 5  # 自定义输出格式

#进行同源性blast
result_message = run_blastp(query_fasta_path, blast_db_path, output_file_path, custom_outfmt)
```

### execute_blast_workflow（需要你的终端环境已经配置好了NCBI Blast工具）

```python
from RWexptest import Pseqpa

# 指定相关路径
input_fasta_path = "<your_train_data_path/train_data.fasta>" #路径不能有空格，路径必须是英文
output_db_path = "<Blast_database_path/Train_protein_seq_database>" #路径不能有空格，路径必须是英文
query_fasta_path = "<your_test_data_path/test_data.fasta>" #路径不能有空格，路径必须是英文
custom_outfmt = 5 #路径不能有空格，路径必须是英文
dbtype = "prot" #或者
xml_result_path = "<your_save_path/test_data_blast_results.xml>"  # 自定义XML结果的保存位置，路径不能有空格，路径必须是英文

# 一次性完成数据库的创建和blast工作并获得xml文件
result = execute_blast_workflow(input_fasta_path, output_db_path, dbtype, query_fasta_path, custom_outfmt, xml_result_path)
```

### parse_blast_xml_to_excel

```python
import pandas as pd
from Bio import SearchIO
from RWexptest import Pseqpa

# 调用函数并传递输入XML文件和输出Excel文件的路径
input_xml = '<经过NCBI Blast处理后获得的xml文件路径/result.xml>' #路径不能有空格，路劲必须是英文
output_excel = '<保存路径/reuslt.xlsx>' #路径不能有空格，路劲必须是英文

parse_blast_xml_to_excel(input_xml, output_excel)
```

