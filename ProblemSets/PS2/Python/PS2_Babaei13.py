import calculator as calc

def pythagorean(i, j):
    print(calc.sqrt(calc.funcS(calc.funcP(i, i), calc.funcP(j,j))))

i = 3
j = 4
pythagorean(i, j)
