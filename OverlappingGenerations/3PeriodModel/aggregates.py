# market clearning conditions


def get_L(n):
    '''
    Find aggregate labor supply
    '''
    L = n.sum()

    return L


def get_K(b_sp1):
    '''
    Find aggregate capital supply
    '''
    K = b_sp1.sum()

    return K
