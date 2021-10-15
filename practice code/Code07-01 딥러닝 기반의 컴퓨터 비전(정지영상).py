import cv2
import numpy as np
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
            if idx != 15:  # 15: person index
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

# global variable
filename = "../images/road/slope_test.jpg"
cvImage = cv2.imread(filename)


# main
# 이미지에서 다양한 사물을 골라서 표시하기
# mobilenetSSD. 사물인식용 pre trained 모델 (20여가지):
# 벽지,비행기, 자전거, 새, 배, 병,버스, 일반 차, 고양이, 의자, 소, 식탁, 개, 말, 오토바이
# 사람, 화분, 양, 소파, 기차, tv
ssdNet(cvImage)

cv2.imshow("compute vision", cvImage)
cv2.waitKey(0)
cv2.destroyAllWindows()
