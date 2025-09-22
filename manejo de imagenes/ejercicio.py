import numpy as np
import matplotlib.pyplot as plt


def ejercicio():
    img = np.zeros((10, 10, 3), dtype=np.uint8)
    
    #bordes blanco
    img[1:9,1,:] = 255
    img[1:9,8,:] = 255
    
    #rojo
    img[1,2:8,0] = 255
    #verde
    img[2,2:8,1] = 255
    #azul
    img[3,2:8,2] = 255
    #gris
    img[4:6,2:8,:] = 255/2
    #cyan
    img[6,2:8,:] = 255
    img[6,2:8,0] = 0
    #magenta
    img[7,2:8,:] = 255
    img[7,2:8,1] = 0
    #amarillo
    img[8,2:8,:] = 255
    img[8,2:8,2] = 0
    plt.imshow(img)
    plt.savefig("ejercicio")
    
    
ejercicio()