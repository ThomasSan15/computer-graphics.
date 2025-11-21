import pygame

pygame.init()
ANCHO, ALTO = 600, 600
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Ejercicio 4")

WHITE = (255, 255, 255)
screen.fill(WHITE)

# Cara 
pygame.draw.ellipse(screen, (255, 220, 180), (150, 100, 300, 400))

# Ojos 
pygame.draw.ellipse(screen, (0, 0, 0), (220, 210, 60, 40))   # Ojo izquierdo
pygame.draw.ellipse(screen, (0, 0, 0), (320, 210, 60, 40))   # Ojo derecho

# Boca 
pygame.draw.ellipse(screen, (255, 0, 0), (230, 350, 140, 60), 5)

pygame.image.save(screen, "e4_cara.png")
pygame.quit()
