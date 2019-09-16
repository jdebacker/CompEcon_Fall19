import numpy as np
def mathprod(A, B):
    print(np.dot(np.array(A), np.array(B)))
A = [[3, -1, 4], [1, 5, -9]]
B = [[2, 6, -5, 3], [5, -8, 9, 7], [9, -3, -2, -3]]
mathprod(A, B)
