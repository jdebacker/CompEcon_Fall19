from scipy import optimize as opt
import numpy as np
import firm
import households as hh
import aggregates as agg


def solve_ss(r_init, params):
    '''
    Solves for the steady-state equlibrium of the OG model
    '''
    beta, sigma, n, alpha, A, delta, xi = params
    ss_dist = 7.0
    ss_tol = 1e-8
    ss_iter = 0
    ss_max_iter = 300
    r = r_init
    while (ss_dist > ss_tol) & (ss_iter < ss_max_iter):
        # get w
        w = firm.get_w(r, alpha, A, delta)
        # solve HH problem
        foc_args = (beta, sigma, r, w, n, 0.0)
        b_sp1_guess = [0.05, 0.05]
        result = opt.root(hh.FOCs, b_sp1_guess, args=foc_args)
        b_sp1 = result.x
        euler_errors = result.fun
        b_s = np.append(0.0, b_sp1)
        # use market clearing
        L = agg.get_L(n)
        K = agg.get_K(b_s)
        # find implied r
        r_prime = firm.get_r(L, K, alpha, A, delta)
        # check distance
        ss_dist = np.absolute(r - r_prime)
        print('Iteration = ', ss_iter, ', Distance = ', ss_dist,
              ', r = ', r)
        # update r
        r = xi * r_prime + (1 - xi) * r
        # update iteration counter
        ss_iter += 1

    return r, b_sp1, euler_errors
