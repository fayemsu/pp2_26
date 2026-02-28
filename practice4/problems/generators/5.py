def sq(n):
    for i in range(n, -1, -1 ):
        yield i

n = int(input())

for i in sq(n):
    print(i)