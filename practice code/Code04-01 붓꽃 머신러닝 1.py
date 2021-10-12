# 붓꽃 구별하기 머신러닝 프로젝트 1
# python 3.10 --> scikit-learn 미지원
# python 3.8 로 낮추자
from sklearn.neighbors import KNeighborsClassifier  # KNN 알고리즘
from sklearn import metrics, utils  # 편리한 함수
import pandas as pd  # csv 파일을 편리하게 사용
import numpy as np  # 필수


# 0. 데이터 준비 --> 제일 어렵고 중요 (문제 + 정답) --> Data + Label
# data frame 약자, 엑셀의 데이터 시트 처럼 읽어들인다
df = pd.read_csv('iris.csv')
df = utils.shuffle(df)  # 데이터 섞기 (필수)

# 0.1 학습용 데이터, 테스트용 데이터 분리 --> 8:2
dataLen = df.shape[0]  # 행 개수(=데이터 개수)
trainSize = int(dataLen * 0.8)  # 학습용 데이터 개수
testSize = dataLen - trainSize  # 테스트용 데이터 개수

train_data = df.iloc[0:trainSize, 0:-1]  # 80%행, 마지막 열 제외
train_label = df.iloc[0:trainSize, [-1]]  # 80%행, 마지막 열만
test_data = df.iloc[trainSize:, 0:-1]
test_label = df.iloc[trainSize:, [-1]]

# 1. 학습 방법을 결정 (머신러닝 알고리즘 선택): KNN, SVM, DeepLearning ...
clf = KNeighborsClassifier(n_neighbors=3)

# 2. 학습하기 (훈련하기) --> 오랫 동안 cpu 가 작업함. (** 오래 걸림 **) --> 결과: 모델 : 인공지능
clf.fit(train_data, train_label) # 실제 공부
# 3. 모델의 정답율 구하기 (몇 점짜리 인공지능인지)
results = clf.predict(test_data)
score = metrics.accuracy_score(results, test_label)
print("정답률 ->%5.2f %% " % (score * 100))

# 3.1 모델 저장시키기 (iris_150_KNN3_정답률.dmp)
import joblib
joblib.dump(clf, "iris_150_KNN3_" + str(int(score*100)) + ".dmp")

# 4. 정답을 모르는 데이터를 '예측' 하기
myData = [ 4.8, 3.3, 1.3, 0.2 ]
result = clf.predict([myData])

print("모델-> 이 꽃은 %s 입니다. 단, %5.2f %% 보장함" % (result[0], score*100))
