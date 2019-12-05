# firm functions


def get_r(L, K, alpha, A, delta):
    '''
    The interest rate implied by the firm FOC for the choice of capital
    '''
    r = alpha * A * (L / K) ** (1 - alpha) - delta

    return r


def get_w(r, alpha, A, delta):
    '''
    The wage rate implied by the interest rate
    '''
    w = ((1 - alpha) * A * ((r + delta) / (alpha * A)) **
         (alpha / (alpha - 1)))

    return w
