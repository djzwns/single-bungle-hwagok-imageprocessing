"""
    1.2 3.3 11.2    0.5 --> A
    1.2 3.3 10.2    0.3 --> B
    1.2 3.3 10.1    0.5 --> B
"""


# 새로코딩 --> ## 주석 0 1 2
# 학습: 테스트 == 7:3 알고리즘 SVM으로 바꾸거나 KNN 9로 설정

from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm
from sklearn import metrics, utils
import pandas as pd
import numpy as np


# 중요 순서 익히기!!

# 0. 데이터 준비
df = pd.read_csv("iris.csv")
df = utils.shuffle(df)

# 0-1. 학습용 - 테스트용 분류
dataLen = df.shape[0]
trainSize = int(dataLen * 0.7)
testSize = dataLen - trainSize

# 0-2. 문제, 답 분리
train_data = df.iloc[0:trainSize, 0:-1]
train_label = df.iloc[0:trainSize, [-1]]
test_data = df.iloc[trainSize:, 0:-1]
test_label = df.iloc[trainSize:, [-1]]

# 1. 학습 방법 결정
clf = svm.SVC(kernel="linear")

# 2. 학습 하기
clf.fit(train_data, train_label)

# 3. 모델의 정답률 구하기
results = clf.predict(test_data)
score = metrics.accuracy_score(results, test_label)
print("정답률--> %5.2f %%" % (score * 100))

# 4. 정답을 모르는 데이터 예측
myData = [
    [1.2, 3.3, 11.2, 0.5],
    [1.2, 3.3, 10.2, 0.3],
    [1.2, 3.3, 10.1, 0.5]
]

result = clf.predict(myData)
for i in range(len(result)):
    print("이 꽃은 %s 입니다." % result[i])
print("단, 정답 확률 %5.2f %% 입니다." % (score * 100))