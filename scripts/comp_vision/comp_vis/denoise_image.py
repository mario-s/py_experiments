import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('assets/noise.jpg')
dst = cv2.fastNlMeansDenoisingColored(img,None,9,9,7,21)

#cv2.imwrite('22-1.jpg', dst)

stack = np.hstack((img,dst))
cv2.imshow('denoise', stack)
cv2.waitKey(0)
cv2.destroyAllWindows()


