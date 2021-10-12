# data2.txt 읽고 합계 계산
total = 0
inFp = open("data2.txt", "r")

while True:
    inStr = inFp.readline()
    if inStr == '':
        break

    splitStr = inStr.split()
    for i in range(len(splitStr)):
        total += int(splitStr[i])

print("total: ", total)

inFp.close()
