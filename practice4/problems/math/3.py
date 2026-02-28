import math

n = int(input("Nummber of sides: "))
a = float(input("Length: "))

alpha = math.radians(360 / n / 2)
#tan alpha = a/2 / apoth
apothem = a/2 / math.tan(alpha)
area = n * a * apothem / 2
print("Area:", f'{area:.2f}')