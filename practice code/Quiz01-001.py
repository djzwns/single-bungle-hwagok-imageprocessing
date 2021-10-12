# function
import math


def calc_function(n1: int, n2: int):
    ret1 = n1 + n2
    ret2 = n1 - n2
    ret3 = n1 * n2
    ret4 = n1 / n2 if n2 != 0 else math.nan
    ret5 = n1 % n2
    ret6 = n1 // n2
    ret7 = n1 ** n2
    return ret1, ret2, ret3, ret4, ret5, ret6, ret7


# global var
num1, num2 = 0, 0


# main
num1 = int(input("val1 input: "))
num2 = int(input("val2 input: "))

print(calc_function(num1, num2))
