import pygame

pygame.init()
ANCHO, ALTO = 600, 600
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Ejercicio 3")

WHITE = (255, 255, 255)
screen.fill(WHITE)

cx, cy = ANCHO // 2, ALTO // 2  # centro

# Círculo grande (solo borde)
pygame.draw.circle(screen, (0, 0, 255), (cx, cy), 180, 8)

# Círculo medio (relleno)
pygame.draw.circle(screen, (0, 255, 0), (cx, cy), 120)

# Círculo pequeño (solo borde)
pygame.draw.circle(screen, (255, 0, 0), (cx, cy), 60, 6)

pygame.image.save(screen, "e3_circulos.png")
pygame.quit()
