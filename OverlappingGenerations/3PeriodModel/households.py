import numpy as np

# household functions


def FOCs(b_sp1, *args):
    '''
    Use the HH FOCs to solve for optimal saves, b2 and b3
    (1) u'(c1) = beta * (1 + r)* u'(c2) -> b2
    (2) u'(c2) = beta * (1 + r)* u'(c3) -> b3
    '''
    beta, sigma, r, w, n = args
    b_s = np.append([0], b_sp1)
    c1 = get_c(r, w, n[0], b_s[0], b_sp1[0])
    c2 = get_c(r, w, n[1], b_s[1], b_sp1[1])
    c3 = get_c(r, w, n[2], b_s[2], 0)
    mu_c1 = u_prime(c1, sigma)
    mu_c2 = u_prime(c2, sigma)
    mu_c3 = u_prime(c3, sigma)
    error1 = mu_c1 - beta * (1+r) * mu_c2
    error2 = mu_c2 - beta * (1+r) * mu_c3
    foc_errors = [error1, error2]

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
