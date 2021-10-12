# 함수

# 전역
i = 0
sum = 0

# 메인
'''
    int hap=0;
    for (int i = 1; i < 11; ++i)
        hap += i;
'''
# range(초기값, 최종값, 증가값) -> array 를 생성해줌
for i in range(1, 11, 1):
    sum += i

print("1에서 10까지의 합", sum)

# 1부터 100까지 짝수의 합
sum = 0
for i in range(1, 101, 1):
    if i & 1 == 0:
        sum += i

print("1부터 100까지 짝수의 합:", sum)

# 1부터 1000까지 333의 배수의 합
sum = 0
for i in range(1, 1001, 1):
    if i % 333 == 0:
        sum += i
print("1부터 1000까지 333의 배수의 합: ", sum)

# 123456부터 678900까지 8585의 배수의 합
sum = 0
for i in range(123456, 678901, 1):
    if i % 8585 == 0:
        sum += i
print("1부터 1000까지 333의 배수의 합: ", sum)
