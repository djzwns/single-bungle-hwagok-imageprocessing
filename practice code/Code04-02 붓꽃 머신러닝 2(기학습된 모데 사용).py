# 기 학습된 모델(Pre-Trained Model)을 불러와서 예측하기
import joblib
clf = joblib.load("iris_150_KNN3_96.dmp")

myData = [4.8, 3.3, 1.3, 0.3]
result = clf.predict([myData])
print("이 꽃은 %s 입니다." % (result[0]))
