import shutil

shutil.copy('outer/1.txt', 'outer/middle/inner/1_copy.txt')

shutil.move('outer/middle/inner/1_copy.txt', 'outer/middle/1_copy_moved.txt')