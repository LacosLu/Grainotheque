import cv2

# Define the GStreamer pipeline for libcamera
# This pipeline uses the libcamera source to grab frames
gstreamer_pipeline = (
    "libcamera-vid -t 0 --inline --camera 0 --framerate 30 --width 640 --height 480 ! "
    "video/x-raw, format=BGR ! videoconvert ! appsink"
)

# Open the GStreamer pipeline with OpenCV
cap = cv2.VideoCapture(gstreamer_pipeline, cv2.CAP_GSTREAMER)

if not cap.isOpened():
    print("Error: Could not open video capture.")
else:
    print("Video capture initialized successfully.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to grab frame.")
            break

        # Display the frame
        cv2.imshow("Frame", frame)

        # Break the loop on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
