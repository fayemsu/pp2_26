import os

with open('outer/1.txt', 'w') as f:
    f.write('come outside and breath in\n')
with open('outer/middle/inner/2.txt', 'w') as f:
    f.write('i will save your live\n')


for x in os.listdir('outer'):
    print(x)

for x in os.listdir('outer/middle'):
    print(x)