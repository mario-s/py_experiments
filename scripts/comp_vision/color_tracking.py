import cv2
import numpy as np


boundaries = [
([169, 100, 100], [189, 255, 255], "red"),
([110,50,50], [130,255,255], "blue"),
([20, 100, 100], [40, 255, 255], "yellow"),
([0, 48, 80], [20, 255, 255], "skin")
]

def track(frame):
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    for boundary in boundaries:
        # define range of color in HSV
        lower = np.array(boundary[0])
        upper = np.array(boundary[1])

        # Threshold the HSV image to get only desired colors
        #blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
        mask = cv2.inRange(hsv, lower, upper)

        # Bitwise-AND mask and original image
        res = cv2.bitwise_and(frame,frame, mask= mask)
        cv2.imshow('tracking: {}'.format(boundary[2]),res)


#access to build in cam
cap = cv2.VideoCapture(0)

#access to stream via DroidCam
#cap = cv2.VideoCapture()
#cap.open('http://192.168.2.100:4747/video')

while(1):
    # Take each frame
    _, frame = cap.read()

    cv2.imshow('frame',frame)

    track(frame)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
