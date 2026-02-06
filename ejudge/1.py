a = int(input())
n = list(map(int, input().split()))

c = [0] * 2001
for x in n:
    c[x+1000]+=1

"""
4 4 7 3 7 4 3 3 4 3 4
c[1004]=5
c[1007]=2
c[1003]=4

"""
t = max(c)
for i in range(2000):
    if c[i] == t:
        print(i-1000)
        break