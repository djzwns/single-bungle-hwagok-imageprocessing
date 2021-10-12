# data.txt 파일 읽어서 합계 계산하고 출력

total = 0

inFp = open("data.txt", "r")

while True:
    inStr = inFp.readline()
    if inStr == '':
        break
    total += int(inStr)

print(total)

inFp.close()
