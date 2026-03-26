with open("1.txt", "a") as f:
    f.write('\n\n')
    f.write('sound of the waves collide\n')
    f.write('take me one more timeee\n')
    f.write('take me one more wave\n')

with open("1.txt", "r") as f:
    print(f.read())