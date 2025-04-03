from picamera2 import Picamera2
import cv2 as cv

cap = cv.VideoCapture(0)
print(cap)

# Check if camera opened successfully
print(cap.isOpened())
if (cap.isOpened() == False):
    print("Error opening video stream or file")

while cap.isOpened():
    ret, frame = cap.read()
    print(ret)
    print(frame)
    if ret == True:
        cv.imshow("frame", frame)
        k = cv.waitKey(0)
    else:
        break

cv.destroyAllWindows()
cap.release()

"""camera = Picamera2()
camera.resolution = (1024, 768)
camera.start_preview()
# Camera warm-up time
sleep(2)
camera.capture_file('foo.jpg')"""