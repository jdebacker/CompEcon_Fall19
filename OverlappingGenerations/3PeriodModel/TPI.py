import numpy as np
import scipy.optimize as opt
import firm
import households as hh
import aggregates as agg


def solve_tp(r_path_init, params):
    '''
    Solves for the time path equlibrium using TPI
    '''
    (beta, sigma, n, alpha, A, delta, T, xi, b_sp1_pre, r_ss,
     b_sp1_ss) = params
    tpi_dist = 7.0
    tpi_tol = 1e-8
    tpi_iter = 0
    tpi_max_iter = 300
    r_path = np.append(r_path_init, np.ones(2) * r_ss)
    while (tpi_dist > tpi_tol) & (tpi_iter < tpi_max_iter):
        w_path = firm.get_w(r_path, alpha, A, delta)
        # Solve HH problem
        b_sp1_mat = np.zeros((T + 2, 2))
        euler_errors_mat = np.zeros((T + 2, 2))
        # solve upper right corner
        foc_args = (beta, sigma, r_path[:2], w_path[:2], n[-2:],
                    b_sp1_pre[0])
        b_sp1_guess = b_sp1_ss[-1]
        result = opt.root(hh.FOCs, b_sp1_guess, args=foc_args)
        b_sp1_mat[0, -1] = result.x
        euler_errors_mat[0, -1] = result.fun
        # solve all full lifetimes
        DiagMaskb = np.eye(2, dtype=bool)
        for t in range(T):
            foc_args = (beta, sigma, r_path[t:t+3], w_path[t:t+3], n,
                        0.0)
            b_sp1_guess = b_sp1_ss
            result = opt.root(hh.FOCs, b_sp1_guess, args=foc_args)
            b_sp1_mat[t:t+2, :] = (DiagMaskb * result.x +
                                   b_sp1_mat[t:t+2, :])
            euler_errors_mat[t:t+2, :] = (
                DiagMaskb * result.fun + euler_errors_mat[t:t+2, :])
        # create a b_s_mat
        b_s_mat = np.zeros((T, 3))
        b_s_mat[0, 1:] = b_sp1_pre
        b_s_mat[1:, 1:] = b_sp1_mat[:T-1, :]
        # use market clearing
        L_path = np.ones(T) * agg.get_L(n)
        K_path = agg.get_K(b_s_mat)
        # find implied r
        r_path_prime = firm.get_r(L_path, K_path, alpha, A, delta)
        # check distance
        tpi_dist = np.absolute(r_path[:T] - r_path_prime[:T]).max()
        print('Iteration = ', tpi_iter, ', Distance = ', tpi_dist)
        # update r
        r_path[:T] = xi * r_path_prime[:T] + (1 - xi) * r_path[:T]
        # update iteration counter
        tpi_iter += 1

    if tpi_iter < tpi_max_iter:
        print('The time path solved')
    else:
        print('The time path did not solve')

    return r_path[:T], euler_errors_mat[:T, :]
