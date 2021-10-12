# 머신러닝 주제 선정 후 관련 내용 정리 및 pre-trained 데이터 카페 등록
# csv, *.dmp 파일 업로드
"""
    1. 주제에 대한 개요와 설명
    2. csv 데이터의 열에 대한 설명
    3. 데이터 개수, 사용한 알고리즘
    4. pre-trained 데이터의 정답률
    5. 정답이 없는 예측해본 샘플 데이터
"""

from sklearn import svm
from sklearn import metrics, utils
import pandas as pd
import numpy as np
import joblib


# # # 데이터 준비
# df = pd.read_csv("data01.csv")
# df = utils.shuffle(df)
# df = df.fillna(0)
# 
# # 학습-테스트 데이터 분리 7:3
# dataLen = df.shape[0]
# trainSize = int(dataLen * 0.7)
# testSize = dataLen - trainSize
# 
# # 데이터-결과 분리
# trainData = df.iloc[0:trainSize, 3:]
# trainLabel = df.iloc[0:trainSize, [2]]
# testData = df.iloc[trainSize:, 3:]
# testLabel = df.iloc[trainSize:, [2]]
# print(trainData)
# 
# # 학습 방법 설정
# clf = svm.SVC(kernel="linear")
# 
# # 학습하기
# clf.fit(trainData, trainLabel)
# 
# # 모델 정답률 구하기
# results = clf.predict(testData)
# score = metrics.accuracy_score(results, testLabel) * 100
# print("예측성공률: %5.2f %%" % score)
# 
# # 모델 저장
# joblib.dump(clf, "mortal_1177_SVM_Linear_" + str(int(score)) + ".dmp")

# 기학습된 모델 불러오기
clf = joblib.load("mortal_1177_SVM_Linear_85.dmp")

# 나이, 성별, BMI, 고혈압, 심방세동, 선천성 심장 질환(심근경색ㄴㄴ), 당뇨병, 결핍증, 우울증, 고지혈증, 신부전증,
# 만성 폐색성 폐질환, 심박수, 수축기 혈압, 확장기 혈압, 호흡수, 체온, 혈중 산소 포화도, 소변 배출량, 혈구비율(평균40~45%), 적혈구,
# 평균 혈구내 혈색소 양, 평균 혈구내 헤모글로빈농도, 평균 적혈구 용적크기, 적혈구 용적 분포폭치, 백혈구, 혈소판,
# 호중성과립구, 호염기성 백혈구, 림프구, 프로트롬빈시간, 국제표준화시간, NT-proBNP, 크레아틴 키나아제, 크레아티닌, 요소 질소
# 포도당, 혈중 칼륨, 혈중 나트륨, 혈중 칼슘, 염화물, 음이온차, 마그네슘이온, 산성농도, 탄산수소염, 락트산, 혈중이산화탄소 양, 혈액구출분율
myData = [28, 1, 27, 0, 0, 0, 0, 0, 0, 0, 0,
          0, 80, 160, 70, 20, 36.2, 99, 2000, 44, 3,
          30, 30, 100, 20, 10, 250,
          70, 0.4, 15, 10, 1, 2000, 150, 2, 50,
          115, 5, 138, 8, 100, 13, 2.4, 7.2, 22, 0.5, 40, 55]

result = clf.predict([myData])
print("당신은 %s 할 수 있습니다." % ("사망" if result[0] == 1 else "생존"))

