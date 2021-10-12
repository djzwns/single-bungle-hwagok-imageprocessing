# 두 수를 입력 받고, 더하기/빼기/곱하기/나누기 한번에 처리되는 함수 만들기

# funcion
def calc_func(n1: int, n2: int):
    ret1, ret2, ret3, ret4 = [0] * 4
    ret1 = n1 + n2
    ret2 = n1 - n2
    ret3 = n1 * n2
    ret4 = n1 / n2
    return ret1, ret2, ret3, ret4


# global var
num1: int = 0
num2: int = 0
add, sub, mul, div = [0] * 4

# main
num1 = int(input("값1 입력:"))
num2 = int(input("값2 입력:"))
add, sub, mul, div = calc_func(num1, num2)
print(add, sub, mul, div)
