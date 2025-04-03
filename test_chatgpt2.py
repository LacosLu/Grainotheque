import subprocess
import cv2
import matplotlib.pyplot as plt

# Run libcamera-raw to capture a still image
subprocess.run(['libcamera-jpeg', '-o', 'image.jpeg'])

# Now, read the captured image with OpenCV
image = cv2.imread(cv2.samples.findFile("image.jpeg"))


plt.imshow(image)
plt.show()
"""# --- Affichage d'une photo ---
cv2.imshow("Image", image)
k = cv2.waitKey(0)"""