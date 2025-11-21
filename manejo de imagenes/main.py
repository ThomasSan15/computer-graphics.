import numpy as np
import matplotlib.pyplot as plt


# --- Brillo y Contraste ---
def ajustar_brillo(img, valor):
	img = img.astype(np.int16)
	img = img + valor * 255
	img = np.clip(img, 0, 255)
	return img.astype(np.uint8)

def ajustar_brillo_canal(img, valores):
	img = img.astype(np.int16)
	for i in range(3):
		img[:,:,i] = np.clip(img[:,:,i] + valores[i], 0, 255)
	return img.astype(np.uint8)

def contraste_logaritmico(img, c=1):
	img = img.astype(np.float32)
	img = c * np.log1p(img)
	img = img * (255.0 / np.max(img))
	return np.clip(img, 0, 255).astype(np.uint8)

def contraste_exponencial(img, gamma=1.0):
	img = img.astype(np.float32) / 255.0
	img = np.power(img, gamma)
	img = img * 255.0
	return np.clip(img, 0, 255).astype(np.uint8)

# --- Geometría y Recorte ---
def recortar_imagen(img, x1, y1, x2, y2):
	return img[y1:y2, x1:x2]

def zoom_area(img, x1, y1, x2, y2, escala=2):
	area = img[y1:y2, x1:x2]
	h, w = area.shape[:2]
	zoomed = np.repeat(np.repeat(area, escala, axis=0), escala, axis=1)
	return zoomed

def rotar_imagen(img, angulo, centro=None, escala=1.0):
	angulo = angulo % 360
	if angulo == 90:
		return np.rot90(img)
	elif angulo == 180:
		return np.rot90(img, 2)
	elif angulo == 270:
		return np.rot90(img, 3)
	elif angulo == 0:
		return img.copy()
	else:
		raise NotImplementedError("Rotación libre requiere interpolación, solo múltiplos de 90 soportados con numpy.")

# --- Estadística e Histograma ---
def mostrar_histograma(img):
	color = ('r','g','b')
	for i, col in enumerate(color):
		plt.hist(img[:,:,i].ravel(), bins=256, color=col, alpha=0.5)
	plt.title('Histograma RGB')
	plt.xlabel('Valor de pixel')
	plt.ylabel('Frecuencia')
	plt.show()

# --- Fusión y Ecualización ---
def fusionar_imagenes(img1, img2, alpha=0.5):
	img1 = img1.astype(np.float32)
	img2 = img2.astype(np.float32)
	return np.clip(img1 * alpha + img2 * (1 - alpha), 0, 255).astype(np.uint8)

def fusionar_imagenes_ecualizadas(img1, img2, alpha=0.5):
	def ecualizar(img):
		eq = np.zeros_like(img)
		for i in range(3):
			hist, bins = np.histogram(img[:,:,i].flatten(), 256, [0,256])
			cdf = hist.cumsum()
			cdf_m = np.ma.masked_equal(cdf,0)
			cdf_m = (cdf_m - cdf_m.min())*255/(cdf_m.max()-cdf_m.min())
			cdf = np.ma.filled(cdf_m,0).astype('uint8')
			eq[:,:,i] = cdf[img[:,:,i]]
		return eq
	eq1 = ecualizar(img1)
	eq2 = ecualizar(img2)
	return fusionar_imagenes(eq1, eq2, alpha)

# --- Extracción de Capas ---
def extraer_capa_rgb(img, canal):
	capa = np.zeros_like(img)
	capa[:,:,canal] = img[:,:,canal]
	return capa

def extraer_capa_cmyk(img, canal):
	img = img.astype(np.float32) / 255.0
	K = 1 - np.max(img, axis=2)
	C = (1-img[:,:,2]-K)/(1-K+1e-8)
	M = (1-img[:,:,1]-K)/(1-K+1e-8)
	Y = (1-img[:,:,0]-K)/(1-K+1e-8)
	CMYK = [C, M, Y, K]
	canal_img = (CMYK[canal]*255).astype(np.uint8)
	# Crear imagen RGB coloreada para cada canal
	rgb = np.zeros((*canal_img.shape, 3), dtype=np.uint8)
	if canal == 0:  # Cian
		rgb[...,0] = 0
		rgb[...,1] = canal_img
		rgb[...,2] = canal_img
	elif canal == 1:  # Magenta
		rgb[...,0] = canal_img
		rgb[...,1] = 0
		rgb[...,2] = canal_img
	elif canal == 2:  # Amarillo
		rgb[...,0] = canal_img
		rgb[...,1] = canal_img
		rgb[...,2] = 0
	elif canal == 3:  # Negro
		rgb[...,0] = canal_img
		rgb[...,1] = canal_img
		rgb[...,2] = canal_img
	return rgb

# --- Negativo, Grises y Binario ---
def foto_negativa(img):
	return 255 - img

def convertir_a_grises(img):
	return np.dot(img[...,:3], [0.299, 0.587, 0.114]).astype(np.uint8)

def binarizar(img, umbral=128):
	if len(img.shape) == 3:
		img = convertir_a_grises(img)
	bin_img = np.where(img > umbral, 255, 0).astype(np.uint8)
	return bin_img