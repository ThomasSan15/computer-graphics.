import sys, os
import pygame
from pygame import Vector2
import random
import cv2
import mediapipe as mp
import numpy as np
import math

pygame.init()  # Inicializa pygame

# ==========================
#     FUNCIONES UTILES
# ==========================

def openTopScoreFile():
    """Lee el archivo con el puntaje más alto registrado"""
    with open('TopScoreFile.txt') as file:
        topScore = int(file.read())
    file.close()
    return topScore


def saveTopScoreFile():
    """Guarda el nuevo record si SCORE es mayor al TOPSCORE anterior"""
    global TOPSCORE
    if SCORE > TOPSCORE:
        TOPSCORE = SCORE
        with open('TopScoreFile.txt', 'w') as file:
            file.write(str(TOPSCORE))
        file.close()
    return


def gameImageLoad(imagefilepath, size):
    """Carga una imagen y la escala al tamaño especificado"""
    image = pygame.image.load(imagefilepath)
    image = pygame.transform.scale(image, (size[0], size[1]))
    return image


def asteroidImageLoading():
    """Carga en memoria todas las imágenes de asteroides según su tamaño"""
    large = 180
    medium = 125
    small = 75
    for imgSize in ['large', 'medium', 'small']:  # Recorre carpetas
        if imgSize == 'large':
            imgSpriteSize = large
        elif imgSize == 'medium':
            imgSpriteSize = medium
        else:
            imgSpriteSize = small
        
        # Carga imágenes dependiendo del prefijo del archivo
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
    """Genera una posición aleatoria en pantalla alejada del jugador"""
    playerPosX, playerPosY = player.pos
    validLocation = False
    while not validLocation:
        asteroidPosX = random.randrange(0, SCREENWIDTH)
        asteroidPosY = random.randrange(0, SCREENHEIGHT)
        asteroidLocation = Vector2(asteroidPosX, asteroidPosY)
        if asteroidLocation.distance_to(player.pos) >= 100:  # Evita nacer encima del jugador
            validLocation = True
    return asteroidLocation


def check_asteroidCount_increase_stage():
    """Si ya no quedan asteroides, incrementa la etapa y genera más"""
    global STAGE
    if len(asteroidObjects) == 0 and not GAMEOVER:
        STAGE += 1
        generate_asteroids()


def generate_asteroids():
    """Genera asteroides grandes dependiendo de la etapa actual"""
    for _ in range(STAGE):
        asteroidObjects.append(Asteroid('large'))


def resetAfterLosingALife():
    """Reinicia posición del jugador y asteroides tras perder vida"""
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
    """Devuelve la cantidad de asteroides restantes (incluyendo divisiones futuras)"""
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
    """Renderiza texto con opción de sombra"""
    font = pygame.font.SysFont("consolas", size, bold=True)
    text = font.render(message, True, color)

    if shadow:
        shadow_surf = font.render(message, True, (0,0,0))
        return shadow_surf, text
    return None, text


def gameWindowUpdating():
    """Dibuja todos los elementos en pantalla y actualiza el frame"""
    GAMESCREEN.blit(BGIMG, (0, 0))

    if not GAMEOVER:
        for bullet in playerBullets:
            bullet.draw(GAMESCREEN)

        for asteroidObject in asteroidObjects:
            asteroidObject.draw(GAMESCREEN)
            asteroidObject._animate_image()

        player.draw(GAMESCREEN)

    # ♥ Dibuja vidas con corazones PNG
    for i in range(LIVES):
        GAMESCREEN.blit(heartImg, (40 + i*35, 25))

    # Texto Score y Best Score
    shadow, score = textScreen(f"SCORE {SCORE}", 32,(255,230,0))
    GAMESCREEN.blit(shadow,(SCREENWIDTH-200,25))
    GAMESCREEN.blit(score,(SCREENWIDTH-200,25))

    shadow, topscore = textScreen(f"BEST {TOPSCORE}", 28,(0,255,255))
    GAMESCREEN.blit(shadow,(SCREENWIDTH-200,60))
    GAMESCREEN.blit(topscore,(SCREENWIDTH-200,60))

    # ★ Etapa
    shadow, stage = textScreen(f"STAGE {STAGE}", 30,(140,255,140))
    GAMESCREEN.blit(shadow,(85,85))
    GAMESCREEN.blit(stage,(85,85))

    # Barra de progreso de asteroides restantes
    numAsteroids = calculateTotalNumAsteroids()
    total = STAGE * 7
    barW = 200
    pygame.draw.rect(GAMESCREEN,(60,60,60),(25,70,barW,14),border_radius=10)
    pygame.draw.rect(GAMESCREEN,(80,255,80),(25,70,barW*(numAsteroids/total),14),border_radius=10)

    # Pantalla de Game Over
    if GAMEOVER:
        shadow, gameOverText = textScreen("GAME OVER! Press TAB to restart", 46,(255,50,50))
        GAMESCREEN.blit(shadow,(SCREENWIDTH//2 - gameOverText.get_width()//2-2,SCREENHEIGHT//2-40))
        GAMESCREEN.blit(gameOverText,(SCREENWIDTH//2 - gameOverText.get_width()//2,SCREENHEIGHT//2-40))

    pygame.display.update()


# ==============================
#       CLASE PLAYER
# ==============================

class Player:
    """Jugador/Nave controlada por el usuario"""

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
        """Aumenta velocidad en la dirección apuntada"""
        self.velocity += self.direction * self.speed
        if self.velocity.length() > 4:  # Velocidad máxima
            self.velocity.scale_to_length(4)

    def rotation(self, rotation=1):
        """Rota la nave"""
        angle = self.rotation_speed * rotation
        self.direction.rotate_ip(angle)

    def _wrap_to_screen(self, position):
        """Hace que el jugador aparezca del otro lado de la pantalla"""
        self.x, self.y = position
        return Vector2(self.x % SCREENWIDTH, self.y % SCREENHEIGHT)

    def move(self):
        """Actualiza movimiento"""
        self.pos = self._wrap_to_screen(self.pos + self.velocity)
        self.imgRect.x, self.imgRect.y = self.pos[0] - self.width//2, self.pos[1] - self.height//2

    def draw(self, window):
        """Dibuja la nave rotando correctamente"""
        angle = self.direction.angle_to(Vector2(0, -1))
        rotated_img = pygame.transform.rotozoom(self.img, angle, 1.0)
        rotated_img_size = Vector2(rotated_img.get_size())
        blit_pos = self.pos - rotated_img_size * 0.5
        window.blit(rotated_img, blit_pos)


# ==============================
#         BALAS
# ==============================

class Bullet:
    """Objeto proyectil disparado por el jugador"""

    def __init__(self, coOrds, direction):
        self.width = 4
        self.height = 4
        self.pos = Vector2(coOrds[0], coOrds[1])
        self.direction = Vector2(direction[0], direction[1])
        self.velocity = Vector2()
        self.speed = 8

    def move(self):
        """Movimiento recto constante"""
        self.pos += (self.direction * self.speed)

    def _check_if_offscreen(self):
        """Destruye bala si sale de pantalla"""
        if self.pos[0] < 0 or self.pos[0] > SCREENWIDTH or self.pos[1] < 0 or self.pos[1] > SCREENHEIGHT:
            return True

    def draw(self, window):
        """Dibuja bala y actualiza hitbox"""
        pygame.draw.rect(window, (255, 255, 255), [self.pos[0], self.pos[1], self.width, self.height])
        self.bulletRect = pygame.rect.Rect(int(self.pos[0]), int(self.pos[1]), self.width, self.height)


# ==============================
#       ASTEROIDES
# ==============================

class Asteroid(Player):
    """Asteroide con rotación, colisión y división"""

    def __init__(self, size, coOrds=(0, 0), imgSet=None):
        super().__init__(coOrds)
        self.size = size
        self.x, self.y = generate_random_location() if self.size == 'large' else coOrds
        self.imgSet = self._generate_random_image_set() if not imgSet else imgSet
        self.imgIndex = 0
        self.img = self.imgSet[self.size][self.imgIndex]
        self.width = self.img.get_width()//2
        self.height = self.img.get_height()//2
        self.imgRect.x = self.x - self.width//2
        self.imgRect.y = self.y - self.height//2
        self.imgRect = pygame.rect.Rect(self.imgRect.x, self.imgRect.y, self.width, self.height)

        # Movimiento aleatorio
        self.direction = Vector2(random.randrange(-100, 100)/100, random.randrange(-100, 100)/100)
        self.speed = random.randrange(3, 6)

        # Animación
        self.imgInd = 0
        self.animate_speed = random.randrange(3, 7)

        # Vida y puntaje según tamaño
        self.health = 3 if self.size == 'large' else 2 if self.size == 'medium' else 1
        self.score = 10 if self.size == 'large' else 20 if self.size == 'medium' else 50

    def _generate_random_image_set(self):
        """Retorna set aleatorio de sprites para animación"""
        if self.size == 'large':
            imgSet = random.choice([AsteroidImgA, AsteroidImgB, AsteroidImgC,
                                    AsteroidImgD, AsteroidImgE, AsteroidImgF,
                                    AsteroidImgF])
            return imgSet

    def accelerate(self):
        """Actualiza velocidad base"""
        self.velocity = self.direction * self.speed

    def _animate_image(self):
        """Cambia sprite para animar rotación"""
        self.imgInd += 1
        if self.imgInd % self.animate_speed == 0:
            self.imgIndex = self.imgInd // self.animate_speed
        if self.imgIndex == len(self.imgSet[self.size]) - 1:
            self.imgInd = 0
            self.imgIndex = 0
        self.img = self.imgSet[self.size][self.imgIndex]

    def move(self):
        """Actualiza movimiento y aplica velocidad"""
        super().move()
        self.accelerate()


# ==============================
#   VARIABLES DEL JUEGO
# ==============================

SCREENWIDTH = 1200
SCREENHEIGHT = 700
object_rotation_speed = 3
object_speed = 0.10
CLOCK = pygame.time.Clock()
STAGE = 0
LIVES = 3
GAMEOVER = False
SCORE = 0
TOPSCORE = openTopScoreFile()  # Carga record previo

# ==============================
#   VENTANA PRINCIPAL
# ==============================

GAMESCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption('Asteroids')

# Icono de la ventana
icnImg = gameImageLoad('assets/Nave.png', (20, 20))
icnImg = pygame.transform.rotate(icnImg, -90)
pygame.display.set_icon(icnImg)

# ==============================
#   CARGA DE ASSETS
# ==============================

BGIMG = gameImageLoad('assets/mapa.png', (SCREENWIDTH, SCREENHEIGHT))

# Diccionarios donde se guardarán sprites animados
AsteroidImgA = {'large': [], 'medium': [], 'small': []}
AsteroidImgB = {'large': [], 'medium': [], 'small': []}
AsteroidImgC = {'large': [], 'medium': [], 'small': []}
AsteroidImgD = {'large': [], 'medium': [], 'small': []}
AsteroidImgE = {'large': [], 'medium': [], 'small': []}
AsteroidImgF = {'large': [], 'medium': [], 'small': []}
AsteroidImgG = {'large': [], 'medium': [], 'small': []}

PlayerImg = gameImageLoad('assets/Nave.png', (65, 65))  # Nave del jugador

heartImg = pygame.image.load("assets/corazon.png").convert_alpha()  # Corazón vida
heartImg = pygame.transform.scale(heartImg, (32, 32))

# Sonidos
shootSound = pygame.mixer.Sound('assets/sounds/laser.wav')
explSound = pygame.mixer.Sound('assets/sounds/bangSmall.wav')
shipExplSound = pygame.mixer.Sound('assets/sounds/bangLarge.wav')

# ==============================
#   OBJETOS INICIALES DEL JUEGO
# ==============================

asteroidImageLoading()  # Carga sprites
player = Player((SCREENWIDTH//2, SCREENHEIGHT//2))

playerBullets = []      # Lista de balas activas
asteroidObjects = []    # Asteroides en juego
# Disparo automático: intervalo entre balas (ms)
shot_interval_ms = 220
last_shot_time = 0

# ==============================
#      BUCLE PRINCIPAL
# ==============================

# -----------------------------
# Inicialización control por mano
# -----------------------------
use_hand_control = False
cap = None
hands_detector = None
try:
    cap = cv2.VideoCapture(0)
    mp_hands = mp.solutions.hands
    hands_detector = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.6)
    mp_draw = mp.solutions.drawing_utils
    use_hand_control = True
    print('Hand control initialized')
    # Parámetros de suavizado para reducir temblor
    hand_pos_alpha = 0.35  # mayor = sigue más rápido
    hand_dir_alpha = 0.5
    last_hand_pos = Vector2(player.pos)
    last_hand_dir = Vector2(player.direction)
    # Corrección de signo para la rotación (si la rotación se siente invertida)
    # Se inicializa neutro; se ajustará automáticamente según la mano detectada.
    hand_rotation_flip = 1
except Exception as e:
    print('Hand control not available:', e)

RUNGAME = True
while RUNGAME:

    if not GAMEOVER:

        check_asteroidCount_increase_stage()  # Cambia etapa si no quedan asteroides

        # -------------------------
        # Lectura de cámara y control por mano (si está disponible)
        # -------------------------
        if use_hand_control and cap is not None and hands_detector is not None:
            ret, frame = cap.read()
            if ret:
                frame = cv2.flip(frame, 1)
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = hands_detector.process(rgb_frame)

                if results.multi_hand_landmarks:
                    # Usamos la primera mano detectada
                    hand_landmarks = results.multi_hand_landmarks[0]
                    lm = hand_landmarks.landmark

                    # --- POSICIÓN: usar punta del pulgar (landmark 4) ---
                    thumb_tip = lm[4]
                    measured_x = thumb_tip.x * SCREENWIDTH
                    measured_y = thumb_tip.y * SCREENHEIGHT
                    measured_pos = Vector2(measured_x, measured_y)

                    # Suavizar posición (exponential smoothing)
                    last_hand_pos = last_hand_pos * (1.0 - hand_pos_alpha) + measured_pos * hand_pos_alpha
                    player.pos = Vector2(last_hand_pos)
                    player.imgRect.x = int(player.pos[0] - player.width//2)
                    player.imgRect.y = int(player.pos[1] - player.height//2)

                    # Determinar automáticamente si hay que invertir la rotación
                    # usando la clasificación de mano que devuelve MediaPipe.
                    if hasattr(results, 'multi_handedness') and results.multi_handedness:
                        try:
                            handedness_label = results.multi_handedness[0].classification[0].label
                            # Ajuste heurístico: para la 'Right' hand invertimos el signo
                            # (esto corrige la inversión causada por la vista espejo en la mayoría de webcams)
                            if handedness_label == 'Right':
                                hand_rotation_flip = -1
                            else:
                                hand_rotation_flip = 1
                        except Exception:
                            pass

                    # --- ROTACIÓN: usar vector wrist (0) -> thumb_tip (4) ---
                    wrist = lm[0]
                    vx = thumb_tip.x - wrist.x
                    vy = thumb_tip.y - wrist.y
                    # Convertir a coordenadas del juego (y hacia arriba)
                    measured_dir = Vector2(vx, -vy)
                    if measured_dir.length() > 1e-6:
                        # Calculamos ángulo medido
                        measured_angle = math.atan2(measured_dir.y, measured_dir.x)

                        # Invertimos el sentido de rotación (problema reportado)
                        corrected_angle = -measured_angle

                        # Suavizar ángulo con interpolación polar
                        try:
                            last_angle = math.atan2(last_hand_dir.y, last_hand_dir.x)
                        except Exception:
                            last_angle = corrected_angle

                        # Interpolación angular segura (evita saltos en -pi/pi)
                        def lerp_angle(a, b, t):
                            diff = (b - a + math.pi) % (2 * math.pi) - math.pi
                            return a + diff * t

                        mixed_angle = lerp_angle(last_angle, corrected_angle, hand_dir_alpha)

                        # Actualizar vectores
                        new_dir = Vector2(math.cos(mixed_angle), math.sin(mixed_angle))
                        last_hand_dir = Vector2(new_dir)
                        player.direction = Vector2(new_dir)

                # Opcional: dibujar ventana de cámara con landmarks para debug
                # mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                # cv2.imshow('Hand Camera', frame)
                # cv2.waitKey(1)

        # -------------------------
        # Movimiento de jugador
        # -------------------------
        player.move()

        # -------------------------
        # Disparo automático continuo (sin gesto)
        # -------------------------
        now = pygame.time.get_ticks()
        if now - last_shot_time >= shot_interval_ms:
            playerBullets.append(Bullet(player.pos, player.direction))
            try:
                shootSound.play()
            except Exception:
                pass
            last_shot_time = now

        # -------------------------
        # Movimiento de Balas
        # -------------------------
        for ind, bullet in enumerate(playerBullets):
            bullet.move()

            # Si sale de pantalla, se elimina
            if bullet._check_if_offscreen():
                del playerBullets[ind]
                break

        # -------------------------
        # Movimiento de Asteroides + Colisiones
        # -------------------------
        for ind, asteroidObject in enumerate(asteroidObjects):
            asteroidObject.move()

            # Colisión bala ↔ asteroide
            for index, bullet in enumerate(playerBullets):
                if hasattr(bullet, 'bulletRect') and bullet.bulletRect.colliderect(asteroidObject.imgRect):
                    asteroidObject.health -= 1
                    SCORE += asteroidObject.score

                    if asteroidObject.health == 0:
                        # Asteroide grande se divide
                        if asteroidObject.size == 'large':
                            asteroidObjects.append(Asteroid('medium', asteroidObject.pos, asteroidObject.imgSet))
                            asteroidObjects.append(Asteroid('medium', asteroidObject.pos, asteroidObject.imgSet))

                        # Mediano → pequeño
                        elif asteroidObject.size == 'medium':
                            asteroidObjects.append(Asteroid('small', asteroidObject.pos, asteroidObject.imgSet))
                            asteroidObjects.append(Asteroid('small', asteroidObject.pos, asteroidObject.imgSet))

                        del asteroidObjects[ind]
                        explSound.play()

                    del playerBullets[index]
                    break

            # Colisión nave ↔ asteroide
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

    # ========================================
    #         EVENTOS DEL TECLADO
    # ========================================

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNGAME = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                RUNGAME = False

            # Disparo
            if event.key == pygame.K_SPACE:
                playerBullets.append(Bullet(player.pos, player.direction))
                shootSound.play()

            # Invertir rotación de mano (toggle)
            if event.key == pygame.K_r:
                try:
                    hand_rotation_flip *= -1
                    print(f'hand_rotation_flip = {hand_rotation_flip}')
                except NameError:
                    pass

            # Reiniciar tras Game Over
            if GAMEOVER and event.key == pygame.K_TAB:
                resetAfterLosingALife()
                STAGE = 1
                LIVES = 3
                generate_asteroids()
                GAMEOVER = False

    # ==========================
    #   CONTROLES NAVE
    # ==========================

    keys_pressed = pygame.key.get_pressed()

    if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:
        player.rotation(-1)
    elif keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:
        player.rotation(1)

    # Avanzar
    if keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w]:
        player.accelerate()

    # Retroceso (inverso)
    if keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]:
        player.velocity -= player.direction * player.speed
        if player.velocity.length() > 4:
            player.velocity.scale_to_length(4)

    # Dibuja todo
    gameWindowUpdating()
    CLOCK.tick(60)  # Limitación FPS

# Limpieza recursos de cámara / MediaPipe si se activó control por mano
if use_hand_control:
    try:
        if hands_detector is not None:
            hands_detector.close()
        if cap is not None:
            cap.release()
        cv2.destroyAllWindows()
    except Exception:
        pass

pygame.quit()
sys.exit()
