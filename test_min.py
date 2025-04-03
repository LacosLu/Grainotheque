import cv2 as cv
from time import sleep

cap = cv.VideoCapture(0)

while True:
    ret, frame = cap.read()
    sleep(1)
    if ret:
        break

cv.imshow("frame", frame)
k = cv.waitKey(0)