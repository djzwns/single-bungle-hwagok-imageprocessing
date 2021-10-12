# 영상 처리 알고리즘의 분류
"""
    - 화소점 처리: 밝게, 어둡게, 반전, 흑백, 감마, 파라볼라 ...
    - 기하학 처리: 미러링, 축소, 확대, 회전, 이동 ...
    - 화소영역 처리: 블러링, 경계선 추출, 엠보싱, 카툰렌더링, 블룸, 안티앨리어싱 등 주변의 화소에 영향을 받음 -> 고급
    - 히스토그램 처리: 영상 전체 분포를 확인한 후 처리 -> 흑백(평균값)
"""


import math
import os.path
from tkinter import *
from tkinter import messagebox
from tkinter.simpledialog import *
from tkinter.filedialog import *


## function declaration
## -- common functions --
def clamp(_min: int, _max: int, val: int) -> int:
    if _min > _max:
        t = _min
        _min = _max
        _max = t

    return int(max(_min, min(_max, val)))


def malloc2d(h: int, w: int) -> list[list[int]]:
    memory = []
    for i in range(h):
        tmp = []
        for k in range(w):
            tmp.append(0)
        memory.append(tmp)
    return memory


def saveImage():
    pass


def displayImage():
    pass

def openImage():
    global window, filename, inImage, outImage, inH, inW
    # messagebox.showinfo("파일", "열기를 선택함")
    filename = askopenfilename(parent=window, filetypes=(("raw 파일", "*.raw"), ("모든 파일", "*.*")))

    filesize = os.path.getsize(filename)    # 파일의 크기 (byte)
    
    # 중요
    inH = inW = int(math.sqrt(filesize))
    inImage = malloc2d(inH, inW)

    rawFp = open(filename, "rb")

    for i in range(inH):
        for k in range(inW):
            inImage[i][k] = ord(rawFp.read(1))

    rawFp.close()
    equalImage()


def addImage(): # 밝기 조절 알고리즘
    global window, inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상의 크기를 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    outImage = malloc2d(outH, outW)

    value: int = askinteger("밝기/어둡기 조절", "-255~255 사이의 값을 입력해 주세요.", minvalue=-255, maxvalue=255)

    # 진짜 영상처리 알고리즘 구현
    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = clamp(0, 255, inImage[i][k] + value)
    displayImage()


## -- image processing functions --
def equalImage(): # 동일 영상 알고리즘
    global window, inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상의 크기를 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    outImage = malloc2d(outH, outW)
    
    # 진짜 영상처리 알고리즘 구현
    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = inImage[i][k]
    displayImage()


def displayImage():
    global window, canvas, paper, inImage, outImage, inH, inW, outH, outW

    if canvas is not None:
        canvas.destroy()

    window.geometry("{}x{}".format(outW, outH))
    canvas = Canvas(window, height=outH, width=outW)
    canvas.pack()

    paper = PhotoImage(height=outH, width=outW)
    canvas.create_image((outH * 0.5, outW * 0.5), image=paper, state="normal")

    # 느린방식
    # for i in range(outH):
    #     for k in range(outW):
    #         color = outImage[i][k]
    #         paper.put("#%02x%02x%02x" % (color, color, color), (k, i))

    # 빠른방식
    rgbString = ""
    for i in range(outH):
        tmpString = "" # 한 줄 불러오기
        for k in range(outW):
            p = outImage[i][k]
            tmpString += "#%02x%02x%02x  " % (p, p, p)
        rgbString += '{' + tmpString + '}  '
    paper.put(rgbString)


def brightenImage():
    pass


def negativeImage():
    global window, inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상의 크기를 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    outImage = malloc2d(outH, outW)

    # 진짜 영상처리 알고리즘 구현
    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = 255 - inImage[i][k]
    displayImage()


def bw127Image():
    pass


def bwAvgImage():
    pass


def bwMedianImage():
    pass


def zoomImage():
    global window, inImage, outImage, inH, inW, outH, outW
    scale = askfloat("확대/축소", "0.1~4.0 범위의 값을 입력해주세요", minvalue=0.1, maxvalue=4.0)
    # 중요! 출력 영상의 크기를 결정 --> 알고리즘에 의존
    outH = int(inH * scale)
    outW = int(inW * scale)
    outImage = malloc2d(outH, outW)
    for i in range(outH):
        y = clamp(0, inH - 1, i // scale)
        for k in range(outW):
            x = clamp(0, inW - 1, k // scale)

            outImage[i][k] = inImage[y][x]
    displayImage()

## global variables
inImage, inH, inW = None, 0, 0
outImage, outH, outW = None, 0, 0
window, canvas, paper = None, None ,None
filename = ""


## main
window = Tk()
window.title("영상처리 Ver 0.3")
window.geometry("500x300")

mainMenu = Menu(window) # 빈 메뉴 바
window.config(menu=mainMenu)

fileMenu = Menu(mainMenu)
mainMenu.add_cascade(label="file", menu=fileMenu)
fileMenu.add_command(label="Open", command=openImage)
fileMenu.add_command(label="Save", command=None)
fileMenu.add_separator()
fileMenu.add_command(label="Close", command=None)

imageMenu = Menu(mainMenu)
mainMenu.add_cascade(label="화소점처리", menu=imageMenu)
imageMenu.add_command(label="원본", command=equalImage)
imageMenu.add_command(label="밝게/어둡게", command=addImage)
imageMenu.add_command(label="반전", command=negativeImage)
imageMenu.add_command(label="흑백", command=None)

image2Menu = Menu(mainMenu)
mainMenu.add_cascade(label="기하학처리", menu=image2Menu)
image2Menu.add_command(label="미러", command=None)
image2Menu.add_command(label="확대/축소", command=zoomImage)

window.mainloop()