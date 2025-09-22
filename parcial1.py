import numpy as np
import matplotlib.pyplot as plt

def img_izq():
    img = np.zeros((10,10,3))  #creamos la imagen toda de negro
    
    img[1:9,0,0] = 1  #color rojo
    img[1:9,1,1] = 1  #color verde
    img[1:9,2,2] = 1  #color azul
    
    img[1:4,3:5,:] = 1 #color amarillo, colocamos todas las capas en 1
    img[1:4,3:5,2] = 0 #color amarillo, quitamos la capa azul
    
    img[1:4,5:8,:] = 1 #color magenta
    img[1:4,5:8,1] = 0 #color magenta, quitamos el verde
    
    img[1:4,8:10,:] = 1 #color cyan
    img[1:4,8:10,0] = 0 #color cyan, quitamos el rojo
    
    img[4,3:10,:] = 0.9 #gris 0.9
    img[5,3:10,:] = 0.8 #gris 0.8
    img[6,3:10,:] = 0.7 #gris 0.7
    img[7,3:10,:] = 0.6 #gris 0.6
    img[8,3:10,:] = 0.5 #gris 0.5
    
    plt.imshow(img)
    plt.axis("off") #desactivamos el axis 
    plt.show()
    

def img_derecha():
    img = np.zeros((13,13,3))  #creamos la imagen toda de negro
    
    img[1:5,1:5,:] = 1 #bloque cyan
    img[1:5,1:5,0] = 0 #bloque cyan, quitamos el rojo
    
    img[2:4,8,:] = 0.8 #linea izquierda gris 0.8
    img[2:4,11,:] = 0.8 #linea derecha gris 0.8
    
    img[1,8:12,:] = 0.5 #linea horizontal superior gris 0.5
    img[4,8:12,:] = 0.5 #linea horizontal gris 0.5
    
    img[0:13,6,2] = 1 #linea vertical azul
    
    img[6,0:13,1] = 1 #linea horizontal verde
    
    img[5:8,5:8,0] = 1 #bloque rojo de la mitad
    img[6,6,:] = 1 #punto blanco de la mitad
    
    img[8:12,1:5,:] = 1 #bloque amarillo
    img[8:12,1:5,2] = 0 #bloque amarillo, quitamos el azul
    
    img[8:12,8:12,:] = 1 #bloque magenta
    img[8:12,8:12,1] = 0 #bloque magenta, quitamos el verde
    

    plt.imshow(img) 
    plt.axis("off") #desactivamos el axis para mostrar solo la imagen
    plt.show()

img_izq()
img_derecha()