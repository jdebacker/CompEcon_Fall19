import numpy as np

# household functions


def FOCs(b_sp1, *args):
    '''
    Use the HH FOCs to solve for optimal saves, b2 and b3
    (1) u'(c1) = beta * (1 + r)* u'(c2) -> b2
    (2) u'(c2) = beta * (1 + r)* u'(c3) -> b3
    '''
    beta, sigma, r, w, n, b_init = args
    b_s = np.append(b_init, b_sp1)
    b_sp1 = np.append(b_sp1, 0.0)
    c = get_c(r, w, n, b_s, b_sp1)
    mu_c = u_prime(c, sigma)
    lhs_euler = mu_c
    rhs_euler = beta * (1+r) * mu_c
    foc_errors = lhs_euler[:-1] - rhs_euler[1:]
    return foc_errors


def get_c(r, w, n, b_s, b_sp1):
    '''
    Use the budget constraint to solve for consumption
    '''
    c = w * n + (1 + r) * b_s - b_sp1

    return c


def u_prime(c, sigma):
    '''
    Marginal utility of consumption
    '''
    mu_c = c ** -sigma

    return mu_c
