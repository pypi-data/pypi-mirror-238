# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 20:45:20 2023

@author: 22193
"""
import numpy as np
img_size= 8
n_mid = 16      #中间层的神经元数量
n_out = 10      #输出层的维度
eta = 1e-4      #学习系数

#--全连接层的父类--
class BaseLayer:
    '这里是对SGD（随机梯度下降法）的编程实现'
    def update(self, eta):  #eta是一个参数，为学习率（learning rate）的意思
        self.w -= eta * self.grad_w
        self.b -= eta * self.grad_b

#--中间层--
class MiddleLayer(BaseLayer):
    def __init__(self, n_upper, n):
        # He的初始值
        self.w = np.random.randn(n_upper, n) * np.sqrt(2/n_upper)  #这里进行了权重初始化（Xavier），该方法使权重缩小在一个适度范围，预防梯度消失或爆炸
        self.b = np.zeros(n)
        
    def forward(self, x):
        self.x = x
        self.u = np.dot(x, self.w) + self.b
        self.y = np.where(self.u <= 0, 0, self.u)     #ReLU
        
    def backward(self, grad_y):
        delta = grad_y * np.where(self.u <= 0, 0, 1)  #ReLU的微分
        
        self.grad_w = np.dot(self.x.T, delta)
        self.grad_b = np.sum(delta, axis=0)
        self.grad_x = np.dot(delta, self.w.T)

#--输出层--
class OutputLayer(BaseLayer):
    def __init__(self, n_upper, n):
        # Xavier的初始值
        self.w = np.random.randn(n_upper, n) / np.sqrt(n_upper)   #这是 Xavier 初始化中的一部分。这个除法操作的目的是将权重值缩小，以便更好地满足网络的训练需求。
        self.b = np.zeros(n)
        
    def forward(self, x):
        self.x = x
        u = np.dot(x, self.w) + self.b
        #Softmax函数
        self.y = np.exp(u)/np.sum(np.exp(u), axis = 1, keepdims=True)
        
    def backward(self, t):
        delta = self.y - t
        
        self.grad_w = np.dot(self.x.T, delta)
        self.grad_b = np.sum(delta, axis=0)
        self.grad_x = np.dot(delta, self.w.T)

#--各个网络层的初始化--
layers = [MiddleLayer(img_size*img_size, n_mid),
          MiddleLayer(n_mid, n_mid),
          OutputLayer(n_mid, n_out)]

#--正向传播--
def forward_propagation(x):
    for layer in layers:
        layer.forward(x)
        x = layer.y
    return x

#--反向传播--
def backpropagation(t):
    grad_y = t
    for layer in reversed(layers):
        layer.backward(grad_y)
        grad_y = layer.grad_x
    return grad_y

#--参数的更新--
def update_params(eta):
    for layer in layers:
        layer.update(eta)
        
#--误差的测定--
def get_error(x, t):
    y = forward_propagation(x)
    return -np.sum(t*np.log(y+1e-7))/len(y)  #较差熵误差

#--准确率的测定--
def get_accuracy(x, t):
    y = forward_propagation(x)
    count = np.sum(np.argmax(y, axis=1) == np.argmax(t, axis=1))
    return count/len(y)



