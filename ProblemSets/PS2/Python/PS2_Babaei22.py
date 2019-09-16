import numpy as np
def func(A):
    A = np.array(A)
    print((-A * A * A) + (9 * A * A) - (15 * A))
A = [[3, 1, 4], [1, 5, 9], [-5, 3, 1]]
func(A)
