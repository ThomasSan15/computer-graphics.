import pygame
import math

pygame.init()
ANCHO, ALTO = 600, 600
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Ejercicio 5")

WHITE = (255, 255, 255)
screen.fill(WHITE)

# --- TRIÁNGULO EQUILÁTERO ---
lado = 200
h = (math.sqrt(3) / 2) * lado
x0, y0 = ANCHO // 2, 150

triangulo = [
    (x0, y0),
    (x0 - lado/2, y0 + h),
    (x0 + lado/2, y0 + h)
]

pygame.draw.polygon(screen, (0, 100, 255), triangulo)

# --- ESTRELLA DE 5 PUNTAS ---
cx, cy = ANCHO // 2, 420
R = 100   # radio exterior
r = 40    # radio interior

puntos = []
for i in range(10):
    ang = i * 36  # 360 / 10
    rad = math.radians(ang)
    if i % 2 == 0:
        x = cx + R * math.cos(rad)
        y = cy + R * math.sin(rad)
    else:
        x = cx + r * math.cos(rad)
        y = cy + r * math.sin(rad)
    puntos.append((x, y))

pygame.draw.polygon(screen, (255, 200, 0), puntos)

pygame.image.save(screen, "e5_poligonos.png")
pygame.quit()
