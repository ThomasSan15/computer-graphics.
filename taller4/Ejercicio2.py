import pygame

pygame.init()
ANCHO, ALTO = 600, 600
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Ejercicio 2")

WHITE = (255, 255, 255)
screen.fill(WHITE)

# Rectángulo relleno centrado
rect_w, rect_h = 300, 200
x = (ANCHO - rect_w) // 2
y = (ALTO - rect_h) // 2
pygame.draw.rect(screen, (0, 120, 255), (x, y, rect_w, rect_h))

# Marco alrededor del lienzo (borde)
pygame.draw.rect(screen, (0, 0, 0), (0, 0, ANCHO, ALTO), 10)

pygame.image.save(screen, "e2_rectangulos.png")

pygame.quit()
