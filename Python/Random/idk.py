a = {1, 2}
b = [a, a]
a.add(3)
b[0] = {4}
b.pop()

print(a, b)