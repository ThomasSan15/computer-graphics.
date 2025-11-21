import pygame
import math

pygame.init()
ANCHO, ALTO = 600, 600
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Ejercicio 6 - Casa")

WHITE = (255, 255, 255)
screen.fill(WHITE)

# jardin
pygame.draw.rect(screen, (0, 180, 0), (0, 450, ANCHO, 150))

# --- CUERPO DE LA CASA
pygame.draw.rect(screen, (200, 150, 100), (200, 250, 200, 200))

techo = [
    (200, 250),
    (400, 250),
    (300, 150)
]
pygame.draw.polygon(screen, (150, 50, 0), techo)

# --- PUERTA ---
pygame.draw.rect(screen, (120, 70, 30), (275, 330, 50, 120))

# --- VENTANA ---
pygame.draw.rect(screen, (135, 206, 250), (210, 290, 60, 60))
# Línea horizontal (mitad)
pygame.draw.line(screen, (0, 0, 0), (210, 320), (270, 320), 3)

# Línea vertical (mitad)
pygame.draw.line(screen, (0, 0, 0), (240, 290), (240, 350), 3)

# --- SOL ---
pygame.draw.circle(screen, (255, 255, 0), (500, 100), 60)


pygame.image.save(screen, "e7_casa.png")
pygame.quit()
