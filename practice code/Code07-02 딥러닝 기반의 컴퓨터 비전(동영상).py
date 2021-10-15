import cv2
import numpy as np
import random


# function
def ssdNet(image) :
    CONF_VALUE = 0.2  # 사물 20% 이상 인식하면 표시
    CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
               "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
               "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
               "sofa", "train", "tvmonitor"]
    COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))
    net = cv2.dnn.readNetFromCaffe("../SSD/MobileNetSSD_deploy.prototxt.txt", "../SSD/MobileNetSSD_deploy.caffemodel")
    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)
    net.setInput(blob)
    detections = net.forward()
    for i in np.arange(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > CONF_VALUE:
            idx = int(detections[0, 0, i, 1])
            if idx != 7:  # 15: person index
                continue

            # person check
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
            cv2.rectangle(image, (startX, startY), (endX, endY),
                          COLORS[idx], 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(image, label, (startX, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
    return image


def snapshot(image):
    cv2.imwrite("../images/save" + str(random.randint(11111, 99999)) + ".png", image)


# global variable
filename = "../videos/traffic.mp4"
video = cv2.VideoCapture(filename)
s_factor = 0.3


# main
frameCount = 0
eventFrame = 5
while True:
    ret, frame = video.read()
    if not ret:
        break

    frameCount += 1
    if frameCount % eventFrame == 0:
        frame = cv2.resize(frame, None, fx=s_factor, fy=s_factor, interpolation=cv2.INTER_AREA)
        result = ssdNet(frame)
        cv2.imshow("compute vision", result)

    key = cv2.waitKey(20)
    if key == 27:
        break
    if key == (ord('c') or ord('C')):
        snapshot(frame)

cv2.destroyAllWindows()
