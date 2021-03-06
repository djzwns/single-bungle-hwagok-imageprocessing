import copy
import math
from tkinter import *
from tkinter import messagebox


# common function
def malloc2d(h, w):
    memory = []
    for i in range(h):
        tmp = []
        for k in range(w):
            tmp.append(0)
        memory.append(tmp)
    return memory


def loadImage(fname: str):
    global image, height, width, filename
    rawFp = open(fname, "rb")
    fsize = 65536
    height = width = int(math.sqrt(fsize))
    image = malloc2d(height, width)

    for i in range(height):
        for k in range(width):
            pixel = ord(rawFp.read(1))
            image[i][k] = pixel
    rawFp.close()


def displayImage(string, tmp):
    global image, height, width, filename
    # print("--", string, "--")
    # for i in range(5):
    #     for k in range(5):
    #         print("%3d" % tmp[i + 50][k + 50], end=' ')
    #     print()
    # print()
    splitstr = string.split("x")
    for i in range(height):
        for k in range(width):
            color = tmp[i][k]
            paper.put("#%02x%02x%02x" % (color, color, color), (k, i))
            # paper.put("#%02x%02x%02x" % (color, color, color), (k//2, i//2))

            # x = int(k//0.5)
            # y = int(i//0.5)
            # paper.put("#%02x%02x%02x" % (color, color, color), (x, y))
            # paper.put("#%02x%02x%02x" % (color, color, color), (x+1, y+1))


# image processing function
def calcImage(val: int):
    global image, height, width, filename
    tmp = malloc2d(height, width)
    for i in range(height):
        for k in range(width):
            tmp[i][k] = max(0, min(255, image[i][k] + val))
    return tmp


def reverseImage():
    global image, height, width, filename
    tmp = malloc2d(height, width)
    for i in range(height):
        for k in range(width):
            tmp[i][k] = 255 - image[i][k]
    return tmp


def bw127Image():
    global image, height, width, filename
    tmp = malloc2d(height, width)
    for i in range(height):
        for k in range(width):
            tmp[i][k] = 0 if image[i][k] < 127 else 255
    return tmp


def bwAvgImage():
    global image, height, width, filename
    tmp = malloc2d(height, width)
    avg = 0
    for i in range(height):
        for k in range(width):
            avg += image[i][k]
    avg //= (height * width)
    print("?????????->", avg)
    for i in range(height):
        for k in range(width):
            tmp[i][k] = 0 if image[i][k] < avg else 255
    return tmp


def bwCenterImage():
    global image, height, width, filename
    tmp1 = copy.deepcopy(image)
    tmp1.sort()
    tmp = malloc2d(height, width)
    center = tmp1[height // 2][width // 2]
    print("?????????->", center)
    for i in range(height):
        for k in range(width):
            tmp[i][k] = 0 if image[i][k] < center else 255
    return tmp



def mirrorLeftRight():
    global image, height, width, filename
    tmp = malloc2d(height, width)
    for i in range(height):
        for k in range(width):
            tmp[i][k] = image[i][width - k - 1]
    return tmp


def mirrorTopBottom():
    global image, height, width, filename
    tmp = malloc2d(height, width)
    for i in range(height):
        for k in range(width):
            tmp[i][k] = image[height - i - 1][k]
    return tmp


# global variable
image = []
height, width = 256, 256
filename = "../images/Etc_Raw(squre)/lena256.raw"

# main
window = Tk()
window.title("Image Processing (Ver 0.1)")
window.geometry("256x256")
window.resizable(width=False, height=False)

canvas = Canvas(window, height=256, width=256)
canvas.pack()

paper = PhotoImage(height=256, width=256)
canvas.create_image((256/2, 256/2), image=paper, state="normal")



# image open
loadImage(filename)
# displayImage("???????????????", image)

# add
addImage = calcImage(50)
# displayImage("??????????????????", addImage)

# sub
subImage = calcImage(-50)
# displayImage("?????????????????????", subImage)

# reverse
reverse = reverseImage()
# displayImage("???????????????", reverse)

# bw127
bw127 = bw127Image()
# displayImage("??????127", bw127)

# bw avg
bwAvg = bwAvgImage()
# displayImage("????????????", bwAvg)

# bw (?????????==?????????)
# ?????? ??????
bwCenter = bwCenterImage()
# displayImage("???????????????", bwCenter)

# mirror LR
lrImage = mirrorLeftRight()
# displayImage("?????????????????????", lrImage)

# mirror TB
tbImage = mirrorTopBottom()
# displayImage("?????????????????????", tbImage)

displayImage("", image)
window.mainloop()
