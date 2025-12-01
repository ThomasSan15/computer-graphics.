import sys, os
import pygame
from pygame import Vector2
import random


pygame.init()


#  Utility Functions
def openTopScoreFile():
    with open('TopScoreFile.txt') as file:
        topScore = int(file.read())
    file.close()
    return topScore


def saveTopScoreFile():
    global TOPSCORE
    if SCORE > TOPSCORE:
        TOPSCORE = SCORE
        with open('TopScoreFile.txt', 'w') as file:
            file.write(str(TOPSCORE))
        file.close()
    return


def gameImageLoad(imagefilepath, size):
    """A utility function, for loading all of the game assets, and converting sizes where necessary"""
    image = pygame.image.load(imagefilepath)
    image = pygame.transform.scale(image, (size[0], size[1]))
    return image


def asteroidImageLoading():
    """Utility function for mass loading the various asteroid images"""
    large = 180
    medium = 125
    small = 75
    for imgSize in ['large', 'medium', 'small']:
        if imgSize == 'large':
            imgSpriteSize = large
        elif imgSize == 'medium':
            imgSpriteSize = medium
        else:
            imgSpriteSize = small
        for item in os.listdir(f'assets/asteroids/{imgSize}'):
            if str(item)[:2] == 'a1':
                AsteroidImgA[imgSize].append(gameImageLoad(f'assets/asteroids/{imgSize}/{item}', (imgSpriteSize, imgSpriteSize)))
            elif str(item)[:2] == 'a3':
                AsteroidImgB[imgSize].append(gameImageLoad(f'assets/asteroids/{imgSize}/{item}', (imgSpriteSize, imgSpriteSize)))
            elif str(item)[:2] == 'b1':
                AsteroidImgC[imgSize].append(gameImageLoad(f'assets/asteroids/{imgSize}/{item}', (imgSpriteSize, imgSpriteSize)))
            elif str(item)[:2] == 'b3':
                AsteroidImgD[imgSize].append(gameImageLoad(f'assets/asteroids/{imgSize}/{item}', (imgSpriteSize, imgSpriteSize)))
            elif str(item)[:2] == 'c1':
                AsteroidImgE[imgSize].append(gameImageLoad(f'assets/asteroids/{imgSize}/{item}', (imgSpriteSize, imgSpriteSize)))
            elif str(item)[:2] == 'c3':
                AsteroidImgF[imgSize].append(gameImageLoad(f'assets/asteroids/{imgSize}/{item}', (imgSpriteSize, imgSpriteSize)))
            elif str(item)[:2] == 'c4':
                AsteroidImgG[imgSize].append(gameImageLoad(f'assets/asteroids/{imgSize}/{item}', (imgSpriteSize, imgSpriteSize)))


def generate_random_location():
    """Generate the random location of asteroids, a certain distance away from the player character"""
    playerPosX, playerPosY = player.pos
    validLocation = False
    while not validLocation:
        asteroidPosX = random.randrange(0, SCREENWIDTH)
        asteroidPosY = random.randrange(0, SCREENHEIGHT)
        asteroidLocation = Vector2(asteroidPosX, asteroidPosY)
        if asteroidLocation.distance_to(player.pos) >= 100:
            validLocation = True
        else:
            continue
    return asteroidLocation


def check_asteroidCount_increase_stage():
    """Checks the number of asteroids currently on screen, then increases stage level"""
    global STAGE
    if len(asteroidObjects) == 0 and not GAMEOVER:
        STAGE += 1
        generate_asteroids()


def generate_asteroids():
    """Generates asteroids per the stage level"""
    for _ in range(STAGE):
        asteroidObjects.append(Asteroid('large'))


def resetAfterLosingALife():
    """"reset the player character to the middle of the screen, move the asteroids to new locations,
    clear screen of bullets."""
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


def calculateTotalNumAsteroids():
    """Calculates the total number of asteroids on the stage"""
    numAsteroids = 0
    for asteroidObject in asteroidObjects:
        if asteroidObject.size == 'large':
            numAsteroids += 7
        elif asteroidObject.size == 'medium':
            numAsteroids += 3
        else:
            numAsteroids += 1
    return numAsteroids


def textScreen(message, size=32, color=(255,255,255), shadow=True):
    font = pygame.font.SysFont("consolas", size, bold=True)

    text = font.render(message, True, color)

    # Sombra opcional
    if shadow:
        shadow_surf = font.render(message, True, (0,0,0))
        return shadow_surf, text
    return None, text



def gameWindowUpdating():
    GAMESCREEN.blit(BGIMG, (0, 0))

    if not GAMEOVER:
        for bullet in playerBullets:
            bullet.draw(GAMESCREEN)

        for asteroidObject in asteroidObjects:
            asteroidObject.draw(GAMESCREEN)
            asteroidObject._animate_image()

        player.draw(GAMESCREEN)

    # vida con corazones 
    
    # VIDAS CON PNG ❤️
    for i in range(LIVES):
        GAMESCREEN.blit(heartImg, (40 + i*35, 25))  # X + separación , Y


    # SCORE y TOPSCORE
    shadow, score = textScreen(f"SCORE {SCORE}", 32,(255,230,0))
    GAMESCREEN.blit(shadow,(SCREENWIDTH-200,25))
    GAMESCREEN.blit(score,(SCREENWIDTH-200,25))

    shadow, topscore = textScreen(f"BEST {TOPSCORE}", 28,(0,255,255))
    GAMESCREEN.blit(shadow,(SCREENWIDTH-200,60))
    GAMESCREEN.blit(topscore,(SCREENWIDTH-200,60))

    # ETAPA
    shadow, stage = textScreen(f"STAGE {STAGE}", 30,(140,255,140))
    GAMESCREEN.blit(shadow,(85,85))
    GAMESCREEN.blit(stage,(85,85))

    # BARRA DE ASTEROIDES RESTANTES
    numAsteroids = calculateTotalNumAsteroids()
    total = STAGE * 7

    barW = 200
    pygame.draw.rect(GAMESCREEN,(60,60,60),(25,70,barW,14),border_radius=10)  # Base
    pygame.draw.rect(GAMESCREEN,(80,255,80),(25,70,barW*(numAsteroids/total),14),border_radius=10)

    if GAMEOVER:
        shadow, gameOverText = textScreen("GAME OVER! Press TAB to restart", 46,(255,50,50))
        GAMESCREEN.blit(shadow,(SCREENWIDTH//2 - gameOverText.get_width()//2-2,SCREENHEIGHT//2-40))
        GAMESCREEN.blit(gameOverText,(SCREENWIDTH//2 - gameOverText.get_width()//2,SCREENHEIGHT//2-40))

    pygame.display.update()


#  Game Objects
class Player:
    def __init__(self, coOrds):
        self.img = PlayerImg
        self.imgRect = self.img.get_rect()
        self.x, self.y = coOrds
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.imgRect.x = self.x - self.width//2
        self.imgRect.y = self.y - self.height//2
        self.pos = Vector2(self.imgRect.x, self.imgRect.y)
        self.direction = Vector2(0, -1)
        self.velocity = Vector2()
        self.rotation_speed = object_rotation_speed
        self.speed = object_speed


    def accelerate(self):
        """Increases the speed of the player object"""
        self.velocity += self.direction * self.speed
         # limitar velocidad máxima
        if self.velocity.length() > 4:  
            self.velocity.scale_to_length(4)


    def rotation(self, rotation=1):
        """Accepts input for rotating the objcet"""
        angle = self.rotation_speed * rotation
        self.direction.rotate_ip(angle)


    def _wrap_to_screen(self, position):
        """Wraps the player to the screen"""
        self.x, self.y = position
        return Vector2(self.x % SCREENWIDTH, self.y % SCREENHEIGHT)


    def move(self):
        """Updates the position of the Object"""
        self.pos = self._wrap_to_screen(self.pos + self.velocity)
        self.imgRect.x, self.imgRect.y = self.pos[0] - self.width//2, self.pos[1] - self.height//2


    def draw(self, window):
        
        angle = self.direction.angle_to(Vector2(0, -1))
        rotated_img = pygame.transform.rotozoom(self.img, angle, 1.0)
        rotated_img_size = Vector2(rotated_img.get_size())
        blit_pos = self.pos - rotated_img_size * 0.5
        window.blit(rotated_img, blit_pos)
        #pygame.draw.rect(window, [255, 255, 255], [self.imgRect.x, self.imgRect.y, self.width, self.height], 1) #Hitbox de la nave


class Bullet:
    def __init__(self, coOrds, direction):
        self.width = 4
        self.height = 4
        self.pos = Vector2(coOrds[0], coOrds[1])
        self.direction = Vector2(direction[0], direction[1])
        self.velocity = Vector2()
        self.speed = 8
        #self.bulletRect = pygame.rect.Rect(int(self.pos[0]), int(self.pos[1]), self.width, self.height)


    def move(self):
        """Updates the position of the bullet"""
        self.pos += (self.direction * self.speed)


    def _check_if_offscreen(self):
        """Checks to see if the object is off the screen"""
        if self.pos[0] < 0 or self.pos[0] > SCREENWIDTH or self.pos[1] < 0 or self.pos[1] > SCREENHEIGHT:
            return True


    def draw(self, window):
        """Updates the position of the Object"""
        pygame.draw.rect(window, (255, 255, 255), [self.pos[0], self.pos[1], self.width, self.height])
        self.bulletRect = pygame.rect.Rect(int(self.pos[0]), int(self.pos[1]), self.width, self.height)


class Asteroid(Player):
    def __init__(self, size, coOrds=(0, 0), imgSet=None):
        super().__init__(coOrds)
        self.size = size
        self.x, self.y = generate_random_location() if self.size == 'large' else coOrds
        self.imgSet = self._generate_random_image_set() if not imgSet else imgSet
        self.imgIndex = 0
        self.img = self.imgSet[self.size][self.imgIndex]
        #self.imgRect = self.img.get_rect()
        self.width = self.img.get_width()//2
        self.height = self.img.get_height()//2
        self.imgRect.x = self.x - self.width//2
        self.imgRect.y = self.y - self.height//2
        self.imgRect = pygame.rect.Rect(self.imgRect.x, self.imgRect.y, self.width, self.height)
        self.direction = Vector2(random.randrange(-100, 100)/100, random.randrange(-100, 100)/100)
        self.speed = random.randrange(3, 6)
        self.imgInd = 0
        self.animate_speed = random.randrange(3, 7)
        self.health = 3 if self.size == 'large' else 2 if self.size == 'medium' else 1
        self.score = 10 if self.size == 'large' else 20 if self.size == 'medium' else 50


    def _generate_random_image_set(self):
        if self.size == 'large':
            imgSet = random.choice([AsteroidImgA, AsteroidImgB, AsteroidImgC,
                                    AsteroidImgD, AsteroidImgE, AsteroidImgF,
                                    AsteroidImgF])
            return imgSet


    def accelerate(self):
        """Increases the speed of the player object"""
        self.velocity = self.direction * self.speed


    def _animate_image(self):
        """Animates the Asteroid object at random animation speeds"""
        self.imgInd += 1
        if self.imgInd % self.animate_speed == 0:
            self.imgIndex = self.imgInd // self.animate_speed
        if self.imgIndex == len(self.imgSet[self.size]) - 1:
            self.imgInd = 0
            self.imgIndex = 0
        self.img = self.imgSet[self.size][self.imgIndex]


    def move(self):
        super().move()
        self.accelerate()


#  Game Settings Variables
SCREENWIDTH = 1200
SCREENHEIGHT = 700
object_rotation_speed = 3
object_speed = 0.10
CLOCK = pygame.time.Clock()
STAGE = 0
LIVES = 3
GAMEOVER = False
SCORE = 0
TOPSCORE = openTopScoreFile()


#  Pygame display window initialisation
GAMESCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption('Asteroids')
icnImg = gameImageLoad('assets/Nave.png', (20, 20))
icnImg = pygame.transform.rotate(icnImg, -90)
pygame.display.set_icon(icnImg)


#  Pygame loading game assets
BGIMG = gameImageLoad('assets/mapa.png', (SCREENWIDTH, SCREENHEIGHT))
AsteroidImgA = {'large': [], 'medium': [], 'small': []}
AsteroidImgB = {'large': [], 'medium': [], 'small': []}
AsteroidImgC = {'large': [], 'medium': [], 'small': []}
AsteroidImgD = {'large': [], 'medium': [], 'small': []}
AsteroidImgE = {'large': [], 'medium': [], 'small': []}
AsteroidImgF = {'large': [], 'medium': [], 'small': []}
AsteroidImgG = {'large': [], 'medium': [], 'small': []}
PlayerImg = gameImageLoad('assets/Nave.png', (65, 65))#Nave
heartImg = pygame.image.load("assets/corazon.png").convert_alpha() 
heartImg = pygame.transform.scale(heartImg, (32, 32))  # corazon
shootSound = pygame.mixer.Sound('assets/sounds/laser.wav')
explSound = pygame.mixer.Sound('assets/sounds/bangSmall.wav')
shipExplSound = pygame.mixer.Sound('assets/sounds/bangLarge.wav')


#  Run once off functions, load GameObjects
asteroidImageLoading()
player = Player((SCREENWIDTH//2, SCREENHEIGHT//2))

#  Game Object Lists
playerBullets = []
asteroidObjects = []

#object1 = Asteroid('large')
#asteroidObjects.append(object1)
#object2 = Asteroid('medium')
#asteroidObjects.append(object2)


#  Main Game Loop
RUNGAME = True
while RUNGAME:


    if not GAMEOVER:

        check_asteroidCount_increase_stage()


        #  Update game object movements
        player.move()
        for ind, bullet in enumerate(playerBullets):    #  Cycle through each of the bullet objects
            bullet.move()


            #  Check to see if the bullet object is offscreen
            if bullet._check_if_offscreen():
                del playerBullets[ind]
                break


        for ind, asteroidObject in enumerate(asteroidObjects):
            asteroidObject.move()
            for index, bullet in enumerate(playerBullets):
                if bullet.bulletRect.colliderect(asteroidObject.imgRect):
                    asteroidObject.health -= 1
                    SCORE += asteroidObject.score
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
            if asteroidObject.imgRect.colliderect(player.imgRect):
                LIVES -= 1
                shipExplSound.play()
                if LIVES <= 0:
                    GAMEOVER = True
                    saveTopScoreFile()
                    SCORE = 0
                else:
                    resetAfterLosingALife()
                    del asteroidObjects[ind]
                    break
                break


    #  Event handling for loop, check for quit, and Escape key
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNGAME = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                RUNGAME = False
            if event.key == pygame.K_SPACE:
                playerBullets.append(Bullet(player.pos, player.direction))
                shootSound.play()
            if GAMEOVER:
                if event.key == pygame.K_TAB:
                    resetAfterLosingALife()
                    STAGE = 1
                    LIVES = 3
                    generate_asteroids()
                    GAMEOVER = False


        #  Handling input
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:
        player.rotation(-1)
    elif keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:
        player.rotation(1)

    # Avanzar
    if keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w]:
        player.accelerate()

    # Retroceder
    if keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]:
        player.velocity -= player.direction * player.speed   # <-- Movimiento hacia atrás
         # limitar velocidad máxima
        if player.velocity.length() > 4:  
            player.velocity.scale_to_length(4)
        

    gameWindowUpdating()
    CLOCK.tick(60)

pygame.quit()
sys.exit()