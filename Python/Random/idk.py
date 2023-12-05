from itertools import product, chain, combinations

X = {1,2,3,4,6,8,10,12}
Y = {1,2,3,5,6,9,11,13}
Z = {1,2,4,5,7,8,11,14}
T = {1,3,4,5,7,9,10,15}


def subsets(s):
    return map(set, chain(*map(lambda x: combinations(s, x), range(0, len(s)+1))))


def check(x, y, z, t):
    # Equation 1
    a1 = (z | t) | (x & y)
    a2 = ((y - x) & t) - (x & z)
    a = a1.issubset(a2)

    if not a:
        return False

    # Equation 2
    b1 = (x | y) | (z - t)
    b2 = (y | z) - (t | x)
    b = b1.issubset(b2)

    if not b:
        return False

    # Equation 3
    c1 = ((z & y) | x) | (y - t)
    c2 = (x | y) - (z | t)
    c = c1 == c2

    if not c:
        return False

    # Equation 4
    d1 = (z - t) & (x | y)
    d2 = (t | x) | (y & z)
    d = d1 == d2

    return d


print("Sets X, Y, Z, T:")

X_subsets = subsets(X)
Y_subsets = subsets(Y)
Z_subsets = subsets(Z)
T_subsets = subsets(T)

combinations_of_subsets = product(X_subsets, Y_subsets, Z_subsets, T_subsets)

for c in combinations_of_subsets:
    if check(*c):
        print(c)



