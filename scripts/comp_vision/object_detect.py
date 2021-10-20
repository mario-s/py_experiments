#
#trying to detect cars on a video stream
#
import cv2

cap = cv2.VideoCapture()
#IP cam (e.g. DroidCam)
cap.open('http://192.168.2.24:4747/video')

car_cascade = cv2.CascadeClassifier('assets/cars.xml')

while True:
    ret, img = cap.read()
    if (type(img) == type(None)):
        break

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    cars = car_cascade.detectMultiScale(gray, 1.1, 1)

    for (x,y,w,h) in cars:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)

    cv2.imshow('object detect', img)

    if cv2.waitKey(33) == 27:
        break

cv2.destroyAllWindows()