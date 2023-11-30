import cv2
import cvzone
import numpy as np
import requests

# Replace 'http://192.168.66.81' with the actual IP address of your ESP32 camera
cap = cv2.VideoCapture("http://192.168.4.1:81/stream")
cap.set(3, 640)
cap.set(4, 480)

totalMoney = 0

def empty(a):
    pass

def preProcessing(img):
    imgPre = cv2.GaussianBlur(img, (7, 7), 3)
    kernel = np.ones((2, 2), np.uint8)
    imgPre = cv2.dilate(imgPre, kernel, iterations=1)
    imgPre = cv2.morphologyEx(imgPre, cv2.MORPH_CLOSE, kernel)
    return imgPre

while True:
    success, img = cap.read()
    if not success:
        break

    imgPre = preProcessing(img)
    
    imgStacked = cvzone.stackImages([img], 1, 1)
    
    cv2.imshow("Image", imgStacked)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('c'):
        # Save the captured image
        cv2.imwrite("captured_image.jpg", img)
        print("Image captured!")

        # Send the captured image to the React application
        files = {'file': open('captured_image.jpg', 'rb')}
        response = requests.post('http://localhost:8000/predict', files=files)

# Release the video capture object
cap.release()
cv2.destroyAllWindows()
