import os
import cv2
import numpy as np

def merge(images):
    """Merge the given images into one using the Mertens algorithm"""

    merge_mertens = cv2.createMergeMertens()
    return merge_mertens.process(images)

def align(source):
    """Aligns the given images"""

    images = []
    M = np.eye(3, 3, dtype=np.float32)
    first_image = None
    for image in img_list:
        if first_image is None:
            # convert to gray scale floating point image
            first_image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
            images.append(image)
        else:
            # Estimate perspective transform
            s, M = cv2.findTransformECC(cv2.cvtColor(image,cv2.COLOR_BGR2GRAY), first_image, M, cv2.MOTION_HOMOGRAPHY)
            w, h, _ = image.shape
            # Align image to first image
            img = cv2.warpPerspective(image, M, (h, w))
            images.append(img)
    return images

def read_img(path):
    """Given a path to an image file, returns a cv2 array or raises error if path is not a file

    str -> np.ndarray"""
    
    if os.path.isfile(path):
        return cv2.imread(path)
    else:
        raise ValueError('Path is not a valid file: {}'.format(path))
        

img_fn = ["1.jpg", "2.jpg", "3.jpg"]
img_list = [read_img("assets/"+fn) for fn in img_fn]

aligned = align(img_list)
res_mertens = merge(aligned)
res_mertens_8bit = np.clip(res_mertens*255, 0, 255).astype('uint8')
cv2.imwrite("aligned_fusion_mertens.jpg", res_mertens_8bit)
