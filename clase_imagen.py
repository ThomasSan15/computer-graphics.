import numpy as np
import matplotlib.pyplot as plt

# Cargar imagen
img = np.array(plt.imread('perrito_compu.jpg'))

print(img.shape)

plt.subplot(3, 3, 1)
plt.imshow(img)
plt.axis('off')
plt.title("Imagen original")

plt.subplot(3,3,2)
imgR = np.copy(img)
imgR[:,:,1] = 0 #cancelar la capa verde
imgR[:,:,2] = 0 #cancelar la capa azul

plt.imshow(imgR)
plt.axis('off')
plt.title("capa roja")

plt.subplot(3,3,3)
imgA = np.copy(img)
imgA[:,:,0] = 0
imgA[:,:,1] = 0

plt.imshow(imgA)
plt.axis('off')
plt.title("capa azul")

plt.subplot(3,3,4)
imgV = np.copy(img)
imgV[:,:,0] = 0
imgV[:,:,2] = 0

plt.imshow(imgV)
plt.axis('off')
plt.title("capa verde")

plt.subplot(3,3,5)
imgV = np.copy(img)
imgV[:,:,1] = 0


plt.imshow(imgV)
plt.axis('off')
plt.title("capa magenta")

plt.subplot(3,3,6)
imgV = np.copy(img)
imgV[:,:,0] = 0

plt.imshow(imgV)
plt.axis('off')
plt.title("capa cyan")


plt.subplot(3,3,7)
imgA = np.copy(img)
imgA[:,:,1] = 0
imgA[:,:,2] = 170

plt.imshow(imgA)
plt.axis('off')
plt.title("capa sapote")


# Guardar la imagen como archivo en lugar de mostrarla en ventana
plt.savefig("salida.png")

# plt.show()  # <- esto no funciona en WSL si no tienes X server
