""" 구현 요구 사항

    * 미니 프로젝트. 메뉴 구성도 및 프로그램 구성도 완성 + 코딩
        -> 내 프로젝트에 추가할 openCV 기능 정리
        -> 책 또는 구글링
"""

# import --------------------------
import copy
import math
import time
import os
from tkinter.simpledialog import *
from tkinter.filedialog import *
import cv2
import numpy as np
from datetime import datetime
from enum import Enum
from PIL import Image, ImageTk
import threading


# enum
class Detection(Enum):
    Any = -1
    Background = 0
    Airplane = 1
    Bicycle = 2
    Bird = 3
    Boat = 4
    Bottle = 5
    Bus = 6
    Car = 7
    Cat = 8
    Chair = 9
    Cow = 10
    DiningTable = 11
    Dog = 12
    Horse = 13
    MotorBike = 14
    Person = 15
    PottedPlant = 16
    Sheep = 17
    Sofa = 18
    Train = 19
    TV = 20


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class VideoPlayer:
    def __init__(self, mainWindow):
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.window = mainWindow
        self.panel = None
        self.video = None
        self.s_factor = 0.3
        self.fps = 1.0 / 10.0
        self.frame_cnt = 0
        self.eyeCascade = cv2.CascadeClassifier("haar/haarcascade_eye.xml")
        self.faceCascade = cv2.CascadeClassifier("haar/haarcascade_frontalface_alt.xml")
        self.glasses = cv2.imread("images/sunglasses.png", flags=cv2.IMREAD_UNCHANGED)
        self.current_frame = 0
        self.prev_time = 0

    def run(self):
        global DetectionType
        self.current_frame = 0
        self.prev_time = 0

        while self.video.isOpened():
            ret, frame = self.video.read()
            if not ret:
                continue

            current_time = time.time() - self.prev_time
            self.current_frame += 1

            if current_time <= self.fps:
                continue
            self.prev_time = current_time

            image = cv2.resize(frame, None, fx=self.s_factor, fy=self.s_factor, interpolation=cv2.INTER_AREA)
            if DetectionType > -2:
                ssdNet(image)
            else:
                self.glassesOnFace(image)

            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            image = ImageTk.PhotoImage(image=image)
            self.currentImage = frame

            if self.panel is None:
                self.panel = Label(self.window, image=image)
                self.panel.image = image
                self.panel.pack()
            else:
                self.panel.config(image=image)
                self.panel.image = image

            if self.current_frame >= self.frame_cnt:
                break

        print("thread close")
        self.panel.config(image=None)
        self.panel.image = None
        self.panel.destroy()
        self.panel = None

    def open(self, videoname):
        self.video = cv2.VideoCapture(videoname)

        if not self.video.isOpened():
            return

        frame_w = self.video.get(cv2.CAP_PROP_FRAME_WIDTH)
        frame_h = self.video.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.frame_cnt = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))

        # window 크기 초기화
        self.window.geometry("{}x{}".format(int(frame_w * self.s_factor), int(frame_h * self.s_factor)))

        if not self.thread.is_alive():
            print("open and start")
            self.restart()

    def stop(self):
        if self.panel is not None:
            self.panel.config(image=None)
            self.panel.image = None
            self.panel.destroy()
            self.panel = None
        if self.thread.is_alive():
            print("stop: video release")
            self.video.release()
        # 실행중이던 정보 초기화
        self.current_frame = 0
        self.prev_time = 0

    def restart(self):
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()

    def glassesOnFace(self, image) -> None:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        face_rects = self.faceCascade.detectMultiScale(gray, 1.1, 2)

        for (fx, fy, fw, fh) in face_rects:
            cropImg = gray[fy:fy + fh, fx:fx + fw]
            eye_points = []
            eye_rects = self.eyeCascade.detectMultiScale(cropImg, 1.1, 2)
            # cv2.rectangle(image, (fx, fy), (fx + fw, fy + fh), (255, 0, 0), 2)
            for (ex, ey, ew, eh) in eye_rects:
                c_x = int(fx + ex + ew * 0.5)
                c_y = int(fy + ey + eh * 0.5)
                eye_points.append(Point(c_x, c_y))

                # cv2.circle(image, (c_x, c_y), int(ew * 0.5), (0, 255, 0), 2)

            if len(eye_points) == 2:
                eye1 = eye_points[0]
                eye2 = eye_points[1]

                if eye1.x > eye2.x:
                    t = eye1
                    eye1 = eye2
                    eye2 = t

                eye_w = abs(eye2.x - eye1.x)
                eye_h = abs(eye2.y - eye1.y)

                if eye_w > eye_h:
                    img_scale = eye_w / 330.0
                    offsetx = 150 * img_scale
                    offsety = 160 * img_scale

                    w = self.glasses.shape[1] * img_scale
                    h = self.glasses.shape[0] * img_scale
                    resize_glasses = cv2.resize(self.glasses, dsize=(int(w), int(h)))
                    self.overlayImage(image, resize_glasses, Point(eye1.x - offsetx, eye1.y - offsety))

    def overlayImage(self, image, reimg, point):
        for y in range(max(int(point.y), 0), image.shape[0]):
            fY = int(y - point.y)

            if fY >= reimg.shape[0]:
                break

            for x in range(max(int(point.x), 0), image.shape[1]):
                fX = int(x - point.x)

                if fX >= reimg.shape[1]:
                    break

                opacity = reimg[fY, fX, 3] / 255.0

                for c in range(image.shape[2]):
                    rex = reimg[fY, fX, c]
                    imx = image[y, x, c]
                    image[y, x, c] = imx * (1.0 - opacity) + rex * opacity




# functions -----------------------
# common function
def currentTime() -> str:
    return datetime.now().strftime("%Y.%m.%d_%H-%M-%S")


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
    global videoPlayer, canvas

    # 이미지 파일 경로 불러오기
    filename = askopenfilename(parent=window,
                               filetypes=[
                                   ("이미지 파일", "*.jpg;*.jpeg;*.png;*.bmp;*.tif;*.tiff;*.raw"),
                                   ("동영상 파일", "*.mp4;*.avi"),
                                   ("모든 파일", "*.*")])


    if canvas is not None:
        canvas.destroy()
    videoPlayer.stop()
    ext = filename.rsplit('.', 1)[1]
    if ext != "mp4" and ext != "avi":
        guiMenu2Delete()
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

    else:  # 동영상
        guiMenuDelete()
        guiMenu2Init()
        videoPlayer.open(filename)


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
    fileMenu.add_separator()
    fileMenu.add_command(label="닫기", command=exit)


def guiMenuDelete() -> None:
    global mainMenu, gui1Initialized

    if gui1Initialized is False:
        return

    gui1Initialized = False
    mainMenu.delete("원본")
    mainMenu.delete("이미지처리")
    mainMenu.delete("openCV")


def guiMenu2Delete() -> None:
    global mainMenu, gui2Initialized

    if gui2Initialized is False:
        return

    gui2Initialized = False
    mainMenu.delete("동영상처리")


def guiMenuInit() -> None:  # 추가적인 메뉴바를 설정한다
    global mainMenu, gui1Initialized

    if gui1Initialized is True:
        return

    # 메뉴 추가
    # 내가 구현한 이미지 처리
    myProcessMenu = Menu(mainMenu)
    mainMenu.add_command(label="원본", command=equalImage)
    mainMenu.add_command(label="저장", command=saveImage)
    mainMenu.add_cascade(label="이미지처리", menu=myProcessMenu)

    # opencv 활용 이미지 처리
    cvProcessMenu = Menu(mainMenu)
    mainMenu.add_cascade(label="openCV", menu=cvProcessMenu)

    # 내가 구현한 이미지 처리 방식 등록
    # 화소점 처리 메뉴
    myImageMenu = Menu(myProcessMenu)
    myProcessMenu.add_cascade(label="화소점처리", menu=myImageMenu)
    myImageMenu.add_command(label="밝게/어둡게", command=brightenImage)
    myImageMenu.add_command(label="반전", command=negativeImage)
    myImageMenu.add_command(label="그레이스케일", command=grayScaleImage)
    myImageMenu.add_command(label="흑백(입력)", command=bwImage)
    myImageMenu.add_command(label="흑백(평균)", command=bwAvgImage)
    myImageMenu.add_command(label="흑백(중앙값)", command=bwMedianImage)
    myImageMenu.add_command(label="감마", command=gammaImage)
    myImageMenu.add_command(label="파라볼라", command=parabolaImage)

    # 기하학 처리 메뉴
    myImage2Menu = Menu(myProcessMenu)
    myProcessMenu.add_cascade(label="기하학처리", menu=myImage2Menu)
    myImage2Menu.add_command(label="미러(상하)", command=mirrorTopBottom)
    myImage2Menu.add_command(label="미러(좌우)", command=mirrorLeftRight)
    myImage2Menu.add_command(label="확대/축소(기본)", command=zoomImage)
    myImage2Menu.add_command(label="확대/축소(보간)", command=zoomInterpolaration)
    myImage2Menu.add_command(label="이동", command=moveImage)
    myImage2Menu.add_command(label="회전", command=rotateImage)

    # 화소영역 처리 메뉴
    myImage3Menu = Menu(myProcessMenu)
    myProcessMenu.add_cascade(label="화소영역 처리", menu=myImage3Menu)
    myImage3Menu.add_command(label="블러링", command=blurImage)
    myImage3Menu.add_command(label="엠보싱", command=embossingImage)
    myImage3Menu.add_command(label="샤프닝", command=sharpeningImage)
    myImage3Menu.add_command(label="경계선 검출", command=edgeDetectionImage)

    # opencv 이미지 처리 등록
    cvImageMenu = Menu(cvProcessMenu)
    cvProcessMenu.add_cascade(label="화소점처리", menu=cvImageMenu)
    cvImageMenu.add_command(label="그레이스케일", command=grayScale_cv)
    cvImageMenu.add_command(label="이진화(기준값)", command=bw1_cv)
    cvImageMenu.add_command(label="이진화(적응형)", command=bw2_cv)

    cvImage2Menu = Menu(cvProcessMenu)
    cvProcessMenu.add_cascade(label="기하학처리", menu=cvImage2Menu)
    cvImage2Menu.add_command(label="확대/축소", command=zoom_cv)

    cvImage3Menu = Menu(cvProcessMenu)
    cvProcessMenu.add_cascade(label="화소영역", menu=cvImage3Menu)
    # cvImage3Menu.add_command(label="블러", command=blur_cv)
    cvImage3Menu.add_command(label="엠보싱", command=embossing_cv)

    cvImage4Menu = Menu(cvProcessMenu)
    cvProcessMenu.add_cascade(label="컴퓨터비전", menu=cvImage4Menu)
    cvImage4Menu.add_command(label="색 추출", command=colorPick_cv)
    cvImage4Menu.add_command(label="얼굴인식", command=frontFace_cv)

    gui1Initialized = True


def guiMenu2Init() -> None:  # 추가적인 메뉴바를 설정한다
    global mainMenu, gui2Initialized

    if gui2Initialized is True:
        return

    myProcessMenu = Menu(mainMenu)
    mainMenu.add_cascade(label="동영상처리", menu=myProcessMenu)

    videoMenu = Menu(myProcessMenu)
    myProcessMenu.add_command(label="캡쳐", command=lambda: snapshot(videoPlayer.currentImage))
    myProcessMenu.add_command(label="전체감지", command=lambda: setDetection(-1))
    myProcessMenu.add_command(label="사람감지", command=lambda: setDetection(15))
    myProcessMenu.add_command(label="자동차감지", command=lambda: setDetection(7))
    myProcessMenu.add_command(label="안경써요", command=lambda: setDetection(-2))

    gui2Initialized = True


# image processing function -------
def ssdNet(image) -> None:
    global DetectionType
    CONF_VALUE = 0.4  # 사물 40% 이상 인식하면 표시
    CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
               "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
               "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
               "sofa", "train", "tvmonitor"]
    COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))
    net = cv2.dnn.readNetFromCaffe("./SSD/MobileNetSSD_deploy.prototxt.txt", "./SSD/MobileNetSSD_deploy.caffemodel")
    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)
    net.setInput(blob)
    detections = net.forward()
    for i in np.arange(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > CONF_VALUE:
            idx = int(detections[0, 0, i, 1])

            if DetectionType == -1:
                pass
            elif idx != DetectionType:
                continue

            # detections check
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
            cv2.rectangle(image, (startX, startY), (endX, endY),
                          COLORS[idx], 1)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(image, label, (startX, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 1)


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


####################
## OpenCV 전용 함수
####################
def cv2output():
    global outImageR, outImageG, outImageB, outH, outW
    global outCvImage
    outH = outCvImage.shape[0]
    outW = outCvImage.shape[1]

    outImageR = malloc2d(outH, outW)
    outImageG = malloc2d(outH, outW)
    outImageB = malloc2d(outH, outW)

    for i in range(outH):
        for k in range(outW):
            if outCvImage.ndim == 3:
                outImageR[i][k] = outCvImage.item(i, k, 2)
                outImageG[i][k] = outCvImage.item(i, k, 1)
                outImageB[i][k] = outCvImage.item(i, k, 0)
            else:
                outImageR[i][k] = outCvImage.item(i, k)
                outImageG[i][k] = outCvImage.item(i, k)
                outImageB[i][k] = outCvImage.item(i, k)


def grayScale_cv():
    global outCvImage, inCvImage
    outCvImage = cv2.cvtColor(inCvImage, cv2.COLOR_BGR2GRAY)
    cv2output()
    displayImage()


def bw1_cv():
    global outCvImage, inCvImage
    value = askinteger("이진화 기준값", "값 입력(0~255)", minvalue=0, maxvalue=255)
    outCvImage = cv2.cvtColor(inCvImage, cv2.COLOR_BGR2GRAY)
    _, outCvImage = cv2.threshold(outCvImage, value, 255, cv2.THRESH_BINARY)
    cv2output()
    displayImage()


def bw2_cv():
    global outCvImage, inCvImage
    outCvImage = cv2.cvtColor(inCvImage, cv2.COLOR_BGR2GRAY)
    outCvImage = cv2.adaptiveThreshold(outCvImage, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 33, -5)
    cv2output()
    displayImage()


def zoom_cv():
    global outCvImage, inCvImage, inH, inW
    scale = askfloat("확대/축소", "배율 입력(0.1~4.0)", minvalue=1.0, maxvalue=4.0)
    outCvImage = cv2.resize(inCvImage, dsize=(int(inW * scale), int(inH * scale)), interpolation=cv2.INTER_NEAREST)
    cv2output()
    displayImage()


def embossing_cv():
    global outCvImage, inCvImage

    mask = np.zeros((3, 3), np.float32)
    mask[0][0] = -1.0
    mask[2][2] = 1.0
    outCvImage = cv2.filter2D(inCvImage, -1, mask)
    outCvImage += 127
    cv2output()
    displayImage()


def colorPick_cv():
    global outCvImage, inCvImage

    hsv = cv2.cvtColor(inCvImage, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    h_orange = cv2.inRange(h, 8, 20)

    outCvImage = cv2.bitwise_and(hsv, hsv, mask=h_orange)
    outCvImage = cv2.cvtColor(outCvImage, cv2.COLOR_HSV2BGR)
    cv2output()
    displayImage()


def frontFace_cv():
    global outCvImage, inCvImage

    # 학습 된 모델 불러오기
    face_clf = cv2.CascadeClassifier("haar/haarcascade_frontalface_alt.xml")

    # 얼굴 찾기
    gray = cv2.cvtColor(inCvImage, cv2.COLOR_BGR2GRAY)
    face_rects = face_clf.detectMultiScale(gray, 1.1, 5)  # 파라미터 조절 가능
    print(face_rects)
    outCvImage = inCvImage[:]

    for (x, y, w, h) in face_rects:
        cv2.rectangle(outCvImage, (x, y), (x + w, y + h), (0, 255, 0), 3)

    cv2output()
    displayImage()


######################
## 동영상 처리
######################
def setDetection(detection) -> None:
    global DetectionType
    DetectionType = detection


def snapshot(image):
    directory = "snapshot"
    if not os.path.isdir(directory):
        os.mkdir(directory)
    snapname = directory + "/snap" + currentTime() + ".png"
    print(snapname)
    cv2.imwrite(snapname, image)


# global variable -----------------
window = None
canvas = None
panel = None
paper = None
imageName = None
mainMenu = None
filename = ""
gui1Initialized = False
gui2Initialized = False

inImageR, inImageG, inImageB, inH, inW = None, None, None, 0, 0
outImageR, outImageG, outImageB, outH, outW = None, None, None, 0, 0
inCvImage, outCvImage = None, None
grayscale = None

DetectionType: int = -1
videoPlayer = None

# main code -----------------------
guiInit(title="Computer Vision Ver 0.5")
videoPlayer = VideoPlayer(window)
window.mainloop()
