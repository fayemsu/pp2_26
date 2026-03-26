import os

for root, dirs, files in os.walk('dirs'):
    for f in files:
        if f.endswith('.txt'):
            print(os.path.join(root, f))
        if f.endswith('.py'):
            print(os.path.join(root, f))