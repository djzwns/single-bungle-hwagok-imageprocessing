""" 구현 요구 사항

    * 영상처리 프로그램 (Ver 0.4) 완성하기 -> 처음부터 만들 것
        - 화소점 처리: 밝게/어둡게, 반전, 흑백(입력), 흑백(평균), 흑백(중앙값), 감마, 파라볼라
        - 기하학 처리: 미러링(상하), 미러링(좌우), 축소, 확대(기본, 이웃화소보간), 이동, 회전
        - 화소영역 처리: 블러링, 엠보싱, 샤프닝, 경계선 검출
"""

# import --------------------------
import copy
import math
import os.path
from tkinter import *
from tkinter import messagebox
from tkinter.simpledialog import *
from tkinter.filedialog import *
import cv2
import numpy as np


# functions -----------------------
# common function
def clamp(_min: int, _max: int, val: int) -> int:  # val 값을 _min~_max 사이의 값으로 잘라주는 함수
    if _min > _max:
        t = _min
        _min = _max
        _max = t

    return int(max(_min, min(_max, val)))


def malloc2d(h: int, w: int):  # 이미지 크기 만큼 메모리 구성
    memory = []
    for i in range(h):
        tmp = []
        for k in range(w):
            tmp.append(0)
        memory.append(tmp)
    return memory


def openImage() -> None:  # 이미지를 여는 함수
    global window, inH, inW, filename, inCvImage, outCvImage
    global inImageR, inImageG, inImageB, outImageR, outImageG, outImageB

    # 이미지 파일 경로 불러오기
    filename = askopenfilename(parent=window,
                               filetypes=(("이미지 파일", "*.jpg;*.jpeg;*.png;*.bmp;*.tif;*.tiff;*.raw"), ("모든 파일", "*.*")))

    print(filename)
    # opencv 개체
    inCvImage = cv2.imread(filename)

    # 입력 이미지의 폭, 높이 알아내기
    inH = inCvImage.shape[0]
    inW = inCvImage.shape[1]

    # 원본 이미지 초기 설정
    inImageR = malloc2d(inH, inW)
    inImageG = malloc2d(inH, inW)
    inImageB = malloc2d(inH, inW)

    # 실제 이미지 등록 과정
    for i in range(inH):
        for k in range(inW):
            inImageR[i][k] = inCvImage.item(i, k, 2)
            inImageG[i][k] = inCvImage.item(i, k, 1)
            inImageB[i][k] = inCvImage.item(i, k, 0)

    # 생성된 이미지 그레이 스케일 미리 만들기
    grayScale()

    # 이미지 불러오면 메뉴바 추가 설정
    guiMenuInit()

    # outImage 로 이미지 데이터 복사 후 출력
    equalImage()


def saveImage() -> None:
    global window, inH, inW, filename, inCvImage, outCvImage
    global inImageR, inImageG, inImageB, outImageR, outImageG, outImageB

    # opencv 개체 준비, 3차원 배열. 모두 0으로 채움
    saveCvImage = np.zeros((outH, outW, 3), np.uint8)

    # 출력 이미지 --> 넘파이 배열
    for i in range(outH):
        for k in range(outW):
            # python tuple ((37, 240, 55))
            saveCvImage[i, k] = tuple(([outImageB[i][k], outImageG[i][k], outImageR[i][k]]))

    savename = asksaveasfile(parent=window, mode="wb", defaultextension='.',
                             filetypes=(("이미지 파일", "*.jpg;*.jpeg;*.png;*.bmp;*.tif;*.tiff;*.raw"), ("모든 파일", "*.*")))

    cv2.imwrite(savename.name, saveCvImage)
    messagebox.showinfo("저장 성공", savename.name + "가 저장됨")


def displayImage() -> None:
    global window, canvas, paper, filename, imageName
    global outH, outW
    global outImageR, outImageG, outImageB
    if canvas is not None:
        canvas.destroy()

    # window, canvas, paper 이미지에 맞게 설정
    window.geometry("{}x{}".format(outW, outH))
    canvas = Canvas(window, width=outW, height=outH)
    canvas.pack()

    paper = PhotoImage(width=outW, height=outH)
    filenamesplit = filename.split('/')
    string = filenamesplit[len(filenamesplit) - 1] + "({}x{})".format(outW, outH)
    strsize = len(string)
    canvas.create_image((outW * 0.5, outH * 0.5), image=paper, state="normal")
    txt = canvas.create_text((strsize + 100, 15), text=string, fill="lightblue", font=("", 15))
    box = canvas.create_rectangle(canvas.bbox(txt), fill="black")
    canvas.tag_lower(box, txt)

    # 이미지 로드
    rgbString = ""
    for i in range(outH):
        tmpString = ""  # 한 줄 불러오기
        for k in range(outW):
            r = outImageR[i][k]
            g = outImageG[i][k]
            b = outImageB[i][k]
            tmpString += "#%02x%02x%02x  " % (r, g, b)
        rgbString += '{' + tmpString + '}  '
    paper.put(rgbString)


def guiInit(width: int = 300, height: int = 300, title: str = "") -> None:  # gui 초기화
    global window, canvas, paper, mainMenu

    window = Tk()
    window.geometry("{}x{}".format(width, height))
    window.title(title)
    window.resizable(False, False)

    mainMenu = Menu(window)  # 빈 메뉴 바
    window.config(menu=mainMenu)

    fileMenu = Menu(mainMenu)
    mainMenu.add_cascade(label="파일", menu=fileMenu)
    fileMenu.add_command(label="열기", command=openImage)
    fileMenu.add_command(label="저장", command=saveImage)
    fileMenu.add_separator()
    fileMenu.add_command(label="닫기", command=None)


def guiMenuInit() -> None:  # 추가적인 메뉴바를 설정한다
    global mainMenu, guiInitialized

    if guiInitialized is True:
        return

    # 화소점 처리 메뉴
    imageMenu = Menu(mainMenu)
    mainMenu.add_cascade(label="화소점처리", menu=imageMenu)
    imageMenu.add_command(label="원본", command=equalImage)
    imageMenu.add_command(label="밝게/어둡게", command=brightenImage)
    imageMenu.add_command(label="반전", command=negativeImage)
    imageMenu.add_command(label="그레이스케일", command=grayScaleImage)
    imageMenu.add_command(label="흑백(입력)", command=bwImage)
    imageMenu.add_command(label="흑백(평균)", command=bwAvgImage)
    imageMenu.add_command(label="흑백(중앙값)", command=bwMedianImage)
    imageMenu.add_command(label="감마", command=gammaImage)
    imageMenu.add_command(label="파라볼라", command=parabolaImage)

    # 기하학 처리 메뉴
    image2Menu = Menu(mainMenu)
    mainMenu.add_cascade(label="기하학처리", menu=image2Menu)
    image2Menu.add_command(label="미러(상하)", command=mirrorTopBottom)
    image2Menu.add_command(label="미러(좌우)", command=mirrorLeftRight)
    image2Menu.add_command(label="확대/축소(기본)", command=zoomImage)
    image2Menu.add_command(label="확대/축소(보간)", command=zoomInterpolaration)
    image2Menu.add_command(label="이동", command=moveImage)
    image2Menu.add_command(label="회전", command=rotateImage)

    # 화소영역 처리 메뉴
    image3Menu = Menu(mainMenu)
    mainMenu.add_cascade(label="화소영역 처리", menu=image3Menu)
    image3Menu.add_command(label="블러링", command=blurImage)
    image3Menu.add_command(label="엠보싱", command=embossingImage)
    image3Menu.add_command(label="샤프닝", command=sharpeningImage)
    image3Menu.add_command(label="경계선 검출", command=edgeDetectionImage)

    guiInitialized = True


# image processing function -------
def equalImage() -> None:  # 원본 이미지를 복사 후 출력
    global inH, inW, outH, outW, inCvImage, outCvImage
    global inImageR, inImageG, inImageB, outImageR, outImageG, outImageB

    # outImage 초기 설정
    outW = inW
    outH = inH
    outImageR = malloc2d(outH, outW)
    outImageG = malloc2d(outH, outW)
    outImageB = malloc2d(outH, outW)

    for i in range(outH):
        for k in range(outW):
            outImageR[i][k] = inImageR[i][k]
            outImageG[i][k] = inImageG[i][k]
            outImageB[i][k] = inImageB[i][k]
    displayImage()


def brightenImage() -> None:  # 밝게/어둡게 처리
    global inH, inW, outH, outW, inCvImage, outCvImage
    global inImageR, inImageG, inImageB, outImageR, outImageG, outImageB

    # outImage 초기 설정
    outW = inW
    outH = inH
    outImageR = malloc2d(outH, outW)
    outImageG = malloc2d(outH, outW)
    outImageB = malloc2d(outH, outW)

    value = askinteger("밝게/어둡게", "조정하고 싶은 값을 입력해주세요(-255~255)", minvalue=-255, maxvalue=255)

    for i in range(outH):
        for k in range(outW):
            outImageR[i][k] = clamp(0, 255, inImageR[i][k] + value)
            outImageG[i][k] = clamp(0, 255, inImageG[i][k] + value)
            outImageB[i][k] = clamp(0, 255, inImageB[i][k] + value)
    displayImage()


def negativeImage() -> None:  # 이미지 반전
    global inH, inW, outH, outW, inCvImage, outCvImage
    global inImageR, inImageG, inImageB, outImageR, outImageG, outImageB

    # outImage 초기 설정
    outW = inW
    outH = inH
    outImageR = malloc2d(outH, outW)
    outImageG = malloc2d(outH, outW)
    outImageB = malloc2d(outH, outW)

    for i in range(outH):
        for k in range(outW):
            outImageR[i][k] = 255 - inImageR[i][k]
            outImageG[i][k] = 255 - inImageG[i][k]
            outImageB[i][k] = 255 - inImageB[i][k]
    displayImage()


def grayScale() -> None:  # 그레이스케일 값 만들기
    global inH, inW, grayscale
    global inImageR, inImageG, inImageB

    # grayscale 초기 설정
    grayscale = malloc2d(inH, inW)

    for i in range(inH):
        for k in range(inW):
            grayscale[i][k] = int((inImageR[i][k] + inImageG[i][k] + inImageB[i][k]) / 3)


def grayScaleImage() -> None:
    global inH, inW, outH, outW, inCvImage, outCvImage
    global inImageR, inImageG, inImageB, outImageR, outImageG, outImageB

    # outImage 초기 설정
    outW = inW
    outH = inH
    outImageR = malloc2d(outH, outW)
    outImageG = malloc2d(outH, outW)
    outImageB = malloc2d(outH, outW)

    for i in range(outH):
        for k in range(outW):
            outImageR[i][k] = grayscale[i][k]
            outImageG[i][k] = grayscale[i][k]
            outImageB[i][k] = grayscale[i][k]
    displayImage()


def bwImage() -> None:  # 이미지 흑백 처리
    global inH, inW, outH, outW, grayscale
    global inImageR, inImageG, inImageB, outImageR, outImageG, outImageB

    # outImage 초기 설정
    outW = inW
    outH = inH
    outImageR = malloc2d(outH, outW)
    outImageG = malloc2d(outH, outW)
    outImageB = malloc2d(outH, outW)

    value = askinteger("흑백 처리", "기준값을 입력해주세요(0~255)", minvalue=0, maxvalue=255)

    for i in range(outH):
        for k in range(outW):
            bwColor = 0 if grayscale[i][k] < value else 255
            outImageR[i][k] = bwColor
            outImageG[i][k] = bwColor
            outImageB[i][k] = bwColor
    displayImage()


def bwAvgImage() -> None:  # 이미지 흑백 처리(평균)
    global inH, inW, outH, outW, grayscale
    global inImageR, inImageG, inImageB, outImageR, outImageG, outImageB

    # outImage 초기 설정
    outW = inW
    outH = inH
    outImageR = malloc2d(outH, outW)
    outImageG = malloc2d(outH, outW)
    outImageB = malloc2d(outH, outW)

    avg = 0
    for i in range(inH):
        for k in range(inW):
            avg += grayscale[i][k]
    avg //= (inH * inW)

    for i in range(outH):
        for k in range(outW):
            bwAvgColor = 0 if grayscale[i][k] < avg else 255
            outImageR[i][k] = bwAvgColor
            outImageG[i][k] = bwAvgColor
            outImageB[i][k] = bwAvgColor
    displayImage()


def bwMedianImage() -> None:  # 이미지 흑백 처리(중앙값)
    global inH, inW, outH, outW, grayscale
    global inImageR, inImageG, inImageB, outImageR, outImageG, outImageB

    # outImage 초기 설정
    outW = inW
    outH = inH
    outImageR = malloc2d(outH, outW)
    outImageG = malloc2d(outH, outW)
    outImageB = malloc2d(outH, outW)

    tmp = copy.deepcopy(grayscale)
    tmp.sort()
    medianColor = tmp[outH // 2][outW // 2]

    for i in range(outH):
        for k in range(outW):
            median = 0 if grayscale[i][k] < medianColor else 255
            outImageR[i][k] = median
            outImageG[i][k] = median
            outImageB[i][k] = median
    displayImage()


def gammaImage() -> None:  # 이미지 감마 보정
    global inH, inW, outH, outW
    global inImageR, inImageG, inImageB, outImageR, outImageG, outImageB

    # outImage 초기 설정
    outW = inW
    outH = inH
    outImageR = malloc2d(outH, outW)
    outImageG = malloc2d(outH, outW)
    outImageB = malloc2d(outH, outW)

    gamma = askfloat("감마 보정", "감마 값을 입력해주세요. (0.1~2.4)", minvalue=0.1, maxvalue=2.4)

    for i in range(outH):
        for k in range(outW):
            r = int(inImageR[i][k] * gamma)
            g = int(inImageG[i][k] * gamma)
            b = int(inImageB[i][k] * gamma)
            outImageR[i][k] = clamp(0, 255, r)
            outImageG[i][k] = clamp(0, 255, g)
            outImageB[i][k] = clamp(0, 255, b)
    displayImage()


def parabolaImage() -> None:  # 이미지 파라볼라 처리
    global inH, inW, outH, outW
    global inImageR, inImageG, inImageB, outImageR, outImageG, outImageB

    # outImage 초기 설정
    outW = inW
    outH = inH
    outImageR = malloc2d(outH, outW)
    outImageG = malloc2d(outH, outW)
    outImageB = malloc2d(outH, outW)

    for i in range(outH):
        for k in range(outW):
            r = int(255 * (inImageR[i][k] / 128 - 1) * 2)
            g = int(255 * (inImageG[i][k] / 128 - 1) * 2)
            b = int(255 * (inImageB[i][k] / 128 - 1) * 2)
            outImageR[i][k] = clamp(0, 255, r)
            outImageG[i][k] = clamp(0, 255, g)
            outImageB[i][k] = clamp(0, 255, b)
    displayImage()


def mirrorTopBottom() -> None:  # 상하 반전
    global inH, inW, outH, outW
    global inImageR, inImageG, inImageB, outImageR, outImageG, outImageB

    # outImage 초기 설정
    outW = inW
    outH = inH
    outImageR = malloc2d(outH, outW)
    outImageG = malloc2d(outH, outW)
    outImageB = malloc2d(outH, outW)

    for i in range(outH):
        for k in range(outW):
            outImageR[i][k] = inImageR[inH - i - 1][k]
            outImageG[i][k] = inImageG[inH - i - 1][k]
            outImageB[i][k] = inImageB[inH - i - 1][k]
    displayImage()


def mirrorLeftRight() -> None:  # 좌우 반전
    global inH, inW, outH, outW
    global inImageR, inImageG, inImageB, outImageR, outImageG, outImageB

    # outImage 초기 설정
    outW = inW
    outH = inH
    outImageR = malloc2d(outH, outW)
    outImageG = malloc2d(outH, outW)
    outImageB = malloc2d(outH, outW)

    for i in range(outH):
        for k in range(outW):
            outImageR[i][k] = inImageR[i][inW - k - 1]
            outImageG[i][k] = inImageG[i][inW - k - 1]
            outImageB[i][k] = inImageB[i][inW - k - 1]
    displayImage()


def zoomImage() -> None:  # 확대/축소 기본
    global inH, inW, outH, outW
    global inImageR, inImageG, inImageB, outImageR, outImageG, outImageB

    scale = askfloat("확대/축소 기본 보정", "확대/축소 비율을 입력해주세요(0.1~4.0)", minvalue=0.1, maxvalue=4.0)

    # outImage 초기 설정
    outW = int(inW * scale)
    outH = int(inH * scale)
    outImageR = malloc2d(outH, outW)
    outImageG = malloc2d(outH, outW)
    outImageB = malloc2d(outH, outW)

    for i in range(outH):
        y = clamp(0, inH - 1, i // scale)
        for k in range(outW):
            x = clamp(0, inW - 1, k // scale)
            outImageR[i][k] = inImageR[y][x]
            outImageG[i][k] = inImageG[y][x]
            outImageB[i][k] = inImageB[y][x]
    displayImage()


def zoomInterpolaration() -> None:  # 확대/축소 보간
    global inH, inW, outH, outW
    global inImageR, inImageG, inImageB, outImageR, outImageG, outImageB
    i_h, i_w = [0] * 2
    color = 0
    r_h, r_w, s_h, s_w = [0] * 4
    c1, c2, c3, c4 = [0] * 4
    scale = askfloat("확대/축소 보간 보정", "확대/축소 비율을 입력해주세요(0.1~4.0)", minvalue=0.1, maxvalue=4.0)

    # outImage 초기 설정
    outW = int(inW * scale)
    outH = int(inH * scale)
    outImageR = malloc2d(outH, outW)
    outImageG = malloc2d(outH, outW)
    outImageB = malloc2d(outH, outW)

    for i in range(outH):
        for k in range(outW):
            r_h = i / scale
            r_w = k / scale
            i_h = int(r_h)
            i_w = int(r_w)
            s_h = r_h - i_h
            s_w = r_w - i_w

            if i_h < 0 or i_h >= (inH - 1) or i_w < 0 or i_w >= (inW - 1):
                outImageR[i][k] = 255
                outImageG[i][k] = 255
                outImageB[i][k] = 255
            else:
                c1 = inImageR[i_h][i_w]
                c2 = inImageR[i_h][i_w + 1]
                c3 = inImageR[i_h + 1][i_w + 1]
                c4 = inImageR[i_h + 1][i_w]
                color = (c1 * (1 - s_h) * (1 - s_w) + c2 * s_w * (1 - s_h) + c3 * s_w * s_h + c4 * (1 - s_w) * s_h)
                outImageR[i][k] = int(color)

                c1 = inImageG[i_h][i_w]
                c2 = inImageG[i_h][i_w + 1]
                c3 = inImageG[i_h + 1][i_w + 1]
                c4 = inImageG[i_h + 1][i_w]
                color = (c1 * (1 - s_h) * (1 - s_w) + c2 * s_w * (1 - s_h) + c3 * s_w * s_h + c4 * (1 - s_w) * s_h)
                outImageG[i][k] = int(color)

                c1 = inImageB[i_h][i_w]
                c2 = inImageB[i_h][i_w + 1]
                c3 = inImageB[i_h + 1][i_w + 1]
                c4 = inImageB[i_h + 1][i_w]
                color = (c1 * (1 - s_h) * (1 - s_w) + c2 * s_w * (1 - s_h) + c3 * s_w * s_h + c4 * (1 - s_w) * s_h)
                outImageB[i][k] = int(color)

    displayImage()


def moveImage() -> None:  # 이미지 이동
    global inH, inW, outH, outW
    global inImageR, inImageG, inImageB, outImageR, outImageG, outImageB

    # outImage 초기 설정
    outW = inW
    outH = inH
    outImageR = malloc2d(outH, outW)
    outImageG = malloc2d(outH, outW)
    outImageB = malloc2d(outH, outW)

    offset: str = askstring("이동 처리", "이동값 입력해주세요(123 123)")
    offsetSplit = offset.split(sep=' ')
    if len(offsetSplit) != 2:
        messagebox.showerror(title="입력값이 올바르지 않습니다", message="x y 띄어쓰기 구분 필요")
    offsetx = int(offsetSplit[0])
    offsety = int(offsetSplit[1])

    # 이동
    for i in range(outH):
        y = clamp(0, outH - 1, i + offsety)
        for k in range(outW):
            x = clamp(0, outW - 1, k + offsetx)
            outImageR[y][x] = inImageR[i][k]
            outImageG[y][x] = inImageG[i][k]
            outImageB[y][x] = inImageB[i][k]
    displayImage()


def rotateImage() -> None:  # 이미지 회전
    global inH, inW, outH, outW
    global inImageR, inImageG, inImageB, outImageR, outImageG, outImageB
    # <x*cos0 - y*sin0, x*sin0 + y*cos0>
    # <(x-offsetx)*cos0 - (y-offsety)*sin0+offsetx), (x-offsetx)*sin0 + (y-offsety)*cos0+offsety)>

    outW = inW
    outH = inH
    outImageR = malloc2d(outH, outW)
    outImageG = malloc2d(outH, outW)
    outImageB = malloc2d(outH, outW)

    rotation = askfloat("회전", "회전값 입력", minvalue=-360, maxvalue=360)
    radian = math.radians(rotation)
    offsetx = int(outW * 0.5)
    offsety = int(outH * 0.5)

    for i in range(outH):
        for k in range(outW):
            x = int(((k - offsetx) * math.cos(radian)) - ((i - offsety) * math.sin(radian)) + offsetx)
            y = int(((k - offsetx) * math.sin(radian)) + ((i - offsety) * math.cos(radian)) + offsety)
            if x < 0: continue
            if x >= outW: continue
            if y < 0: continue
            if y >= outH: continue

            outImageR[y][x] = inImageR[i][k]
            outImageG[y][x] = inImageG[i][k]
            outImageB[y][x] = inImageB[i][k]

    # 회전 중에 생기는 홀, 오버랩 현상 처리
    for i in range(outH):
        for k in range(outW):
            if k == 0:
                right_pixR = outImageR[i][k + 1]
                right_pixG = outImageG[i][k + 1]
                right_pixB = outImageB[i][k + 1]
                left_pixR = right_pixR
                left_pixG = right_pixG
                left_pixB = right_pixB
            elif k == outW - 1:
                left_pixR = outImageR[i][k - 1]
                left_pixG = outImageG[i][k - 1]
                left_pixB = outImageB[i][k - 1]
                right_pixR = left_pixR
                right_pixG = left_pixG
                right_pixB = left_pixB
            else:
                left_pixR = outImageR[i][k - 1]
                left_pixG = outImageG[i][k - 1]
                left_pixB = outImageB[i][k - 1]
                right_pixR = outImageR[i][k + 1]
                right_pixG = outImageG[i][k + 1]
                right_pixB = outImageB[i][k + 1]

            if outImageR[i][k] == 0 and left_pixR != 0 and right_pixR != 0:
                outImageR[i][k] = int((left_pixR + right_pixR) * 0.5)
            if outImageG[i][k] == 0 and left_pixG != 0 and right_pixG != 0:
                outImageG[i][k] = int((left_pixG + right_pixG) * 0.5)
            if outImageB[i][k] == 0 and left_pixB != 0 and right_pixB != 0:
                outImageB[i][k] = int((left_pixB + right_pixB) * 0.5)
    displayImage()


def blurImage() -> None:  # 이미지 블러 효과
    global inH, inW, outH, outW
    global inImageR, inImageG, inImageB, outImageR, outImageG, outImageB

    outW = inW
    outH = inH
    outImageR = malloc2d(outH, outW)
    outImageG = malloc2d(outH, outW)
    outImageB = malloc2d(outH, outW)

    filter = askinteger("블러 필터 크기 지정", "필터의 크기를 입력해주세요(2~9)", minvalue=2, maxvalue=9)
    minf = -(filter // 2)
    maxf = filter - (filter // 2)

    # blur filter
    kernel = []
    # 필터내의 가중치 계산, 가우시안 필터의 경우는 중간으로 갈수록 가중치가 높다고 한다. 여기서는 그냥 골고루 분포
    v = 1 / (filter ** 2)
    for i in range(filter):
        tmp = []
        for k in range(filter):
            tmp.append(v)
        kernel.append(tmp)

    # 블러 처리 과정
    for y in range(1, outH - 1):
        for x in range(1, outW - 1):
            r, g, b = 0, 0, 0
            # filter 를 통해서 해당 영역의 평균값을 구함
            for ky in range(minf, maxf):
                for kx in range(minf, maxf):
                    kky = clamp(0, outH - 1, y + ky)
                    kkx = clamp(0, outW - 1, x + kx)
                    valR = inImageR[kky][kkx]
                    r += (kernel[ky + 1][kx + 1] * valR)
                    valG = inImageG[kky][kkx]
                    g += (kernel[ky + 1][kx + 1] * valG)
                    valB = inImageB[kky][kkx]
                    b += (kernel[ky + 1][kx + 1] * valB)
            outImageR[y][x] = int(r)
            outImageG[y][x] = int(g)
            outImageB[y][x] = int(b)

    displayImage()


def embossingImage() -> None:  # 이미지 엠보싱 효과
    global inH, inW, outH, outW
    global inImageR, inImageG, inImageB, outImageR, outImageG, outImageB

    outW = inW
    outH = inH
    outImageR = malloc2d(outH, outW)
    outImageG = malloc2d(outH, outW)
    outImageB = malloc2d(outH, outW)

    mask = [
        [-2, -1, 0],
        [-1, 1, 1],
        [0, 1, 2]
    ]
    emboss = 3

    for i in range(1, outH - 1):
        for j in range(1, outW - 1):
            hapR, hapG, hapB = 0, 0, 0
            for k in range(3):
                for m in range(3):
                    y = clamp(0, outH - 1, i - ((2 >> 1) >> 1) + k)
                    x = clamp(0, outW - 1, j - ((2 >> 1) >> 1) + m)
                    hapR += inImageR[y][x] * mask[k][m]
                    hapG += inImageG[y][x] * mask[k][m]
                    hapB += inImageB[y][x] * mask[k][m]
            hapR /= emboss
            hapR = clamp(0, 255, int(hapR + 128))
            outImageR[i][j] = hapR
            hapG /= emboss
            hapG = clamp(0, 255, int(hapG + 128))
            outImageG[i][j] = hapG
            hapB /= emboss
            hapB = clamp(0, 255, int(hapB + 128))
            outImageB[i][j] = hapB

    displayImage()


def maskFilterCalc(origImg, mask, y, x):
    return mask[0][0] * origImg[y - 1][x - 1] + mask[0][1] * origImg[y - 1][x] + mask[0][2] * origImg[y - 1][x + 1] \
    + mask[1][0] * origImg[y][x - 1] + mask[1][1] * origImg[y][x] + mask[1][2] * origImg[y][x + 1] \
    + mask[2][0] * origImg[y + 1][x - 1] + mask[2][1] * origImg[y + 1][x] + mask[2][2] * origImg[y + 1][x + 1]


def sharpeningImage() -> None:  # 이미지 샤픈 효과
    global inH, inW, outH, outW
    global inImageR, inImageG, inImageB, outImageR, outImageG, outImageB

    outW = inW
    outH = inH
    outImageR = malloc2d(outH, outW)
    outImageG = malloc2d(outH, outW)
    outImageB = malloc2d(outH, outW)

    masknum = askinteger("샤픈 마스크 번호입력", "마스크 번호를 입력해주세요(0~5)", minvalue=0, maxvalue=5)

    masks = [
        [  # mask 0
            [1, -2, 1],
            [-2, 5, -2],
            [1, -2, 1]
        ],
        [  # mask 1
            [0, -1, 0],
            [-1, 5, -1],
            [0, -1, 0]
        ],
        [  # mask 2
            [-1, -1, -1],
            [-1, 9, -1],
            [-1, -1, -1]
        ],
        [  # mask 3
            [1, 1, 1],
            [1, -7, 1],
            [1, 1, 1]
        ],
        [  # mask 4
            [0, -1 / 6, 0],
            [-1 / 6, 10 / 6, -1 / 6],
            [0, -1 / 6, 0]
        ],
        [  # mask 5
            [0, -1 / 4, 0],
            [-1 / 4, 8 / 4, -1 / 4],
            [0, -1 / 4, 0]
        ]
    ]

    mask = masks[masknum]

    for i in range(1, outH - 1):
        for k in range(1, outW - 1):
            outImageR[i][k] = clamp(0, 255, maskFilterCalc(inImageR, mask, i, k))
            outImageG[i][k] = clamp(0, 255, maskFilterCalc(inImageG, mask, i, k))
            outImageB[i][k] = clamp(0, 255, maskFilterCalc(inImageB, mask, i, k))

    displayImage()


def edgeDetectionImage() -> None:  # 이미지 경계선 검출
    global inH, inW, outH, outW
    global inImageR, inImageG, inImageB, outImageR, outImageG, outImageB

    outW = inW
    outH = inH
    outImageR = malloc2d(outH, outW)
    outImageG = malloc2d(outH, outW)
    outImageB = malloc2d(outH, outW)

    masknum = askinteger("검출 필터 번호입력", "필터 번호를 입력해주세요(0~3)", minvalue=0, maxvalue=3)

    masks = [
        [  # mask prewitt vertical
            [-1, 0, 1],
            [-1, 0, 1],
            [-1, 0, 1]
        ],
        [  # mask prewitt horizontal
            [1, 1, 1],
            [0, 0, 0],
            [-1, -1, -1]
        ],
        [  # mask sobel vertical
            [-1, 0, 1],
            [-2, 0, 2],
            [-1, 0, 1]
        ],
        [  # mask sobel horizontal
            [1, 2, 1],
            [0, 0, 0],
            [-1, -2, -1]
        ],
        [  # mask laplacian vertical
            [0, -1, 0],
            [-1, 4, -1],
            [0, -1, 0]
        ],
        [  # mask laplacian horizontal
            [0, -1, 0],
            [-1, 4, -1],
            [0, -1, 0]
        ],
        [  # mask robert vertical
            [0, 0, -1],
            [0, 1, 0],
            [0, 0, 0]
        ],
        [  # mask robert horizontal
            [-1, 0, 0],
            [0, 1, 0],
            [0, 0, 0]
        ]
    ]

    """
        canny edge detection
            1. 블러링을 통한 노이즈 제거(가우시안 블러등..)
            2. 마스크를 이용한 엣지 검출
            3. non-maximum value 제거
            4. double threshold 로 크기 구분
            5. 엣지 연결
   """
    vertical = masknum * 2
    horizontal = vertical + 1

    mask = masks[vertical]
    for i in range(1, outH - 1):
        for k in range(1, outW - 1):
            outImageR[i][k] = clamp(0, 255, maskFilterCalc(inImageR, mask, i, k))
            outImageG[i][k] = clamp(0, 255, maskFilterCalc(inImageG, mask, i, k))
            outImageB[i][k] = clamp(0, 255, maskFilterCalc(inImageB, mask, i, k))

    mask = masks[horizontal]
    for i in range(1, outH - 1):
        for k in range(1, outW - 1):
            outImageR[i][k] = int((outImageR[i][k] + clamp(0, 255, maskFilterCalc(inImageR, mask, i, k))) * 0.5)
            outImageG[i][k] = int((outImageG[i][k] + clamp(0, 255, maskFilterCalc(inImageG, mask, i, k))) * 0.5)
            outImageB[i][k] = int((outImageB[i][k] + clamp(0, 255, maskFilterCalc(inImageB, mask, i, k))) * 0.5)

    displayImage()


# global variable -----------------
window = None
canvas = None
paper = None
imageName = None
mainMenu = None
filename = ""
guiInitialized = False

inImageR, inImageG, inImageB, inH, inW = None, None, None, 0, 0
outImageR, outImageG, outImageB, outH, outW = None, None, None, 0, 0
inCvImage, outCvImage = None, None
grayscale = None

# main code -----------------------
guiInit(title="Digital Image Processing Ver 0.5")
window.mainloop()
