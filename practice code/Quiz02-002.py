def malloc2d(h: int, w: int) -> list[list[int]]:
    memory = []
    for i in range(h):
        tmp = []
        for k in range(w):
            tmp.append(0)
        memory.append(tmp)
    return memory


def loadImage(filename: str, h: int, w: int) -> list[list[int]]:
    file = open(filename, "rb")

    image = malloc2d(h, w)
    for i in range(h):
        for k in range(w):
            image[i][k] = ord(file.read(1))

    return image


def minMaxAvgPixel(image: list[list[int]], h: int, w: int) -> (int, int, float):
    min = 255
    max = 0
    avg = 0
    for i in range(h):
        for k in range(w):
            avg += image[i][k]
            min = min if image[i][k] > min else image[i][k]
            max = max if image[i][k] < max else image[i][k]

    avg /= (h * w)

    return min, max, avg


load = loadImage("Citrus256.raw", 256, 256)
print(minMaxAvgPixel(load, 256, 256))