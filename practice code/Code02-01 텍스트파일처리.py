# 파일의 종류: 텍스트파일, 이진파일
# 텍스트파일 : 메모장에서 열었을 때 글자가 보이는 파일, *.txt *.c *.cpp 등..
#   - 1byte 씩 의미가 있음(한 글자 한 글자 끊어짐)
# 이진파일(binary file): 비트에 의미가 있음 *.hwp, *.bmp ...
#   - ex: 2bit 글자 색상, 7bit 글자 폰트, 12bit 글자모양, 4bit 글자

# 파일 처리 3단계
# 파일 열기 - 읽기/쓰기 - 파일 닫기

# 1단계 파일열기
inFp = open("c:/windows/win.ini", "r")

# 2단계
while True:
    inStr = inFp.readline()
    if inStr == '':
        break
    print(inStr, end='')

# 3단계 파일닫기
inFp.close()
