from functools import reduce


n = [151, 5670, 6543, 141]


n2 = list(map(lambda x: x%10, n))
n3 = list(filter(lambda x: x%2==0, n))
print(n2)
print(n3)


n4 = reduce(lambda a, b: a * b, n)
print(n4)


freu = ['jdan', 'ani', 'bayan', 'kuka', 'altair']
for i, n in enumerate(freu, start=1):
    print(i, n[0])


gpa = [4.16, 4.11, 4.07, 4.31, 4.28]
for n, g in zip(freu, gpa):
    print(n, g)


x = True
print(type(x))
print(isinstance(x, str))
print(isinstance(x, bool))

print(str(x))
print(int(x))
