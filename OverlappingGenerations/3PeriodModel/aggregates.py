# market clearning conditions


def get_L(n):
    '''
    Find aggregate labor supply
    '''
    L = n.sum()

    return L


def get_K(b_s):
    '''
    Find aggregate capital supply
    '''
    if b_s.ndim == 1:
        K = b_s.sum()
    if b_s.ndim == 2:
        K = b_s.sum(axis=1)
    return K
