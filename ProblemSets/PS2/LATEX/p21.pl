>>> # Problem 1
>>> import numpy as np
>>> def mathprod(A, B):
...    R1 = np.dot(np.array(A), np.array(B))
...    print(R1)
>>>
>>> A = [[3, -1, 4], [1, 5, -9]]
>>> B = [[2, 6, -5, 3], [5, -8, 9, 7], [9, -3, -2, -3]]
>>> mathprod(A, B)
[[ 37  14 -32 -10]
 [-54  -7  58  65]]
