import sys, os
import pygame
from pygame import Vector2
import random

# Inicializar pygame
pygame.init()


# -------------------------------------------------------------------
# FUNCIONES UTILITARIAS
# -------------------------------------------------------------------

# Lee el archivo de puntaje más alto (Top Score)
def openTopScoreFile():
    with open('TopScoreFile.txt') as file:
        topScore = int(file.read())  # se convierte el texto a entero
    file.close()
    return topScore


# Guarda el nuevo récord si el score actual lo supera
def saveTopScoreFile():
    global TOPSCORE
    if SCORE > TOPSCORE:              # Si se supera el puntaje guardado...
        TOPSCORE = SCORE              # Se actualiza
        with open('TopScoreFile.txt', 'w') as file:
            file.write(str(TOPSCORE)) # Se escribe en el archivo
        file.close()
    return


# Carga una imagen y la escala al tamaño indicado
def gameImageLoad(imagefilepath, size):
    image = pygame.image.load(imagefilepath)                      # carga
    image = pygame.transform.scale(image, (size[0], size[1]))     # redimensiona
    return image


# Carga masivamente los sprites de asteroides en sus tamaños
def asteroidImageLoading():
    large = 180
    medium = 125
    small = 75

    # Se recorren los tamaños de asteroide
    for imgSize in ['large', 'medium', 'small']:
        if imgSize == 'large': imgSpriteSize = large
        elif imgSize == 'medium': imgSpriteSize = medium
        else: imgSpriteSize = small
        
        # Recorre la carpeta assets/asteroids/... según tamaño
        for item in os.listdir(f'assets/asteroids/{imgSize}'):

            # Según código en el nombre, se agrega a una categoría
            if str(item)[:2] == 'a1': AsteroidImgA[imgSize].append(gameImageLoad(f'assets/asteroids/{imgSize}/{item}', (imgSpriteSize, imgSpriteSize)))
            elif str(item)[:2] == 'a3': AsteroidImgB[imgSize].append(gameImageLoad(f'assets/asteroids/{imgSize}/{item}', (imgSpriteSize, imgSpriteSize)))
            elif str(item)[:2] == 'b1': AsteroidImgC[imgSize].append(gameImageLoad(f'assets/asteroids/{imgSize}/{item}', (imgSpriteSize, imgSpriteSize)))
            elif str(item)[:2] == 'b3': AsteroidImgD[imgSize].append(gameImageLoad(f'assets/asteroids/{imgSize}/{item}', (imgSpriteSize, imgSpriteSize)))
            elif str(item)[:2] == 'c1': AsteroidImgE[imgSize].append(gameImageLoad(f'assets/asteroids/{imgSize}/{item}', (imgSpriteSize, imgSpriteSize)))
            elif str(item)[:2] == 'c3': AsteroidImgF[imgSize].append(gameImageLoad(f'assets/asteroids/{imgSize}/{item}', (imgSpriteSize, imgSpriteSize)))
            elif str(item)[:2] == 'c4': AsteroidImgG[imgSize].append(gameImageLoad(f'assets/asteroids/{imgSize}/{item}', (imgSpriteSize, imgSpriteSize)))


# Genera una posición aleatoria para asteroides lejos del jugador
def generate_random_location():
    playerPosX, playerPosY = player.pos
    validLocation = False

    while not validLocation:
        asteroidPosX = random.randrange(0, SCREENWIDTH)
        asteroidPosY = random.randrange(0, SCREENHEIGHT)
        asteroidLocation = Vector2(asteroidPosX, asteroidPosY)

        # Debe estar a más de 100px del jugador
        if asteroidLocation.distance_to(player.pos) >= 100:
            validLocation = True

    return asteroidLocation


# Si ya no hay asteroides, sube de nivel
def check_asteroidCount_increase_stage():
    global STAGE
    if len(asteroidObjects) == 0 and not GAMEOVER:
        STAGE += 1           # aumenta etapa
        generate_asteroids() # genera más asteroides


# Genera asteroides dependiendo del nivel actual
def generate_asteroids():
    for _ in range(STAGE):
        asteroidObjects.append(Asteroid('large'))


# Reinicia ciertos valores tras perder una vida
def resetAfterLosingALife():
    player.pos = (SCREENWIDTH//2, SCREENHEIGHT//2)
    player.direction = Vector2(0, -1)
    player.velocity = Vector2()
    playerBullets.clear()

    if not GAMEOVER:
        for index, asteroidObject in enumerate(asteroidObjects):
            asteroidObject.pos = generate_random_location()
        pygame.time.wait(5000)
    else:
        asteroidObjects.clear()


# Calcula la cantidad total de fragmentos restantes
def calculateTotalNumAsteroids():
    numAsteroids = 0
    for asteroidObject in asteroidObjects:
        if asteroidObject.size == 'large': numAsteroids += 7
        elif asteroidObject.size == 'medium': numAsteroids += 3
        else: numAsteroids += 1
    return numAsteroids


# Crea texto con sombra para UI
def textScreen(message, size=32, color=(255,255,255), shadow=True):
    font = pygame.font.SysFont("consolas", size, bold=True)
    text = font.render(message, True, color)

    if shadow:
        shadow_surf = font.render(message, True, (0,0,0))
        return shadow_surf, text
    return None, text



# -------------------------------------------------------------------
# RENDERIZADOR PRINCIPAL DE PANTALLA
# -------------------------------------------------------------------

def gameWindowUpdating():
    GAMESCREEN.blit(BGIMG, (0, 0))   # Fondo

    if not GAMEOVER:
        # Dibuja balas
        for bullet in playerBullets:
            bullet.draw(GAMESCREEN)

        # Dibuja asteroides
        for asteroidObject in asteroidObjects:
            asteroidObject.draw(GAMESCREEN)
            asteroidObject._animate_image()

        # Dibuja jugador
        player.draw(GAMESCREEN)

    # Muestra vidas con imágenes de corazón
    for i in range(LIVES):
        GAMESCREEN.blit(heartImg, (40 + i*35, 25))

    # Score y mejor puntaje
    shadow, score = textScreen(f"SCORE {SCORE}", 32,(255,230,0))
    GAMESCREEN.blit(shadow,(SCREENWIDTH-200,25))
    GAMESCREEN.blit(score,(SCREENWIDTH-200,25))

    shadow, topscore = textScreen(f"BEST {TOPSCORE}", 28,(0,255,255))
    GAMESCREEN.blit(shadow,(SCREENWIDTH-200,60))
    GAMESCREEN.blit(topscore,(SCREENWIDTH-200,60))

    # Nivel actual
    shadow, stage = textScreen(f"STAGE {STAGE}", 30,(140,255,140))
    GAMESCREEN.blit(shadow,(85,85))
    GAMESCREEN.blit(stage,(85,85))

    # Barra de progreso (fragmentos restantes)
    numAsteroids = calculateTotalNumAsteroids()
    total = STAGE * 7
    barW = 200

    pygame.draw.rect(GAMESCREEN,(60,60,60),(25,70,barW,14),border_radius=10)
    pygame.draw.rect(GAMESCREEN,(80,255,80),(25,70,barW*(numAsteroids/total),14),border_radius=10)

    # Pantalla GAME OVER
    if GAMEOVER:
        shadow, gameOverText = textScreen("GAME OVER! Press TAB to restart", 46,(255,50,50))
        GAMESCREEN.blit(shadow,(SCREENWIDTH//2 - gameOverText.get_width()//2-2,SCREENHEIGHT//2-40))
        GAMESCREEN.blit(gameOverText,(SCREENWIDTH//2 - gameOverText.get_width()//2,SCREENHEIGHT//2-40))

    pygame.display.update()



# -------------------------------------------------------------------
# CLASE JUGADOR
# -------------------------------------------------------------------

class Player:
    def __init__(self, coOrds):
        self.img = PlayerImg
        self.imgRect = self.img.get_rect()
        self.x, self.y = coOrds
        self.width = self.img.get_width()
        self.height = self.img.get_height()

        # Centrar
        self.imgRect.x = self.x - self.width//2
        self.imgRect.y = self.y - self.height//2

        self.pos = Vector2(self.imgRect.x, self.imgRect.y)
        self.direction = Vector2(0, -1)  # apunta hacia arriba
        self.velocity = Vector2()
        self.rotation_speed = object_rotation_speed
        self.speed = object_speed

    # Avanzar utilizando vector dirección
    def accelerate(self):
        self.velocity += self.direction * self.speed
        if self.velocity.length() > 4:
            self.velocity.scale_to_length(4)  # velocidad máxima

    # Rotación con teclas
    def rotation(self, rotation=1):
        angle = self.rotation_speed * rotation
        self.direction.rotate_ip(angle)

    # Si sale por un borde, aparece del otro lado
    def _wrap_to_screen(self, position):
        self.x, self.y = position
        return Vector2(self.x % SCREENWIDTH, self.y % SCREENHEIGHT)

    # Actualiza posición
    def move(self):
        self.pos = self._wrap_to_screen(self.pos + self.velocity)
        self.imgRect.x, self.imgRect.y = self.pos[0] - self.width//2, self.pos[1] - self.height//2

    # Render del jugador
    def draw(self, window):
        angle = self.direction.angle_to(Vector2(0, -1))
        rotated_img = pygame.transform.rotozoom(self.img, angle, 1.0)
        rotated_img_size = Vector2(rotated_img.get_size())
        blit_pos = self.pos - rotated_img_size * 0.5
        window.blit(rotated_img, blit_pos)
        #pygame.draw.rect(window,[255,255,255],[self.imgRect.x,self.imgRect.y,self.width,self.height],1)



# -------------------------------------------------------------------
# CLASE BALA
# -------------------------------------------------------------------

class Bullet:
    def __init__(self, coOrds, direction):
        self.width = 4
        self.height = 4
        self.pos = Vector2(coOrds[0], coOrds[1])
        self.direction = Vector2(direction[0], direction[1])
        self.velocity = Vector2()
        self.speed = 8

    # Mover bala
    def move(self):
        self.pos += (self.direction * self.speed)

    # Eliminar si sale de la pantalla
    def _check_if_offscreen(self):
        if self.pos[0] < 0 or self.pos[0] > SCREENWIDTH or self.pos[1] < 0 or self.pos[1] > SCREENHEIGHT:
            return True

    # Dibujar
    def draw(self, window):
        pygame.draw.rect(window,(255,255,255),[self.pos[0],self.pos[1],self.width,self.height])
        self.bulletRect = pygame.rect.Rect(int(self.pos[0]),int(self.pos[1]),self.width,self.height)



# -------------------------------------------------------------------
# CLASE ASTEROIDE (HEREDA PLAYER para reutilizar movimiento/rotación)
# -------------------------------------------------------------------

class Asteroid(Player):
    def __init__(self, size, coOrds=(0, 0), imgSet=None):
        super().__init__(coOrds)
        self.size = size

        self.x, self.y = generate_random_location() if self.size == 'large' else coOrds

        self.imgSet = self._generate_random_image_set() if not imgSet else imgSet

        # Frame inicial
        self.imgIndex = 0
        self.img = self.imgSet[self.size][self.imgIndex]

        self.width = self.img.get_width()//2
        self.height = self.img.get_height()//2

        self.imgRect.x = self.x - self.width//2
        self.imgRect.y = self.y - self.height//2
        self.imgRect = pygame.rect.Rect(self.imgRect.x,self.imgRect.y,self.width,self.height)

        self.direction = Vector2(random.randrange(-100,100)/100, random.randrange(-100,100)/100)
        self.speed = random.randrange(3,6)

        self.imgInd = 0
        self.animate_speed = random.randrange(3,7)

        # Salud según tamaño
        self.health = 3 if self.size == 'large' else 2 if self.size == 'medium' else 1
        self.score  = 10 if self.size == 'large' else 20 if self.size == 'medium' else 50

    # Elige set aleatorio de imágenes grandes
    def _generate_random_image_set(self):
        if self.size == 'large':
            return random.choice([AsteroidImgA,AsteroidImgB,AsteroidImgC,AsteroidImgD,AsteroidImgE,AsteroidImgF,AsteroidImgF])

    # Velocidad
    def accelerate(self):
        self.velocity = self.direction * self.speed

    # Animación de sprites
    def _animate_image(self):
        self.imgInd += 1
        if self.imgInd % self.animate_speed == 0:
            self.imgIndex = self.imgInd // self.animate_speed
        if self.imgIndex == len(self.imgSet[self.size]) - 1:
            self.imgInd = 0
            self.imgIndex = 0
        self.img = self.imgSet[self.size][self.imgIndex]

    # Movimiento usando Player.move()
    def move(self):
        super().move()
        self.accelerate()




# -------------------------------------------------------------------
# VARIABLES GLOBALES Y CONFIGURACIÓN DEL JUEGO
# -------------------------------------------------------------------

SCREENWIDTH  = 1200
SCREENHEIGHT = 700
object_rotation_speed = 3
object_speed = 0.10
CLOCK = pygame.time.Clock()
STAGE = 0
LIVES = 3
GAMEOVER = False
SCORE = 0
TOPSCORE = openTopScoreFile() # ← lee récord


# Crear ventana principal
GAMESCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption('Asteroids')

# Icono
icnImg = gameImageLoad('assets/Nave.png',(20,20))
icnImg = pygame.transform.rotate(icnImg, -90)
pygame.display.set_icon(icnImg)


# Carga de imágenes
BGIMG = gameImageLoad('assets/mapa.png',(SCREENWIDTH,SCREENHEIGHT))
AsteroidImgA = {'large': [], 'medium': [], 'small': []}
AsteroidImgB = {'large': [], 'medium': [], 'small': []}
AsteroidImgC = {'large': [], 'medium': [], 'small': []}
AsteroidImgD = {'large': [], 'medium': [], 'small': []}
AsteroidImgE = {'large': [], 'medium': [], 'small': []}
AsteroidImgF = {'large': [], 'medium': [], 'small': []}
AsteroidImgG = {'large': [], 'medium': [], 'small': []}

PlayerImg = gameImageLoad('assets/Nave.png',(65,65))  # Nave
heartImg  = pygame.image.load("assets/corazon.png").convert_alpha()
heartImg  = pygame.transform.scale(heartImg,(32,32))   # corazones UI

# Sonidos
shootSound     = pygame.mixer.Sound('assets/sounds/laser.wav')
explSound      = pygame.mixer.Sound('assets/sounds/bangSmall.wav')
shipExplSound  = pygame.mixer.Sound('assets/sounds/bangLarge.wav')


# Carga de asteroides y creación del jugador
asteroidImageLoading()
player = Player((SCREENWIDTH//2,SCREENHEIGHT//2))


# Listas de objetos
playerBullets   = []
asteroidObjects = []


# -------------------------------------------------------------------
# CICLO PRINCIPAL DEL JUEGO
# -------------------------------------------------------------------

RUNGAME = True
while RUNGAME:

    if not GAMEOVER:
        check_asteroidCount_increase_stage() # pasar de nivel

        # Mover jugador
        player.move()

        # Mover balas
        for ind, bullet in enumerate(playerBullets):
            bullet.move()

            # Eliminar si sale
            if bullet._check_if_offscreen():
                del playerBullets[ind]
                break

        # Colisiones bala ↔ asteroide
        for ind, asteroidObject in enumerate(asteroidObjects):
            asteroidObject.move()

            for index, bullet in enumerate(playerBullets):
                if bullet.bulletRect.colliderect(asteroidObject.imgRect):
                    
                    asteroidObject.health -= 1
                    SCORE += asteroidObject.score

                    # Si muere, se divide en más pequeños
                    if asteroidObject.health == 0:
                        if asteroidObject.size == 'large':
                            asteroidObjects.append(Asteroid('medium', asteroidObject.pos, asteroidObject.imgSet))
                            asteroidObjects.append(Asteroid('medium', asteroidObject.pos, asteroidObject.imgSet))

                        elif asteroidObject.size == 'medium':
                            asteroidObjects.append(Asteroid('small', asteroidObject.pos, asteroidObject.imgSet))
                            asteroidObjects.append(Asteroid('small', asteroidObject.pos, asteroidObject.imgSet))

                        del asteroidObjects[ind]
                        explSound.play()

                    del playerBullets[index]
                    break

            # Colisión jugador ↔ asteroide
            if asteroidObject.imgRect.colliderect(player.imgRect):
                LIVES -= 1
                shipExplSound.play()

                if LIVES <= 0:
                    GAMEOVER = True
                    saveTopScoreFile() # guarda récord si corresponde
                    SCORE = 0
                else:
                    resetAfterLosingALife()
                    del asteroidObjects[ind]
                    break
                break


    # Eventos de teclado
    for event in pygame.event.get():

        if event.type == pygame.QUIT: RUNGAME = False
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE: RUNGAME = False

            # Disparo
            if event.key == pygame.K_SPACE:
                playerBullets.append(Bullet(player.pos, player.direction))
                shootSound.play()

            # Restart si está en GAME OVER
            if GAMEOVER:
                if event.key == pygame.K_TAB:
                    resetAfterLosingALife()
                    STAGE = 1
                    LIVES = 3
                    generate_asteroids()
                    GAMEOVER = False


    # Movimiento con teclas
    keys_pressed = pygame.key.get_pressed()

    if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:   player.rotation(-1)
    elif keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]: player.rotation(1)

    if keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w]: player.accelerate()

    # Movimiento hacia atrás
    if keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]:
        player.velocity -= player.direction * player.speed
        if player.velocity.length() > 4:
            player.velocity.scale_to_length(4)

    # Actualizar pantalla
    gameWindowUpdating()
    CLOCK.tick(60)


pygame.quit()
sys.exit()
