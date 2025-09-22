import numpy as np
import matplotlib.pyplot as plt
import imgPro as im

img = plt.imread("perrito_compu.jpg")
img2 = plt.imread("premium_photo-1709440655728-295d8c1cb722.jpg")
img = im.gray_conversion(img)
im.show_img(img)