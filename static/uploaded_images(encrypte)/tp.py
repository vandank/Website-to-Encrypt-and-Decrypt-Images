import cv2 as cv
import numpy as np
from PIL import Image, ImageDraw
import scipy.misc
# import skimage.io as io

# x = io.imread('static/uploaded_images(encrypte)/IMG-20170930-WA0036.jpg')
# # x = np.array(x)
# print(x)
# io.imsave('static/uploaded_images(encrypte)/img.jpg', x)
# y = io.imread('static/uploaded_images(encrypte)/img.jpg')
# print(y)

x = cv.imread('static/uploaded_images(encrypte)/IMG-20170930-WA0036.jpg')
print(x)
cv.imwrite('static/uploaded_images(encrypte)/img.png', x)
y = cv.imread('static/uploaded_images(encrypte)/img.png')
print(y)

# image = Image.open('static/uploaded_images(encrypte)/IMG-20170930-WA0036.jpg')
# im = np.array(image)
# print(im)
# result = Image.fromarray(im.astype(np.uint8))
# result.save('static/uploaded_images(encrypte)/img.jpg')
# y = Image.open('static/uploaded_images(encrypte)/img.jpg')
# imy = np.array(y)
# print(imy)
# print(cv.__version__)