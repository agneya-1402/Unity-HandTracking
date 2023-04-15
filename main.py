import cv2
from cvzone.HandTrackingModule import HandDetector
import socket
import mediapipe as mp

width, height = 1280, 720

cap = cv2.VideoCapture(0)
cap.set(3,width)
cap.set(4,height)

detector = HandDetector(maxHands=1, detectionCon=0.8)

#unity
soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddressPort = ('127.0.0.1',5052)

while True:

    success, img = cap.read()
    hands,img = detector.findHands(img)

    data = []
    #sending data to unity
    #landmarks  (x,y,z) * 21
    if hands:
        hands = hands[0]
        lmList = hands['lmList']
        print(lmList)
        for lm in lmList:
            data.extend([lm[0],height - lm[1],lm[2]])
        print(data)
        soc.sendto(str.encode(str(data)),serverAddressPort)
    img = cv2.resize(img,(0,0),None,0.5,0.5)
    cv2.imshow('Video',img)
    cv2.waitKey(1)