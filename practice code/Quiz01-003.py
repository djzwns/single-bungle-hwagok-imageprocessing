import random


# function
def print_array(string, array):
    print("--", string, "--")
    for i in range(5):
        print("[", sep='', end='')
        for j in range(5):
            if j < 4:
                print(array[i][j], sep='', end=', ')
            else:
                print(array[i][j], sep='', end='')
        print("]")
    print()


def array_calc(array, val: int):
    global x, y
    for i in range(y):
        for j in range(x):
            array[i][j] = max(0, min(255, array[i][j] + val))


def array_bw(array):
    global x, y
    for i in range(y):
        for j in range(x):
            array[i][j] = 0 if array[i][j] < 127 else 255


# global var
ary = []
x, y = 0, 0

# main
x = random.randint(100, 200)
y = random.randint(100, 200)

for i in range(y):
    tmp = []
    for j in range(x):
        tmp.append(random.randint(0, 255))
    ary.append(tmp)

print_array("init", ary)
array_calc(ary, 50)
print_array("+50", ary)
array_calc(ary, -100)
print_array("-100", ary)
array_bw(ary)
print_array("b & w", ary)
