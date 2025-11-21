import pygame


def load_resources(tamano=(800, 600)):
    """Inicializa el mixer y carga sonidos e imágenes (si existen).
    Devuelve un diccionario con keys: 'sounds', 'images', 'consts'.
    """
    # Inicializar mixer para sonidos
    sounds = {'raqueta': None, 'rebote': None, 'gol': None}
    try:
        pygame.mixer.init()
    except Exception:
        print('Advertencia: pygame.mixer no pudo inicializarse. No habrá sonido.')

    # Cargar sonidos respetando nombres presentes en el repo
    try:
        sounds['raqueta'] = pygame.mixer.Sound('Raqueta.mp3')
    except Exception:
        print('Aviso: no se encontró o no se pudo cargar "Raqueta.mp3"')
    try:
        sounds['rebote'] = pygame.mixer.Sound('Rebote.mp3')
    except Exception:
        print('Aviso: no se encontró o no se pudo cargar "Rebote.mp3"')
    try:
        sounds['gol'] = pygame.mixer.Sound('Gol.mp3')
    except Exception:
        print('Aviso: no se encontró o no se pudo cargar "Gol.mp3"')

    # Cargar imágenes
    images = {'presentacion': None, 'menu': None, 'ayuda': None}
    try:
        img = pygame.image.load('Presentacion.jpg')
        images['presentacion'] = pygame.transform.scale(img, tamano)
    except Exception:
        print('Aviso: no se pudo cargar Presentacion.jpg')
    try:
        img = pygame.image.load('Menu.jpg')
        images['menu'] = pygame.transform.scale(img, tamano)
    except Exception:
        print('Aviso: no se pudo cargar Menu.jpg')
    try:
        img = pygame.image.load('Ayuda.jpg')
        images['ayuda'] = pygame.transform.scale(img, tamano)
    except Exception:
        print('Aviso: no se pudo cargar Ayuda.jpg')

    consts = {
        'COOLDOWN_MS': 120,
        'Negro': (0, 0, 0),
        'Blanco': (255, 255, 255),
        'Tamano': tamano,
        'PlayerAncho': 15,
        'PlayerAlto': 90,
    }

    return {'sounds': sounds, 'images': images, 'consts': consts}