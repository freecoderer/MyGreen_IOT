import cv2
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(4,GPIO.OUT) 

# Load the pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialize the video capture
video_capture = cv2.VideoCapture(0)

GPIO.output(4,False)

while True:
    # Read a frame from the video capture
    ret, frame = video_capture.read()

    # Convert the frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Perform face detection
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Process the detected faces
    for (x, y, w, h) in faces:
        # Do something with the detected faces
        # For example, you can print the coordinates of each face
        print(f"Detected face: x={x}, y={y}, width={w}, height={h}")
        GPIO.output(4,True)
        time.sleep(3)
        GPIO.output(4,False)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture
video_capture.release()
