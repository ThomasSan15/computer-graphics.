import numpy as np
import matplotlib.pyplot as plt
from PIL import Image 

img1 = Image.open("premium_photo-1709440655728-295d8c1cb722.jpg")
img2 = Image.open("perrito_compu.jpg")

img2_resize = img2.resize(img1.size)

img1 = np.array(img1)/255
img2 = np.array(img2_resize)/255

img_fusionada = (img1 + img2)/2
#img = plt.imread("premium_photo-1709440655728-295d8c1cb722.jpg") / 255
#img2 = plt.imread("perrito_compu.jpg") / 255
#negativa de la imagen
#imgN = 1 - img 


plt.imshow(img_fusionada)
plt.axis('off')
plt.title("Imagen original")

#plt.subplot(1,2,2)
#plt.imshow(imgN)
#plt.axis("off")
#plt.title("Imagen invertida")

# Guardar la imagen como archivo en lugar de mostrarla en ventana
plt.savefig("salida.png")
