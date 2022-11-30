from itertools import product

t = [1, 2, 3, 4]
for i in range(1, 5):
    poss = product(t, repeat=i)
    for item in poss:
        print(item)
