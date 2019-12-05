# import packages
import numpy as np
import SS

# set model parameters
sigma = 1.5  # CRRA
beta = 0.8  # discount rate
alpha = 0.3   # capital share of output
delta = 0.1  # rate of depreciation
A = 1.0  # TFP

# exogenous labor supply
n = np.array([1.0, 1.0, 0.2])
# parameter for convergence of GE loop
xi = 0.1

# solve the SS
ss_params = (beta, sigma, n, alpha, A, delta, xi)
r_init = 1 / beta - 1
r_ss = SS.solve_ss(r_init, ss_params)

# solve the time path
