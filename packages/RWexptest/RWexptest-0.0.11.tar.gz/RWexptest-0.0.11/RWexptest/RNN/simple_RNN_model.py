# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 16:03:50 2023

@author: 22193
"""

import numpy as np

#--RNN层--
class SimpleRNNLayer:
    def __init__(self, n_upper, n):
        #参数的初始值
        #Xavier的初始值
        self.w = np.random.randn(n_upper, n)/np.sqrt(n_upper)
        #Xavier的初始值
        self.v = np.random.randn(n, n)/np.sqrt(n)
        self.b = np.zeros(n)
        
    def forward(self, x, y_prev):     #y_prev:前一时刻的输出
        u = np.dot(x, self.w) + np.dot(y_prev, self.v) + self.b
        self.y = np.tanh(u)     #输出
        
    def backward(self, x, y, y_prev, grad_y):
        delta = grad_y * (1 - y**2)
        
        #各个梯度
        self.grad_w += np.dot(x.T, delta)
        self.grad_v += np.dot(y_prev.T, delta)
        self.grad_b += np.sum(delta, axis=0)
        
        self.grad_x += np.dot(delta, self.w.T)
        self.grad_y_prev = np.dot(delta, self.v.T)
        
    def reset_sum_grad(self):
        self.grad_w = np.zeros_like(self.w)
        self.grad_v = np.zeros_like(self.v)
        self.grad_b = np.zeros_like(self.b)
        
    def update(self, eta):
        self.w -= eta * self.grad_w
        self.v -= eta * self.grad_v
        self.b -= eta * self.grad_b
        
#--全连接 输出层--
class OutputLayer:
    def __init__(self, n_upper, n):
        #Xavier的初始值
        self.w = np.random.randn(n_upper, n)/np.sqrt(n_upper)
        self.b = np.zeros(n)
        
    def forward(self, x):
        self.x = x
        u = np.dot(x, self.w) + self.b
        self.y = u     #恒等函数
        
    def backward(self, t):
        delta = self.y - t
        
        self.grad_w = np.dot(self.x.T, delta)
        self.grad_b = np.sum(delta, axis =0)
        self.grad_x = np.dot(delta, self.w.T)
        
    def updata(self, eta):
        self.w -= eta * self.grad_w
        self.b -= eta * self.grad_b
        
#--各个网络层的初始化--
rnn_layer = SimpleRNNLayer(n_in, n_dim)
output_layer = OutputLayer(n_dim, n_out)

#--训练--
def tran(x_mb, t_mb):
    #正向传播 RNN层
    y_rnn = np.zeros((len(x_mb), n_time+1, n_mid))
    y_prev = y_rnn[:, 0, :]
    for i in range(n_time):
        x = x_mb[:, i, :]
        rnn_layer.forward(x, y_prev)
        y = rnn_layer.y
        y_rnn[:, i+1, :] = y
        y_prev = y
        
    #正向传播 输出层
    output_layer.forward(y)
    
    #反向传播 输出层
    output_layer.backward(t_mb)
    grad_y = output_layer.grad_x
    
    #反向传播 RNN层
    rnn_layer.reset_sum_grad()
    for i in reversed(range(n_time)):
        x = x_mb[:, i, :]
        y = t_rnn[:, i, :]
        y_prev = y_rnn[:, i, :]
        rnn_layer.backward(x, y, y_prev, grad_y)
        grad_y = rnn_layer.grad_y_prev
        
    #参数的更新
    rnn_layer.update(eta)
    output_layer.update(eta)
    
#--预测--
def predict(x_mb):
    #正向传播 RNN层
    y_prev = np.zeros((len(x_mb), n_mid))
    for i in range(n_time):
        x = x_mb[:, i, :]
        rnn_layer.forward(x, y_prev)
        y = rnn_layer.y
        y_prev = y
        
    #正向传播 输出层
    output_layer.forward(y)
    return output_layer.y

#--计算误差--
def get_error(x, t):
    y = predict(x)
    return 1.0/2.0*np.sum(np.square(y - t))
    
    
    
    
    
    
    

































        
        
        
        









































