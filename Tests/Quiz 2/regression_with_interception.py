#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 16:18:25 2023

@author: bing
"""
import matplotlib.pyplot as plt
from sample import Sample, standardization
import optimizer


class Regression:
    
    def __init__(self, lr):
        self.lr = lr
        
    def compute_erros(self, pred_label, true_label):
        n = len(pred_label)
        error = 0
        for i in range(n):
            error += (pred_label[i] - true_label[i])**2/(2*n)
        return error
    
    def run(self, parameters:list, samples):
        steps = 0
        margin = 0.01
        num_iter = 100
        error_history = []
        
        ##set the optimizer; use gradient descent to update the parameters
        gradient_descent = optimizer.GD(self.lr, samples)
        
        while True:
            pred_y = [parameters[0] * s.get_x() + parameters[1] for s in samples] 
            true_y = [sample.get_y() for sample in samples]
            error = self.compute_erros(pred_y, true_y)
            error_history.append(error)
            steps += 1
            if error<=margin or steps>=num_iter:
                break
            ## call update to update the parameters by gradient descent
            gradient_descent.update(parameters, pred_y)
            
        return error_history
            
    
if __name__=="__main__":
    # load data   
    f = open('Student_Performance.csv', 'r')
    raw_data = f.readlines()
   
    raw_data = [item.strip().split(",") for item in raw_data]
    # print(raw_data)
        
    data = []
    for item in raw_data[1:]: #ignore the first row
        s = Sample(float(item[1]), float(item[-1]))
        data.append(s)
        
    ##Standardization
    data = standardization(data)
    #split data into train set and test set
    
    train_set = data[:160]
    test_set = data[160:]
    
    lr = 0.05
    regression = Regression(lr)
    w = 2
    b = 0
    parameters = [w, b] 
    error_history = regression.run(parameters, train_set)
    w = parameters[0]
    b = parameters[1]
    pred_y = [w * s.get_x() + b for s in test_set] 
    
    
    def plot_data(data, pred_y=[], error_history=[]):
        d_x = [s.get_x() for s in data]
        d_y = [s.get_y() for s in data]
        plt.cla()
        plt.scatter(d_x, d_y)
        if len(pred_y) > 0:
            plt.plot(d_x, pred_y, 'r')
            title_str = "test result when train error = %0.2f" % error_history[-1]
            plt.title(title_str)
            plt.ylabel('Performance Index')
            plt.xlabel('Previous Scores')
        plt.show() 
        
    #plotting the result    
    plot_data(test_set, pred_y, error_history)
    # plt.plot(error_history)
    # plt.title('training error')
    plt.show()
        
    

