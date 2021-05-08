import cv2
import math
import argparse
from os.path import dirname, join


def highlightFace(net, frame, conf_threshold=0.7):
    frameOpencvDnn = frame.copy()
    frameHeight = frameOpencvDnn.shape[0]
    frameWidth = frameOpencvDnn.shape[1]
    blob = cv2.dnn.blobFromImage(frameOpencvDnn, 1.0, (300, 300), [
                                 104, 117, 123], True, False)

    net.setInput(blob)
    detections = net.forward()
    faceBoxes = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > conf_threshold:
            x1 = int(detections[0, 0, i, 3]*frameWidth)
            y1 = int(detections[0, 0, i, 4]*frameHeight)
            x2 = int(detections[0, 0, i, 5]*frameWidth)
            y2 = int(detections[0, 0, i, 6]*frameHeight)
            faceBoxes.append([x1, y1, x2, y2])
            cv2.rectangle(frameOpencvDnn, (x1, y1), (x2, y2),
                          (0, 255, 0), int(round(frameHeight/150)), 8)
    return faceBoxes


faceProto = join(dirname(__file__), "opencv_face_detector.pbtxt")
faceModel = join(dirname(__file__), "opencv_face_detector_uint8.pb")
ageProto = join(dirname(__file__), "age_deploy.prototxt")
ageModel = join(dirname(__file__), "age_net.caffemodel")

MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)',
           '(25-32)', '(38-43)', '(48-53)', '(60-100)']


def age(path):
    faceNet = cv2.dnn.readNet(faceModel, faceProto)
    ageNet = cv2.dnn.readNet(ageModel, ageProto)
    padding = 20

    print(path)

    image = cv2.VideoCapture(path if path else 0)

    ages = []

    while cv2.waitKey(1) < 0:
        hasFrame, frame = image.read()
        if not hasFrame:
            cv2.waitKey()
            break

        faceBoxes = highlightFace(faceNet, frame)
        if not faceBoxes:
            return None

        for faceBox in faceBoxes:
            face = frame[max(0, faceBox[1]-padding):
                         min(faceBox[3]+padding, frame.shape[0]-1), max(0, faceBox[0]-padding):min(faceBox[2]+padding, frame.shape[1]-1)]

            blob = cv2.dnn.blobFromImage(
                face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)

            ageNet.setInput(blob)
            agePreds = ageNet.forward()
            age = ageList[agePreds[0].argmax()]

            ages.append(age[1:-1])

    return ages
