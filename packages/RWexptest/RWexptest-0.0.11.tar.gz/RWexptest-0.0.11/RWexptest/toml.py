# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 18:02:21 2023

@author: 22193
"""

# import toml

# with open('D:/packaging_tutorial/pyproject.toml', 'r') as f:
#     config = toml.load(f)

# config['test'] = 'localhost'
# config['title']='Toml 示例'
# config['cdf']="""
# sadwadsccada\
#     sadwdsavfdsdc\
#         cxdvadcxas\
#             xalijdlsnc\
#                 awlbslacbxalwdj\
#                     xalcnlabjblsawd\
#                         """
# config['str']="我是一个字符串。\"你可以把我引起来\"。姓名\tJos\u00E9\n位置\t旧金山。"
# config['sad']='她说:"这只是一个无意义的条款。"'
# config['table-1']={ "asdcx", "ascji", "sajlinc"}
# config['asdcx']=["sADACD"]
# config['sadafe'] =[ ['afhaie'],['alisnlf']]

# with open('D:/packaging_tutorial/pyproject.toml.toml', 'w') as f:
#     toml.dump(config, f)

# print(config['str'])

# import configparser

# config = configparser.ConfigParser()

# config["build-system"] = {"requires": '["setuptools>=61.0"]', "build-backend": "setuptools.build_meta"}

# with open("config.toml", "w") as f:
#     config.write(f)


import configparser

# 创建一个 ConfigParser 对象
config = configparser.ConfigParser()

# 设置值
config["build-system"] = {"requires": '["setuptools>=61.0"]', "build-backend": "setuptools.build_meta"}

config["project"] = {
    "name": "example_package_ RuiwangW",
    "version": "0.0.1",
    "description": "A small example package",
    "readme": "README.md",
    "requires-python": ">=3.7",
}
config["project.urls"] = {
    "Homepage": "https://github.com/pypa/sampleproject",
    "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
}
config["project.authors"] = {
    "name": "RuiwangW",
    "email": "2219312248@qq.com",
}

config["project.classifiers"] = {
    "Programming Language": "Python :: 3",
    "License": "OSI Approved :: MIT License",
    "Operating System": "OS Independent",
}

# 将配置写入到文件中
with open("D:/packaging_tutorial/pyproject.toml", "w") as f:
    config.write(f)

