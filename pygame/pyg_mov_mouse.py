import pygame 

pygame.init()

ancho,alto = 500, 500
screen = pygame.display.set_mode((ancho,alto))
clock = pygame.time.Clock()

pos = [250,250]
radio = 15
arrastrar = False
running = True 

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            arrastrar = True
        elif event.type == pygame.MOUSEBUTTONUP:
            arrastrar = False
    
    if arrastrar:
        pos = pygame.mouse.get_pos()
    
    screen.fill((0,0,0))
    pygame.draw.circle(screen,"red",pos,radio)
    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()