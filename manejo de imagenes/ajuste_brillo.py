import numpy as np
import matplotlib.pyplot as plt


img = plt.imread("perrito_compu.jpg")/255

plt.subplot(3,3,1)
plt.axis("off")
plt.imshow(img)

brillo = 0.5
img_brillo = img + brillo
plt.subplot(3,3,2)
plt.axis("off")
plt.imshow(img_brillo)

#aumentar a un solo canal

img_copia = np.copy(img)
capa = 0
img_copia[:,:,capa] = img[:,:,capa] + brillo 
plt.subplot(3,3,3)
plt.axis("off")
plt.title("capa roja aumentada")
plt.imshow(img_copia)



contraste = 0.5


plt.subplot(3,3,4)
imgcontraste = contraste*np.log10(1+img)
plt.axis("off")
plt.title("contraste zonas oscuras")
plt.imshow(imgcontraste)

plt.subplot(3,3,5)
imgcontraste = contraste*np.exp(img-1)
plt.axis("off")
plt.title("Contraste zonas claras")
plt.imshow(imgcontraste)


img_gris = (img[:,:,0] + img[:,:,1] + img[:,:,2]) / 3
umbral = 0.5
imgbin = (img_gris > umbral)
plt.subplot(3,3,6)
plt.axis("off")
plt.title("imagen binaria")
plt.imshow(img_gris,cmap = "gray")

xIni = 100
Xfin = 300
yIni = 50
Yfin = 200

Imgrecorte = img[yIni:Yfin , xIni:Xfin]
print("Tamaño imagen escalada : ",Imgrecorte.shape)

plt.subplot(3,3,7)
plt.title("Imagen recortada")
plt.axis("off")
plt.imshow(Imgrecorte)


zoom_factor= 10

zoomed = img[::zoom_factor, ::zoom_factor]
print("tamaño imagen original: " ,img.shape)
print("tamaño con la reduccion de resolucion: ", zoomed.shape)

plt.subplot(3,3,8)
plt.axis("off")
plt.title("reducida")
plt.imshow(zoomed)




plt.savefig("salida3")


    


