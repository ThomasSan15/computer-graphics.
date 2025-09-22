import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
def primero():
    matriz = np.array( [[[0,255,255],[255,255,255],[255,0,0]],
              [[255,0,255], [180,180,180],[0,255,0]],
              [[255,255,0],[0,0,0],[0,0,255]]])
    plt.subplot(1,2,1)
    plt.imshow(matriz)
    plt.axis('off')
    plt.show()

def segundo():
    alto, ancho = 200, 300
    cambio = 150
    
    img = np.zeros((alto, ancho, 3), dtype=np.uint8)
    colores = [
        (170, 170, 0),     # amarillo-oliva
        (0, 170, 170),     # cian
        (0, 170, 0),       # verde
        (170, 0, 170),     # magenta
        (170, 0, 0),       # rojo
        (0, 0, 170)        # azul
    ]
    ancho_col = ancho // len(colores)
    
    # Pintamos la parte superior
    for i, color in enumerate(colores):
        img[0:cambio, i*ancho_col:(i+1)*ancho_col] = color
    
    # Escala de grises en la parte inferior
    grises = np.linspace(200, 0, len(colores)+4, dtype=np.uint8)
    ancho_gris = ancho // len(grises)
    
    for i, g in enumerate(grises):
        img[cambio:alto, i*ancho_gris:(i+1)*ancho_gris] = (g, g, g)
    
    plt.imshow(img)
    plt.axis('off')
    plt.show()
    
def tercero():
    img = plt.imread("perrito_compu.jpg")/255
    img_nueva = 1 - img 
    plt.imshow(img_nueva)
    plt.axis("off")
    plt.show()
    
def cuarto(img):
    """Extraer solo la capa R"""
    img_capa = np.zeros_like(img)
    img_capa[:,:,0] = img[:,:,0]  # copiar canal R
    return img_capa

def quinto(img):
    """Extraer solo la capa G"""
    img_capa = np.zeros_like(img)
    img_capa[:,:,1] = img[:,:,1]  # copiar canal G
    return img_capa

def sexto(img):
    """Extraer solo la capa B"""
    img_capa = np.zeros_like(img)
    img_capa[:,:,2] = img[:,:,2] 
    return img_capa
def septimo(img):
    """Conservar R y B, eliminar G """
    img_capa = np.zeros_like(img)
    img_capa[:,:,0] = img[:,:,0]  
    img_capa[:,:,2] = img[:,:,2]  
    return img_capa

def octavo(img):
    """Conservar G y B, eliminar R"""
    img_capa = np.zeros_like(img)
    img_capa[:,:,1] = img[:,:,1]  
    img_capa[:,:,2] = img[:,:,2]  
    return img_capa

def noveno(img):
    """Conservar R y G, eliminar B"""
    img_capa = np.zeros_like(img)
    img_capa[:,:,0] = img[:,:,0]  
    img_capa[:,:,1] = img[:,:,1]  
    return img_capa
def decimo(r, g, b):
    """Fusionar las tres capas en una imagen RGB"""
    R = r[:,:,0]
    G = g[:,:,1]
    B = b[:,:,2]
    img = np.dstack((R, G, B))
    return img

def gris_promedio(img):
    
    return np.mean(img, axis=2)

def gris_luminosidad(img):
   
    r = img[:,:,0]
    g = img[:,:,1]
    b = img[:,:,2]
    gray = 0.21*r + 0.72*g + 0.07*b
    return gray

def gris_midgray(img):
   
    max_val = np.max(img, axis=2)
    min_val = np.min(img, axis=2)
    gray = (max_val + min_val) / 2
    return gray
