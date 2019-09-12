>>> # Problem 5
>>> import numpy as np
>>> def blockmat(A, B, C):
...    A = np.array(A)
...    B = np.array(B)
...    C = np.array(C)
...    print(np.vstack(((np.column_stack((np.zeros((3,3)), A.T, np.eye((3))))), (np.column_stack((A, np.zeros((2, 2)), np.zeros((2, 3))))), (np.column_stack((B, np.zeros((3,2)), C))))))
>>> A = [[0, 2, 4], [1, 3, 5]]
>>> B = [[3, 0, 0], [3, 3, 0], [3, 3, 3]]
>>> C = [[-2, 0, 0], [0, -2, 0], [0, 0, -2]]
>>> blockmat(A, B, C)
[[ 0.  0.  0.  0.  1.  1.  0.  0.]
 [ 0.  0.  0.  2.  3.  0.  1.  0.]
 [ 0.  0.  0.  4.  5.  0.  0.  1.]
 [ 0.  2.  4.  0.  0.  0.  0.  0.]
 [ 1.  3.  5.  0.  0.  0.  0.  0.]
 [ 3.  0.  0.  0.  0. -2.  0.  0.]
 [ 3.  3.  0.  0.  0.  0. -2.  0.]
 [ 3.  3.  3.  0.  0.  0.  0. -2.]]
