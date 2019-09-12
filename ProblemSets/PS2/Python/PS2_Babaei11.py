# Problem 1
def myfunc(L):
    minimum = min(L)
    maximum = max(L)
    avg = sum(L)/len(L)
    # or
    '''
    sum = 0
    count = 0
    for v in L:
        count = count + 1
        sum = sum + v
    avg = sum/count
    '''
    Lstat = [minimum, maximum, avg]
    print(Lstat)

# Example 1
L = [1, 2, 3]
myfunc(L)

# Example 2: implementing function in one line
myfunc([0, 1, 2])
