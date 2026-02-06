
a = int(input())

s = set()
d = dict()

for i in range(a):
    n = input()
    if n not in s:
        s.add(n)
        d[n]=i+1

for x in sorted(d):
    print(x, d[x])
    




