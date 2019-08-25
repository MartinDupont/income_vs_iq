# -*- coding: utf-8 -*-
"""
Script to try and fit income as a function of IQ, using the assumption that 
the residuals are pareto distributed, and not normally distributed. 

https://en.wikipedia.org/wiki/Pareto_distribution

A typical pareto distribution has two parameters, a minimum value, and a 
scale parameter, α. We assume that α is no longer constant, but a linear function
of iq. I.e. let x = iq, then α = m * x + b. 

If we let y indicate income, we fit the model by maximizing the likelihood of 
getting the data under the model, by varying b and m.
"""

import numpy as np
import matplotlib.pyplot as plt
from preprocess_data import read_in_and_clean
from likelihoods import mean_of_pareto, log_likelihood, d_db, d_dm

# ============================== switchboard ================================ #

MIN_INCOME = 25000 # Incomes must be truncated because pareto blows up at zero
    
epsilon = 0.00001 # training rate
m_0 = - 1.0 /100 
b_0 = 2

training_epochs = 10000


# ============================= Begin main code ============================= #

def main(epsilon, m_0, b_0, n_epochs, min_income):
    x, y = read_in_and_clean("./nlsy79/nlsy79.csv", MIN_INCOME)
    
    plt.scatter(x * 15 + 100, y, alpha = 0.125)
    plt.title("Income vs IQ")
    plt.xlabel("Average income in 2014 US dollars")
    plt.xlabel("IQ")
    plt.show()
    
    y_0 = min_income
    
    m = m_0
    b = b_0
    
    likelihoods = []
    m_vals = []
    b_vals = []
    
    for i in range(n_epochs):
    
        likelihood = log_likelihood(x, y, y_0, m, b)
        likelihoods += [likelihood]
        
        delta_b = d_db(x, y, y_0, m, b)
        delta_m = d_dm(x, y, y_0, m, b)
        
        m = m + epsilon * delta_m
        b = b + epsilon * delta_b
        
        m_vals += [m]
        b_vals += [b]
        
        if i % 10 == 0:
            print("======================= Epoch: {} ===============================".format(i))
            print("likelihood: {}".format(likelihood))
            print("Δ m: {}, Δ b:  {} ".format(delta_m, delta_b))
            print("m: {}, b: {}".format(m, b)) 
      
        
    plt.figure()
    plt.title("log likelihood vs epoch")
    plt.plot(likelihoods)
    plt.show()
    
    plt.figure()
    plt.title("m vs epoch")
    plt.plot(m_vals)
    plt.show()
    
    plt.figure()
    plt.title("b vs epoch")
    plt.plot(b_vals)
    plt.show()
    
    # classical approach, no regression, assume α constant for all IQ:
    n = len(y)
    alpha = n / sum([np.log(y_i/min_income) for y_i in y])
    
    print("======================================================================")
    print("                             Final Results                            ")
    print("======================================================================")
    
    print("m: {}, b: {}".format(m, b))
    print("α of whole sample, without regression: {}".format(alpha))
    
    normalized_iqs = np.array([-1, 0, 1, 2])
    iqs = normalized_iqs * 15 + 100
    expected_incomes = [mean_of_pareto(m, b, iq, min_income) for iq in normalized_iqs]
    
    print("average expected income from model: {}".format(int(mean_of_pareto(1, 0, alpha, min_income))))
    
    for iq, income, normed_iq in zip(iqs, expected_incomes, normalized_iqs):
        print("")
        print("A person with an IQ of {} can expect an average income of {} per year".format(iq, int(income)))
        print("Effective α for a person with IQ {} is {}".format(iq, (m * normed_iq + b)))
        
    return(m, b)
    
if __name__ == "__main__":
    main(epsilon, m_0, b_0, training_epochs, MIN_INCOME)