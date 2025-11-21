import pygame

pygame.init()
ANCHO, ALTO = 600, 600
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Ejercicio 1")

WHITE = (255, 255, 255)
screen.fill(WHITE)

# Dibujar cuadrícula cada 100 px
GRIS = (200, 200, 200)
for x in range(0, ANCHO, 100):
    pygame.draw.line(screen, GRIS, (x, 0), (x, ALTO), 1)
for y in range(0, ALTO, 100):
    pygame.draw.line(screen, GRIS, (0, y), (ANCHO, y), 1)

# 3 líneas de colores y grosores diferentes
pygame.draw.line(screen, (255, 0, 0), (50, 50), (550, 50), 3)   # Rojo
pygame.draw.line(screen, (0, 255, 0), (50, 150), (550, 300), 8) # Verde
pygame.draw.line(screen, (0, 0, 255), (50, 500), (550, 400), 12) # Azul

pygame.image.save(screen, "e1_lineas.png")

pygame.quit()
