# function


# global var
import random

list1 = []
list2 = []
result = []

# main

# 20개짜리 배열 2개를 준비, 랜덤 1~99 숫자 채우기
# 두 배열의 각 위치를 합해 새로운 배열을 만든다
for i in range(20):
    list1.append(random.randint(1, 99))
    list2.append(random.randint(1, 99))
    result.append(list1[i] + list2[i])

print(list1)
print(list2)
print(result)
result.clear()
print("---- quiz1 end ----")
print()


# 20개짜리 배열 2개를 준비, 두 배열을 결합
# 결합 시 사이사이 끼워 넣는 방식 1 1 1 1 2 2 2 2 ㄴㄴ 1 2 1 2 1 2 1 2
for i in range(20):
    result.append(list1[i])
    result.append(list2[i])

print(result)
result.clear()
print("---- quiz2 end ----")
print()

# 20개짜리 배열 1개 준비, 배열 역순으로 새로운 배열 만들기
# 단, reverse 함수 사용 금지
for i in range(19, -1, -1):
    result.append(list1[i])

# for _ in range(20):
#     result.append(list1.pop())

print(result)
print("---- quiz3 end ----")
print()
