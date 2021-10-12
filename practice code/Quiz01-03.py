# 2부터 1000까지 소수를 출력하고 그 합계를 구하자.
# 소수란? 1과 자기자신 외에는 나누어 떨어지지 않는 정수
# 2, 3, 5, 7 ...

# 함수

# 전역
i: int = 0
j: int = 0
sum: int = 0

# 메인
for i in range(2, 1001, 1):
    for j in range(2, i, 1):
        if i % j == 0:
            break
    # if i == j:
        print(i, j)


