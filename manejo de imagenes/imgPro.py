import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def show_img(img):
    plt.imshow(img)
    plt.axis("off")
    plt.savefig("imagen")
    
def layer(img, rgb=(1,1,1)):
    img_capa = np.zeros_like(img)
    
    for i in range(3):
        img_capa[:,:,i] = img[:,:,i] * rgb[i]
          
    return img_capa


def brightness(img,factor):
    
    if factor >= 0 and factor <= 1:
        return img + factor
    else: 
        raise Exception("Error")
        
def brightness_layer(img,factor,capa):
    img_copia = np.copy(img)
    img_copia[:,:,capa] = img[:,:,capa] + factor
    if factor >= 0 and factor <= 1:
        return  img_copia
    else: 
        raise Exception("Error")
    
def inversion(img):
    return 1 - img

def fusion():
    img1 = Image.open("premium_photo-1709440655728-295d8c1cb722.jpg")
    img2 = Image.open("perrito_compu.jpg")

    img2_resize = img2.resize(img1.size)

    img1 = np.array(img1)/255
    img2 = np.array(img2_resize)/255

    img_fusionada = (img1 + img2)/2

    return (img1 + img2)/2

#FALTAN LOS OTROS 2
def gray_conversion(img):
    img = img /255
    return (img[:,:,0] + img[:,:,1] + img[:,:,2]) / 3

def contrast(img,factor,zone):
    if zone = "dark":
        return factor * np.log10(1+img)

        
     

