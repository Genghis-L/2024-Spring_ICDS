#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 13 22:01:38 2021

@author: bing
"""


class GD:

    def __init__(self, lr, samples):
        self.lr = lr
        self.y = [s.get_y() for s in samples]
        self.x = [s.get_x() for s in samples]

    def compute_grad(self, pred_y: list):
        '''
        compute and return the gradient of w and b respectively
        '''
        grad_w = 0
        grad_b = 0
        n = len(pred_y)
        grad_w = sum([(pred_y[i] - self.y[i]) * self.x[i]
                     for i in range(n)]) / n
        grad_b = sum([pred_y[i] - self.y[i] for i in range(n)]) / n

        return grad_w, grad_b

    def update(self, parameters: list, pred_y: list):
        '''
        parameters is a list of [w, b]
        1. compute the gradients of w and b
        2. update both elements in parameters
        '''
        grad_w, grad_b = self.compute_grad(pred_y)
        parameters[0], parameters[1] = parameters[0] - \
            self.lr*grad_w, parameters[1]-self.lr*grad_b

        return parameters
