import cv2
import numpy as np

src = cv2.imread('assets/1.jpg')

#denoising
#blur = cv2.fastNlMeansDenoisingColored(src,None,10,10,7,21) 
blur = cv2.bilateralFilter(src,9,75,75)

gray_pencil, pencil = cv2.pencilSketch(blur, sigma_s=60, sigma_r=0.07, shade_factor=0.05)
stylize = cv2.stylization(blur, sigma_s=60, sigma_r=0.07)
enhanced = cv2.detailEnhance(blur, 150, .5)
filtered = cv2.edgePreservingFilter(blur)

imgs = [('source',src), ('blur',blur), 
    ('gray',gray_pencil), ('color',pencil), 
    ('stylize',stylize), 
    ('filtered',filtered), ('enhanced',enhanced)]

width = 0
for img in imgs:
    name = img[0]
    i = img[1]
    cv2.imshow(name, i)
    cv2.moveWindow(name, width, 0)
    width = width + int(i.shape[1]/2)

cv2.waitKey(0)
cv2.destroyAllWindows()