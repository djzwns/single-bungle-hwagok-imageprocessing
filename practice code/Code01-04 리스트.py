import random

# function


# global var
arr = []
total = 0


# main
# for i in arr:
#     print(i)

# arr 1~100 랜덤값 20개
for _ in range(20):
    arr.append(random.randint(1, 100))

print(arr)