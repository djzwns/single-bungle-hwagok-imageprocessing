import joblib

clf = joblib.load("heartattack_303_KNN5_69.dmp")

myData = [28, 1, 2, 100, 304, 0, 0, 125, 1, 0.9, 1, 2, 2]
result = clf.predict([myData])

print("당신은 심장병이 %s" % ("맞습니다." if result[0] == 1 else "아닙니다."))
