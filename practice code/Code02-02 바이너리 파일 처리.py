# jpg 파일을 읽어서 처리하고 싶다 --> jpg 파일의 구조를 알아야 함
# 영상처리: 이미지파일 처리 --> 이미지 포맷 중 가장 단순한 포맷 raw
# raw 파일은 grayscale(0~255 까지의 회색영상), 압축x, 1pixel == 1byte

rawFileName = "../images/Etc_Raw(squre)/flower512.raw"
rawFp = open(rawFileName, "rb")

image = []
height, width = 512, 512

for i in range(height):
    tmp = []
    for j in range(width):
        tmp.append(ord(rawFp.read(1)))
    image.append(tmp)

print(image)

# while True:
#     inStr = rawFp.readline()
#     if inStr == '':
#         break
#     print(inStr)

rawFp.close()
