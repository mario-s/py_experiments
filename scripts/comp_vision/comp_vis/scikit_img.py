from skimage import io
from skimage import measure

"""
Comparing images with skimage: mean-squared error and root-mean-square deviation error.
"""

img1 = io.imread("assets/1.jpg")
img2 = io.imread("assets/2.jpg")
img3 = io.imread("assets/3.jpg")

print("mean-squared error img1, img1: ", measure.compare_mse(img1, img1))
print("root-mean-square deviation error img1, img1: ", measure.compare_nrmse(img1, img1))

print("mean-squared error img1, img2: ", measure.compare_mse(img1, img2))
print("root-mean-square deviation error img1, img2: ", measure.compare_nrmse(img1, img2))

print("mean-squared error img1, img3: ", measure.compare_mse(img1, img3))
print("root-mean-square deviation error img1, img3: ", measure.compare_nrmse(img1, img3))