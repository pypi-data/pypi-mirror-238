# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 20:53:38 2023

@author: 22193
"""

#导入相关工具包
import numpy as np
import random


#创建二元函数
def Bivariate_quadratic_function(x):
     #result = np.zeros_like(x)
     x_index = x.shape[0]
     result = np.array([0 for _ in range(x_index)], np.float32)
     for i in range(x_index):
         xi = x[i]
         result[i] = (xi[0]**2 + xi[1]**2)
        
     #return np.sum(x**2, axis = 1) 
     return result


#创建梯度函数
def Gradient_function(f, x):
    h = 1e-4
    num_of_cols = x.shape[1]
    result = np.zeros_like(x, np.float32)
    
    for col in range(num_of_cols):
        x_col = x[:, col]
        
        # 创建 x 副本
        x_temp_1 = x.copy()
        x_temp_1[:, col] = x_col + h
        fxh1 = f(x_temp_1)
        
        x_temp_2 = x.copy()
        x_temp_2[:, col] = x_col - h
        fxh2 = f(x_temp_2)
        
        result[:, col] = (fxh1 - fxh2)/(2*h)
    
    return result


#定义梯度下降函数
def Gradient_descent(f, initx, lr=0.01, step_num=100):
    x = initx
    x_descent = initx.copy()
    
    for i in range(step_num):
        grad = Gradient_function(f, x_descent)
        x_descent -= lr*grad
    
    return x_descent
