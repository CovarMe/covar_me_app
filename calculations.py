import numpy as np
import pandas as pd
from sklearn.covariance import graph_lasso


def calculate_mean_vector(returns):
    n = len(list(returns))
    data = [0] * n
    for i, ticker in enumerate(list(returns)):
        data[i] = returns[ticker].mean()

    return np.array(data)


def calculate_wolf_weights(covar, means, q):
    # Ledoit, Olivier, and Michael Wolf. 
    # "Improved estimation of the covariance matrix of stock returns with an application to portfolio selection." 
    # Journal of empirical finance 10.5 (2003): 603-621
    n = len(list(covar)) # number of companies
    sigma = covar.as_matrix() # covariance matrix
    prec = np.linalg.inv(sigma) # precision matrix
    ones = np.ones(n)
    A = np.dot(np.dot(ones.transpose(), prec), ones)
    B = np.dot(np.dot(ones.transpose(), prec), means)
    C = np.dot(np.dot(means.transpose(), prec), means)
    denom = (A * C - B ** 2)
    # glasso trials
    # glasso = graph_lasso(covar.as_matrix(), 0.48, 
    #                      verbose = True, mode = 'cd')
    # print glasso
    w = np.dot(np.dot((C - q * B) / denom, prec),ones) + \
            np.dot(np.dot((q * A - B) / denom, prec), means)
    return w
