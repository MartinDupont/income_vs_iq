# -*- coding: utf-8 -*-
"""
Created on Sat Aug 24 21:22:00 2019

@author: martin
"""
import numpy as np


def log_likelihood(x_arr, y_arr, y_0, m, b):
    """
    Log likelihood of data given m and b
    """
    t_1 = np.log(m * x_arr + b )
    t_2 = (m * x_arr + b) * np.log(y_0)
    t_3 = (m * x_arr + b + 1) * np.log(y_arr)
    
    return np.sum(t_1 + t_2 - t_3)

def d_db(x_arr, y_arr, y_0, m, b):
    """
    Calculate derivative w.r.t b of log likelihood
    """
    t_1 = 1.0 / (m * x_arr + b)
    t_2 = np.log(y_0)
    t_3 = np.log(y_arr)
    
    return np.sum(t_1 + t_2 - t_3)
    

def d_dm(x_arr, y_arr, y_0, m, b):
    """
    Calculate derivative w.r.t m of log likelihood
    """
    t_1 = x_arr/(m * x_arr + b)
    t_2 = x_arr * np.log(y_0)
    t_3 = x_arr * np.log(y_arr)
    
    return np.sum(t_1 + t_2 - t_3)
    

def mean_of_pareto(m, b, x, y_0):
    """
    Mean of a pareto distribution given that alpha = mx + b
    """
    alpha = (m * x + b)
    if alpha < 1:
        return float("inf")
    return float(int((alpha * y_0)/(alpha - 1)))