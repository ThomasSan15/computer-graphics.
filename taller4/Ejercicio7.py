import pygame

pygame.init()
ANCHO, ALTO = 800, 600
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Ejercicio 7 - Banderas")

WHITE = (255, 255, 255)
screen.fill(WHITE)

#Bandera de colombia
x0, y0 = 50, 100
w, h = 300, 200

# Franja amarilla (50%)
pygame.draw.rect(screen, (255, 204, 0), (x0, y0, w, h * 0.5))

# Franja azul (25%)
pygame.draw.rect(screen, (0, 0, 255), (x0, y0 + h * 0.5, w, h * 0.25))

# Franja roja (25%)
pygame.draw.rect(screen, (255, 0, 0), (x0, y0 + h * 0.75, w, h * 0.25))

# Marco opcional (borde)
pygame.draw.rect(screen, (0, 0, 0), (x0, y0, w, h), 3)


#Japon
x1, y1 = 450, 100
w2, h2 = 300, 200

# Fondo blanco
pygame.draw.rect(screen, (255, 255, 255), (x1, y1, w2, h2))

# Círculo rojo centrado
cx = x1 + w2 // 2
cy = y1 + h2 // 2
radio = 50

pygame.draw.circle(screen, (188, 0, 45), (cx, cy), radio)

# Marco opcional (borde)
pygame.draw.rect(screen, (0, 0, 0), (x1, y1, w2, h2), 3)


pygame.image.save(screen, "e8_banderas.png")
pygame.quit()
