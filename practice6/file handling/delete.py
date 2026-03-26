import os

if os.path.exists('1.txt'):
    os.remove('1.txt')
    print('File deleted.')
else:
    print('File does not exist.')