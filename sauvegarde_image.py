import subprocess
import cv2 as cv
from led import Led
import torch
import matplotlib.pyplot as plt

# leds
led = Led()
led.toggle()

# Run libcamera-raw to capture a still image
subprocess.run(['libcamera-jpeg', '-o', 'image.jpeg'])

led.toggle()

# Now, read the captured image with OpenCV
image = cv.imread(cv.samples.findFile("image.jpeg"))
img = torch.tensor(cv.resize(image, (32,32))).type(torch.float32)
plt.imshow(img.type(torch.uint8))
plt.show()