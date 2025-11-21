import pygame 

pygame.init()

ancho,alto = 500, 500
screen = pygame.display.set_mode((ancho,alto))
clock = pygame.time.Clock()

pos = [250,250]
pos_rect = [250,250]
dim_rect = [25,25]

radio = 15
vel = 5

running = True 

while running:
   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_UP]:
        pos[1] -= vel
    if keys[pygame.K_DOWN]:
        pos[1] += vel
    if keys[pygame.K_LEFT]:
        pos[0] -= vel    
    if keys[pygame.K_RIGHT]:
        pos[0] += vel
    
    if keys[pygame.K_w]:
        pos_rect[1] -= vel
    if keys[pygame.K_s]:
        pos_rect[1] += vel
    if keys[pygame.K_a]:
        pos_rect[0] -= vel    
    if keys[pygame.K_d]:
        pos_rect[0] += vel
        
    pos[0] = max(radio, min(ancho - radio, pos[0])) 
    pos[1] = max(radio, min(alto - radio, pos[1]))
    pos_rect[0] = max(dim_rect[0] - dim_rect[0] , min(ancho - dim_rect[0], pos_rect[0])) 
    pos_rect[1] = max(dim_rect[1] - dim_rect[1] , min(alto - dim_rect[1], pos_rect[1]))
    
    
    """
    if pos[1] < radio:
            pos[1] = radio 
    if pos[1] > alto - radio:
            pos[1] = alto - radio
    if pos[0] < radio:
            pos[0] = radio
    if pos[0] > ancho - radio:
            pos[0] = ancho - radio
    """
        
    screen.fill((0,0,0))
    pygame.draw.circle(screen,"red",pos,radio)
    pygame.draw.rect(screen,"green", (pos_rect , dim_rect))
    pygame.display.flip()
    clock.tick(60)
    
    
pygame.quit()
    