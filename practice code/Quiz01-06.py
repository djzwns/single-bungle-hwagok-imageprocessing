# 2차원 배열 처리
# 랜덤하게 x, y 크기의 배열 준비 (3~9) 사이
# 랜덤하게 값을 채움 0~255
# 이미지를 반전 처리
# 이미지가 너무 밝아서 100 어둡게
# grayscale 이미지를 흑백 영상으로 바꾸자
# 127 기준으로 흑, 백 구분하기
# 평균 값을 기준 흑, 백  구분
# 이미지 상하 반전 좌우 반전
import random
import copy


# function
def print_image(string: str, array: []):
    print(string)
    global y
    for i in range(y):
        print(array[i])
    print()


# global var
ary = []        # 기본
ary2 = []       # 반전
ary3 = []       # 어둡게
bwAry1 = []     # 흑백
bwAry2 = []     # 흑백
lrAry = []      # 좌우
udAry = []      # 상하

x: int = 0
y: int = 0


# main

# 크기 설정
x = random.randint(3, 9)
y = random.randint(3, 9)

# 1. 랜덤값 채우기
for i in range(y):
    tmp = []
    for j in range(x):
        tmp.append(random.randint(0, 255))
    ary.append(tmp)


# 2. 반전 처리
ary2 = copy.deepcopy(ary)
for i in range(y):
    for j in range(x):
        ary2[i][j] = 255 - ary[i][j]


# 3. 100 만큼 어둡게
ary3 = copy.deepcopy(ary2)
for i in range(y):
    for j in range(x):
        ary3[i][j] = max(0, ary2[i][j] - 100)


# 4. 흑백 처리
# 4.1 127 기준
bwAry1 = copy.deepcopy(ary3)
for i in range(y):
    for j in range(x):
        bwAry1[i][j] = 0 if ary3[i][j] < 127 else 255


# 4.2 평균값 기준
avgColor = 0
bwAry2 = copy.deepcopy(ary3)
for i in range(y):
    for j in range(x):
        avgColor += ary3[i][j]

avgColor = (avgColor // (x * y))

for i in range(y):
    for j in range(x):
        bwAry2[i][j] = 0 if ary3[i][j] < avgColor else 255



# 5. 이미지 상하좌우 반전
# 5.1 상하
udAry = copy.deepcopy(bwAry2)
for i in range(y):
    for j in range(x):
        udAry[i][j] = bwAry2[y - i - 1][j]

# 5.2 좌우
lrAry = copy.deepcopy(udAry)
for i in range(y):
    for j in range(x):
        lrAry[i][j] = udAry[i][x - j - 1]

print_image("초기이미지", ary)
print_image("반전이미지", ary2)
print_image("어두운이미지", ary3)
print_image("흑백이미지(127)", bwAry1)
print("그레이스케일 평균: ", avgColor)
print_image("흑백이미지(평균)", bwAry2)
print_image("상하반전이미지", udAry)
print_image("좌우반전이미지", lrAry)
