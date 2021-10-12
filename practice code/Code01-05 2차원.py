# ary = \
# [   [0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0] ]
import random

ary = []
for i in range(5):
    tmp = []
    for k in range(6):
        tmp.append(0)
    ary.append(tmp)

# 이미지 로드
for i in range(5):
    for k in range(6):
        ary[i][k] = random.randint(0, 255)


# 영상 출력
for i in range(5):
    print(ary[i])


# 이미지가 어두움 밝게
for i in range(5):
    for k in range(6):
        ary[i][k] = min(255, ary[i][k] + 100)

# 영상 출력
for i in range(5):
    print(ary[i])
