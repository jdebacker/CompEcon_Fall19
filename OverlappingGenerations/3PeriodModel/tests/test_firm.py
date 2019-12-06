import numpy as np
import firm


def test_get_r():
    '''
    Teset of the firm.get_r() function
    '''
    A = 1.0
    alpha = 0.5
    delta = 0.1
    L = 4.0
    K = 16.0
    expected_value = 0.15
    test_value = firm.get_r(L, K, alpha, A, delta)

    assert np.allclose(test_value, expected_value)


def test_get_w():
    '''
    Teset of the firm.get_w() function
    '''
    A = 1.0
    alpha = 0.25
    delta = 0.05
    r = 0.05
    expected_value = 1.01790660622309
    test_value = firm.get_w(r, alpha, A, delta)

    assert np.allclose(test_value, expected_value)
