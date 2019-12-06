# import packages
import numpy as np
import matplotlib.pyplot as plt
import SS
import TPI

# set model parameters
sigma = 1.5  # CRRA
beta = 0.8  # discount rate
alpha = 0.3   # capital share of output
delta = 0.1  # rate of depreciation
A = 1.0  # TFP
T = 20  # number of periods until SS

# exogenous labor supply
n = np.array([1.0, 1.0, 0.2])
# parameter for convergence of GE loop
xi = 0.1

# solve the SS
ss_params = (beta, sigma, n, alpha, A, delta, xi)
r_init = 1 / beta - 1
r_ss, b_sp1_ss, euler_errors_ss = SS.solve_ss(r_init, ss_params)
print('SS interest rate is ', r_ss)
print('Maximum Euler error in the SS is ',
      np.absolute(euler_errors_ss).max())

# solve the time path
r_path_init = np.ones(T) * r_ss
b_sp1_pre = 1.1 * b_sp1_ss  # initial distribiton of savings -
# determined before t=1
# NOTE: if the initial distribution of savings is the same as the SS
# value, then the path of interest rates should equal the SS value in
# each period...
tpi_params = (beta, sigma, n, alpha, A, delta, T, xi, b_sp1_pre, r_ss,
              b_sp1_ss)
r_path, euler_errors_path = TPI.solve_tp(r_path_init, tpi_params)
print('Maximum Euler error along the time path is ',
      np.absolute(euler_errors_path).max())
plt.plot(np.arange(T), r_path)
plt.title("Path of real interest rates")
plt.show()
