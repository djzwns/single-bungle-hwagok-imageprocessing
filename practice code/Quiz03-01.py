# [영상처리] 메뉴 만들고 >> 밝게/반전/흑백/미러링 등 추가

## import
import copy
import math
from tkinter import *


## function
def initialize(filesize: int, fname: str) -> None:
    global isInitialized, image, height, width, filename, window, canvas, paper
    # image setup
    height = width = int(math.sqrt(filesize)) - 1
    image = malloc2d(height, width)
    filename = fname

    # window setup
    window = Tk()
    window.title("Digital Image Processing Ver 0.2")
    window.geometry("{}x{}".format(width, height + 200))
    window.resizable(width=False, height=False)

    header = Frame(window, width=width, height=height)
    header.grid(row=0, column=0)

    # canvas setup
    canvas = Canvas(header, height=height, width=width)
    canvas.pack()

    # photo image setup
    paper = PhotoImage(height=height, width=width)
    canvas.create_image((height / 2, width / 2), image=paper, state="normal")

    guiBtnInit()

    isInitialized = True


def malloc2d(h: int, w: int) -> list[list[int]]:
    memory = []
    for i in range(h):
        tmp = []
        for k in range(w):
            tmp.append(0)
        memory.append(tmp)
    return memory


def loadImage(fname: str) -> None:
    global image, height, width
    if not isInitialized:
        print("초기화가 안됐음")
        return

    rawFp = open(fname, "rb")
    for i in range(height):
        for k in range(width):
            pixel = ord(rawFp.read(1))
            image[i][k] = pixel

    rawFp.close()


def displayImage(tmpImage: list[list[int]]) -> None:
    global image, height, width, window
    if not isInitialized:
        print("초기화가 안됐음")
        return

    for i in range(height):
        for k in range(width):
            color = tmpImage[i][k]
            # r g b 값을 각각 입력해주는 듯함. grayscale 이미지라서 color 하나로 3채널 똑같이 넣어줌
            paper.put("#%02x%02x%02x" % (color, color, color), (k, i))


def guiBtnInit():
    global window, width, height

    mainMenu = Menu(window)
    window.config(menu=mainMenu)

    imageMenu = Menu(mainMenu)
    mainMenu.add_cascade(label="영상처리", menu=imageMenu)
    imageMenu.add_command(label="밝게", command=lambda: displayImage(brightnessImage(50)))
    imageMenu.add_command(label="반전", command=lambda: displayImage(reverseImage()))
    imageMenu.add_command(label="흑백127", command=lambda: displayImage(bw127Image()))
    imageMenu.add_command(label="상하반전", command=lambda: displayImage(mirrorTopBottom()))

    footer = Frame(window, width=width, height=200)
    footer.grid(row=1, column=0)

    btn_orig = Button(footer, text="원본", command=lambda: displayImage(image))
    btn_orig.grid(row=0, column=0)

    btn_reverse = Button(footer, text="반전", command=lambda: displayImage(reverseImage()))
    btn_reverse.grid(row=0, column=1)

    btn_bw127 = Button(footer, text="흑백127", command=lambda: displayImage(bw127Image()))
    btn_bw127.grid(row=1, column=0)

    btn_bwAvg = Button(footer, text="흑백평균", command=lambda: displayImage(bwAvgImage()))
    btn_bwAvg.grid(row=1, column=1)

    btn_bwMed = Button(footer, text="흑백중위", command=lambda: displayImage(bwMedianImage()))
    btn_bwMed.grid(row=1, column=2)

    btn_lr = Button(footer, text="좌우", command=lambda: displayImage(mirrorLeftRight()))
    btn_lr.grid(row=2, column=0)

    btn_tb = Button(footer, text="상하", command=lambda: displayImage(mirrorTopBottom()))
    btn_tb.grid(row=2, column=1)

    btn_para = Button(footer, text="파라볼라", command=lambda: displayImage(parabolaCorrection()))
    btn_para.grid(row=2, column=2)

    btn_solar = Button(footer, text="솔라라이즈", command=lambda: displayImage(solarizingCorrection()))
    btn_solar.grid(row=2, column=3)

    text_gamma = StringVar()
    text_gamma_entry = Entry(footer, width=5, textvariable=text_gamma)
    text_gamma_entry.grid(row=3, column=0)
    btn_gamma = Button(footer, text="감마", command=lambda: displayImage(gammaCorrection(float(text_gamma.get()))))
    btn_gamma.grid(row=3, column=1)

    text_zoom = StringVar()
    text_zoom_entry = Entry(footer, width=5, textvariable=text_zoom)
    text_zoom_entry.grid(row=4, column=0)
    btn_zoom = Button(footer, text="확대축소", command=lambda: displayImage(zoomImage(float(text_zoom.get()))))
    btn_zoom.grid(row=4, column=1)

    text_move = StringVar()
    text_move_entry = Entry(footer, width=5, textvariable=text_move)
    text_move_entry.grid(row=5, column=0)
    btn_move = Button(footer, text="이동", command=lambda: displayImage(moveImage(int(text_move.get()))))
    btn_move.grid(row=5, column=1)


# clamp 함수: 최소 최대값 넘어가면 잘라줌
# ex) clamp(0, 255, color) -> color 값을 0~255 범위로 잘라준다
def clamp(_min: int, _max: int, val: int) -> int:
    if _min > _max:
        t = _min
        _min = _max
        _max = t

    return int(max(_min, min(_max, val)))


# -- image processing function --
# 원본 이미지가 훼손되는 것이 싫어서 image 유지한 상태로 이미지를 새로 만드는 방향으로 구현함
# 밝기, 반전, 흑백(127, 평균, 중위값), 상하, 좌우 반전
def brightnessImage(value: int) -> list[list[int]]:
    global image, height, width
    tmp = malloc2d(height, width)

    for i in range(height):
        for k in range(width):
            color = image[i][k] + value
            tmp[i][k] = clamp(0, 255, color)
    return tmp


def reverseImage() -> list[list[int]]:
    global image, height, width
    tmp = malloc2d(height, width)

    for i in range(height):
        for k in range(width):
            tmp[i][k] = 255 - image[i][k]
    return tmp


def bw127Image() -> list[list[int]]:
    global image, height, width
    tmp = malloc2d(height, width)

    for i in range(height):
        for k in range(width):
            tmp[i][k] = 0 if image[i][k] < 127 else 255
    return tmp


def bwAvgImage() -> list[list[int]]:
    global image, height, width
    tmp = malloc2d(height, width)
    hap = 0
    avg = 0

    for i in range(height):
        for k in range(width):
            hap += image[i][k]

    avg = hap // (height * width)
    for i in range(height):
        for k in range(width):
            tmp[i][k] = 0 if image[i][k] < avg else 255
    return tmp


def bwMedianImage() -> list[list[int]]:
    global image, height, width
    tmp = malloc2d(height, width)

    # 원본 훼손 없이 정렬하기 위한 깊은 복사
    sortTmp = copy.deepcopy(image)
    sortTmp.sort()

    # 대충 중간 값
    median = sortTmp[width // 2][height // 2]
    for i in range(height):
        for k in range(width):
            tmp[i][k] = 0 if image[i][k] < median else 255
    return tmp


def mirrorLeftRight() -> list[list[int]]:
    global image, height, width
    tmp = malloc2d(height, width)

    for i in range(height):
        for k in range(width):
            tmp[i][k] = image[i][width - k - 1]
    return tmp


def mirrorTopBottom() -> list[list[int]]:
    global image, height, width
    tmp = malloc2d(height, width)

    for i in range(height):
        for k in range(width):
            tmp[i][k] = image[height - i - 1][k]
    return tmp


def gammaCorrection(gamma: float) -> list[list[int]]:
    global image, height, width
    tmp = malloc2d(height, width)

    for i in range(height):
        for k in range(width):
            color = int(image[i][k] * gamma)
            tmp[i][k] = clamp(0, 255, color)
    return tmp


def parabolaCorrection() -> list[list[int]]:
    global image, height, width
    tmp = malloc2d(height, width)

    for i in range(height):
        for k in range(width):
            color = int(255 * (image[i][k] / 128 - 1) * 2)
            tmp[i][k] = clamp(0, 255, color)
    return tmp


# 파라볼라 반전 효과랑 같음
def solarizingCorrection() -> list[list[int]]:
    global image, height, width
    tmp = malloc2d(height, width)

    for i in range(height):
        for k in range(width):
            color = int(255 - 255 * (image[i][k] / 128 - 1) * 2)
            tmp[i][k] = clamp(0, 255, color)
    return tmp


def zoomImage(zoom: float) -> list[list[int]]:
    global image, height, width
    tmp = malloc2d(height, width)
    maxX = (width - 1) * zoom
    maxY = (height - 1) * zoom
    for i in range(height):
        y = clamp(0, height - 1, i // zoom)
        for k in range(width):
            x = clamp(0, width - 1, k // zoom)

            # 범위 초과시 색 추가 안함
            if k > maxX or i > maxY:
                continue

            tmp[i][k] = image[y][x]
    return tmp


def moveImage(offset: int) -> list[list[int]]:
    global image, height, width
    tmp = malloc2d(height, width)
    for i in range(height):
        y = clamp(0, height - 1, i + offset)
        for k in range(width):
            x = clamp(0, width - 1, k + offset)
            if i < 0 or i >= height or k < 0 or k >= width:
                continue
            tmp[y][x] = image[i][k]
    return tmp


## global variable
isInitialized: bool = False
image: list[list[int]]
height: int
width: int
filename: str

# image sample path
citrus: str = "./Citrus256.raw"
lena: str = "./LENA256.RAW"

window: Tk
canvas: Canvas
paper: PhotoImage

## main
initialize(filesize=66536, fname=lena)
loadImage(fname=filename)

window.mainloop()
