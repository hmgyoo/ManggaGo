import cv2
import cvzone
import numpy as np

# Replace 'http://192.168.66.81' with the actual IP address of your ESP32 camera
cap = cv2.VideoCapture("http://192.168.254.167:81/stream")
#cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

totalMoney = 0

def empty(a):
    pass

cv2.namedWindow("Settings")
cv2.resizeWindow("Settings", 640, 240)

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
    #cvzone.putTextRect(imgStacked, f"Php.{totalMoney}", (50, 50))

    cv2.imshow("Image", imgStacked)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object
cap.release()
cv2.destroyAllWindows()
