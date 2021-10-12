import math


# function
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
    fsize = 262144
    height = width = int(math.sqrt(fsize))
    image = malloc2d(height, width)

    for i in range(height):
        for k in range(width):
            pixel = ord(rawFp.read(1))
            image[i][k] = pixel
    rawFp.close()


def displayImage():
    global image, height, width, filename
    for i in range(5):
        for k in range(5):
            print("%3d" % image[i + 50][k + 50], end=' ')
        print()
    print("---------------------------------")


def addImage(val: int):
    pass


def subImage(val: int):
    pass


# global var
image = []
height, width = 512, 512
filename = "../images/Etc_Raw(squre)/flower512.raw"


# main
loadImage(filename)
displayImage()


# add
addImage(50)
displayImage()

# sub
subImage(50)
displayImage()