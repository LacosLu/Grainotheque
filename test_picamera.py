import picamera

# Initialize the camera
with picamera.PiCamera() as camera:
    # Set resolution
    camera.resolution = (640, 480)
    camera.capture('test.jpg')  # Save the captured image as 'test.jpg'
    print("Image Captured")