## 함수 선언부
def func() -> int:
    a = 10
    b = 20
    a += b
    return a


## 전역 변수부
# python 에는 선언이 따로 없어서 미리 표시해주는 것을 권장
num1 = 0

## 메인 코드부
if __name__ == "__main__":
    num1 = int(input("값 입력: "))
    # 좋은 코드 == 가독성이 좋은 코드
    if num1 > 100:
        print("100 보다 큼.")
    elif num1 < 100:
        print("100 보다 작음.")
    else:
        if True:
            print(True)
        print("100 과 같음.")

    print("종료")
