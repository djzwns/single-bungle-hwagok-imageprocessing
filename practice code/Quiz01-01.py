# 변수 선언
num1 = 0
num2 = 0

# 메인
if __name__ == "__main__":
    num1 = input("값1 입력: ")
    num2 = input("값2 입력: ")

    print("큰 값은 {}".format(num1 if num1 > num2 else num2))
