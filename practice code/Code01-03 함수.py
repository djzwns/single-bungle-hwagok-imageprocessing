# function
def add_number(n1: int, n2: int) -> int:
    retValue1 = 0
    retValue2 = 1
    retValue1 = n1 + n2
    retValue2 = n1 * n2
    return retValue1, retValue2  # (retValue1, retValue2)


def mul_number(n1: int, n2: int) -> int:
    return n1 * n2


def func1():
    # num = 1 # local var
    global num
    num += 1


def func2():
    pass


# global var
num: int = 100

func1()
print(num)
# main
# num1, num2 = 100, 200
# total, mul = add_number(num1, num2)
# print(total, mul)
